# The Call Stack - Let's Make a Redstone Computer! #8

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=XVWUCgqGwHM
- **Duration:** 12:02
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer last episode we added some instructions that made programming a lot easier jump and Branch today we're going to continue to make programming Easier by making a call stack but first I want to introduce a new assembly feature called labels labels allow you to use a word for an instruction address instead of a number in our Assembly

**[0:20]** Language they always start with a DOT and they get placed before the op code for example consider this program it starts by comparing register 1 to register 2 and if they're equal it branches to the halt skipping over the increment but if they're not equal it increments register 3 and then halts let's add a label named skip to line three now whenever you write do skip the

**[0:42]** assembler will literally replace it with a three so on this line you can just write do skip when the program gets assembled it'll get replaced with a three before becoming machine code because that's what the value of skip truly is okay but why do this why make a label and then write the name of the label in instead of just writing three well what if you wanted to add more code

**[1:03]** to the start of the program if you did that then three wouldn't be the right number for the branch anymore you would need to fix it and make it point to the halt again but if you use labels this problem doesn't exist the branch isn't pointing to a specific number anymore it's pointing to a label and the actual value of that label will change automatically thanks to the assembler

**[1:23]** next consider this Fibonacci program we've seen Fibonacci programs before but this one is cool cuz it uses a loop depending on what what you set register one to in the beginning it'll produce a different Fibonacci number in register 4 if you set register one to one register 4 will end with one or if you set register one to six register 4 will end with eight this program has three labels

**[1:44]** FIB Loop and done and thanks to these labels you can put this code anywhere in the program and it'll still work if you put it at the very beginning then FIB resolves to zero Loop resolves to four and done resolves to 10 or if you put it later in the program they'll resolve to something else but the point is it doesn't really matter what these labels resolve to in fact most of the time

**[2:05]** while you're programming you won't even know what they resolve to because you don't have to all that really matters is that when you say something like jump label it jumps to that label wherever that may be okay so hopefully it's clear by now that jumping and branching are super important for programming they allow for things like if statements and Loops but as you get into the higher

**[2:24]** levels of programming you might realize there's kind of a problem let me show you what I mean let's say want the fourth Fibonacci number easy just set register 1 to three and use the Fibonacci program then you write some more code and then later on in the same program you want another Fibonacci number let's say the sixth one so you set register one to five and write the

**[2:44]** Fibonacci code again this works but now you have duplicated code which is not a good idea for many reasons one reason is because if you find a bug you have to remember to change it in both places that might not sound that bad but what if there were 20 copies it just gets really annoying and you don't want to run the the risk of forgetting to change one another reason is because

**[3:02]** duplicating code is a waste of space why should you have to say how to calculate a Fibonacci number again if it already did it before that seems very inefficient it would be much nicer if you could just write the Fibonacci code once and reuse it or call it every time you want a Fibonacci number so let's introduce a new instruction called call with OP code 12 and nemonic Cal call is

**[3:25]** basically the same thing as jump it takes one address as an operand and when it's executed it jumps to that address so now if you want the fourth Fibonacci number you can do the following set register one to three and then do call FIB this jumps to wherever FIB is located and you'll get the fourth Fibonacci number as normal but after it finishes we still need some way to

**[3:46]** return to where the call came from so here's what we're going to do when a call is executed it's not just going to jump it's also going to save where we left off in a special register called the return register specifically it'll save the current address plus one because that's the address of the next instruction once we get back so now once the Fibonacci part is done all we have

**[4:07]** to do is jump back to what's in the return register to do this let's introduce another new instruction called return with OP code 13 emonic re return has no operands all it does is jump to whatever is in the return register let's place a return at the end of the Fibonacci part and now it'll jump back to where we left off what we've just done is created a sub sub routine a set

**[4:30]** of instructions that we can call to execute on demand and return back to where we were and the amazing thing is if you want another Fibonacci number later you can just call the sub routine again there's no need to duplicate code just like last time it'll jump to FIB run it and return let's look at another example of sub routines in this program there are two sub routines one named add

**[4:52]** one and another named add two and then there's the main part of the program at the beginning so let's go ahead and run this the first instructions sets register 1 to zero easy enough the next instruction is a call to add one so it jumps to add one and saves the current address plus one then the add immediate adds one and the return takes us back to whatever was saved which is right here

**[5:15]** then there's a call to add two so it jumps to add two once again saving the current address plus one then the add immediate adds two and the return takes us back then there's one more call to add one so once again it jumps to add one runs the add immediate and returns to Halt after the program halts register one has a four this makes sense because we just called add one then add two then

**[5:38]** add one again all right let's make call and return in Hardware first I'll make the return register over here on the left on a call the current address plus one should go into it and the nice thing is the current address plus one is available right here so it's really easy to plug in then on a return the output should go into the program counter so I'll take the output and plug it into

