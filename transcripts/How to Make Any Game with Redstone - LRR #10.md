# How to Make Any Game with Redstone - LRR #10

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=WI3RNlOErFI
- **Duration:** 21:48
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome to the final episode of logical Redstone reloaded today we'll be making two entire Redstone games from scratch lights out and Connect 4 I'm also going to be giving you guys some tips and tricks about the game design process so that you can apply them to your own games I hope you enjoy so what's the best way to make a redstone game looking out at the blank Sandstone

**[0:20]** world making a game can feel like an extremely daunting task should you start building things right away should you draw things out on paper maybe I mean where do you even start unfortunately there's no magic formula for how you should build a game everyone is different and it's too complex to put into a formula but I have some tips that I want to share with you these are from

**[0:39]** my own experience and from what I've seen in the Redstone community over the years and a lot of these tips also apply to any computer science project not just a redstone game but again it's important to remember that there is no magic formula so if my advice doesn't work that's okay my goal for this video is to just be as helpful for as many people as possible so what are these tips tips my

**[1:00]** first big tip is to plan as much as possible outside of Minecraft before you start building anything it might seem silly at first but I recommend taking out a sheet of paper and actually drawing the build or if you have a drawing program on your computer you can use that too now don't draw every single wire just draw the general idea make some boxes for the components you might

**[1:20]** need and draw the general connections between them the main reason I recommend this is efficiency building Redstone is slow but drawing on paper is really fast and as you draw you might realize there's an issue with it like maybe something you didn't think about until you saw it visually trust me it's much better to find an issue before you start building rather than after you've

**[1:40]** already built a ton of redstone another option when it comes to planning is to program your game first I've actually done this a few times for example I made my 2048 game in Python before building it this becomes especially useful when you want to compare the output of your game to the correct simulated output assuming that what you coded is actually correct but but regardless of your

**[2:00]** code's correctness this is still a great option because you'll learn way more about the inner workings of your game by programming it and if you don't have any experience well it's never too late to start programming is one of the most useful skills you can possibly have and there are so many resources for it online I'll put a few of my favorites in the description my next big tip is to

**[2:21]** use something called abstraction within computer science abstraction means to abstract lower level details into a higher level function in other words keeping the implementation separate from the functionality for example to drive a car there are really only three things that you need to know the gas pedal makes it Go the brake makes it stop and the wheel steers it those are pretty

**[2:42]** much the only functions you need to operate a car you don't have to know how the engine works or how the circuits work or anything that's the implementation so applying this to Redstone take this multiplier for example which multiplies two binary numbers together I don't know all the details about how it works because I didn't make it my friend sloy me did but

**[3:01]** just like a car I don't have to know how it works to use it all I have to know is that the two inputs are right here and the output is right here 3 * 3 is 9 so you can essentially use other people's Redstone without having to know how it works but abstraction isn't just about using other people's work the real power of abstraction is the ability to build machines that get more and more

**[3:25]** complex without it actually feeling like it's getting more complex to show you what I mean let's say I wanted to make an 8 bit binary Adder just like in episode 4 to do this I would start by making the basic logic gates and once I know how to make them I can just view them as little symbols each with input and output then I don't have to worry about the implementation anymore now

**[3:46]** using these symbols I can construct a half adder and a half adder is once again just defined by some inputs and outputs so I can make a symbol to represent the entire half adder then using some half adders and another logic gate I can make a full adder and finally using eight full adders I can make an 8bit Adder notice that at every stage I never did anything super complex but if

**[4:10]** you open up the 8bit adder and look at all the logic inside it's pretty complicated so when you're building your own Redstone game try to use this technique to your advantage start by breaking things down into smaller and smaller components and then build your way back up using abstraction my third tip is to use mods because they can save you a ton of time in the very first

**[4:30]** episode of this series I told you guys about my two favorite mods world edit and carpet and I can't stress this enough learning how to use these two mods will save you so much time also one thing I forgot to mention in that first video is that world edit has a schematic feature which allows you to save Redstone builds and paste them in later you can use this to transfer builds

**[4:48]** Between Worlds or even send them to your friends another really cool mod for Redstone is called Redstone tools which was developed a little bit after that first episode I made a video going through its features it's a quality of Life mod that's literally designed by people like me to save your time finally my last tip is not really Redstone related but it's still really important

