# The Arithmetic Logic Unit - Let's Make a Redstone Computer! #2

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=ChR7wS94WoY
- **Duration:** 17:10
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer in the previous episode I gave you a very brief overview I showed you a diagram of the full computer and I said we're going to make a custom Assembly Language to write programs in today I want to start by expanding on that overview because I didn't give a lot of detail and then we're going to spend the entire rest of

**[0:17]** the episode focusing on the first component the ALU I hope you enjoy so like I said before we're going to eventually write programs in a custom language but what does that language actually look like well every program will be a list of instructions where each instruction is a small task for the computer to do you can think of our computer like a chef in a kitchen when

**[0:36]** it runs a program it's following a recipe if step one says to put flour in a bowl then that's the first thing it does after Step One is done it moves on to step two which might be turning on the oven the point is a program is just a straightforward list of instructions from top to bottom so in the hardware the first thing we need is something to physically store the program that's the

**[0:57]** job of the instruction memory memory address Z will store the first instruction address one will store the next one Etc we also need something to keep track of which instruction the computer is executing introducing the program counter the program counter stores the address of the instruction we're currently on so it'll start at zero and count up by one every time an

**[1:17]** instruction is completed then we have the ALU which is going to be the star of this video the ALU will be doing most of the computation like addition subtraction and bitwise logic but who cares about computation if you have nowhere to store the numberb introducing the data memory which is a giant memory bank that allows us to read and write data to whatever address we

**[1:36]** want then we have the register file which is like a mini version of the data memory the register file is a small collection of registers where each register holds a single number and finally we have the call stack which allows us to create functions in our program we're going to be going through each of these components in way more detail later but here's what I want you

**[1:54]** to take away from this all of these components have different jobs but they all work together with one common goal perform the instruction now that we know a little bit more about the hardware and software let's dissect a simple program consider this program with four instructions again programs are written in our custom language so what I'm about to say doesn't necessarily apply to

**[2:14]** every language you see only this one first is ldi R12 ldi stands for load immediate so this instruction is telling us to load register 1 with a two let's go ahead and do that then we have ldi R22 so this time we load register 2 with a two then we have ADD R1 R2 R3 this means add the contents of register one and register 2 together and put them into register 3 so register 3 is going

**[2:42]** to receive a four finally HLT means halt which just tells the computer to Halt or stop the program in Python you could write the program like this they're not exactly the same because in Python R1 R2 and R3 are variables not registers but hopefully this shows you in intuitively what the program is doing and over the next few episodes we're going to be building up the hardware to actually run

**[3:05]** this all right let's move on to the main topic of this video the ALU ALU stands for arithmetic logic unit and like I said in episode one The ALU will be doing most of the actual computation in our computer so what kinds of computation are the most useful I don't know about you guys but the first thing I think of is addition addition is super useful I mean it's the classic example

**[3:25]** of computation in my opinion the easiest way to do addition is with a carry cancel L as seen in lrr number four this is an 8bit CCA so you can put in any two 8bit numbers here like 6 and 4 and you'll get the 8 bit result which is 10 you can also do subtraction with an Adder as seen in lrr number five if you invert the B input and add one then it performs a minus B in this circuit right

**[3:50]** here I used torches to invert B and I turned on the carry in to add 1 6 - 4 is 2 so let's make our ALU capable of both addition and subtraction in general addition and subtraction are the main kinds of arithmetic you'll see in alus but what about logic why is that word there too well another useful set of operations is called bitwise logic bitwise logic means to look at each pair

**[4:15]** of bits individually and apply some logical operation to them so for example a bitwise and between 0 1 01 and 0011 would result in 00001 each pair of bits just follows the and function one reason bitwise operations are so useful is because they allow us to control individual bits using bit masks for example if you want to set the first bit of a number to one and leave the rest unchanged you can or

**[4:41]** it with the mask 00001 in Redstone you can do bitwise logic by just building the logic gate at every level this right here is a bitwise ore so if at least one of the lamps are one at any level then that lamp will also be one on the output this is a bitwise and and it's the same idea one1 1 and 011 gives one so these six circuits are the six main kinds of bitwise logic or

**[5:08]** and xor nor nand X nor you might have noticed that I'm missing the not operation and that's because not takes one input instead of two so we're just not going to worry about it right now putting this all together let's make an Alou that has all eight functions addition subtraction and six kinds of bitwise logic we can do this by duplicating the put to every function

