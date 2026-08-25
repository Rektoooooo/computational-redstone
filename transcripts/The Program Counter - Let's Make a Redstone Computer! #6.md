# The Program Counter - Let's Make a Redstone Computer! #6

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=4C0-qWW9LuU
- **Duration:** 11:25
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer last episode we built an instruction memory which allows us to store a program in Redstone today we're going to build a new component to make it much easier to run these programs but first there are a few things I want to talk about regarding last episode cuz I got a lot of questions in the comments first off noop some of you guys asked

**[0:19]** why noop is even a thing because it seems like a pointless instruction well noops are useful when it comes to the timing and alignment of instructions let's say you want instruction B to happen three instructions after instruction a but you don't want anything else to happen in between them in that case you can just fill in the space in between with no Ops in general

**[0:36]** as processors get more complex having complete control over the timing of instructions becomes a lot more useful another thing you guys pointed out is that no op doesn't have to be its own instruction for example you could just do add r0 r0 r0 register Z can't be written to so this behaves exactly the same as a noop in fact you could even go a step further and make the assembler

**[0:56]** assemble the word noop to add r0 r0 r0 in machine code then you could still write it as noop in assembly even though it's not technically a real instruction this is a perfectly valid option and it would essentially make noop a pseudo instruction a pseudo instruction looks like a real instruction in assembly but it actually isn't notice how in this scenario noop looks like a real

**[1:17]** instruction but in machine code it's an ad the reason I made noop a real instruction and not a pseudo instruction is because I feel like it's cleaner and more elegant it uses another op code unnecessarily but I personally think it's worth the sacrifice and like I've said from the beginning this series is opinionated so if you make your own computer you can obviously make your own

**[1:35]** decisions the other thing you guys commented about was the assembler if you go to the GitHub repo in the description use the assembler and paste the schematic in you'll notice that the bits are completely rearranged the assembler doesn't work on the World download from last episode this is because the repo in the description is all based on the final computer which I actually already

**[1:53]** finished and made a video about throughout this series what I'm doing is building up this computer a second time so it's not going to look exactly the same and thus the assembler might not work so if you want to run a program for real you'll have to do it on the final computer just go to the repo in the description and follow the instructions on the readme I also have a section on

**[2:10]** my Discord server dedicated to the computer so you can go there if you run into any problems and when it comes to the world downloads of these episodes I recommend only looking at them as a display all right let's finally get started with today's stuff the first thing I want to do today is revisit our instruction set as we continue to add more instructions and make our computer

**[2:28]** more complicated this control section is going to get really overwhelming and it's not the main focus of what I want this series to be about so I'm just going to remove it I want it to be obvious enough from the diagram to infer how each instruction is executed so on that note let's recap how every instruction so far is executed no op looks like this the register file is not

**[2:48]** enabled so nothing gets written and the instruction does nothing add looks like this registers A and B get read the ALU adds and it gets written to register C subtract exor and nor and right shift are all very similar to ad with the only difference being the operation in the ALU and then load immediate or ldi is the new one the data going into the register file becomes the 8bit immediate

**[3:12]** and the destination becomes register a so in this example ldi r27 puts a 7 into register 2 let's also get a refresher on what our assembly programs look like without the computer here's a simple program that calculates the first five Fibonacci numbers if you didn't know the Fibonacci sequence starts with 1 1 and then the next number is the sum of the previous two so 1 + 1 is 2 1 + 2 is 3

**[3:36]** then 5 8 Etc this program starts by putting a one into register 1 and a one into register 2 then it adds R1 + R2 into R3 2 + 3 into 4 and 3 + 4 into 5 as you can see when it's over with register 5 has the fifth Fibonacci number so as our Minecraft computer stands we can execute a program by doing the following assemble it paste it in and go through each address one by one pressing clock

**[4:03]** to execute each instruction but this is tedious and it always follows the same pattern so let's make a new component to help automate this called the program counter the program counter stores a single number and its job is to keep track of where we are in the program specifically the number it stores will be the 10bit address of the instruction that is currently being executed this

**[4:23]** output wire just shows what the number is so if it's currently storing a seven then the output shows seven and then and then the input doesn't really do anything until you press clock pressing clock writes the input to the memory for example if you put in three and press clock it writes the three so the program counter is essentially a single register in fact some computers just use one of

**[4:44]** the registers in the register file as the program counter for us though it just makes more sense to keep it separate because it holds a 10-bit number whereas the register file holds 8 bit numbers now since the address goes up by one as you execute a program let's add one to the address and plug it back into the program counter that way when you press clock it counts up by one

**[5:05]** notice how if I start at zero and start pressing Clock IT updates to one then two then 3 Etc and then let's plug this whole thing into the instruction memory so now here's how running a program will work let's run this Fibonacci program for example we'll start by putting the program into the instruction memory as normal and set the program counter to zero to execute the first instruction

