# The Basics of Redstone - LRR #1

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=BH0j4qQORqE
- **Duration:** 17:57
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** if you've been watching me for a while you might have seen my previous tutorial series called logical Redstone where I explained some digital logic Concepts and showed off some cool circuits but I'll be honest with you I'm not happy with that series don't get me wrong it'll stay on the channel forever but I think we can do way better welcome to episode 1 of a brand new series logical

**[0:18]** Redstone reloaded my goal for this series among many other things is to provide the most comprehensive easy to follow and engaging course about logical Redstone ever seen on YouTube now if you're brand new to Minecraft digital logic or even both don't worry today we're going to start from the absolute beginning and even if you're not new you'll still want to watch this I

**[0:38]** guarantee you'll learn something I also put timestamps that describe each section of the video so feel free to skip around without further Ado let's get started for this entire series I'm going to use version 1.18.2 of Minecraft Java Edition y118 well it doesn't matter that much but 118 is the version of the most popular logical Redstone servers at the time of uploading this if you use a slightly

**[1:00]** different version like 117 or 119 and you play in single player then everything in this series will probably still work what matters more is that you play in Java Edition not Bedrock edition if you try to build anything from this series on Bedrock there's a chance it just won't work at all so I really do not recommend trying that I would explain why I prefer Java over Bedrock

**[1:21]** but my friend purplers did a beautiful job doing that already so if you're interested in that check out his video in the description now another thing you might want to know is how to make a good world for Redstone obviously there's a ton of Freedom here but here's what I like to do on create new world I make it creative turn cheats on and set the difficulty to Peaceful then in the game

**[1:40]** rule section I like to turn off all the spawning stuff drop stuff and World update stuff too those three categories are just annoying for Redstone and in World options I like to turn structures off and I choose the super flat preset called Redstone ready and just like that you have a beautiful world for Redstone one last thing you might want to set up for yourself before getting started is a

**[2:01]** texture pack because in my opinion the vanilla textures are not that great there are so many options out there for texture packs personally I use one I made called the matpack and the link for it is in the description it's mostly just a mixture of packs made by other people that I put together the first thing to understand about Redstone and really Minecraft in general is that the

**[2:20]** game runs on a tick system there are 20 game ticks per second and so each game tick is a 20th of a second now the kind of weird thing is game ticks are actually not used that often to measure time in The Logical Redstone Community instead we often measure things in terms of redstone ticks which are defined as 10 per second not 20. in other words every two game ticks is equal to one

**[2:44]** Redstone tick this is because because a lot of redstone components operate on a two game tick clock anyways so I guess it's just kind of easier but the point is from here on out including this video whenever I say ticks I'm referring to Redstone ticks which are one tenth of a second okay with that out of the way let's take a look at the most common components in logical Redstone Dust repeaters

**[3:06]** comparators and torches Redstone Dust is the classic it's essentially the wire that you use to transmit Redstone signals you can place it on almost any flat surface in the game from solid blocks to Glass to even upside down half slabs but it can't exist without something under it each individual thus has a signal strength associated with it which is just a value from 0 to 15. zero

**[3:30]** being no power all the way up to 15 being full power one way to give Redstone full power is by placing a power source like a redstone block as you can see the adjacent dust receives a full signal strength of 15. then that value decays by one for every dust along the wire until eventually it reaches zero but before it reaches zero you can use Redstone to power things for example

**[3:53]** I can power a redstone lamp by hooking up a small wire to it and powering the wire and if you're only using dust then this trend there's no delay okay but if signal strength always decays to zero then how do we transmit longer signals for that we need a redstone repeater a repeater converts any signal from 1 through 15 into a signal of 15. for example if I have a long Redstone line which doesn't

**[4:19]** quite reach I can use a repeater to repeat the signal and keep it going this comes at a cost though because repeaters introduce delay by default a repeater introduces one tick of delay which literally means that the time from this dust being powered to this dust being powered is one tick or a tenth of a second you can also right-click a repeater to change that delay to two

**[4:42]** ticks three ticks or four ticks four is the maximum and if you right click again it just goes back to one repeaters can also repeat signals from other repeaters or really any other power source and a really cool feature of repeaters is that they can be locked by powering them from the side with another repeater or comparator this makes them hold their current state rate of either powered or

**[5:04]** unpowered okay now before I move on to comparators let's talk about what happens when you power solid blocks with redstone there are actually two types of power that solid blocks can receive soft power which I'll represent with orange and hard power which I'll represent with red if you power a solid block with redstone dust like this that block becomes soft powered additionally any