**[5:59]** this Muk making our first three-way multiplexer the program counter now has to choose between an increment a jump and a return and in Minecraft building this is honestly really straightforward this is how I would make a return register and it's very similar to all the other registers I've made so far it's just a bunch of repeater locks stacked on top of each other but before

**[6:18]** we put this on the real computer you might have noticed that there's a problem what if you tried to call a sub routine from within a sub routine for example what if you wanted to make a sub routine called outer which calls the sub routine add one well let's try it out there are now two sub routines add one and outer and in the main part of the program there's just a single call to

**[6:38]** Outer at the start of execution the call will jump to Outer and save where we left off then there's a call to add one which jumps to add one and saves where we left off again but hold on a second that just overwrote what we already had in the return register now there's no way to get back to the main part we screwed ourselves so what if instead of having a return register it was more of

**[6:58]** a return stack like a pile of return addresses that you could just keep throwing more onto let's try again with a stack and see what happens we start with a call to Outer which jumps to Outer and puts where we left off on the stack then we have a call to add one which jumps to add one and puts where that left off also on the stack then we have an increment and a return but where

**[7:20]** should the return go should it go to the first thing that got saved or the second one well it should probably go to the most recently placed thing on the stack because that must must have come from the most recent call now we're in business next there's another return which will look at the most recent thing again taking us back out to the halt let's do another example this time I'll

**[7:40]** make a sub routine called add three which calls add one and then add two the first call jumps to add three then it calls add one once add one finishes it returns to the top of the stack which is here then it calls add two once add two finishes it returns to the top of the stack again which is here and then there one last return which again takes us to the top of the stack which is back to

**[8:03]** the halt let's go ahead and update our computer to have a stack instead now the call instruction looks like this it jumps to the address and saves the current address plus one onto the stack which is called a push and the return instruction looks like this it puts the top of the stack into the program counter and then removes it from the stack which is called a pop one thing to

**[8:24]** note here is that while stack is much better than a single register there's still a limit a stack is not infinite for example let's say you made a sub routine that calls itself now when you call it it calls itself which calls itself which calls itself on and on forever except it's not forever eventually the stack would run out of space causing what's called a stack

**[8:44]** Overflow so for our computer let's just make the stack 16 layers deep back in Minecraft the easiest way to make a stack is with a bidirectional shift register as seen in lrr Number 8 if you imagine this as the top of the stack then you can push to the stack by putting data here and shifting right push one push two push three notice how three is the most recent push so it's at

**[9:06]** the top of the stack then to pop the stack shift left pop three pop two pop one now there are many different designs for a bidirectional shift register the one I just showed is kind of the classic design it's three blocks wide per cell and it uses two sets of repeater locks facing in opposite directions when you shift right it uses the top set of repeater locks and when you shift left

**[9:28]** it switches to the bottom set here's another design created by my friend qari this one is two blocks wide per cell and it only uses one set of locks shifting right follows this pattern and shifting left follows this pattern pretty clever but if we want to use any of these for the real call stack we're going to need to make each cell 10 bits instead of one remember instruction addresses are 10

**[9:49]** bits long so I'm just going to choose the classic design and stack it upwards to make 10 total layers and this is the finished call stack to test it out let's go ahead and write a seven and push it then I'll write a 10 and push it and I'll write a 12 and push it the top of the stack is reading a 12 that's a good sign cuz that's the last thing I pushed and then pressing pop will pop the 12

**[10:12]** showing 10 pop the 10 and now it shows 7 pop the seven and the stack is back to empty all we have to do now is hook this up to the computer following the diagram from earlier and here's what that looks like everything should be good to go now you might notice that the computer looks a little bit different from last time the pr program counter is up here now and the control ROM got shoved

**[10:32]** underneath don't worry about this it's just because I'm starting to put the computer into its final layout which looks like this it still matches the diagram perfectly so let's go ahead and run the ad three program from earlier assemble it paste it in and run while it's running you can actually see it pushing and popping from the stack which is really cool and once it's done

**[10:52]** there's a three in register one beautiful clearly sub routines are a huge help in making some really cool Redstone programs but they're not just cool in Redstone Concepts like sub routines and functions show up all the time in many highle languages so if you want to learn more about highle CS then check out brilliant the sponsor of this video brilliant is the best place to

**[11:12]** learn not just CS but all things math programming and data analysis as well it's a platform that focuses on interactive lessons to teach you in the most effective way possible so whether you're building a bridge or visualizing neural networks you'll build critical thinking skills rather than just memorizing and the lessons are available 24/7 so it's easy to fit into whatever

**[11:30]** your schedule is out of all the things brilliant offers data analysis is my weakest point so recently I tried the exploring data visually course it was really cool I got to parse through massive data sets and I got a sense for seeing real world Trends to try everything brilliant has to offer for free for a full 30 days visit brilliant.org slmap batwings or scan the

**[11:48]** QR code on screen or you can click the link in the description you'll also get 20% off in annual premium subscription
