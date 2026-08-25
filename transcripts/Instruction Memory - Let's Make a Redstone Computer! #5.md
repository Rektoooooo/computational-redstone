# Instruction Memory - Let's Make a Redstone Computer! #5

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=wAwMQp0KNMI
- **Duration:** 15:07
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer things are getting a lot more advanced now we have a new control ROM and 6 out of 16 instructions in our instruction set today we're going to create a new component to make running a program way easier before we make a new component though I want to start off by introducing a brand new instruction one that doesn't require any

**[0:19]** new hardware or anything it's called No operation or no Op with OP Code Zero and the pneumonic n o no op literally does nothing when the computer EX it none of the memory should change whatsoever so for the control bits let's make the enable signal for the register file a zero that way it doesn't get written to when the instruction is executed and then it doesn't really matter what the

**[0:42]** rest of the control bits are so I'll just write an X for them meaning they can be one or zero on the diagram let's execute a noop specifically this noop has all zeros for the operands so in assembly it would be written as noop r0 r0 R and to start off let's say that this is the data in the register file the op code goes in here which makes it output a zero for enable and whatever

**[1:06]** you want for the rest of them let's just say zero the operands go into their spots and when you press clock nothing happens because you can't write to a register file when it's disabled as another example let's say the noop has operands R1 R2 and R3 instead op code goes in here operands go in here and once again executing it does nothing in fact nothing even comes out of the

**[1:28]** register file in the first first place because again it's disabled therefore it doesn't actually matter what these operand bits are this is a no op but so is this and so is this they're all functionally the same so it's kind of silly to say that noop has three register operands I mean you can but these operands are not relevant to the instruction to be more accurate let's

**[1:51]** gray out the entire operand section to signify that it doesn't matter what these bits are and then in assembly let's just write no Op with no operands instead of writing it like this or this we'll just write it as noop that's it the assembler will automatically assemble it to 0 followed by well anything will work in my assembler I just made it followed by all zeros all right so in the last

**[2:16]** episode we ended off by assembling and running a three-line program by hand on the real computer and this worked perfectly we saw that the registers got updated just like we expected but this method of putting in machine code manually is really tedious and prone to error one wrong lever input means you're going to execute the wrong instruction so let's make a new component to store

**[2:37]** the program for us I'll call this component the instruction memory the instruction memory will hold a list of instructions each at their own unique address it's a combinational component that takes an address as input and outputs the instruction at that address for example if these instructions are in the instruction memory then putting in address zero will output this or putting

**[2:58]** in address one will output this so naturally when we fill the instruction memory with a program let's make it start at address Z and count up address Z will store the first instruction address one will store the next one and so on now the number of bits in the address directly determines how many instructions we can store if we use a three-bit address then we can

**[3:18]** store up to eight instructions because there are eight combinations of three bits 0000 to 111 or 0 to 7 in general for an nbit address we can store up to 2 to the n and instructions so how big should our actual addresses be this is a really interesting question because it's a balance of pros and cons a bigger address means you can fit bigger programs and therefore do more complex

**[3:41]** things but as the instruction memory gets bigger it also gets slower and laggier so for our computer I'm going to make it a 10bit address meaning we'll be able to store 2 to the 10 or 1,24 instructions when I made this computer the first time I found that 1024 was a pretty good balance it's enough instructions to run crazy things like Tetris but it's not so big that it makes

**[4:02]** Minecraft crash okay let's make the instruction memory in Minecraft the first thing we need is a 10 to 1,24 decoder that way we can put in an address and find the physical location of that instruction so far in this series I've always made decoders in one straight line such as this 4 to6 decoder but this design creates some problems when you scale it up to 10 to 1,24 the

**[4:26]** most obvious problem is that it becomes extremely long so let's make it in a tree formation instead when you put in the address here it spreads out and propagates to all the branches of the decoder this makes the overall footprint more rectangular and it's also quite a bit faster but another problem is that it becomes extremely laggy when you put in the address it visits thousands of