**[5:27]** solid blocks that Redstone Dust is sitting on directly also becomes soft powered but if you power a solid block with a repeater it becomes hard powered both soft powered and hard-powered blocks are very similar they can both activate components next to them like lamps or doors they can also both conduct to repeaters and comparators and by extension this means that you can

**[5:49]** actually pass signals through walls like this the main difference is that a soft power block will not activate Redstone around it whereas a hard powered block will all right with that out of the way let's move on to comparators unlike repeaters that have one input comparators have three inputs the rear and the two sides comparators have a delay of one tick which is the same as a default repeater

**[6:12]** they also have two different modes indicated by the little knob on the front by default when you place them they're in compare mode but if you right click and turn that little knob on they change to subtract mode now if you're not using the side inputs and you're just using the rear a comparator is actually really simple all it does is copy the signal strength from the rear

**[6:34]** to the output for example if I give it a signal strength of 7 it outputs a seven it's basically a worse version of a repeater but if you choose to use the side inputs then the mode it's in actually matters in compare mode if either of the two side inputs are greater than the rear it outputs a zero otherwise it keeps outputting the rear like normal for example if I have an 8

**[6:58]** in the rear and a seven and nine on the sides well nine is greater than eight so we output zero but if I have an eight in the rear and five and six in the sides well neither of them is greater than eight so we just keep outputting eight switching to subtract mode now the comparator will actually perform a subtraction it takes the rear minus the greater of the two sides and outputs the

**[7:23]** results so if I have a three in the rear and a one and two in the sides the comparator will do three minus the greater of the two sides which is two and three minus two is one as another example if I have a three in the rear and a four in the side the comparator will do three minus four which is negative one but signal strength never goes below zero so it actually just

**[7:50]** outputs a zero and this leads to a really cool property of subtract mode which is that if you give full power to the side nothing can get through you've essentially canceled this comparator because anything -15 is going to be zero or less and I'll be honest with you subtract mode is a lot more common in logical Redstone I almost never use compare mode just like repeaters comparators

**[8:13]** hard-powered blocks and on top of that they can pass signal strength through blocks if I give it a 7 in the rear hard power a block and place a redstone dust we get a seven another Super useful feature of comparators is that they can tell you how full a container is for example if I have a barrel completely full of items then a comparator will read 15. if it's only somewhat full I

**[8:37]** get a signal strength that is a representative fraction of how full it is maybe a seven or eight if it's halfway or a 13 if it's mostly full you get the idea and naturally if it's empty you get a zero all right last but not least is the redstone torch Redstone torches are power sources that give off full power they can be placed on the top or side of a block they hard power

**[8:59]** blocks above them and they can activate stuff next to them this includes underneath them if they're on the side of a block The Only Exception is the block they're attached to which is completely unaffected however if you power the block they're attached to the redstone torch becomes unpowered this can be used to invert a redstone signal and the inversion has a delay of one

**[9:20]** tick if a redstone torch inverts too many times too quickly it's possible for it to burn out and it will stay burnt out until it receives an update and that concludes the four main components used in logical Redstone of course there are still Pistons observers Hoppers and more but those just don't get used very often and in my opinion if you're not moving blocks I feel like you just never need

**[9:44]** to use pistons in my experience no matter what circuit I'm designing I tend to find cleaner Solutions using just These Guys these four components will allow you to do pretty much whatever you want in a clean and elegant way next up let's talk about the most important blocks for logical Redstone I already talked about solid blocks and how they can be soft powered or hard

**[10:04]** powered but another really useful block type is transparent blocks some common transparent blocks are glass glowstone ice or upside down slabs me personally I use glass the most transparent blocks have two really useful properties first Redstone can only travel up onto a transparent block but not down this gives you a really easy way to make one-way wires and second if you place a

**[10:30]** transparent block on top of a redstone staircase the Redstone can still slip through it compared to solid blocks which would block the Redstone from getting through this has some really cool side effects like being able to create a glass tower to send Redstone straight upwards or let's say I have two Redstone wires and I want to move them both down by one block I can't do that

**[10:52]** with solid blocks because well the Redstone on the bottom wire is getting blocked off but if I instead use a glass here the Redstone slips through and it works there's no more interference between these two wires that's pretty cool another useful block is the target block a Target block is a solid block with a special property that any Redstone Dust placed next to it will be

**[11:14]** automatically pointed to it this is really useful when it comes to compacting Redstone Circuits Target blocks also give off a signal when hit by a projectile but that's not really used in logical Redstone we just like them for the redirecting property next we have the Redstone Block as you saw earlier it gives full power to Redstone next to it that includes redstone on top

**[11:34]** of it and underneath it and finally containers are pretty useful as well they can be used with a comparator to create any signal strength you want on the Fly all right we've got tons of components and blocks now this is really cool the last thing you might want to use when you create circuits is some form of input and output starting with input the main ones I like to use are levers