**[5:08]** take breaks and take care of yourself I know it seems like it's not that big of a deal to play Minecraft for hours and hours on end cuz it's just a video game but when you're making a literal game out of redstone you're not just playing a video game anymore you're making a project and when you're working on a project you need breakes otherwise you'll burn out really quickly and

**[5:26]** ultimately you won't finish but I think that's about it when it comes to tips let's start making some games but first I have to clarify something real quick at the time of recording this I've actually already made these games off camera so if it seems like I'm super lucky because I'm not running into any issues I'm not it's just that I've already done all the debugging debugging

**[5:45]** is definitely a huge part of the process and I'm sorry that it's not going to be in this video very much but for the purposes of causing as little confusion as possible I just thought it' be best to make these games as if everything works perfectly first try with that out of the way our first game to make make is called lights out lights out is played on a board of square cells where

**[6:03]** each cell can be on or off when you click on a cell it toggles its state as well as the state of the four adjacent neighbors you start off with a certain configuration of on cells and the goal of the game is to turn all the lights off for example if the pattern looks like this I can turn off all the lights by clicking this one this one this one and this one one thing to keep in mind

**[6:27]** is that not all starting patterns are solvable for example this simple 2x1 board is impossible to completely turn off but the cool thing is you can actually generate a complex and solvable board really easily all you have to do is start with a fully off board and click on it in random places you know that it has a solution because you can always just do what you did in

**[6:49]** Reverse okay so let's start drawing our design the first thing I notice about lights out is that all the cells have the exact same functionality So in theory we can just build one cell and then and duplicate it to make a board of any size from the top down view let's make the cell out of a bunch of lamps to show whether it's on or off and then let's have a note block in the middle

**[7:08]** for the player to click on it now when the player clicks the note block two things have to happen the cell has to toggle its own State and it has to toggle the state of the four neighbors the simplest way to do this is to just have a t flipflop underneath every cell I covered T flip flops in episode 7 when the player clicks the note block we'll send a signal down to the T flip flop to

**[7:29]** toggle it as well as a signal to the four neighbors T flip flops and that's literally it that's our design back in Minecraft let's go ahead and build the 3X3 of lamps and put a note block in the middle and let's also put a border around it so that it's easier to tell the cells apart there we go perfect and then for the T flip-flop underneath let's go ahead and do a few observers

**[7:51]** into a block into a sticky piston into a redstone block so when you click on the Note Block it sends a short pulse down and it toggles the Piston if you put a lamp right here you can see that it toggles between off on off you get the idea now eventually we want the lamps on top to toggle not the one down there but let's just worry about that later I think the more important thing is to

**[8:15]** figure out how to toggle the other four neighbors as well we need some system such that when I click this note block the T flip-flop underneath it toggles and all four of these toggle as well the first way I thought to do this was to just split the Observer line into four and plug it into all four neighbors like this and technically this works because when you toggle it it toggles its four

**[8:38]** neighbors the problem is the wiring is so dense that you're essentially screwing yourself over remember these four cells on the outside see the center as their neighbor which means you're going to end up having four more signals plug into the center piston and there's barely any room as is I mean I'm sure it's possible but it just gets really messy the best better approach is to do

**[9:00]** something like this where there's a redstone line between each pair of blocks now when you toggle the center it puts a signal onto all four Redstone lines and toggles all four neighbors and if I toggle this cell for example it'll toggle itself and it will reuse just this Redstone line to toggle its one neighbor so now we have exactly the functionality we want and this is a

**[9:22]** super easy system to expand you can literally just make a grid following this pattern now if I toggle any cell we can see that it toggles itself and the four neighbors perfect and at this point if you want to play Lights Out you technically can you just have to use the display on the bottom but let's go ahead and connect the T flipflop to the display on the top okay so I just added

**[9:43]** this cyan circuit which takes the output of the T flipflop and turns on all the lamps so if we go to toggle it you can see we get that nice spiral pattern turning on turning off all we have to do now is duplicate this a bunch of times and we'll have lights out okay okay here's a nice 3x3 board every cell is on right now and as it turns out that's a solvable pattern if you want to try to

**[10:06]** solve this in your head or on paper go ahead I'll give you a second to pause the video all right so the solution is to do all four corners like this and the center one and all the lights are out so we win so yeah that's lights out with redstone just a t flip-flop for every cell and a little bit of a clever wiring technique I've included a 3X3 5x5 and 7x7 board in

