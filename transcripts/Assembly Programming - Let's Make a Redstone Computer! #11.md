# Assembly Programming - Let's Make a Redstone Computer! #11

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=pCqqpbA9uvs
- **Duration:** 12:56
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to the final episode of let's make a redstone computer in the last episode we completely finished all the hardware so today is about software we're going to make some cool programs and show off what this computer can do I hope you enjoy before jumping into programming though let's go over how our Assembly Language Works in detail cuz there are

**[0:17]** some things I haven't mentioned in this series yet in general every instruction is written as an OP code followed by the operands and the Order of these arguments is the exact same between assembly and machine code now technically you can just write decimal numbers for everything 2 1 2 3 will assemble to add R1 R2 R3 but the better approach is to use symbols the symbol

**[0:39]** for op codes is a three-letter pneumonic and the symbol for registers is R followed by that number then for immediate values like the four in ldi R14 you can write them in decimal or in binary using the z b prefix or in HEX using the 0x prefix as long as the length of the immediate is correct there are also symbols for the condition codes of a branch here are all the ways to

**[1:02]** write the zero flag false condition zero flag true carry flag false and carry flag true remember these equality based ones only make sense when there's a compare or a subtraction directly before the branch and then there's also some symbols for input and output if you write a single character from this character set and wrap it in quotes it'll assemble to its character code

**[1:22]** capitalization doesn't matter because the character set only has one version of a through z and if you write the name of any address 240 to 250 5 from the name column with underscores between the words it'll assemble to that address for example ldi R1 clear screen buffer will put 246 into register 1 on top of symbols our Assembly Language also has labels definitions and comments labels

**[1:47]** always have a DOT as their first character and they can be written before the op code or On Their Own Line in the case that a label is on its own line it assembles to the next instruction Below in this program for example add them assembles to two because the next available instruction add has address two and then stop still assembles to three definitions are similar to labels

**[2:07]** but this time they have to be on their own line and they always follow this syntax Define word number for example if you say Define my Val 4 then my Val will assemble to four you can think of it as creating a new symbol and by the way definitions don't have to be at the beginning they can be anywhere in the program in this program for example there's a Define right in the middle

**[2:28]** this works fine and you can still use this new symbol anywhere in the program even above where you defined it the assembler is smart enough to figure out all the symbols first and then fill them in and then comments are just a way to make a note without affecting the actual program to write a comment just type a slash and then the rest of your message everything after that slash will be

**[2:46]** ignored now you don't have to memorize any of what I just said to make a program all the rules and specifications I just described can be found on the readme of the project Linked In the description this readme is super useful I highly recommend reading through it on top of describing the assembly it also has the final instruction set spreadsheet including IO and pseudo

**[3:05]** instructions and it shows you how to create and run your own program to create a program simply create a new text file change the extension from txt to as open it in your favorite text editor and start coding that's it then to run a program there are two options the one I recommend is to use the simulator created by Ado once you've opened the simulator you can just drag a

**[3:26]** program in and press the start button to run it you can also change the speed speed step line by line and view the memory components as it's running it's basically a simulator and a debugger in one the other option is to actually run it on the Minecraft computer I'll warn you though the instructions for this are more complicated and Minecraft is incredibly slow even if you speed up the

**[3:44]** game with tick rate chances are it just won't be enough the only real solution to run programs in Minecraft is to use a tool called MCH PRS this is a custom server that rewrote Redstone to be much faster allowing you to reach insane speeds all the information to do this is on the readme but again I recommend just using the simulator cuz it's easy all right let's finally make some programs

**[4:06]** I'll start super simple and make a Hello World program a program that just prints hello world to the display first I'll clear the character buffer in case there's anything in it from a previous program I can do this by loading the address for Clear character buffer and storing anything to it in this case I'm storing register zero which always store zero then I'll load the address for

**[4:26]** write characters load the character code for H store it load the character code for E store it again and repeat this for every character in hello world and finally I'll push the character buffer so that it shows up on the screen as you can see from the simulator running this program writes hello world to the display and of course it does in Minecraft as well now let's do something

**[4:46]** more interesting I want to make a program that has a bouncing ball specifically this program has a single Pixel on that travels diagonally and bounces off the walls when it hits them I'll start by assigning four registers to keep track of the ball register 1 and register 2 for the X position and Y position and register 3 and register 4 for the x velocity and Y velocity now

**[5:07]** since this ball can only travel diagonally these velocities will either be 1 and 1 1 and negative 1 negative 1 and 1 or 1 and 1 and for the starting values let's just make the position 25 and the velocity 1 1 then for the actual logic we need to do something like this on every frame check if the ball hit a wall by checking it coordinates and update the velocity as necessary then

**[5:33]** add the velocity to the position which moves the ball one step forward and finally draw the ball so first to make a loop I'll just make a label called Loop and then I'll put the instruction jump loop at the end that way whatever code we put here will be repeated indefinitely now to check if the ball hit the wall notice that you can treat X and Y separately starting with x if it's

**[5:55]** 0 or 31 then the ball is either in the leftmost column or the rightmost column in both cases the x velocity needs to be flipped either from 1 to 1 or-1 to 1 so I'll check if x is zero by comparing to register 0o and I'll check if it's 31 by putting 31 into register 5 and comparing to register 5 if either of these branches are taken it'll jump to here which flips the x velocity using a

