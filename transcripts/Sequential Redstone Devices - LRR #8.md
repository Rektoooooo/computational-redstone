# Sequential Redstone Devices - LRR #8

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=XCug8h5oEGE
- **Duration:** 15:16
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to logical Redstone reloaded last episode we talked about latches and flip-flops today we're going to create some really cool sequential circuits I hope you enjoy let's start with some terminology back in episode 6 I said that all the circuits in that episode were combinational the output of a combinational circuit depends on only the input once you input something you

**[0:20]** automatically know what the output will be it's predetermined by a truth table but the circuits we'll see today are not combinational instead they're called sequential the output of a sequential circuit depends on not just the input but also the state of the circuit itself for example this is the T flip flop from the previous episode which toggles whenever the button is pressed so what

**[0:41]** will the output be when I press this button it depends right it depends on the state of the T flip-flop If the previous output was Zero the next one will be one and if it was one the next one will be zero therefore a t flip-flop is a sequential circuit in fact all latches and flip-flops are sequential circuits for the same reason so for the rest of this episode let's build up a

**[1:02]** toolbox of some useful sequential devices remember that a data latch or a d-latch can be made with just a repeater lock and it allows us to capture one bit of information but one bit is not very much so let's stack eight repeater locks on top of each other and combine all the latching signals together with a glass tower this is called a register specifically this is an 8-bit register

**[1:24]** so it can store any 8-bit number you want to store a number simply put it in the back and activate this two tick pulse generator to quickly unlock and re-lock the repeaters as you can see the repeater locks are now storing the number if I want to store a different number instead I can simply put it here and press the button again this is called loading a register sometimes it's

**[1:45]** called writing to a register as well but I prefer saying load additionally it can be useful to have a read function as well this is an 8-bit register with both load and read the load button does the same thing as before loading the repeater locks with the data but now now the data is not shown on the output because it's being canceled by these comparators pressing the read button

**[2:06]** will quickly uncancel the comparators giving us an output and allowing us to read the data next let's talk about binary counters a binary counter stores a binary number and every time you press the count button it increments by one to make this I'll start by having a t flip flop for every single bit and you'll see why in just a minute now notice from this table that as you count up in

**[2:27]** binary the rightmost bit or the one bit toggles between 0 and 1. you can see the pattern of the one bit going 0 1 0 1 forever so let's just plug the count signal into the rightmost T flip-flop now every time we count up it will toggle between 0 and 1. okay so the one bit is already done the next question is when should the 2-bit toggle well looking at the table again we can see

**[2:52]** that the 2-bit toggles whenever the one bit is carrying over in other words when the one bit goes from one to zero and what's really cool is that this property generalizes to any bit when counting up in binary the 4-bit toggles whenever the 2-bit goes from 1 to 0 and the 8-Bit toggles whenever the four bit goes from 1 to 0. with redstone we can detect this using a torch a torch will turn on when

**[3:16]** a signal goes from one to zero so let's put a torch on the output of every T flip-flop and plug them into the toggle signals of the next bit over when the one bit goes from one to zero it will toggle the two when the two bit goes from 1 to 0 it will toggle the four Etc and now this is a binary counter when you press the count button you get one two three four Etc this type of counter is called a

**[3:44]** ripple counter because the toggles Ripple across the counter and you can repeat this pattern for as long as you want to make a counter of any size of course there are many other designs for a ripple counter as well here's one made by Seth bling that I thought was really cool it just uses pistons and observers where each piston acts like a t flip-flop when we give it an update you

**[4:03]** can see that on the wool blocks it's actually counting up in binary the green wool is one and the red wool is zero and here's another Ripple counter I found on Reddit which is absolutely tiny it's a little difficult to read the binary but it's in The Observers as they pop out one two three four yeah okay so Ripple counters are great but they suffer from the same problem that

**[4:28]** the Ripple carry Adder did as your counter gets larger the toggles take longer and longer to propagate so let's design a synchronous counter or a counter that always gives an output completely synchronized to do this let's start by analyzing the case of seven when going from seven to eight ask yourself this question why should the 8-Bit toggle if you asked a ripple