**[4:46]** repeaters and torches so I'm actually using a fancy trick here to help with that the bottom four bits of the address are used to find which branch it's on first and then the rest of the bits are defined where on that Branch this makes it more efficient and less laggy because instead of searching all the addresses it only searches on one branch if that didn't make sense don't worry this is

**[5:06]** just an optimization it's not super important functionally this is still a normal 10 to 1024 decoder when you put in the 10bit address here the corresponding torch turns on now let's build the storage for the instructions to do this I'll make a glass tower and a set of 16 blocks with nothing on them then you can put repeaters on these blocks wherever the ones are in the

**[5:27]** instruction for example if this is the instruction you want to store then you can just put a repeater here here here and here and as you can see when the address is decoded the instruction comes out let's build this setup for every address and or all the outputs together into one output line and with that we have a finished instruction memory let's put in some instructions and try it out

**[5:48]** I'll just put in the example program from the last episode putting in address zero gives this address one gives this and address two gives this also notice that if I go beyond the program like to address 3 it outputs all zeros which is actually still an instruction it's a noop this brings up an interesting point that I want to make sure is very clear by default when there are all zeros for

**[6:13]** every instruction in the memory it's not that it's empty it's actually completely full with all noops and when you put in a program what you're really doing is replacing some of those noops with the more interesting instructions of your program in our case we just replaced 01 and two with these more interesting instructions okay so we have an instruction memory but it's still a pain

**[6:33]** to put in the machine code if anything we kind of made it worse now instead of turning on lamps we have to fly into the instruction memory and carefully Place repeaters so I'm going to code a part two of the assembler which takes the machine code file and converts it to a Minecraft schematic to paste into the instruction memory as always it's in the description if you want to check it out

**[6:53]** I used a python package called MC schematic created by my friend sloy so now if I run it with this assembly program it'll assemble it to a machine code file and then use that to generate a schematic then I can go over here load the schematic run sl/ paste and it gets put in in diagram form this is what we have now the instruction memory on the left and the rest of the computer on the

**[7:15]** right so let's go ahead and connect them from here on out I'll refer to the leftmost bit of an instruction as bit 15 and the rightmost as bit0 so bits 0 to 3 will go into the right address bits 4 to 7 into read 2 8 to 11 into read 1 and 12 to 15 go into the control ROM this is just what we've been doing manually this entire time by the way to make the diagrams a little bit cleaner I'm not

**[7:40]** going to include the control ROM from here on out but it is still there and the op code always goes into it in Minecraft Let's make these same connections here I put 0 to 3 into write 4 to 7 into read 2 8 to 11 into read 1 and 12 to 15 into the control ROM I should also mention that at this point the re build will start to look a little bit different than the diagram for

**[8:01]** example in Minecraft the input to the instruction memory is on the right but on the diagram it's on the left and if you make your own computer you'll probably find yourself doing this too you'll diagram it one way but then find out it's easier to build in some other orientation just keep in mind that the Minecraft computer and the diagram are equivalent throughout this series

**[8:20]** they'll always have the exact same inputs outputs and connections so now that we're matching the diagram let's run a program I'll start by assembling this new program and pasting it in it does two ads a noop and a subtraction and I'll just put these numbers in the register file to start off first I'll set the instruction address to zero so that the first instruction comes out and

**[8:40]** I'll press clock to execute it then I'll make the address one and press clock again make the address two press clock and make the address three and press clock and just like that the program was run the first four registers went from 1 0 to 3123 if you execute the program by hand you'll see that that's exactly right okay now we can run programs way more easily instead of flipping a bunch of

**[9:05]** levers every time we can just paste in the program once and press clock for every address but there's still a pretty big problem we can't put new values into the register file without doing it manually so let's introduce a new instruction op code 8 will be called load immediate with the pneumonic ldi load immediate has two operands four bits for register a and eight bits for

**[9:28]** an immediate value which is just a number when it's executed it will put the immediate into register a for example ldi R14 assembles to this and when it's executed it will put four into register one to do this in Hardware we need to plug the bottom 8 Bits bits 0 through 7 into the data input of the register file because that's where the immediate is on the instruction but the ALU output is

