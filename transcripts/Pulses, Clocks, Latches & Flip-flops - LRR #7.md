# Pulses, Clocks, Latches & Flip-flops - LRR #7

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=N-edYGFQIjY
- **Duration:** 13:44
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to logical Redstone reloaded last episode we covered a bunch of combinational logic devices today we're going to talk about some smaller circuits that I think you'll find really useful I hope you enjoy so far in this series whenever I showed a circuit I've only cared about what the values of the input and output are I never really focused on the length

**[0:18]** or timing of redstone pulses but today that changes let's get more comfortable with redstone pulses and how to use them remember from episode 1 that Minecraft runs on a tick system and there are 10 Redstone ticks per second therefore each tick is a tenth of a second which we can use as a unit of time for example a stone button stays on for exactly one second but you could also say that it

**[0:39]** stays on for 10 ticks because of this a stone button is essentially a 10 tick pulse generator any Redstone connected to a stone button will receive a 10 tick pulse when the button is pressed and a wooden button is a 15 tick pulse generator activating Redstone around it for one and a half seconds now if you want to generate a shorter pulse my favorite way to do it is with a

**[0:58]** comparator for example this is a two tick pulse generator when I press this button the comparator receives a signal but two ticks later it gets canceled giving us a nice two-tick pulse the delay between the initial signal and the cancellation is the length of the pulse that gets generated if I make the delay 4 ticks instead it becomes a four tick pulse generator and by the way a little

**[1:19]** trick to prove to yourself that this is indeed a Fortec pulse is to put it into a line of repeaters and freeze the game as you can see the pulse is exactly four repeaters long or if you don't have carpet mod you can also lock the repeaters the one downside to this design is that you can't use it to generate a one-tick pulse it simply won't give an output the reason gets

**[1:38]** pretty technical but it's basically because of how competitors update themselves in my opinion though you shouldn't be using one tick pulses anyways because they tend to cause issues but if you to do it is with observers observers output a one-tick pulse whenever they receive a block update in the back but anyways whenever I make pulse generators this comparator setup is my go-to of

**[1:59]** course there are still many different designs as well especially using observers pistons and droppers and I'll leave those in the World download if you're interested now keep in mind that this strategy will only allow you to generate a pulse shorter than the button pulse because the that's kind of what these circuits are doing they're shortening the pulse from a button if

**[2:16]** you want to generate a pulse longer than the button you need to lengthen it instead of shortening it for example let's take this 10 tick button pulse and extend it to last for three more ticks I'll put another dust here a three tick repeater and a block so that the signal Powers the main line and now when I press this button we get a 13 tick pulse a great way to visualize What's

**[2:37]** Happening Here is with a diagram the original button pulse lasts for 10 ticks so if each block represents one tick of time then that's 10 blocks of wool now because of this repeater we're essentially generating another 10 tick pulse three ticks later which looks like this on the diagram and if you ore these together you'll notice that we're getting a consistent signal from at

**[2:57]** least one of them for the first 13 ticks so that's why this circuit works as a 13 tick pulse generator while we're on the subject of pulse extension there's an interesting property of repeaters that I should probably mention in this video If a repeater receives a pulse shorter than its delay length it will extend it up to that length for example here I have a two tick pulse generator immediately

**[3:18]** going into a three tick repeater you would expect the two tick pulse to just go through the repeater and come out three ticks later but that's not exactly what happens yes it does come out three ticks later but it also gets extended to a three tick pulse this extension will happen anytime a repeater receives a pulse that is shorter than its delay setting we saw it happen here because 2

**[3:38]** is less than three as another quick example if you give a one tick pulse to a four tick repeater it'll output a four tick pulse because one is less than four next let's talk about clocks a clock is just a circuit that outputs a signal on a regular basis the easiest way to make a clock is to just create a redstone Loop and put a pulse inside of it for example this clock outputs a signal

**[4:01]** every five ticks the loop is five ticks long so every time the pulse completes a cycle another five ticks have passed and by changing how many ticks are in the loop you can change how long the clock cycle is also when clocks are brought up in discussions you'll often hear the terms period and frequency the period is just the length of the clock cycle the time from one output to the next so

**[4:21]** clock has a five tick period or 0.5 seconds and the frequency is how frequent those Cycles are with respect to time since every Cycle takes half a second there are two cycles per second therefore the frequency is 2 Hertz Hertz literally means cycles per second additionally period icy have an inverse relationship if you take one divided by the period you get the frequency or if

**[4:45]** you take one divided by the frequency you get the period now this type of clock is great but it can be kind of annoying to start it and stop it to start it you have to hook up a pulse generator to it and to stop it you have to somehow kill the pulse perhaps by canceling a comparator or by using a piston to break the loop but there's another design for a clock that is much

**[5:05]** easier to start and stop and it looks like this simply take a comparator on subtract mode and Route it back into its own side when you power the comparator from the back the clock starts and if you stop powering it the clock stops unlike the previous design this new type of clock produces a perfect alternating signal for example this clock's Loop has a total of five ticks one for the

**[5:27]** comparator plus four for the repeater so the signal coming out of it is alternating every five ticks five ticks on five ticks off five ticks on five ticks off and this means that the period of this clock is actually 10 ticks because it's producing a 5 tick pulse every 10 ticks alright as a final challenge just to kind of sum everything up let's create a clock that has I don't

**[5:49]** know a 16 tick period and outputs a three tick pulse I'll start with a comparator and add seven more ticks to the loop before canceling it so this clock will give an 8 tick pulse every 16 ticks to make it a three tick pulse instead we can just add another comparator which gets canceled three ticks later and there we go this is exactly what we want a clock with a 16

