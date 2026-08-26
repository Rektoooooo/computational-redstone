# Wiring like a pro - every wiring problem, solved

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=pT-VWjqYli0
- **Duration:** 11:53
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-26
- **World download:** harvested into `worlds/primitives/wiring/` - 49 builds, no signs

The circuit that matters most here is the hex wire at [6:27]: a dust line, a row of
repeaters, and a second dust line. `out = in + (15 - repeaters)`, in two ticks whatever
the distance. Verified against `primitives/wiring/build-41`.

---

**[0:00]** how would you take these wires and pass

**[0:01]** them through these wires without any of

**[0:03]** them messing with each other how would

**[0:05]** you send this signal strength upwards

**[0:06]** without it taking forever after years of

**[0:08]** wiring Redstone I've run into so many of

**[0:10]** these questions but now I've got a

**[0:12]** solution for every scenario so in this

**[0:15]** video I'm going to show you all of these

**[0:16]** Solutions and a bunch of tips and tricks

**[0:18]** along the way that way you'll spend less

**[0:20]** time on wiring and more time on the more

**[0:21]** exciting parts of your build I hope you

**[0:23]** enjoy starting as simple as possible


## Single Bit


**[0:25]** let's say you just want to wire a binary

**[0:27]** signal from point A to point B if both

**[0:30]** both points are flat on the ground then

**[0:31]** this is really easy you can just use a

**[0:33]** line of dust with a repeater every 15

**[0:35]** blocks if you want to get a little more

**[0:37]** length out of it you can also put a

**[0:38]** block behind and in front of the

**[0:40]** repeater literally the only issue you

**[0:42]** might run into with this circuit is when

**[0:43]** it comes to Turning sometimes if the

**[0:45]** signal strength runs out here the dust

**[0:47]** isn't pointing into the block anymore in

**[0:49]** this case though you can just put a

**[0:50]** Target block here and problem solved but

**[0:52]** of course having both points flat on the

**[0:54]** ground is pretty rare so let's look at

**[0:56]** some other directions if you're sending

**[0:58]** something upwards the most common

**[1:00]** solution is to use glass Towers because

**[1:02]** they're really small and fast when they

**[1:04]** eventually run out of signal strength

**[1:05]** there are a few ways to keep it going

**[1:07]** you can use a repeater and kind of flip

**[1:08]** it back around like this or you can use

**[1:11]** two torches which acts like a repeater

**[1:13]** because it's a double negation and

**[1:14]** speaking of negation if your Tower is

**[1:16]** really high you don't necessarily have

**[1:18]** to make a double negation every time in

**[1:20]** this tower for example I just have one

**[1:22]** negation here and another one here in

**[1:24]** total it's a double negation so it still

**[1:27]** works and it's faster than using two

**[1:29]** torches at at every step now let's go

**[1:31]** the other way downwards if you play on

**[1:33]** Bedrock Edition then the best solution

**[1:35]** for downwards is also glass Towers but

**[1:37]** unfortunately in Java Edition glass

**[1:39]** Towers only send Redstone upwards so to

**[1:42]** go down you have to use some kind of

**[1:44]** staircase a clean way to make a

**[1:45]** staircase is to make it into a spiral

**[1:47]** like this this will send Redstone down

**[1:50]** really fast and if you run out of signal

**[1:51]** strength you can use the exact same

**[1:53]** strategies as the upward Towers you can

**[1:55]** use a repeater a double negation with

**[1:57]** torches or a bunch of single negations

**[1:59]** as as long as there's an even number

**[2:01]** also don't forget that spirals can send

**[2:03]** things up too so if you ever need to

**[2:04]** send something up and down on the same

**[2:06]** wire spirals are the best way to do that

**[2:09]** the last scenario for point A to point B

**[2:11]** is when it's diagonal when you have a

**[2:12]** situation like this remember that you

**[2:14]** can always do it in two parts horizontal

**[2:16]** and then vertical or even vertical and

**[2:18]** then horizontal and there's no shame in

**[2:20]** this in fact it's usually a really clean

**[2:22]** way to do it but of course there are

**[2:23]** more efficient ways to get there if

**[2:25]** you're going up on a diagonal then the

**[2:27]** easiest solution is to just make a

**[2:28]** staircase and put a repeat when you run

**[2:30]** out of signal strength this does make it

**[2:32]** a little bit ugly because now the next

**[2:34]** diagonal is shifted over by one block so

