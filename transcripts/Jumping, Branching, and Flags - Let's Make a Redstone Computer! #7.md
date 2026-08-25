# Jumping, Branching, and Flags - Let's Make a Redstone Computer! #7

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=tuvM7T031zI
- **Duration:** 18:45
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer last episode we made a program counter which keeps track of where we are in the program today we'll be looking at how to make better programs by using jumping and branching but first I want to add one more instruction to our instruction set it's called add immediate with nimonic ADI and op code 9 ad immediate has the exact

**[0:19]** same oper ends as load imediate four bits for register a and eight bits for an immediate value but instead of putting the value into the register it adds the value to the register for example add immediate r13 assembles to this and when it's executed it'll add three to register 1 if register one happens to have a seven in it then after executing this it'll have 10 in Hardware

**[0:42]** we can execute ad immediate by routing the immediate bits 0 through 7 up and over the register file into the B input of the ALU but of course the B input is already taken so we have to add a multiplexer let's execute ad immediate r13 to see how it looks and let's say that register 1 has a 7in to start off as the instruction comes out these are the bits we get the seven from register

**[1:05]** 1 comes out here the immediate three gets selected on this MX the ALU adds them together to get 10 this MX selects the 10 and this MX selects register one to write it back so register 1 gets a 10 add immediate is super useful because it makes modifying registers on the Fly easier for example let's say you want to make a counting program where register one increments by one three times before

**[1:29]** add a me mediate you would have to do something like this put a one into another register like register 2 and then add that to register one three times but now you don't need another register you can just increment register one directly with ADD immediate and incrementing is such a common operation that it's a good idea to make a pseudo instruction for it let's make it so that

**[1:48]** when we type Inc R1 Inc meaning increment the assembler translates it to ad immediate R11 in machine code in general typing ink RX will get translated to add immediate RX1 now our counting program can be written nicely with just three increments and while we're at it let's also make a decrement pseudo instruction notice that if you do add immediate with 255 it makes that register count down by

**[2:12]** one remember all registers just hold an 8bit number so if you take five for example and add 255 which is all ones you'll get this which without the Overflow is four another way to think about this is that working with 8 bit numbers is the same thing as mod 256 5 + 255 is 260 mod 256 is 4 so let's make decrement RX translate to at immediate RX 255 and now we can increment or

**[2:41]** decrement any register with these nice pseudo instructions in assembly in Minecraft let's catch up to the diagram I'll take the immediate bits wrap them around the register file and put them into a MX with the B input of the ALU and then I'll just update the control ROM to support ad immediate to test it out let's run this program this program sets Reg register 1 to zero and then

**[3:01]** adds a 1 2 and three to it paste it in press clock and about a minute later there's a six in register one by the way I always do a lot more testing than this off camera I just don't include it cuz it's kind of boring if you're making your own computer I recommend giving new instructions tons and tons of test cases before continuing so at this point running a program on our computer is

**[3:22]** easier than ever just paste it into the instruction memory and start the clock if the program hits a halt it stops the clock and throughout the past few episodes we've seen our computer run basic programs like this Fibonacci program or this counting program but what if you wanted to make a program that counts up 100 times instead of three currently the only way to do that

**[3:41]** is to physically repeat the counting code 100 times which is kind of silly right a much more efficient strategy would be to just write the code once and then tell the computer how many times to execute it in almost all other programming languages you can do this using a loop in Python for example this two-line code segment will increment X 100 times so I think it would be really

**[4:02]** useful to have loops in our Assembly Language too it would make it easier to write powerful programs with less lines of code in order to be able to Loop we need the program counter to somehow jump back up after getting to the bottom of the code that way it can execute it again and again so let's introduce a new instruction called jump with OP code 10 and nemonic JMP jump takes one operand

**[4:23]** the 10-bit address when it's executed it'll put that address into the program counter for example jump four assembles to this and when it's executed it sets the program counter to four in Hardware we can create a jump by taking bits 0 through 9 and plugging them back into the PC but the current address plus one is already going into it so we'll have to make a MX so on all instructions

**[4:45]** except jump the PC will just count up but on a jump it'll receive the new address from the jump instruction let's see how jump Works in assembly as always the program starts by executing the first instruction which increments register one then it executes jump Z which puts the PC back to zero so now instead of executing address 2 it executes address Z again then it goes to

**[5:07]** the next instruction which again jumps back to zero and yeah register one counts up forever and the PC never reaches the halt as another example let's look at this program it starts by putting a zero into register one then it jumps to address three increments R1 decrements R1 and jumps to address four which decrements again then jumps again and cuses an infinite Loop so this

**[5:31]** decrements R1 forever the PC never reaches the Halt and it also never reaches this ad because it got jumped over in the beginning now obviously infinite Loops aren't great eventually we're going to need a way to only Loop a certain number of times but we'll solve that problem later in Minecraft let's put in jumps I'll plug the bottom 10 bits into a MX with the program counter