**[10:34]** the World download if you want to play it yourself the link for that is in the description remember all you have to do to make a solvable pattern is to just start with them all off and click squares randomly so maybe have a friend do that or something and then you can challenge yourself to turn all the lights out the next game I want to make with you guys is Connect 4 this is a

**[10:52]** pretty well-known game but just in case here's how it works Connect 4 is a two-player game and it's typically played on a 7 X6 board that looks like this one player drops yellow chips and the other drops red chips the players alternate back and forth dropping one chip at a time and the first one to get four in a row wins the game the four in a row can be horizontal vertical or even

**[11:13]** diagonal the absolute easiest way to make this game in Minecraft is to actually just use sand and gravel like this but come on that's kind of boring let's make this using actual digital Logic the first thing I notice about this game is that every column can be thought of individually dropping a chip in one column doesn't affect any of the other columns so we can just build one

**[11:36]** column and duplicate it and according to the original game size the column is going to be six cells tall now each one of these cells has to be able to display three different things red chip yellow chip and empty but as you probably know color displays are not great and I'd rather just use Redstone lamps so let's just represent yellow and red with the symbols X and o on on Redstone lamps and

**[12:00]** when it's empty it'll be completely off that'll look pretty good but now let's think about how this will actually work first things first we know that every cell is going to need some type of memory to store the current state of the cell and since there are three states x o and empty that memory needs to be at least two bits we can't do it with one bit because one bit can only store two

**[12:23]** things but two bits can store four things so let's get really specific about the logic we need here when the game starts every cell will be in the empty State on X's turn if they happen to choose this column we need to replace the lowest empty cell with an X and same thing for O's turn if they choose this column we'll replace the lowest empty cell with an O but finding the lowest

**[12:46]** empty cell is not the easiest thing in the world I mean how do you do that with digital logic well the most straightforward algorithm is to just start at the top check the cell underneath if it's empty move down if it's not stop and repeat this until it goes down as far as possible so at first glance it seems like we're going to need some type of shift register like from

**[13:08]** episode 8 and while you can make Connect 4 with shift registers there's actually a better way to do it using just Sr latches from episode 7 let me show you what I mean imagine for a second that every cell has an Sr latch behind it if the latch is reset that means the cell is empty and if it's set it's occupied for now don't worry about whether it's an X or an O just think of the cells as

**[13:32]** either empty or occupied according to what the SR latch says now whenever a player wants to drop a chip all we have to do is this from top to bottom send a set signal to every Sr latch and if any latch becomes set reset the latch above it for example let's drop our first chip we start by setting this guy and there's no one above it so we don't have to worry about any resetting then we set

**[13:58]** this this one and because it became set let's reset the one above it then we set this one and again it became set so reset the one above it and keep doing this all the way down until you get to the bottom now let's drop another chip so again start by setting this top guy and there's no one above it then set this one it became set so reset the one above it and continue this all the way

**[14:24]** down notice that when you go to set the bottom cell it stays is the way it is and more importantly it didn't become set and so we don't reset the latch above it and there we go we dropped another chip so yeah if you just set every latch top to bottom and follow this one rule you can essentially drop a chip on a column the only other thing we have to think about is how to

**[14:48]** distinguish between X and O but for that I think it's actually just easier to show you in Minecraft so let's head on over and start building as usual I'll start with making the display all right I made a vertical column with a 3X3 of lamps for each cell and then let's have this be o and this be X I know this is more of a plus than an X but when it's only 3x3 the plus looks much better so

**[15:11]** next let's make the display Logic for a single cell so that it can actually show these based on some Redstone inputs we're going to need two input wires one for x and one for o and depending on which one gets activated that's just what the cell will show okay done with that so as you can see when we power this one we get an O and when we power this one we get an X I'm going to go

**[15:34]** ahead and duplicate this for every cell in the column there we go now we can display an X or an O on any cell which is perfect next let's make the circuit I was talking about that will simulate gravity I'm going to do this step by step to start every cell just has an Sr latch behind it that's all I've done so far so you can go to any cell and you can reset it or you can set it and you