**[4:49]** counter this question it would say well the one bit toggled which toggled the two which toggled the four and then the eight but we're smarter than a ripple counter we have a much better reason and that is that all the bits to the right of the 8-Bit are one in fact the only time any bit toggles is when all the bits to the right of it are one I mean look at what happens when you increment

**[5:10]** seven every single bit gets toggled because every bit is followed by all ones the 8-Bit is followed by all ones the 4-bit is followed by all ones the two bit is followed by all ones and the one bit well the one bit always toggles as another example to increment zero one 1 or 11 I can just toggle the bits that are followed by all ones in this case that would be the 4 bit the 2-bit and

**[5:36]** the one bit not the 8-Bit because there's a zero coming after the 8-Bit and sure enough toggling those bits gives us one one zero zero which is twelve perfect this is the logic behind a synchronous counter any bit toggles whenever all the previous bits are one and if you want a fun challenge pause the video now and try making one yourself I haven't done one of these

**[5:56]** challenges in a while so why not bring them back foreign welcome back while you were gone I found this which is one of my favorite designs for a synchronous counter as you can see there is no Rippling the output is completely synchronized the way this is implemented with redstone is actually really clever notice that this type of T flip flop is completely disabled when this Redstone

**[6:17]** is forced on so if you place a torch on all the previous bits and wire them into the Redstone you've essentially made it so that it can only toggle when all the previous bits are one once they're all one all the Torches turn off and now it can toggle so that's the strategy being used in this synchronous counter the only way a bit can toggle is once all the previous torches turn off AKA all

**[6:41]** the previous bits are one this counter also has a beautiful vertical design using a glass tower making it incredibly fast and Compact and it's expandable up to eight bits well as long as the Redstone reaches you might need a Target block at the top but yeah I can't express how much I like this design it's my go-to whenever I need a binary counter it's small fast and of course

**[7:02]** completely synchronized before moving on to the next sequence sequential device I have one more surprise for you that makes this counter even better since the repeater locks are stacked on top of each other now it's relatively easy to implement a load function as well this is a synchronous counter with load to increment the counter press the count button and it

**[7:21]** counts up just like before but now you can also load it with something else simply put the data you want to load here and press load and if you press the count button again it will just continue counting from whatever we loaded which is super cool and that's about it for binary counters as always if you ever want to take a closer look at any of this Redstone the World download is in

**[7:41]** the description next let's talk about shift registers a shift register simply stores a number and allows you to shift it this is an 8-bit shift register that allows you to shift the data upwards when you press the shift button the data moves up by one to make this I just took a normal register and plugged every output up into the next highest input so by unlocking and re-locking the

**[8:03]** repeaters with the shift button the register gets loaded with the shifted up version of its own data and here's a version that shifts down instead of up it looks almost exactly the same the data just moves down this time one of the reasons shift registers are so useful is because in binary shifting up multiplies by two and shifting down divides by two for example this is the

**[8:23]** number six shifting up makes it 12 and shifting down makes it three you can also use a horizontal design to shift data to the left or right this one over here shifts data to the left and this one shifts data to the right the one problem with these designs which you might have already noticed is that there's no load function and without a load function the only way to get data

**[8:44]** into a shift register is to load it in one bit at a time for example if I wanted to put a 4 into this my only option is to load a 1 from the bottom and shift it up twice so this next device is an upward shift register with a load function you can load data by here and pressing load and you can shift it up by pressing shift the way this works is with a multiplexer the shifted

**[9:09]** data and the load data are both being canceled by comparators if you press shift then the shifted data gets uncanceled and the repeater locks capture it but if you press load the load data gets uncanceled and once again the repeater locks capture it and of course using this exact same technique you can add a load function to a downward shift register as well next

**[9:29]** let's look at a bi-directional shift register as the name suggests you can shift the data both up and down using these buttons and this bi-directional shift register has a load function as well so you can literally put in any data you want and immediately shift it up or down now it's worth mentioning that you don't need to have two sets of repeater locks to make this device I