**[6:20]** subtraction 0 - 1 becomes -1 and 0 -1 becomes 1 and then for y it's the same idea if the y-coordinate is 0 or 31 the Y velocity needs to be flipped so again I'll compare it to 0 and 31 and if either of the branches are taken it'll flip the Y velocity then I'll add the velocities to the positions using some add instructions and finally we just need to draw the ball this can be split

**[6:46]** up into three main steps draw the ball on the buffer push the buffer to the screen and then clear the buffer for next time by repeating these three steps it'll continuously redraw the ball on every frame and that's it running this program gives you a ball that bounces off the walls and what's kind of cool is that by changing the start position you can get different patterns starting at 1

**[7:06]** one bounces between the two corners but starting at 47 looks like this okay let's turn up the complexity even more and make a paint program this program will have a cursor that you can move around with the d-pad pressing select will toggle drawing mode which as you can see draws at the cursor and pressing start will toggle erase mode which erases at the cursor I'll start by

**[7:28]** reserving registers one and two to keep track of the cursor position register three for the draw mode toggle and register four for the erase mode toggle these toggles will be zero if the toggle is off or 255 if the toggle is on I'm also going to put in some definitions for the offsets of all the io ports and use register 15 as the base pointer these all have the word port added to

**[7:49]** their names because I didn't want to make a conflict with the regular name which as I said earlier assembles to the direct address sorry kind of confusing but anyways for the actual logic let's something like this on every frame if select is pressed toggle the draw register then if that register is toggled on draw on the screen at the cursor and if start is pressed toggle

**[8:11]** the erase register and again afterwards if it's toggled on erase on the screen at the cursor and then if the d-pad is pressed update the cursor position and finally draw the cursor just like before I'll start off by making a basic Loop then to see if select is pressed I'll load the controller input and do a bitwise and with the bit for select if you haven't seen this before a bitwise

**[8:34]** and can be used to selectively keep certain bits if you take any bit string and do a bitwise and with a second bit string then the columns with one keep the original Bits And The Columns with zero delete them so by doing a bitwise and with the bit for select I'm essentially keeping that bit and throwing out everything else therefore if it's not zero I know for sure that

**[8:55]** select is pressed so I'll make a branch zero to skip over this section that way if it's not zero it'll hit this toggle after that if the toggle is on I'll make it draw at the cursor assuming the cursor coordinates are already stored then to see if start is pressed I'll just use the same strategy load the controller info do a bitwise and and toggle it if it's being pressed and

**[9:17]** after that if the toggle is on it'll erase at the cursor next we need to update the cursor coordinates according to the d-pad to do this I'll load the controller info one more time and use another bit wire and to keep the last four bits if left is on I'll decrement register one which remember is the x coordinate if down is on I'll decrement register 2 which is the y-coordinate if

**[9:40]** right is on I'll increment register 1 and if Up is on I'll increment register 2 and that should update the cursor perfectly store it to pixel X and pixel y the last thing to do is draw the cursor this will follow the same Three Steps from earlier draw it in the buffer push the buffer and clear it from the buffer but the thing is making a cursor on a screen with just two colors is kind

**[10:03]** of hard you can make the cursor an on Pixel but this can be confusing because you can't tell it apart from any other on Pixel so I'm going to do something interesting I'm going to make the cursor by inverting these four pixels that way the cursor is always different from its surroundings and with this in mind it turns out that two of these three steps are actually the same thing now drawing

**[10:23]** the cursor and clearing the cursor can both be done with an inversion so I'm just going to make a giant sub to invert those four pixels and now I can just call it push the buffer and call it again and with that the paint program is done that concludes all the programs I'm going to go through I hope this gave you some insight on how to make your own if

**[10:53]** you want to see more just join my Discord and check out the CPU programs Channel you'll see things like calculators Tetris Flappy Bird 2048 asteroids mind sweeper and so much more and the Beautiful Thing is now that you know how the instruction set works you could theoretically reverse engineer any of these programs I know I've talked about Tetris a few times in this series

**[11:13]** and if you're wondering it's about 900 instructions long but anyways with that the computer series comes to a close if you've made it this far give yourself a gigantic pat on the back you've seen how every common part of a computer works and not just from a truth table but how the actual logic is built you've seen how to create an instruction set and how the machine code of an instruction leads

**[11:32]** to executing it in hardware and now you've seen how to use an assembly language to make powerful programs I know I've said this a thousand times but I really encourage you to go out there and make your own computer chances are it'll be fun and best of all when you get to your first computer architecture class in school you'll get to flex on everyone that you've already made one

**[11:49]** thank you again to cappo and sloy for all your help with the design of this computer thank you to Ado for creating the simulator thank you to all the miscellaneous help I've received in my Discord and thank you once again to brilliant who graciously sponsored this entire series if you guys haven't heard of brilliant by now I don't know what you're doing they're the best place to

**[12:05]** learn engineering online from Building Bridges to simulating neural networks the lessons on brilliant will have you play with Concepts Hands-On making it not only an effective way to learn but also building your critical thinking and problem solving skills learning a little bit every day can stack up fast over time so even with just a few minutes a day brilliant will help you grow real

**[12:23]** knowledge plus it's much better than spending that time mindlessly scrolling just like how I made assembly programs and ran them on the Simulator the creative coding course will show you how to make powerful pseudo code and run it live to try everything brilliant has to offer for free for a full 30 days visit brilliant.org slmap batwings or scan the QR code on screen or you can click the

**[12:40]** link in the description you'll also get 20% off an annual premium subscription