**[15:55]** can see the state of the latches with these lamps right here now remember when the player drops a chip the first thing we want to do is literally just set all the latches top to bottom let's do that with a downward torch Tower okay there's the torch Tower and as you can see it literally just sets every cell now we just need to make our special rule the rule says that if a latch becomes set it

**[16:17]** resets the latch above it to do this we can actually use the pulse generator from episode 7 because a pulse generator at least in the way I described it is really just a rising Edge detector in other words when the signal behind it goes from low to high it outputs a short pulse so if we just take this and attach it to the state of the cell then we'll get a pulse whenever the cell becomes

**[16:39]** set and by plugging the output into the next highest reset that's our rule so let's duplicate this for every cell and we should have a gravity circuit okay let's try this out if we press this button we drop a chip and if we press it again we drop another one beautiful these circuits always feel so magical cuz it almost looks like a physics simulation or something but no it's just

**[17:05]** latches and a rule so yeah we have gravity now the last thing we need to think about is how to switch between player X and player o like I said earlier we know that every cell needs at least two bits of information to store its three states and there's actually a really elegant way to store two bits of information with a single Redstone component no not the comparator I'm

**[17:26]** talking about the repeater because repeaters are not only on or off they're also locked or unlocked giving us a total of four different states so here's how this is going to work we're going to have a repeater like this for every cell in the column if the repeater is unlocked that means the cell is empty if it's locked that means the cell is occupied if it's locked with a zero it's

**[17:51]** an O and if it's locked with a one it's an X let me go ahead and duplicate this so we have one for every cell so now what I'm going to do is I'm going to plug the output of the gravity circuit into these locking signals that are on the left there we go just like this and now we can drop a chip for x or o let me show you what I mean if we press this button which sends a signal all the way

**[18:15]** down in our gravity circuit it's going to come all the way down to here and lock the bottommost repeater and if we look at the display we can see that there's an O on the bottom because the repeater got locked with a zero that makes sense because we weren't powering the back of any of the repeaters but now let's say it's X's turn so I'm going to go ahead and power the back of every

**[18:36]** single repeater so if we press this button again the gravity circuit sends another signal down which locks another repeater but this time it got saved with a one which is X so let me just combine all these signals together and we should be able to control whether an X or an O gets dropped okay I connected them all with a spiral and I put a lever right here so now when the lever's on it drops

**[19:02]** an X and when the lever's off of course it drops an O beautiful building the rest of the game was pretty straightforward I just duplicated the column six more times and I added a reset function which resets all the SR latches in the entire board and I added some note blocks at the top of each column so that the player can just right click any of those and it'll drop a chip and I like doing that

**[19:26]** because it's a much bigger hit box than a button all right here's the finished game when this lever is up it's X's turn and they can drop a chip wherever they want and when the lever is down it's O's turn and of course they can do the same thing they can drop a chip wherever they want and oh my I love the falling animation it's really cool we didn't do any win lose detection or anything like

**[19:48]** that but I'm going to be honest I really don't feel like it also it's kind of annoying to have to flip this lever every time so you could make a circuit to just switch whoever's turn it is whenever a chip is dropped that wouldn't be too bad you could probably just do that with a t flipflop so that's it for games but before you go I want to talk about the future I want to be super

**[20:09]** clear even though this is the end of lrr this is not the end of teaching redstone on my channel the purpose of this series was really just to lay the foundation for learning digital Logic the circuits I included in this series were pretty General they're usually things that you can do for more than one task and I did that because I personally think that's the best way to learn you start by

**[20:28]** building up a toolbox of General circuits and Concepts and when you want to tackle a bigger problem like making a game you bring out the tools and you use them to solve it but of course tackling these bigger problems is really fun and there's so much to talk about especially when it comes to stuff like general purpose computers which I didn't even mention in this series so even though

**[20:50]** lrr is over I've kind of learned that I enjoy teaching way more than I thought and I'm excited to make more videos like this in the future they they may not take on the exact same format I can't know for sure I don't want to make any promises all I know is that there's a lot more to talk about and I'm excited to make more videos if you haven't already subscribe so that you don't miss

**[21:09]** any and before I end I want to give a huge huge thank you to those who helped me create this series thank you to the members of or for giving me feedback and helping me find circuits also thank you to my friend SLO for all kinds of General help and of course thank you to everyone watching this this series would not be possible without you guys guys I hope you learned something I hope you

**[21:30]** enjoyed peace out [Music] guys
