# Everything about Redstone User Interfaces!

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=rwriTG8UvPM
- **Duration:** 5:35
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys welcome back to another video today we're going to be talking about something that doesn't get nearly enough attention in the redstone community user interfaces or ui for sure a user interface is just an interface for a user for example in my most recent calculator this is the user interface the user can type numbers on the keypad and press other buttons as well the ui

**[0:16]** lets them use the calculator this is sometimes the last part of the project that gets built so it's easy to just slap something together and call it good enough but let's do better let's be proud of what we build and figure out how to make a great ui sorry for the interruption i forgot to mention that i have a second channel now i'll be posting shorts and other random stuff

**[0:32]** there if we can get it to a thousand subscribers by the end of the month that would be absolutely amazing all right back to the video the best ui in summary is what provides the best experience possible for everyone that includes new users regular users and developers how do you create a ui that's great for anyone who uses it well first of all you want it to be clear it's never a good

**[0:49]** experience when you feel confused right especially if someone downloads your world and you're not right there to help them they'll probably just give up if it's not clear how to use it additionally you want your ui to be communicative people have extremely short attention spans and you'll learn this if you ever try to make youtube videos if your ui doesn't communicate to

**[1:04]** them and give feedback quickly they're going to lose interest let's look at some examples example 1 mode a and mode b either mode a or mode b must be selected at all times but not both in other words a boolean here's the first solution it's really simple just two buttons and two signs i can tell that this one is labeled a and this one is labeled b this gets the job done but

**[1:24]** there's a few problems i can't tell what mode is currently selected it might not be necessary to know that but it's kind of annoying and also it's not obvious from looking at this that only one is supposed to be selected at a time i mean the signs say a and b but there's nothing stopping the user from thinking that both modes could be activated at the same time if we add some indicator

**[1:42]** lamps now we can tell which mode is currently selected behind the scenes we have an rs nor latch which just toggles between two different states if the user tries to activate both at the same time they'll instantly learn that no matter what they do only one can be on but we can do even better there's a way for the user to know that only one mode can be selected by just looking at it a lever

**[1:59]** with just a lever instead of two buttons i know that it has to be in exactly one of two states so this is our final design in the back we just have a repeater that takes the lever signal out and we have a torch and another repeater to help with the indicator lamps example two eight modes exactly one mode must be selected at all times here's my first solution it's pretty cursed i kind of

**[2:18]** made it as a joke the way it works is first you select which pair of letters you're going to be using so if i know i want d then i'll turn on this for u c d and then this lever under it selects whether you want c or d so i would have to flick this down and now we're selecting d or if i want g i flick this lever for use gh and this lever is already pointing to g so we're good i

**[2:38]** know i know it's terrible but this is also a proven point that there's many different ways to approach these things all right let's change this up instead i'll use buttons this is obviously much more natural to use to make this better we could throw some indicator lamps on there and some signs but i have a better idea if we only care about eight modes that's how many rotations there are on

**[2:56]** an item frame so we can use an item frame selector all you do to use this is point the arrow at the mode you want currently we're selecting c if i want to change it to g there you go and a different signal strength will be outputted in the back according to what mode is selected this is very clear and communicative you can read all the modes clearly and any new user can tell that

**[3:14]** the arrow is pointing to exactly one mode i'd say this is our final design so those are the special cases of two modes and eight modes but in general for end modes i tend to use something like this this is an expandable selector made from rsnor latches when i press a button it selects it and it turns off everything else it's expandable as long as all of the inputs power the entire redstone line

**[3:35]** here because that's what turns them all off during the selection it's also rising edge triggered which means that it goes off right when the button is pressed down and not when it pops back up another popular ui component is keyboards there's many different ways to approach keyboards in minecraft so i'm just going to show you some of my favorites each key has a button on it

**[3:50]** and a sign on it to tell you which character it is every character is assigned a unique 6-bit key for example when i press j this is jay's 6-bit key or if i press m this is m 6-bit key there's also some special lines here like backspace space and enter and they're just directly connected to their buttons you could give these codes as well but sometimes it's just easier to

**[4:09]** keep them separate so to hook up this keyboard to a display you need to send the 6-bit character code and the 4 special characters if this was a keyboard in real life this would be inside the wire going from your keyboard to your monitor the 6-bit character code and your special lines the other keyboard and i gotta say i like this one a lot better is this tiny one which uses

**[4:27]** banners to show you the letters this time instead of a 6-bit code each character is represented by a unique signal strength value which comes out on one of these lines for example if i press d d is represented by a 13 on the blue or if i press i i is represented by an 8 on the green and this is the mapping for the keyboard this shows you what signal strength comes out and what

**[4:46]** color for every key this shows you what color it's going to be designated by the wool and what signal strength it's going to be by the sign for example this tells me that the leftmost key on the second row is a 15 blue and sure enough 15 blue and i've also got two special wires here for backspace and enter that just directly map to their button so when you hook up this keyboard to a

**[5:03]** display all you got to send is the character code and the two special lines the last thing i want to show you guys is a simple keypad design i've been using this guy for ages and i see people asking for it sometimes so here you go 10 buttons one for each digit it's synchronized at a speed of one tick because each button just has one torch and some wiring and that's all i got for

**[5:20]** you guys i hope you learned something i hope you enjoyed peace out guys if they showed up imma show it back if the catch is too small imma throw it back i've done a lot but i ain't got a lot to show for that all right let's do that again