**[5:31]** and then selecting one output at a time this circuit here duplicates a into all the a inputs and then does the same thing for B by passing it through the a line so if you input five and three that five and three gets put into every single function then I have comparators on every output with each one being canceled by a tower of repeaters so depending on what operation you want to do you can just

**[5:59]** 5 - 3 which is 2 the ALU still technically computed everything else but since the subtraction result was the only one that got uncancelled it was the only one that got to the output as another example if you select xor you get the xor result 110 so yeah this is a fully working ALU you can input any two 8 bit numbers and choose from eight different operations if you're making

**[6:22]** your own computer and want the absolute easiest way to make an ALU then this is what I recommend it's pretty straightforward and you can add or remove operations without too much work as you might have guessed though this is not the most optimized way to make an Alou even if you were just doing addition and subtraction you don't technically need two separate adders as

**[6:41]** seen in lrr number five you can modify an Adder to make it add or subtract when this lever is off it's just a normal adder and when it's on it inverts B and adds one using the carry in which of course makes it subtract so is it possible to make even more modifications to put in the bitwise functions as well to really get a good understanding of what modifications we need to make let's

**[7:03]** go all the way back to a single full adder as seen in lrr number four here we have a b carry in carry out and sum according to the truth table the sum is on when either one or three of the inputs are on one way to detect that is with a xor b x or C and that's exactly what this full add is doing using this lime green design for an xor gate it computes a xor b which then Wiggles up

**[7:28]** here into another xor gate with C the carry in so the final sum is a X or B X or C then for the carry out it should be on when at least two of the inputs are on one equation for this is a and b or a xor B and C in other words either both A and B are on or one of them is on and so is C this fatter implements that equation in a really clever way notice that this xor design gives you an and

**[7:54]** gate for free with a torch on the top so this first torch is actually the result of a and B and this second torch is a similar story this is the and between the results of the first xor a xor b and c these two torches get ored with a dust line which gives you this final equation the carry out and as a refresher this fatter can be duplicated to make a ripple carry Adder of any size this one

**[8:18]** right here is a 4bit ripple carry Adder so it can add any two 4-bit numbers 2 + 3 for example is 5 okay now let's start modifying this we know from earlier that if you invert B and turn on the carry in you can do subtraction so let's add those two control signals here I added the control for invert B so when I flip this lever you can see that b goes from 0011 to 1 1 0 0 and this is the carry in

**[8:46]** right here so now if you turn both of these on it computes 5 - 3 which is 2 while we're at it let's also add a control signal for invert a this doesn't do much for us right now but it's really really easy to add and it can't hurt let's also make a little chart to keep track of which control signals we have and which functions we can do the black wool is zero and the white wo is one so

**[9:08]** right now the chart is saying that if everything is zero it adds and if invert B and carry in are one it subtracts so now the question is how can we modify this even further to do bitwise logic well maybe it helps to ask a different question why is this not doing bitwise logic I think the biggest reason is because we have these carry signals propagating across the L they make one

**[9:30]** full ladder affect the others which is not what you want for a bitwise operation to combat this let's try forcing all the carens to be one I'll use four torches underneath like this all connected to a single line called flood carry when flood carry is on all the carry-ins are set to one so what happens if you turn on flood carry and nothing else you actually get bitwise xor 0101 xor

**[9:57]** 0011 is 1 1 01 remember all the sum bits are doing a X or B X or C but flood carry forces all the C's to be one and an xor with one is the same thing as an inversion and also you can do bitwise xor by Just inverting One of the inputs this works because if you invert one of the inputs of xor it inverts the output and becomes xor so now we have four functions add is nothing subtract is

**[10:26]** invert B and carry in xor is flood carry and xor is invert B and flood carry okay we've got some bitwise logic now but we still need or nor and and nand that sounds like a lot but I'd argue these four functions are actually pretty similar they can all be made with an orgate as a base and different combinations of inversions or is no inversions nor is inverting the output

**[10:53]** and is inverting the output and the inputs and nand is just inverting the inputs so if we could make another modification to somehow put in an orgate we might be able to create all four of these functions as it turns out there's a really easy way to do that if you go to the first xor and power this dust it becomes an ore instead and importantly it also disables this torch the first