**[5:51]** and I'll make a new signal for it on the control ROM when it's a jump the PC will take the new address so that's what this torch is for otherwise the PC will will take the current address plus one so no other instruction has a torch now we can run this counting program for real I'll paste it in Speed the game up and press clock just like we expected it Loops forever you can see here that the PC

**[6:12]** just keeps going 0 1 01 and if you look at register one it's continuously incrementing this type of jumping where you specify the address directly is called direct jumping but another common approach is called relative jumping where you specify some kind of offset for example you can make jump three jump three forward instead of jumping directly to three you would just have to

**[6:34]** add three to the PC instead of setting the PC to three these two methods each have their own pros and cons hardware-wise direct jumping is simpler because there's no calculation it's just overriding the program counter with a new number whereas relative jumping is slightly more complex because it has to add a number to the PC however relative jumping has a huge Advantage when it

**[6:54]** comes to software take a look at this program for example it does some work at the start executes some jump and then stops if you're using direct jumping then even if you add one more line of work to the start all the jumps later on get messed up they're all off by one now but if you use relative jumping then editing the start won't break anything the jumps are relative so

**[7:15]** they'll continue to Jump by the same amount for our computer though we're going to actually continue to use direct jumping for everything we'll see later in this series that the editing problem isn't really as big of a problem as it seems so by adding jumps we now have complete control over the PC we can jump to a lower address to send it back a higher address to send it forward or

**[7:35]** even send it to the current address although I don't recommend that cuz it'll keep jumping to itself forever but we still have a big problem when it comes to Loops they're always infinite there's no way to for example Loop for 10 times and then stop this is because the jump instruction is unconditional it always does the same thing no matter how far back you send the program counter

**[7:55]** it'll eventually get to the same jump again and get sent back again it would be really nice if we had some kind of conditional jump one that only jumps if a certain condition is met so what kind of condition should we use this is very debatable and there's a ton of Freedom here but the most common conditions are based on the result of the ALU specifically most alus actually have

**[8:17]** extra circuitry on them called Flags a flag is just a one bit register true or false and its job is to tell you information about the result the four most common kinds of flags are zero carry negative and overflow the zero flag is true if the result is zero simple enough the carry flag is true if the carry out or the ninth bit in our case is one and these last two flags are

**[8:43]** useful when you're dealing with signed numbers I talked about sign numbers in episode 5 of lrr the negative flag is true if the sign bit or the eighth bit in our case is one and the Overflow flag is true if there was a signed overflow during the operation again these two are only useful if you're working with signed numbers and I personally feel like they're not nearly as important as

**[9:03]** zero and carry so we're actually only going to add a zero flag and a carry flag to our computer let's go through this example program and watch how the flags behave the registers will start with this and by default the flags will start as false the first instruction adds 1 + 1 and writes a two two is not zero and there was no carry so both flags are set to false the exor does one

**[9:28]** xor one and writes a zero so the zero flag is true but there was still no carry so that's set to false the next instruction adds 0 + 25 and writes 255 both Flags get set back to false and the last instruction does 1 + 255 which overflows to 256 and writes a zero so the zero flag is true and the carry flag is true too because it overflowed and created a carry during the operation now

**[9:56]** if this program had something like a noop it wouldn't really make sense to talk about the flags cuz a noop doesn't even use the ALU so let's make it so that only instructions that actually use the ALU set the flags this will be specified by a brand new column on the spreadsheet all of these yellow instructions use the Alou so let's mark them as setting the flags and add

**[10:17]** immediate does too so let's have that set flags as well the rest of the instructions will not set the flags so if you added some no Ops to the end of the program the flags would continue to be true and true it just leaves them alone but if you added another xor for example xor uses the ALU so the flags get set again in this case they get set to true and false let's build these

**[10:37]** flags in Minecraft first the zero flag this can be detected by oring all the bits together into a single torch that way if the number is zero the torch is on otherwise the torch is off let's put this circuit onto the output of the Alou and then the carry flag is just the carry out of the original adder in our case it's this lamp on top so I'll just take the carry out and wire it to be

**[10:58]** next to the zero signal then I'll plug both these signals into one bit registers if an instruction has to set the flags all it has to do is clock these repeaters for example let's say that the Alou calculates 1 + 255 when you clock these repeaters both flags are set to true this signifies that the result was zero and there was a carry as another example let's say the Alou

**[11:20]** calculates 1 xor 1 setting the flags again will make the zero flag true and the carry flag false signifying that the result was Zero but there was no carry okay now that we have Flags we can finally make a conditional jump instruction introducing Branch with OP Code 11 and neonic brh branch has two operands a two- bit condition code and a 10-bit address if the condition is true

**[11:45]** it will jump to the address otherwise it will do nothing since the condition code is two bits let's have four possible conditions zero flag true zero flag false carry flag true and carry flag false in in assembly let's signify the condition with one of these keywords for example Branch 07 will assemble to this when it's executed it will only jump to seven if the zero flag is true otherwise

**[12:11]** it'll do nothing similarly we can write Branch not 07 which assembles to this when this is executed it will only Branch to seven if the zero flag is false otherwise it'll do nothing in Hardware implementing branch is simpler than you might think notice that this MX directly controls whether or not the PC increments or receives a new address from the instruction most Instructions

