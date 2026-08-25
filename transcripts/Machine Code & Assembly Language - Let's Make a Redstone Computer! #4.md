# Machine Code & Assembly Language - Let's Make a Redstone Computer! #4

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=_OXBSX0fPEM
- **Duration:** 14:00
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer in the last episode we made a register file today is a big day we're going to transition from just components to something that you could actually call a computer let's recap what we've done in this series so far I started off by saying it would be nice to compute things and I built an ALU it takes in two 8bit numbers in an

**[0:18]** operation and outputs an 8bit result then I talked about how memory is nice too and I built a register file it has two read addresses a write address a data input an enable signal a clock signal sign and two outputs if you don't remember how any of these signals work I recommend rewatching the end of the last episode on their own though both of these components are limited the ALU can

**[0:39]** only do single operations like 1 plus 2 or 3x or 4 it can't evaluate a bigger expression like this and the register file can store things but that's it it can't do any computation so let's combine them I'll plug the two outputs of the register file into the two inputs of the ALU and I'll plug the output of the ALU back into the register file so now when you read two registers the ALU

**[1:01]** will immediately perform an operation on them and the result is ready to be written back to any register for example let's say I want to add register one with register 2 and put the result into register 3 I'll just manually put a seven and eight into these registers to start off to do this I'll start by enabling the register file and reading registers 1 and two this makes it output

**[1:21]** 7 and 8 which immediately go into the Al by default the ALU is already adding them together because that's what happens when the control bits are are zero so 7 + 8 or 15 is coming out of here and it's going back into the register file all I have to do now is put in three for the WR address press clock and just like that register 3 gets a 15 let's look at this circuit in

**[1:44]** diagram form to be even more clear remember all the arrows going into this are the inputs there are three regular inputs read address 1 read address 2 and WR address which are each four Bits And there are two of these blue control inputs the enable for the register file which is one bit and the operation for the Alou which is 6 bits remember using six different control signals we can

**[2:07]** make this ALU do lots of different operations so here's what I just did in Redstone I put in a Seven and an eight manually I enabled the register file put in a one and a two to read put in three as a destination and pressed clock to execute it by the way the addresses put in don't have to be different from each other for example you can do something weird like subtract register one from

**[2:29]** register one and put the result back into register one just input one and one to read enable the register file put in the control bits for subtract put in one as a destination and press clock 7 - 7 is 0 so register 1 received a zero also notice that you don't have to put in the inputs one by one you can put them all in at the same time for example to execute this you can put in the 7 8 9

**[2:54]** enable and the bits for xor all at once as long as you wait long enough for the result to come back around before pressing clock the instruction gets executed all right now that our computer is capable of some pretty cool things let's start thinking about how to program it if you remember from episode one our eventual goal is for the computer to execute an instruction where

**[3:13]** an instruction is just some binary string then we'll be able to write a program by creating a list of instructions so what should our instructions actually look like this is the part of computer architecture where there is so much Freedom there are unlimited ways to design instructions so what I'm going to do is I'm just going to use a system that I was taught in school cuz it served me well and it

**[3:32]** seems to be a pretty common way to do it first things first every instruction will be the exact same length 16 bits this just makes things simpler and more consistent now notice that there are two kinds of inputs on our computer the control inputs on the bottom and the regular inputs the control inputs are called that because they control what the components are fundamentally doing

**[3:52]** for the register file the enable signal controls whether it updates or not and for the Alou these six bits control what operation it's doing so I'm going to call the first four bits of the instruction the operation code or op code and this will determine which control bits are on to do this I'm going to introduce a new component called a control ROM the control ROM takes in the

**[4:14]** op code AS input and turns on whatever control bits are on for that op code for example maybe for op code 0101 you want the computer to enable the register file and subtract on the ALU the control ROM is completely customizable furthermore you can think of the op code as the type of the instruction since our op code is four bits we can have a maximum of 16 types of instructions each with their