**[11:16]** and gate of the carry out this is a very small detail but it's actually necessary for this modification to work disabling that torch means the carry out equation changes from this to this and that makes the carries behave a lot differently because now as long as the first Carry in is zero then the first Carry Out will also be zero which then means the next carry out will also be zero and so on

**[11:41]** and so on all the carries end up being zero so not only does this new control line change the first xor to an or it also forces all the carries to be zero let's call this new control line xor to or and now we can add all the remaining functions or nor and and nand all all have the xor toor control signal turned on and each one just uses some different inversions or uses no inversions nor

**[12:07]** uses flood carry which remember inverts the output and uses flood carry invert a and invert B and nand just uses invert a and invert B let's see some of these in action for a bitwise and we need xor to or flood carry invert a and invert B 0 1 01 and 0 011 is 00001 for a bitwise nor we need xor to or and flood carry 0 1 01 nor

**[12:40]** 0011 is 1 0 0 by the way as a cool bonus you can actually make implies as well implies is not as common but it's basically a function that says if a then B and if you add flood carry to it it becomes implies the negation of implies so now with just five control signals we've created an ALU that can do addition subtraction and eight kinds of bitwise logic you can even make a nice

**[13:06]** ROM or readon memory to automate the settings if you get tired of looking at the table these lines have the control signals baked into them so if I choose subtract for example it'll automatically turn on invert B and C in with these torches very cool now let's see if we can improve this even further by applying the same logic to an 8bit CCA as a refresher from lrr number 4 a c CCA

**[13:29]** calculates the sum in the exact same way as the last dat there's an xor gate on the front to calculate a X or B and then that comes along here and gets xored with C but unlike the last dater a CCA generates all the carries in parallel using a tower of comparators so let's start with the easiest control signal the carry in on a CCA you can make a carry in by just powering the carry

**[13:52]** Tower from the bottom that's it the next easiest control signals are inverting A and inverting B these can both be done with some in iners on the front just like on the last add this lever inverts a and this lever inverts B next let's do flood carry for this I just made a tower of repeaters that forces all the carries to be one in that final xor and finally we need the xor to ore control signal

**[14:15]** notice that on this xor design you can easily get the ore by just taking out this dust so I just took that dust and wired it to the output now when this comparator is uncancelled it overrides the output with the ore thus turning this X or into an ore and that is pretty much it you can put in any two 8bit numbers and choose from 10 different functions using the table and since

**[14:38]** these five control signals behave the same way as before you can use the exact same ROM for it too as a quick test putting in this number or this number gives us all ones beautiful okay so there's actually one more thing that this ALU is going to need a shifting function shifting bits is extremely useful one reason is because shifting a binary number left multiplies it by two

**[15:01]** while shifting it right divides it by two so let's make our ALU capable of both shifting to the left and right the cool thing is our Alou can kind of already do a shift to the left for example to shift a three to the left you can just put it on both A and B and add them because x + x is 2x this gives 6 which is the same thing as three shifted left but our ALU definitely can't shift

**[15:26]** to the right so let's add that function to do this I'll split the output into two parts one for the regular output and one for the right shifted output and then this control signal will either allow the regular output if it's zero or allow the right shifted output if it's one so now if you put in a six and turn on right shift it shifts down to a three the nice thing about doing the shift on

**[15:47]** the end like this is that technically you could combine it with another operation for example you could do 1 0 0 or 1 0 which gives you this and then right shift the result as as well but that's just a fun Sidetrack our Alou will only do one operation at a time in general Al designs can take on many different forms just like most things in computer science so if you want to get

**[16:10]** an even broader perspective then check out the sponsor of this video brilliant brilliant has tons of lessons in not just computer science but also math programming data science and AI their big thing is that every lesson is interactive leading to a much more effective learning experience whether you're solving puzzles or assembling circuits you'll build critical thinking

**[16:29]** skills on top of gaining knowledge even if you only spend 5 minutes a day learning with brilliant is a great Habit to get into it's literally the opposite of mindless scrolling later in this series we're going to use Python to help us out so if you want to get a head start then check out the programming with python course this course will introduce you to all the essential

**[16:46]** coding elements and with the drag and drop editor you'll be able to run programs on day one to try everything brilliant has to offer for free for a full 30 days visit brilliant.org map batwings or click the link in the description you'll also get 20% off in annual premium subscription [Music]