**[2:36]** sometimes what I'll do is I'll put

**[2:37]** torches on the sides of the blocks this

**[2:39]** allows you to do a double negation or

**[2:41]** even a single negation without Shifting

**[2:43]** the blocks over and then if you're going

**[2:45]** down on a diagonal there's really only

**[2:46]** one solution you'll ever need all you

**[2:48]** have to do is put a repeater into a

**[2:50]** block and it'll carry it down nice and

**[2:52]** easy without Shifting the line next


## Multi-Bit


**[2:54]** let's talk about how to wire multiple

**[2:56]** signals at once in general people like

**[2:58]** to send multiple signals in two main

**[3:00]** ways stacking the wires horizontally or

**[3:03]** vertically when Redstone first came out

**[3:05]** horizontal was more popular because it

**[3:07]** looked more like a real circuit But as

**[3:09]** time went on people found some nice

**[3:10]** advantages of making them vertical for

**[3:12]** example it's easier to turn the wires

**[3:14]** instead of every wire having a different

**[3:16]** length vertical wires turn in syn but

**[3:18]** I'm going to cover both of these

**[3:19]** techniques because both kinds of wiring

**[3:21]** still come up a ton now in both of these

**[3:24]** cases the wires are stacked every two

**[3:26]** blocks which is usually small enough for

**[3:28]** whatever you're building but if you need

**[3:30]** to squeeze them together you can stagger

**[3:31]** them one block apart from each other

**[3:33]** like this this works in the exact same

**[3:35]** way if you input the second lamp then

**[3:38]** the second output turns on and you can

**[3:40]** still turn it which is pretty cool going

**[3:42]** upwards there's not really any fancy

**[3:44]** tricks the best you can do is make a

**[3:46]** glass tower for each wire and stack them

**[3:48]** next to each other here I have two

**[3:50]** examples of that one using repeaters and

**[3:52]** one using torches once again if you

**[3:54]** really need to squeeze them together you

**[3:56]** can stagger them like this just make

**[3:58]** sure that the extensions don't mess with

**[3:59]** the towers around them going downwards

**[4:02]** just like before spirals are probably

**[4:04]** the best way to go when putting a bunch

**[4:05]** of spirals next to each other I've seen

**[4:07]** a lot of people do it like this where

**[4:09]** each tower has one block of space in

**[4:11]** between but there actually is a way to

**[4:13]** put them right next to each other you

**[4:14]** just have to alternate between a

**[4:16]** clockwise spiral and a counterclockwise

**[4:18]** spiral so that's pretty cool going

**[4:20]** diagonal this is where things start to

**[4:22]** get interesting if you have horizontal

**[4:23]** wires then you can just use the same

**[4:25]** strategies as before stack next to each

**[4:27]** other and if you want them to be closer

**[4:29]** you can stagger them like this with

**[4:31]** every other wire being two blocks lower

**[4:33]** than the rest if you have vertical wires

**[4:35]** one common solution is to alternate

**[4:37]** between glass and regular blocks which

**[4:39]** allows all the signals to go up

**[4:41]** independently and diagonally however

**[4:44]** this strategy only goes one block up for

**[4:46]** every two blocks across which is kind of

**[4:48]** annoying so to solve this you can just

**[4:50]** stagger them again by having half the

**[4:52]** wires one block over they can all go up

**[4:55]** on a regular diagonal or another way to

**[4:57]** solve it is like this if you make it

**[4:59]** exact L 15 blocks long and the whole

**[5:01]** thing is glass then you actually don't

**[5:04]** need to stagger them this works because

**[5:06]** only the wire you turned on has enough

**[5:08]** strength to get to the repeater and when

**[5:09]** you're going down a diagonal everything

**[5:11]** I've said here Works in Reverse well

**[5:13]** except for that last trick unfortunately

**[5:15]** there's no way to do this when going

**[5:17]** down you'll have to either do this or

**[5:19]** stagger them it's also worth mentioning


## Horizontal / Vertical Conversion


**[5:21]** how to convert between horizontal and

**[5:23]** vertical wiring there are lots of ways

**[5:25]** to do this but my favorite way is with

**[5:27]** glass Towers when going from horizontal

**[5:29]** to Vertical you can use a glass tower

**[5:31]** for each wire getting taller and taller

**[5:34]** and then for vertical to horizontal it's

**[5:36]** really similar this is probably the