**[9:54]** already going into that so let's introduce a multiplexer or a m which will allow us to choose which input we want to allow through I showed multiplexers in episode 6 of lrr when the MX control bit is zero it will choose the bottom input which is the output from the ALU that's what we've been putting in so far but when the control bit is one it will choose the new top input which is the bottom eight

**[10:19]** bits of the instruction since we have a new control bit let's make a new column for it on the spreadsheet let's also do some color coding to make this spreadsheet easier to look at there we go much better better also notice that load immediate puts the value into register a but on our diagram register C is the right address not a so let's add another MX to let us choose which

**[10:41]** register should be the destination when the MX is zero the destination is register C which has been the norm so far but when it's one it switches the destination to register a I'll add this new control bit to the spreadsheet as well and now we can finally fill in these control bits every instruction except for load immediate will put in zeros on these new mxes well except for

**[11:04]** noop which is technically an X because it doesn't matter load immediate will put in ones on these new mxes load immediate will also enable the register file and it doesn't matter what the ALU does it's not going to end up using it so on the diagram let's execute a program with a load immediate nice and slowly and in detail this program has two instructions and all it's going to

**[11:27]** do is load a register one with a four and then add 4+ 4 into register 2 I'll start by putting in instruction address zero for the first instruction as this instruction comes out of the instruction memory these are the bits we get and remember even though it's not on the diagram the op code 10 goes into the control ROM it's a load immediate so it puts a one into these two mxes enables

**[11:52]** the register file and puts in whatever for the Alou that doesn't matter since these two mxes both receive a one they both choose the top input this MX chose one for the destination and this MX chose four for the data so when we press clock the register file puts a four into register one and we successfully performed ldi R14 now let's go to the second instruction by putting in instruction

**[12:19]** address one as this instruction comes out these are the bits we get and again not seen on the diagram the op code for add goes into the control ROM which puts in zeros for the mxes one for enable and zeros on the Alou to make it add since these two mxes both receive a zero they both choose the bottom input two for the destination and eight for the data because that's what's coming out of the

**[12:43]** ALU and when we press clock the register file puts in8 into register 2 we successfully performed add R1 r1r2 and that concludes the program all right let's catch up to the diagram and build these two new mxes in Minecraft here's the for the data input I just made a tower of comparators on each input if the control bit is zero it only allows this Tower and if it's one it

**[13:07]** only allows this Tower and then here's the MX for the destination register it's the exact same thing two comparator towers with one of them canceled at all times also I hooked up the mxes to the control ROM and updated it to match the spreadsheet and now we can run any program with these eight instructions on the real Minecraft computer to keep it simple let's just run the two-line

**[13:28]** program from earlier as always I'll start by assembling it and pasting it in then I'll set the address to zero and press clock set the address to one and press clock and register two gets an eight perfect it's worth mentioning that keeping all the instructions in their own memory bank like this is not the only way to make a computer it's a design choice I made to make things

**[13:48]** easier in Minecraft and this Choice classifies our computer as a Harvard architecture where instructions are separate from regular data but there are many other architectures used in computers and in general there is so much more to computer science than just this series so if you want to learn about all things computer science I recommend brilliant who sponsored this

**[14:07]** video brilliant is where people learn all the nerdy topics like computer science math and Engineering their lessons are unique in the way that they teach they always involve Hands-On activities which builds intuition from the ground up so you won't just feel like you answered questions correctly you'll feel like you actually did something and became a better thinker on

**[14:24]** top of that the lessons are available 24/7 so it's really easy to fit into your schedule even with just minutes a day brilliant can become an awesome learning habit they also have a mobile app that lets you do any lesson from your phone so you can level up wherever you go when it comes to CS one of my favorite courses is the thinking and code course it really gets you to

**[14:42]** visualize programming in a way that I haven't seen other platforms do to try everything brilliant has to offer for free for a full 30 days visit brilliant.org slmap batwings or scan the QR code on screen or you can click the link in the description you'll also get 20% off an annual premium subscription