**[5:27]** send a clock pulse to both the progr counter and the register file we can do that by connecting them into one button and just pressing that button notice that this both executes the first instruction and counts up by one on the program counter so we're already ready to execute the next instruction you can just press this button for more times and it will automatically execute the

**[5:48]** next four instructions but even this is still more manual than it needs to be as you might have guessed the reason these red signals are called clock is because now we can hook up a clock to it there's no need to man manually press the button five times let's just reset the computer and have the clock run the program for us but this creates a new problem how does the clock know when to stop we

**[6:09]** could make it end when it hits the first no op but then we couldn't have a program like this because it would stop before the end instead let's make a new instruction called halt with OP code 1 and pneumonic HLT when the computer receives a halt it will stop the clock and therefore stop executing instructions let's put a halt at the end of the Fibonacci program

**[6:30]** reset the computer and start the clock again now it runs the program and automatically stops when it reaches the halt beautiful all right let's catch up to the diagram in Minecraft I'll start by building a program counter like I said it's basically a single register so it's actually pretty simple you can just put 10 repeater locks on top of each other all connected with a clock signal

**[6:50]** if you put in seven for the input and press clock it writes a seven or if you put in three and press clock it writes a three then let's use an Adder to add one one and loop it back into the input here I'm using a carry cancel Adder but any Adder will work just fine now when you press clock it counts up one 2 3 Etc by the way since this whole thing is essentially a counter I should mention

**[7:13]** that there are lots of different ways to make redstone counters and most designs don't even need an Adder for example in lrr Number 8 I showed you guys this tiny design for a counter it's only8 bits and not 10 bits but I feel like it's important to mention here again just check out lrr number 8 if you want to learn more about it let's go ahead and plug this whole thing into the

**[7:31]** instruction memory and reset the program counter to zero then for the clock I'm going to use this circuit right here when you press the start button it starts running and it sends out a two tick pulse every 100 Redstone ticks and pressing stop just turns it off this circuit works by making a comparator cancel itself after a long delay if you want to learn more about it then check

**[7:50]** out lrr number 7 now let's just hook this up to the clock signals on the program counter and the register file and let's make it so that when the op code for halt is detected it comes over here and stops the clock now I made the clock 100 Redstone ticks because I know for sure without even counting that 100 ticks is much longer than any instruction could take so there's no way

**[8:10]** that the clock is too fast but it's definitely not as fast as it could be if you wanted to find the fastest possible clock speed you would just need to count how long the longest instruction takes and set it to that this brings up an important point about our computer our computer is classified as single cycle because every clock cycle executes exactly one instruction this is in my

**[8:29]** opinion the simplest way to design a computer but it has the disadvantage that you are only as strong as your weakest link the time it takes to execute the longest instruction is the time it has to take to execute any instruction in order to make the clock speed consistent so even if 99% of your instructions are lightning fast if you even have one slow one the clock is slow

**[8:49]** in theory you could make a clock that changes its speed based on the instruction but this is generally frowned upon because it makes the timings unpredictable most computers both in real life and in redstone are not single cycle instead they're multicycle breaking the instructions up into many clock cycles for example you can make a computer that breaks instructions up into three separate

**[9:09]** stages maybe one to fetch the instruction another to decode it and another to perform an operation on the ALU whatever they may be if you break instructions up like this then the computer would take three clock Cycles to execute an instruction why would you want to do that well it actually allows the computer to work on multiple instructions at once notice that after

**[9:28]** the ad instruction moves from stage one to stage two the computer could also start working on a subtract instruction in stage one at the same time then as the add moves to stage three and the subtract moves to stage two they can work on an xor in stage one this is called pipelining and it's an extremely powerful tool to make computers faster as you can see by this graph executing

**[9:49]** an add subtract and exor with a three-stage pipeline takes five Cycles whereas if you did each instruction individually it would take nine Cycles 3 + 3+ 3 but again none of this even matters for our series because our computer is single cycle there's no pipelining every clock cycle executes exactly one full instruction at a time all right now that we're caught up to the diagram and I'm

**[10:12]** done with that tangent let's run this Fibonacci program for real if we built everything right then all we have to do is assemble it paste it in and start the clock about a minute later we can see that the clock got stopped by the Halt and the registers have 1 one 2 3 five in them perfect like I said earlier in the episode this series is somewhat opinionated and if

**[10:33]** you want to go into computer science like I did it's important to learn from many different sources that's why I recommend brilliant who sponsored this series and made it possible brilliant will go Way Beyond my videos and teach you about computer science math and whatever other nerdy topics you're into just like building Redstone their lessons will teach you Hands-On problem

**[10:49]** solving because they always include interactive content this means you'll be playing with the concepts yourself so you'll have more fun and you'll build critical thinking skills instead of just memorizing one of the courses that demon Ates this really well is called exploring data visually it has really great visual models on algorithms regression models and more to try

**[11:06]** everything brilliant has to offer for free for a full 30 days visit brilliant.org slmap batwings or scan the QR code on screen or you can visit the description you'll also get 20% off in annual premium subscription