**[5:38]** cleanest way to convert between the two

**[5:40]** although one problem you might have is

**[5:42]** that the leftmost bit goes to the bottom

**[5:44]** and the rightmost bit goes to the top

**[5:46]** sometimes you actually want that to be

**[5:47]** the reverse in that case you have two

**[5:50]** options you can make it with spirals

**[5:52]** instead going down or you can just go to

**[5:54]** the right instead of left both of these

**[5:56]** options will basically flip the output

**[5:58]** finally let's talk talk about wiring hex


## Hex


**[6:00]** or signal strength values one tip I

**[6:03]** always tell people when wiring hex is to

**[6:05]** ask yourself do I really need to wire

**[6:07]** hex I mean the conversion from hex to

**[6:09]** Binary and binary to hex is really fast

**[6:12]** just two or three ticks on most designs

**[6:14]** so if it's a long distance you should

**[6:16]** see if it's better to convert to Binary

**[6:17]** first and then back to hex at the end

**[6:19]** that'll make it way faster in a lot of

**[6:21]** cases but once you're sure that you need

**[6:23]** to wire hex here are some of the best

**[6:25]** Solutions starting with flat ground the

**[6:27]** most straightforward approach is to use

**[6:29]** a chain of comparators but this is very

**[6:31]** slow the faster way to do it is with

**[6:33]** something like this this circuit uses

**[6:35]** the property that a signal strength X

**[6:38]** will travel for X blocks right now I put

**[6:41]** in a five so the fifth repeater is the

**[6:43]** last one to turn on and since there are

**[6:45]** 15 repeaters in this row it'll decrease

**[6:47]** for 10 more blocks which puts it back to

**[6:49]** five so no matter what strength you put

**[6:51]** in here it comes out on the other side

**[6:53]** very quickly now in this version of the

**[6:55]** circuit it's 15 repeaters long but it

**[6:57]** doesn't have to be if you want to

**[6:59]** shorten it it's really easy you just

**[7:01]** have to subtract from the total the

**[7:02]** number of blocks shorter it is for

**[7:04]** example this one is four blocks shorter

**[7:06]** so I just need to subtract a four on the

**[7:08]** end and as you can see if I put in a

**[7:10]** five I still get a five now if I'm being

**[7:13]** honest all of the remaining hex

**[7:15]** Solutions are basically just variations

**[7:17]** on this circuit they all follow the

**[7:19]** exact same pattern a dust line a bunch

**[7:21]** of repeaters and another dust line the

**[7:24]** one going upwards has a glass tower a

**[7:26]** bunch of repeaters and another glass

**[7:28]** tower so of course if you put in a seven

**[7:30]** you'll get a seven at the top the one

**[7:32]** going down definitely looks like it

**[7:34]** might be different but I assure you it's

**[7:36]** the exact same circuit this spiral right

**[7:39]** here is the first dust line then there's

**[7:40]** a bunch of repeaters and this spiral is

**[7:42]** the second dust line then for diagonal

**[7:45]** you can just take the circuit and

**[7:46]** staircase it like this this one right

**[7:48]** here is three blocks wide but there's

**[7:50]** also a version that's only two blocks

**[7:52]** wide and that goes for the downward

**[7:54]** diagonal as well there's a three wide

**[7:55]** version and a two wide the only other


## Crosswire


**[7:58]** major scenario that you'll probably run

**[8:00]** into a lot is crossing wires through

**[8:02]** each other for example let's say you

**[8:04]** have two wires one going this way and

**[8:06]** one going this way and you don't want

**[8:07]** them to interfere with each other in

**[8:09]** this case the solution is really simple

**[8:11]** just put one wire over the other one but

**[8:13]** when you have two multi-bit signals

**[8:15]** trying to cross things can get a little

**[8:17]** more complicated luckily though there's

**[8:19]** an easy solution all you have to do is

**[8:21]** use an intersection like this which uses

**[8:23]** repeaters to make sure that they don't

**[8:24]** interfere with each other and this type

**[8:26]** of intersection is stackable every two

**[8:28]** blocks so you can use it to cross two

**[8:30]** sets of vertical wires personally I

**[8:33]** think this is the most elegant solution

**[8:34]** but I should probably mention that

**[8:36]** there's another way to do it without

**[8:37]** using repeaters At All by using 3D space

**[8:40]** and a lot of Staggering you can actually

**[8:42]** make a zero tick crossover I've never