**[9:50]** just chose to do that because it makes the wiring a little bit easier honestly you can just imagine them as one set of repeaters because they're always kept the exact same but with that out of the way this device is not any more complicated than the previous two it's really just another multiplexer this time it's a three-way multiplexer between the upshifted data the

**[10:11]** downshifted data and the load data whichever option we choose out of these three buttons the corresponding data gets uncanceled and then captured by the repeater locks also bi-directional shift registers can be made horizontally too here's a design that I made a long time ago using Pistons unfortunately it doesn't have a load function but you can still shift left and shift right and the

**[10:32]** last shifting device I want to show you is a bit of a special one if you take a shift register with a single bit in it and you plug the output all the way back into the input it becomes a ring counter the bit travels around and around the register as if it was on a circus ring I guess I actually don't know why they're called rain counters someone enlightened me in the comments but yeah these come

**[10:53]** up every once in a while and they can be pretty useful you can also hook up an encoder to a ring counter and now you have a way to go through any sequence you want you could make it a binary counter or a fake prime number generator or even another ring counter it's up to you next up this device allows you to keep a running total as you add binary numbers for example starting from zero I

**[11:15]** can add three and then add 2 to the total to get five and then add four to the total to get nine this works by combining a register with an Adder whatever is currently in the register comes around here and gets added with whatever number you want which is then plugged back into the register I'm not exactly sure what this device is called I've heard some people call it an

**[11:40]** accumulator but it's possible that it doesn't really have a name also it's worth mentioning that if you just keep the added number as one it becomes a binary counter and if you make the added number all ones which is negative one in two's complement it counts down instead of up so yeah I really like this device because it's basically a counter with more freedom and if you wanted to do a

**[12:01]** different operation you could always just swap out the adder for something else all right so all the circuits we've seen so far have only worked with 8 Bits at a time but what if you wanted to work with more memory well you could just make a bigger register but a better strategy is to combine many registers together into a single system this is a device that combines eight registers together into a

**[12:23]** single memory bank each register is given an address zero through seven which is basically that registers unique identifier using this input panel I can write to or read from any of the registers for example let's write a 15 to register three the 15 goes here the address of three goes here and then we press right let's also write a 10 to register 2. the 10 goes here the 2 goes

**[12:51]** here and right now that we've loaded some registers let's try reading them I'll put in a three and read and look at that we get 15 or if we read what's at address 2 we get 10. very nice and let me show you how the actual Redstone works too because I think it's really cool basically the right signal in green is attempting to write to every single register but it will only go

**[13:15]** through if that register has been decoded for by this decoder so by putting an address here we're unlocking only the register with that address if I unlock the third register then when I press right only the third register gets written to and it's the exact same idea with the read signal if I unlock the second register and press read only the second register gets read and that's

**[13:39]** most of the complexity from there you just add your registers on top combine all the inputs together and combine all the outputs together finally let's talk about some hexadecimal devices this is a signal strength memory cell it's just two comparators in a loop you can think of this like a data latch but for any signal strength 0-15 if I input a 3 the 3 gets stored in the cell and to store a

**[14:03]** new number I can just reset the cell and and input something else I use this type of memory whenever it's more convenient to store hex values than binary values for example in my 2048 game every tile was stored internally as a single hex value another useful device is the hexadecimal incrementer decrementer when I press this button the signal strength counts up and when I press this button

**[14:26]** the signal strength counts down another cool thing you can do with signal strength is create a decaying signal this is a comparator loop where the signal strength inside of it will Decay by 1 after every cycle if I input 15 then it decays to 14 13 12 Etc this can be used to create super small Redstone timers because when I press this button the Redstone won't turn off for a very

**[14:49]** long time only once the signal on the inside decays to zero will the Redstone finally turn off next episode we'll talk about displays I'll see you there if you enjoy these videos subscribe and check out my patreon page in the description I also have a redstone Discord server so come join us if that sounds interesting I hope you learned something I hope you enjoyed peace out guys [Music]