**[6:10]** tick period that outputs a three tick pulse and best of all we can easily turn it on and off with this lever in the back beautiful alright for the rest of this video let's talk about latches and flip-flops latches and flip-flops are basically small useful circuits that use memory to their advantage but how can a circuit have memory what does that even mean well take a look at this circuit we

**[6:31]** have an or gate with the output looping back to one of the inputs if I power the input then it will stay on forever even if I stop powering it in a way this lamp being on is the circuit remembering what I did the problem is it can't forget it there's no way to switch this back to zero unless I manually break the circuit so consider this circuit instead this time we have two torches in a chain with

**[6:55]** the output of the second one looping back into the first one if we force the first torch to be off then the second torch turns on giving us a permanent output and if we force the second torch to be off then the first torch turns on and it switches back to how it was before with the lamp permanently off this is called a set reset latch or an Sr latch because you can set the lamp to

**[7:19]** be on or you can reset it to be off now me personally I find SR latches easiest to think about if you view them as two not gates with someone hijacking the signal but technically that's not how it works these torches are actually nor gates in fact if you make a big Sr latch like this it's much easier to see why it's made with two Norse the set signal and the output are clearly no board and

**[7:42]** put into a second nor with the reset signal and as you can see it's the same circuit I can set it and I can reset it one cool thing about Sr latches is that you can get the inverse of the output for free notice that the first nor always outputs the opposite of the second one so if you just route that to the front as well you now have the regular output and the inverted output

**[8:04]** this wiring is kind of weird though so another way to do it is to put the nor gates side by side and have the outputs crisscross each other on the way back this makes it way easier to get the regular output and the inverted output and if you search Sr latch on Google Images you'll notice that this is the most common layout for it it's the design that you'll see many times if you

**[8:23]** take a class on digital logic but in Minecraft you don't have to use this giant circuit for an Sr latch there are actually some much smaller designs for example here's my favorite design for an Sr latch it's absolutely tiny here's your set here's your reset here's your regular output and here's your inverted output the last thing I want to mention about Sr latches is that it can be

**[8:44]** useful to enable them or disable them you can do this by putting two comparators in the front with a torch this lever is called the enable signal when the enable signal is one the latch is enabled so you can set it or reset it just like normal but when the enable signal is off the latch is disabled so you can't mess with it very nice alright so Sr latches are great and I use them

**[9:08]** all the time but an interesting question is what happens if you try to set it and reset it at the same time well this is where it gets weird if you set and reset at the same time then the output and the inverted output are both one which makes no sense something in its inversion should never be the same thing so this next type of latch called a data latch or d-latch is kind of an attempt to

**[9:33]** solve that problem a data latch uses an Sr latch as a base and then it has one input called the data the data is plugged directly into set and the inverted version is plugged into reset the motivation behind this is that when you're using an Sr latch you tend to either be setting and not resetting or resetting and not setting which is exactly what this setup forces you to do

**[9:55]** so this is a data latch when the data is one the the output is one and when the data is zero the output is zero but that's not very useful right I mean what's the point of having a circuit where the output is just the input well honestly there isn't one however it starts to get interesting when you add an enable signal to a d-latch if you disable a d-latch then the output is

**[10:19]** whatever the data was at the time of disabling it so this allows us to capture data at a specific time think of it this way when the latch is enabled it's simply listening to the data and repeating what it hears but when it gets disabled it captures the current data in place and now it's not listening anymore and this idea of capturing data is so useful that Mojang gave us a way to do

**[10:42]** it really really easily it's a repeater lock a repeater lock is literally a d-latch when it's unlocked it simply repeats the data and locking it captures the data so yeah if you find yourself needing a d-latch you don't need to use this big setup you can just use a repeater lock and that's it for latches Sr and data are the two main types of latches in digital logic finally let's

**[11:05]** talk about flip-flops flip-flops are extremely similar to latches as far as I can tell from my research the main difference is how the enable signal gets used a latch can be enabled or disabled at will which means that latches are either constantly responding to the inputs or never responding to the inputs on the other hand a flip-flop is meant to be used with a clock by hooking up a

**[11:27]** clock to the enable signal a flip-flop updates itself every clock cycle and as it turns out the SR latch and the d-latch have a corresponding Sr flip-flop and D flip-flop but they're literally the exact same circuit the only difference is that the enable signal is hooked up to a clock I mean this is the D flip flop it's literally just a repeater lock like we had before

**[11:48]** but this time it gets quickly unlocked after every clock cycle this means that on every clock cycle it gets updated with whatever the current data is the other flip-flop I want to show you is the toggle flip-flop or t flip flop every clock cycle if the input is 1 it toggles otherwise it does nothing this design uses an Sr as a base but there's actually a much better design for a t

**[12:12]** flip-flop this is a tiny T flip-flop using once again a repeater lock when I press this button the output toggles between on and off I don't know enough about the game's code to understand how this one actually works but feel free to explain it in the comments if you know now technically this design isn't exactly a t flip-flop it's more like a t flip-flop where the main input is always

**[12:34]** one and you are the clock signal when you press this button but whatever it's close enough ultimately what makes it useful is its ability to toggle and there are many other designs for a t flip-flop as well which I've included in the World download for example here's a tiny one using an observer and a piston now you might be wondering what about a t latch is that a thing well even though

**[12:56]** latches and flip-flops are very similar I would argue that a t-latch is not a thing I say that because if you force a t flip-flop to be constantly enabled instead of using a short clock pulse it just keeps toggling forever and that is definitely not something a latch should do so yeah I don't think a t-latch makes a lot of sense but everything else here is pretty well defined next episode

**[13:19]** we'll be using these latches to create registers counters and other exciting circuits if you enjoy these videos subscribe and check out my patreon page in the description I also have a redstone Discord server so come join us if that sounds interesting I hope you learned something I hope you enjoyed peace out guys [Music]