**[8:45]** used this because it's kind of messy but

**[8:47]** if you really need that extra speed it's

**[8:49]** a good option okay so that covers most


## Building Techniques


**[8:52]** of the scenarios you'll hit when

**[8:53]** building Redstone but there's still a

**[8:55]** big question that I haven't really

**[8:56]** answered what's the best way to build

**[8:58]** these well first first and foremost

**[9:00]** don't build them by hand I highly

**[9:02]** recommend getting a mod called world

**[9:03]** edit which allows you to edit the world

**[9:05]** using in-game commands I also recommend

**[9:07]** getting a mod called Redstone tools

**[9:09]** which I'm the owner of redstone tools

**[9:11]** gives you even more commands and even

**[9:13]** lets you set custom macros to fit your

**[9:15]** style me personally I have three macros

**[9:17]** set up two for moving things back and

**[9:19]** forth and one for stacking unfortunately

**[9:22]** there's not enough time for me to show

**[9:23]** you how I would build every circuit here

**[9:25]** but let's go through a few examples

**[9:27]** first let's say I wanted to make 8

**[9:29]** horizontal wires I'd probably start with

**[9:31]** just three dust and stack it four times

**[9:34]** then I'd put a repeater on the end and

**[9:36]** stack it a bunch of times this way then

**[9:38]** I'd select the whole thing and stack it

**[9:40]** seven times next let's say I wanted to

**[9:42]** make eight glass Towers I'd start with

**[9:44]** two glass put redstone on top of them

**[9:46]** and then run/ SLR stack 30 up 2 you can

**[9:51]** use regular stack for this but sometimes

**[9:53]** this makes the Redstone disappear

**[9:54]** because it doesn't have glass under it

**[9:56]** as it Stacks then I'd power it from the

**[9:58]** bottom to see where it runs out of

**[10:00]** signal strength it's right here so I

**[10:02]** would build two torches then I would

**[10:03]** select the two torches and run SL SLR

**[10:06]** stack to up 16 this puts torches every

**[10:10]** 16 blocks allowing the signal to reach

**[10:12]** the top then I'd select the whole Tower

**[10:14]** and stack it seven times and finally

**[10:16]** let's say I wanted to make eight

**[10:17]** vertical wires go down diagonally I'd

**[10:19]** probably start with the bottom wire I'd

**[10:21]** build a block glass block glass then

**[10:25]** copy that and paste it and copy and

**[10:27]** paste it one more time then I'd put put

**[10:29]** repeaters on the end since it's exactly

**[10:31]** 16 blocks long and copy and paste this

**[10:33]** for as long as I need then I'd select

**[10:35]** the whole wire and run sl/ rstack 7

**[10:39]** up2 I hope this video was helpful to you


## Subscribe!


**[10:41]** in one way or another the World download

**[10:43]** is in the description if you'd like to

**[10:44]** check out any of the circuits if you

**[10:46]** enjoyed this video subscribe and if you

**[10:48]** really liked it you can support me on

**[10:50]** patreon in the description building


## Sponsor


**[10:52]** circuits takes a lot of practice and

**[10:54]** sometimes it can be difficult to know

**[10:55]** where to go to learn more but one place

**[10:57]** that has always helped me out is

**[10:58]** brilliant the sponsor of this video

**[11:00]** brilliant is where you learn by doing

**[11:02]** with thousands of interactive lessons in

**[11:04]** math data analysis programming and AI

**[11:06]** it's a platform based on understanding

**[11:08]** things from the ground up you learn

**[11:10]** things way faster than you would

**[11:11]** watching videos because there are

**[11:12]** Hands-On activities in every Lesson by

**[11:14]** solving actual problems and not just

**[11:16]** memorizing things you won't just build

**[11:18]** knowledge you'll become a better thinker

**[11:20]** learning a little bit every day is a

**[11:22]** great way to grow both personally and

**[11:24]** professionally brilliant helps you do

**[11:25]** this with lessons that are available

**[11:26]** whenever you have time one of my

**[11:28]** favorite courses is how technology Works

**[11:30]** which takes you inside the tech you use

**[11:32]** every day you'll play with things like

**[11:34]** computer memory GPS systems and more to

**[11:36]** try everything brilliant has to offer

**[11:38]** for free for a full 30 days visit

**[11:40]** brilliant.org batwings or click the link

**[11:42]** in the description you'll also get 20%

**[11:44]** off in annual premium subscription
