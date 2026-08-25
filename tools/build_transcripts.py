#!/usr/bin/env python3
"""
Fetches YouTube transcripts with yt-dlp and writes them as Markdown in exactly
the same shape the browser extension produces, so the files sit alongside the
ten that are already there.

Mirrors background.js: same 30s/400-char chunking, same header, same filename
sanitising, and the same dropRepeatedPass guard.
"""
import json, re, subprocess, sys, time
from pathlib import Path

SCRATCH = Path(__file__).resolve().parent
YTDLP = SCRATCH / "ytvenv" / "bin" / "yt-dlp"
SUBS = SCRATCH / "subs"
OUT = Path.home() / "Downloads" / "YouTube Transcripts"

CHUNK_MAX_SECONDS = 30
CHUNK_MAX_CHARS = 400
RESTART_BACKWARD_SECONDS = 5


def format_timestamp(total_seconds):
    whole = int(total_seconds)
    s, m, h = whole % 60, (whole // 60) % 60, whole // 3600
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def safe_filename(title):
    name = re.sub(r'[\\/:*?"<>|]', "-", title)
    name = re.sub(r"[\x00-\x1f\x7f]", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    name = name.strip(".").strip()
    return (name[:120].strip()) or "youtube-transcript"


def parse_json3(path):
    """json3 -> [{start, text}]. aAppend events are roll-up newline markers."""
    data = json.loads(path.read_text(encoding="utf-8"))
    segments = []
    for event in data.get("events", []):
        if not event.get("segs") or event.get("aAppend"):
            continue
        text = "".join(s.get("utf8", "") for s in event["segs"])
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            segments.append({"start": event.get("tStartMs", 0) / 1000, "text": text})
    return segments


def drop_repeated_pass(segments):
    for i in range(1, len(segments)):
        if segments[i - 1]["start"] - segments[i]["start"] > RESTART_BACKWARD_SECONDS:
            return segments[:i]
    return segments


def group_segments(segments):
    chunks, current = [], None
    for seg in segments:
        if current is None:
            current = {"start": seg["start"], "text": seg["text"]}
            continue
        too_long = len(current["text"]) + len(seg["text"]) > CHUNK_MAX_CHARS
        too_old = seg["start"] - current["start"] > CHUNK_MAX_SECONDS
        out_of_order = seg["start"] < current["start"]
        if too_long or too_old or out_of_order:
            chunks.append(current)
            current = {"start": seg["start"], "text": seg["text"]}
        else:
            current["text"] += " " + seg["text"]
    if current:
        chunks.append(current)
    return chunks


def build_markdown(info, track_label, segments, saved):
    lines = [f"# {info['title']}", ""]
    if info.get("channel"):
        lines.append(f"- **Channel:** {info['channel']}")
    lines.append(f"- **URL:** https://www.youtube.com/watch?v={info['id']}")
    if info.get("duration"):
        lines.append(f"- **Duration:** {format_timestamp(info['duration'])}")
    lines.append(f"- **Transcript:** {track_label}")
    lines.append(f"- **Saved:** {saved}")
    lines += ["", "---", ""]
    for chunk in group_segments(segments):
        lines.append(f"**[{format_timestamp(chunk['start'])}]** {chunk['text']}")
        lines.append("")
    return "\n".join(lines)


def fetch(video_id):
    subprocess.run(
        [str(YTDLP), "--write-auto-subs", "--write-subs", "--sub-langs", "en.*",
         "--skip-download", "--sub-format", "json3", "--write-info-json",
         "--no-warnings", "--quiet", "-o", f"{SUBS}/%(id)s.%(ext)s",
         f"https://www.youtube.com/watch?v={video_id}"],
        check=True, capture_output=True, text=True, timeout=180,
    )


def main():
    ids = [line.strip() for line in sys.argv[1:] if line.strip()]
    SUBS.mkdir(exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    saved = time.strftime("%Y-%m-%d")
    ok, failed = [], []

    for n, vid in enumerate(ids, 1):
        try:
            info_path = SUBS / f"{vid}.info.json"
            if not info_path.exists():
                fetch(vid)
            info = json.loads(info_path.read_text(encoding="utf-8"))

            sub = next((SUBS / f"{vid}.{lang}.json3" for lang in ("en", "en-orig", "en-US")
                        if (SUBS / f"{vid}.{lang}.json3").exists()), None)
            if sub is None:
                raise FileNotFoundError("no english json3 subtitle")

            segments = drop_repeated_pass(parse_json3(sub))
            label = "English (auto-generated)" if info.get("automatic_captions") else "English"
            md = build_markdown(info, label, segments, saved)

            dest = OUT / (safe_filename(info["title"]) + ".md")
            dest.write_text(md, encoding="utf-8")
            ok.append(dest.name)
            print(f"[{n}/{len(ids)}] OK   {len(segments):4} lines  {dest.name}")
        except Exception as e:
            failed.append((vid, str(e)[:120]))
            print(f"[{n}/{len(ids)}] FAIL {vid}: {str(e)[:120]}")
        time.sleep(1)

    print(f"\nDone. {len(ok)} saved, {len(failed)} failed.")
    for vid, err in failed:
        print(f"  FAILED {vid}: {err}")


if __name__ == "__main__":
    main()