**[4:37]** own unique set of control bits to turn on then the remaining 12 bits will be for the operands which you can think of as the arguments of the instruction for now let's just make the operands directly line up with the remaining inputs on our computer the first four operand bits will line up with read one the next four with read 2 and the last four with write in reality the operands

**[4:58]** are going to be different depending ending on the op code but let's not worry about that right now so for example let's say I want to execute this instruction the op code 0011 or three will be plugged into the control ROM and the control bits for three will turn on whatever that ends up being the next four bits 7even will be plugged into read 1 then nine will be plugged into

**[5:18]** read 2 and five into right and finally I'll send a clock pulse which executes the instruction okay our instruction set is going to be a lot to keep track of so let's make a spreadsheet this 16bit section will be for describing the format of the instructions black is zero and white is one so the first row will describe the format for op code 000000 all the way down to the last row for op

**[5:41]** code 1111 right now the operands are the same for every op code but that'll change in the future and then these columns are to keep track of which control bits each op code will activate I also have a few extra columns off to the sides to help with note taking the pneumonic which in our case is a three-letter name for the instruction the description which is just for notes

**[6:00]** in case the pneumonic is not obvious enough and the pseudo code where I'll describe exactly what the instruction does in code form don't worry if these columns don't make sense yet as I start to fill this out hopefully it'll be more clear also if you ever want to look at this spreadsheet yourself I put it in the description now if I had planned out this series more carefully I would start

**[6:17]** with OP Code Zero but instead I'm going to start with OP code 2 and save zero and one for later arguably the simplest thing our computer can do is add so let's make op code 2 an add instruction with the pneumonic a d d in terms of control bits the register file should be enabled and the ALU should be set up to add so the control ROM needs a one here and Zer is here and for the pseudo code

**[6:40]** it's going to add a with b and put it into C so I'll just write that down let's go ahead and execute an add instruction on the diagram to see how it looks specifically let's execute this add instruction the op code 2 goes in here making the control ROM spit out a one followed by all zeros the operands go into their corresponding spots and when I press clock it performs the

**[7:01]** instruction it added register 1 with register 2 and wrote it to register 3 which is exactly what the pseudo code said it would do let's keep going with this our computer can also do subtraction so let's make a subtraction instruction with the pneumonic Su just like add it has to enable the register file but this time it also has to turn on invert B and carry in on the diagram

**[7:22]** let's execute a subtraction instruction the op code 3 goes in here making it spit out a one for enable invert B and carry in the operands go into their correct spots and when I press clock it performs the instruction in this case it did register one minus register 2 and put it into register 3 following this same pattern I could make six more instructions for these six kinds of

**[7:43]** bitwise logic but that's kind of a lot so instead I'm just going to make one for nor and an exor don't worry the computer will still be able to do all kinds of bitwise logic it just might take more than one instruction to do it more on that later in the series to execute any of these it looks extremely similar to add or subtract op code goes in here operands go in here and press

**[8:04]** clock finally I'll make a right shift instruction right shift is special because it's only applied to a Not A and B so I'm going to have to remove the B operand specifically in the right shift instruction these four bits will be all zeros when it's executed it'll right shift a and put it into C on the diagram here's what a right shift looks like all right now that we've got six finished

**[8:26]** instructions we can write a real program for example Le let's write a program that executes this pseudo code starting on the first line the op code for add is two and in this case the operands are one for a one for B and two for C then the op code for exor is six and the operands are 1 2 and three the op code for right shift is seven and the operands are two for a and two for C the

**[8:52]** remaining four bits are forced to be zero and there we go that's the program if you executed these three instructions on the computer computer it would execute this pseudo code this notation where every instruction is a binary string is called machine code it's called that because in a way it's the code for the machine it's literally the exact ones and zeros that the computer