**[12:34]** make it choose the increment and the jump instruction makes it choose the new address but for branch we can't just choose one or the other it depends on the condition so what we'll do is plug the condition directly into this MX for example when executing Branch 07 the zero flag will be plugged into the MX that way if it's true the PC gets a seven otherwise the PC just counts up or

**[12:58]** when executing Branch not 07 the inverse of the zero flag will go into the MX that way if it's false the PC gets a seven and otherwise it counts up all right let's get a feel for how Branch Works in a program this program is designed to loop three times and then stop it starts by putting a three into register 1 then it decrements register 1 to two and remember decrement is

**[13:21]** secretly an add immediate which sets the flags since the result was two the zero flag gets set to false then we have Branch Z 0 4 the zero flag is false so this does nothing it doesn't take the branch then it jumps back up to here decrements register one to one and the zero flag gets set to false so the branch is not taken again jump back up decrement register 1 to zero setting the

**[13:44]** zero flag to true and now the branch gets taken it's a branch to Halt so the program stops we've successfully looped three times but this isn't the only way to make a loop this program also Loops three times but it uses one less instruction thanks to a fancy trick it starts by loading a two and decrementing it this sets the flags to false and true it's easy to see why zero

**[14:06]** is false that's just because the result was not zero but why is carry true well remember decrement is secretly an ad immediate with 255 so what really happened is 2 + 255 which created a carry as it wrapped back around to one that's why the carry flag got set to true so the branch gets taken and we jump back up decrement to zero take the branch again and now notice that

**[14:29]** decrementing zero sets the carry flag to false it translates to 0 + 255 which does not overflow this means the branch is not taken and we continue out to the halt in both of these programs the result is the same we looped three times the main difference is that in the first case the branch was not taken during the loop and taken to exit the loop whereas in the second case the branch was taken

**[14:53]** during the loop and not taken to exit the loop all right let's Implement branching in Minecraft first we need to get the signals for the four conditions since we already have the flags this is really easy the first condition is just the zero flag the second is the zero flag inverted with a torch then it's the carry flag and the carry flag inverted with a torch these four signals display

**[15:14]** the four different conditions now we just have to choose the right condition based on the 2 bit condition code to do this we can build a 2 to four decoder and hook it up to select only one condition at a time as you can see if the code is 0 0 it chooses the first condition condition if the code is 01 it chooses the second condition Etc and that's basically all the hardware you

**[15:35]** need now that you have the right condition you can just plug it into the MX whenever there's a branch let's hook this up and run a looping program on the real computer if it runs correctly then we should see the program counter go through this sequence I'll paste the program in and start the clock 1 2 one 2 1 2 3 perfect another cool thing about these conditions is that they can give you

**[15:59]** information about the registers for example consider this code segment it does register 1 minus register 2 and if the result is zero it takes the branch this means that if it takes the branch you know for sure that register 1 equals register 2 if a minus B is zero a has to equal B and if the branch is not taken well you know they're not equal and we can also get information from the carry

**[16:22]** flag if you do a minus B and get a carry then that means a was greater than or equal to B I strongly recommend proving this to yourself by getting a subtractor and testing it out so in this segment if R1 is greater than or equal to R2 the branch gets taken so let's add some more condition code notations to the assembler just to make programming even easier on top of using zero not zero

**[16:43]** carry and not carry you can now also use equals not equals greater than or equal to or less than they are equivalent notations the new notation just makes sense when there's a subtraction directly before the branch and it's actually so common to do a subtraction before a branch brch then I'm going to make a simple pseudo instruction for it called compare or CMP compare RX r y

**[17:05]** subtracts x - Y and writes it to register zero to throw out the result compare R1 R2 for example assembles to subtract R1 R2 r0 so now let's say you want to see if register 5 is less than register 6 you can just do compare register 5 register 6 and Branch less than this assembles to a subtraction and a branch not carry so if Reg 5 is indeed less than register 6 there won't be a

**[17:32]** carry and the branch gets taken in the very first episode I talked about Turing completeness and I just want to mention that now that our computer has branching it's officially turning complete I don't have the knowledge to fully explain this but what I do know is that conditional branches are the magic ingredient that brings a computer to a new level and if you want to reach new levels as the

**[17:50]** computer programmer I recommend trying out brilliant the sponsor of this video as someone who enjoys learning online I can tell you that brilliant is one of the best platforms to learn computer science as well as math programming or any other engineering topic by including Hands-On activities in every lesson their platform is an extremely effective way to learn interacting with content

**[18:08]** makes it stick to your brain way better than watching a video and it's not like the lessons are at strict times they're available 24/7 so you can fit them into your schedule however you want lately I've been filling some of my free time with the intro to probability course cuz that's something I don't usually learn about this course shows you how to parse and visualize massive data sets and make

**[18:24]** them easier to interpret as well to try everything brilliant has to offer for free for full 30 days visit brilliant.org slmap batwings or scan the QR code on screen or you can click the link in the description you'll also get 20% off in annual premium subscription [Music]