**[11:56]** buttons and pressure plates levers are pretty simple they just attach to a block when they're turned on by a player they hard power that block buttons also attach to blocks when they're pressed by a player they hard power that block with a short pulse a stone button pulse is 10 ticks long while a wooden button pulse is 15 ticks long pressure plates can only be placed on top of blocks they

**[12:19]** hard power the block underneath them whenever you or another entity is standing on them and by the way levers buttons and pressure plates can also activate things around them now for output there are only two real options in my opinion Redstone lamps and trapdoors Redstone lamps are the classic they simply light up when they're powered anytime you want to read a

**[12:39]** signal or make a screen they're super super useful the only flaw about Redstone lamps is that while they turn on instantly they take two ticks to realize that they're not being powered anymore this can actually be really annoying when you're trying to read the state of a circuit because during those two ticks it's not really telling you the correct State luckily though trap

**[13:00]** doors don't have that problem they update instantly both ways so you can always rely on them to give you an accurate reading of a circuit at any time and I'm such a fan of this property that my texture pack actually re-textures trapdoors that are on the side of blocks to look like lamps and that concludes input and output at this point you've learned literally everything commonly used in logical

**[13:23]** Redstone if you're brand new to this and this seemed like a ton of information you're right it was but I promise you after just a few weeks of playing around with redstone yourself all of these properties become second nature my brain doesn't even think about Redstone in terms of like soft powering and hard powering anymore I've just internalized how it behaves and I think most people

**[13:43]** get to that point pretty quickly the last thing I want to talk about in this video is mods don't get me wrong all the Redstone we build will always work in the vanilla version of the game but there are some mods that are incredibly useful for Redstone building my two favorites are world edit and carpet these are both fabric mods so you'll need to learn how to install fabric

**[14:03]** first I've left a bunch of links in the description for how to do that it's not that bad once you've installed world edit and carpet come back to this part of the video and I'll show you how I use them let's start with world edit the idea of world edit is to create a selection and then run commands that manipulate the world to help you build to make a selection start by running

**[14:21]** slash wand this gives you the default selection tool which is a wooden ax left-click a block to set the first corner of your selection and right-click a block to set the second corner all the space between those two corners is your selection world edit has a ton of commands but I really only use like five of them set move copy paste and stack let's do a really quick rundown of how

**[14:44]** these work set will set your selection to a block for example if I want to set the floor to Stone I would select the first Corner then the second corner and run slash set stone you can also use set to remove things by setting the area to air so if I run slash set air the floor gets removed move moves your selection for example if I want to move this Circuit by three

**[15:08]** blocks up I would select the circuit like this and then I'd run slash slash move three up or I can also just look up and run slash move three copy and paste are used to well copy and paste for example let's say I want to copy this circuit and paste it somewhere else first I select it then I run slash copy go over here and run slash paste and lastly we have stack stack is really

**[15:39]** useful when you want to copy something a bunch of times for example if I have a repeater here and I want to have 10 more repeaters just like it all I need to do is select the repeater and run slash stack 10. it will then copy and paste it 10 more times in the direction that I'm looking world edit also has some flags that I use sometimes the most common one is Dash a if you include this flag when

**[16:03]** you run a command it will ignore air so let's say I want to move this piece into this piece by default if I try to do that it won't work because selections always have straight edges but if I run the same command with Dash a it perfectly fits because it didn't move the air now let's talk about carpet mod just like with world edit there's a ton of stuff in this mod but I only use a

**[16:26]** few things first they have a toggle called creative no clip that you can enable with this Command right here it allows you to fly through blocks but you still land on them when you stop and that is just so useful when you're trying to build tight circuits I also use carpet mod to speed up slow down or even freeze the game as I said in the beginning there are 20 game ticks per

**[16:47]** second but you can change that with tick rate for example running slash tick rate 5 will slow down the game to 5 ticks per second or 1 4 speed on the flip side running slash tick rate 500 will speed up the game a ton you can also freeze the game with Slash tick freeze once the game is frozen you can step through time with Slash tick step for example if I want to jump ahead by one Redstone tick

**[17:12]** or two game ticks I would run slash tick step two and to unfreeze the game just run tick freeze again and with that I believe I covered pretty much everything I needed to cover for a beginner if you think I missed anything leave a comment and I'll try to mention it starting next episode I'm gonna assume you've already played around with redstone yourself for a good amount of time and that you've

**[17:34]** gotten comfortable with the basics and yeah I uh I really hope you guys enjoy this series and are as excited for it as I am I hope you learned something I hope you enjoyed peace out guys [Music]