**[9:13]** receives but the problem is for humans machine code is really hard to read for this small program it's not too bad but imagine trying to understand what this program does so what I'm going to do is make an alternate notation that's a bit easier to program in called an Assembly Language I'm going to refer to op code as their three-letter pneumonic instead and I'm going to refer to register

**[9:33]** operand as R followed by that number now in this new Assembly Language we can describe machine code in a more human way it's definitely not amazing but it's much better than ones and zeros in order to actually execute this though it still needs to be converted to machine code machine code is still ultimately what the computer needs to run the program so I made a Python program to convert from

**[9:54]** our Assembly Language to machine code this is called an assembler as you can see if I run it with the assembly program it outputs the corresponding machine code the details of the assembler are a bit out of scope for this series but the GitHub is in the description if you want to explore it one really important thing to note here is that different assembly languages

**[10:11]** will have different syntax in our case for this specific language that I just created right now I chose to require the op code first and then the oper ends after in order notice how add R1 R2 R3 lines up exactly with its assembled instruction 2 1 2 three in general this doesn't have to be the case you can make an assembler that assembles this statement to that machine code instead

**[10:36]** the assembler would just have to swap the order before turning it into ones and zeros but for us to keep things as simple as possible the order of the words in assembly will always match the order of bits in the machine code and the Syntax for assembly instructions will always follow this exact pattern a three-letter op code followed by the operands finally back in Minecraft let's

**[10:56]** catch up on the diagram we need to make a control ROM which remember takes in the 4bit op code and outputs the corresponding control bits to do this I'll start by making a 4 to6 decoder so when you put in the op code here like three only the line for number three will be on and nothing else then I'll use torches to set the control bits according to the spreadsheet the control

**[11:16]** bits for add are enable and nothing else for subtraction it's enable carry in and invert B and yeah I won't bore you with the rest of them the point is is that these torches match the control bits in the spreadsheet if you put in the op code for xor for example the corresponding torches turn on and the correct control bits get set so now let's run this program from earlier on

**[11:37]** the real computer before we start though I'll just manually put these numbers into the registers okay now add R1 r1r2 assembles to 2112 so let's put in 2 1 1 2 execute xor R1 R2 R3 assembles to 61 23 execute and right shift R2 R2 assembles to 7202 execute and there we go we just assembled and ran a program the

**[12:09]** registers now have these numbers in them which if you execute the pseudo code is exactly right that was a lot so let's summarize in our instruction set there are now six out of 16 instructions these instructions can be described in two different ways you can describe them in our custom Assembly Language where each instruction is a three-letter op code followed by the operands or you can

**[12:30]** describe them in machine code which is the binary equivalent if you write a program in assembly then you can use the assembler I wrote to convert it to machine code and once you've done that you can execute each machine code instruction by doing the following plug the op code into the control ROM plug the operands into the correct spots and press clock in every episode from here

**[12:49]** on out we'll be adding more components to the computer and more instructions to the instruction set making it capable of more amazing things and if you want to be capable of more amazing things too then check out brilliant sponsor of this video brilliant is the best way to learn all things math data analysis programming and AI it's an online platform that took a unique and

**[13:07]** effective approach to learning every lesson is filled with Hands-On activities that lets you play with the concepts yourself so while you'll gain knowledge on specific topics you'll also become a better thinker because it's a lot more than just memorizing by using brilliant a little bit every day you can develop a pretty powerful learning habit the lessons are available 24/7 so the

**[13:24]** next time you want to scroll on your phone try a brilliant lesson instead and speaking of phones brilliant now makes it easy to learn from their mobile app so you can learn wherever you go have you ever wondered how things like chat GPT actually work if you have check out the course how LMS work you'll Peak under the hood of large language models to see how they build knowledge and

**[13:41]** generate useful predictions to try everything brilliant has to offer for free for a full 30 days visit brilliant.org slmap batwings or scan the QR code on screen or you can click the link in the description you'll also get 20% off in annual premium subscription [Music]
