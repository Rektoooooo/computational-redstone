# YouTube Transcript → Markdown

A Chrome extension (Manifest V3). While you are on a YouTube video page, it grabs the
video's transcript and saves it as a Markdown file named after the video title.

## Install

1. Open `chrome://extensions`
2. Turn on **Developer mode** (top right)
3. Click **Load unpacked** and pick this folder (`yt-transcript-md`)
4. Optionally pin the extension so its icon is visible in the toolbar

## Use

Open a YouTube video, then either:

- click the extension icon → pick the language → **Save as .md**, or
- press **Alt+Shift+Y** to save straight away with the default settings.

The file goes to `~/Downloads/YouTube Transcripts/<video title>.md`.

## What the file looks like

```markdown
# How to make sourdough

- **Channel:** Some Baking Channel
- **URL:** https://www.youtube.com/watch?v=abc123
- **Duration:** 12:04
- **Transcript:** English
- **Saved:** 2026-08-25

---

**[0:00]** Today we are making sourdough from scratch...

**[0:31]** The starter needs to be bubbly and active before you...
```

Untick **Include timestamps** in the popup to get plain paragraphs instead.

## How it works

| Step | Where | What |
|---|---|---|
| 1 | `background.js` → `pageReadVideoInfo` | Runs in the page's MAIN world, reads `movie_player.getPlayerResponse()` for the title, channel and caption track list |
| 2 | `background.js` → `pageFetchCaptionTrack` | Downloads the chosen caption track as `fmt=json3` from inside the page, so the request carries YouTube's own origin and cookies |
| 3 | `background.js` → `pageScrapeTranscriptPanel` | Fallback: opens YouTube's own "Show transcript" panel and reads the segments out of the DOM |
| 4 | `dropRepeatedPass` | Cuts the transcript off at the point where caption times jump backwards, so a source that returns the video twice is saved once |
| 5 | `groupSegments` / `buildMarkdown` | Merges the tiny caption fragments into readable chunks (max 30 s or 400 characters) and writes the Markdown |
| 6 | `chrome.downloads` | Saves the file, with the title sanitised into a legal filename |

Two ways of getting the transcript are included because YouTube periodically tightens
access to the caption endpoint. If the direct fetch fails for any reason, the extension
falls back to the transcript panel that YouTube itself renders.

## Settings you may want to change

Both are at the top of `background.js`:

- `DOWNLOAD_SUBFOLDER` — set to `''` to save into the Downloads root instead of a subfolder.
- `CHUNK_MAX_SECONDS` / `CHUNK_MAX_CHARS` — how long each paragraph/timestamped line gets.

To change the keyboard shortcut, go to `chrome://extensions/shortcuts`.

## Limits

- Only works on `youtube.com/watch` pages.
- A video with captions disabled entirely has no transcript to save.
- Live streams may only expose a partial transcript.
