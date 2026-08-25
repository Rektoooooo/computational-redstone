# Redstone Calculator Tutorial Part 6 - Division

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=rBJOGLLC0XA
- **Duration:** 49:29
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** all right this is part six we're going to be talking about division so just like multiplication i'm going to show you it on paper then i'm going to show you the schematic for it and then we're going to build a machine so first let's do it on paper here so we have a setup with long division we have a 5 going into a 25 so this is 25 divided by 5. the first thing we look at when we do this

**[0:20]** is can five go into this first digit here which is just a one and the answer is no so we put a zero then we move this line over and we look at the first two digits can five go into three the answer is still no so we put another zero then we move it over again we say can five go into six the answer is yes so we put a one and then we have to

**[0:52]** subtract the five from the six so six minus five gives us a one now we have to bring this number down to line it up with the rest of them and put it here and now we can look at

**[1:22]** the number again does 5 go into 2 the answer is no so we put a 0. now we bring another number down and does five go into five the answer is yes it goes in once we subtract it again

**[1:57]** and we get a remainder of zero so now we have to look at how to put this algorithm into an actual schematic for some reason this is like way simpler to show in a schematic than multiplication so i usually like explaining this part to people because if you think about it as we're doing division we're really just shifting this 25 over and we're looking at one digit

**[2:20]** at a time first we're just looking at the first one right and comparing five to it then we're looking at the next one the one one and comparing five to it then looking at the one one zero so this 25 is just getting shifted in one at a time from the left and every time it gets shifted in we're doing the exact same thing we're just asking can i subtract 5 from it if not put a 0

**[2:43]** and don't do anything if i can put a 1 do the subtraction and then continue to and just continue as normal so gradually those zeros and ones that we get from either subtracting or not subtracting give us our answer and so this is the schematic for it right here it's doing the red divided by the blue and so the red is going to get shifted in from the left so that we look at the 1 and then the 1

**[3:10]** 1 etc this orange is a conditional subtractor it will only subtract if it gets a positive answer or an answer that's like zero or above and if it can do the subtraction well it'll output a one and this sign bit if you remember from subtraction if we got a positive answer the sign bit is already a one if it's positive so that works perfectly so let's just try this out so let's do 25 divided by five

**[3:42]** so we're first looking at one minus five and it can't do it so the first bit of our answer is a zero and i'm going to use green wool to mark that this bit is finished now we're going to shift it over and now this is looking at three minus five three minus five you still can't do so we have another zero in our output so so far our answer is zero zero and it's looking good so far because

**[4:14]** when we did it over here the first part of our answer was also zero zero so let's shift this over again now we're doing six minus five now i can actually subtract six minus five is a one and the sign bit is also going to be a one because it's a positive answer i'm just going to put it over here because that's how our answer has been displayed so far and it's also going to replace

**[4:43]** the red with whatever the answer was so it's going to put this one down here because remember after doing the subtraction it uses this new one as its new reference to compare the five with so now we're gonna shift it over again now it's doing two minus five i can't do that so put another zero shift one more time and we get five minus five which is a zero which we're going to go call positive

**[5:14]** because it could do the subtraction and that means our last output is a one and then of course it puts the result of the subtraction back into the red and our remainder in the red is a zero and our output over here zero zero one zero one this is a five all right let's do another example and this time with a remainder so i can show you how that works so the red this time is going to be 27

**[5:39]** the blue this time is a six so we're doing 27 divided by six this should give us an answer of four remainder three so we start with the one minus six i can't do that so the first answer is a zero shift everything over now we're doing three minus six i still can't do that second bit of the answer is also a zero shift everything over and now we're doing six minus six

**[6:08]** which i can do so we put a one here and the result of the subtraction is a zero which gets replaced with this in the red now we shift over again one minus six i can't do again we put a zero shift three minus six i can't do so put a zero so our final answer is four one zero zero and the remainder which is going to be

**[6:40]** in this red part is a three so you might be a little confused because i'm showing you how to do division with remainders and yet this calculator that we're building gives an answer with a decimal point and two points of precision so how does it do that well it's not actually doing decimal points or fractions or any of that i'm kind of cheating and the way i'm doing that is i'm multiplying the top

**[7:04]** number behind the scenes by 100 and then i'm just displaying whatever the answer is and then that decimal point right there is fake it just comes up no matter what the answer is because it'll always work out to give the right answer so for example what this is doing right now is instead of 2 divided by 3 it's doing 200 divided by 3 which is like 66 you know remained or something and so 66

**[7:33]** is being sent to the display and it pops up there and then the decimal point is just turned on whenever division is turned on so before with addition subtraction multiplication the highest numbers they had to deal with was 255 because that's the max for eight bits since division is using this trick where we multiply the top number by 100 we're going to have to deal with numbers as big as

**[7:55]** 255 times 100 25 500. so we're going to make a 16-bit divider instead of an 8-bit divider to make our divider we're first going to start with building the conditional subtractor so we'll start with a normal 8-bit cca and then we'll turn it into a subtractor by turning on the carry in like this and inverting all of our b inputs i'm just going to put a lamp here

**[8:22]** and a lever so we can start inputting b if we want to take this stack at 7 up and now since we need this entire thing to be 16 bits we need to copy this whole thing and paste it above itself so take the first position take the second position from here and i'm going to pick the reference point being right next to the first layer here

**[8:52]** now the first layer of the next stack up has to be one two three four and then five has to be on the fifth one so four blocks in between them and so we can go right here slash paste dash a now we have our second set of eight bits but in order to combine them and make them the same adder we need to put the carry out of this guy into the carry in of this guy and in order to do that

**[9:21]** i'm going to make this a upwards torch i'm going to put the carryout right here make it power a block which depowers a torch into a small little redstone line and then put a slab here and you can actually move this line over to here and now we have the carry out powering the carry in so this is one giant subtractor now if you want to you

**[9:51]** can put um your a input here and try out some subtraction so let's do that right now if we do five minus three we get a two and right now as long as our answer goes through and it's positive we should always be getting a carry out right here because this carryout is telling us that we could subtract and we're getting a positive answer now

**[10:22]** of course this subtractor is not set up to work properly with negative numbers but the thing is we don't want it to work properly with negative numbers because remember when we get a negative number we don't want it to subtract we want it to just keep going keep shifting until it can subtract so in order to control for that we're going to use cancellation just like we've done

**[10:41]** a lot of times before i'm going to put a comparator here and i'm also going to put a comparator under here and one of these is always going to be canceled and we're going to put a dust here block repeater and then we can connect these two lines and make this set up for all the other 15 outputs as well now it should look something like this and now we're going to build the part

**[11:11]** that's responsible for the shifting so each input needs to be shifted up on its way back and so we're going to do a slab thing again like this block slab block slab all the way up like this and then we want to put a repeater here and then you can copy this all the way up seven up seven up

**[11:45]** and for this one it's going to be a little bit different because it has to go into this block so now we can just use normal blocks the entire way we can just go like this and then for the other ones up here we do the same thing as before where we used block slab block slab

**[12:21]** and stack it seven up this one up here doesn't matter because it is running out of room it can't get shifted into anything and then of course you need uh these repeaters as well now you need the cancellation towers for both of these sides so i'm going to start with a repeater here and stack seven up and then a slab tower

**[12:56]** actually i'll make the slap tower going this way so we have more room and then you can copy this entire part your reference point i'll pick right here and put it onto the lower half now you need repeaters into all these

**[13:32]** copy these repeaters and then take this slab tower and copy the entire thing oops let me do it from

**[14:05]** and there you go when you're done you should have four different slab towers all for cancelling these giant towers here since the carryout is going to be the thing that determines which side gets cancelled we're going to take it out from here put a redstone another block one two three one two three redstone dust and then we're gonna start a spiral that goes down

**[14:37]** all the way almost to the bottom of these guys but it's going to stop right here and you're going to put redstone dust on all of these now to continue this line you want to put a slab here with a repeater into a block which extends it down to here

**[15:07]** make a little u-shape and then you want a repeater coming off of this block and then extend this by one and put a torch on this block so now we have the carryout controlling for canceling the top half of both of our lines now let's continue the spiral for the bottom

**[15:38]** half and put redstone dust so one more block here make it go down like this i'm going to put a repeater here another dust and a torch and then i'm going to modify the bottoms of these a little bit

**[16:11]** i'm going to make it into more of a spiral so take it like this and then this can be a block and same exact thing over here we're

**[16:43]** just going to modify it a little bit and that should be good now let's double check that it's working when the carryout is on it's canceling this right side

**[17:13]** so all of these 16 repeaters are on and they are and then when the carryout is off all of these repeaters should be on cool now we need a way to save all these answers every time so you can do that on the top half with just a normal set of repeaters and a slab tower

**[17:44]** whoops but then for the bottom half i'm gonna do something a little weird i'm gonna put two repeaters and you'll see why it's basically because i want um the entire unlock to be synchronized so then i'm going to start from here and build up this laptop we don't need this hold up a slap tower

**[18:17]** stack five up and then you put a repeater into here bring this out and yeah bring it out like this then you're gonna need

**[18:48]** this to come out over here and now you just want your locking device thingy so to build that you go like this you go like this one tick two ticks a torch here and another torch here so this will unlock them really quickly to save our answer

**[19:18]** and you'll notice that now they all take two ticks to be unlocked because starting from here all these bottom ones take two ticks and all the top ones take two ticks because it takes this extra and the one so when we press this button all of our answers should be unlocked really quick so this should be a working conditional subtractor and now we can test it so i'm going to pull out this first bit

**[19:44]** so that we can actually input stuff into it and so if we're sending in a one and we're doing one minus five well the machine can't do one minus five so just give me a one back and let's save this now you can see since this repeater is lit up the machine is doing two minus five which again it can't do

**[20:15]** so just give me the two back now the next time it gets sent in it's a 4 and it's doing 4 minus 5 which it can't do again so just give me the 4 and then finally it's going to do 8 minus 5 which it finally can do and it'll give me a three and so we can keep going with this now the three comes along and it's gonna be a six minus a five which again it can do so we should get a

**[20:47]** one out here and then we're back to where we started one comes around into the two into the four until it gets big enough to subtract five from so now all we need is a way to gradually shift in our a number starting from the bottom and to do that i'm gonna use a giant like extra tower thing just like i used for the multiplier start this tower go out by one block from this lever

**[21:09]** and then go one two three four five six and then the next two blocks are gonna have repeaters on them this one's on four ticks and this one's on three ticks then you want a slab here block here slab here and then continue this down four ticks three ticks block here and then a block here and then put redstone like this redstone like this and you're going to

**[21:40]** stack this entire side 15 down and then you're also going to stack this entire side 15 down now you want this to be redstone this to be a block and then this to be a repeater and then you're going to go one down and do the opposite so these are going to be alternating you're going to do repeater here and these are also going to be alternating so you're going to do a dust here

**[22:06]** and then copy this block down grab a sticky piston sticky piston is going to go right here with a lamp and a lever and same thing right here sticky piston lamp lever and now you can copy this whole part and stack seven down now you want a repeater on this block and stack the whole thing

**[22:37]** 15 down then you need to start a spiral from here so i'm going to bring this down and then i'm going to stack it uh four down and then over here on this block uh you can get rid of those for now place

**[23:08]** another block here and then a dust here then you want to bring this out and put a repeater under it into a block and do a redstone and then this redstone is going to go down like this and then it's going to start another spiral all the way down here oops

**[23:43]** until it meets up with this redstone here and just make sure that every repeater and every dust is connected to the tower and i just noticed this guy isn't connected so you can connect it just like this now we have to delay some of the repeaters so that this whole thing is synchronized so starting from this repeater that we were just messing with with the l around it

**[24:10]** we're gonna make this two ticks and then we're gonna make every other repeater below it also two ticks now for the other spiral tower you can start by putting blocks on all of these and stack 15 down then this spiral tower is going to go down like this and you can stack this entire tower by selecting here and here and i'm going to stack it

**[24:43]** six down now for any of these repeaters that don't go through a block and power redstone like this one you'll have to put another redstone on top so that it can power it from here and so you have to alternate with this in order for all the repeaters to reach the i'm also going to put an extra one on here now you can connect these by putting two blocks like this and a slab and then starting from the

**[25:08]** top of the tower one two three four five six seven eighth repeater right here you're gonna go to this block and just put a repeater set up so that it can continue the spiral like that now we need this eighth repeater and below to all be two ticks to adjust for the timings again now take a repeater out from the first tower go down by four

**[25:40]** and just line it up with this guy but we need a delay here we need a delay of 10 ticks so i'm gonna do four four and two now we need the end of this spiral tower to do something we need it to be unlocking these repeaters every single time that's why there's repeaters connecting to this spiral at every point but these ones depend on what we're coding for

**[26:11]** so this goes down here like this down by one down again and down again bring it across and it just needs to be input into this guy right here so bring this all the way down connect these two with redstone and then you need a delay of two ticks now that our tower's all finished we

**[26:42]** also need a way to save the answer because right now our answer is just flashing through on this carryout so to do that i'm gonna go one two three like this and then i'm gonna start going down with the spiral so i'm gonna make four blocks of it here and then i'm just gonna stack it so take it like this and one here one here stack

**[27:13]** six down uh to continue the signal strength here just build a slab with a repeater and then a block and then redstone like this then when it runs out again down here you can do the exact same thing put another slab here and a repeater into a block and this time we're going to bring it down go out one two three so this is four blocks

**[27:43]** and then another two like this a lamp and then the whole thing with a wire so now we have to start a tower that shifts up because this carryout is always going to be brought to the bottom here and then it's going to be shifted up to give us our answer in a nice vertical form like the rest of them do so we're going to put a slab here block slab another block and then a repeater and then this is

**[28:07]** going to repeat so you're going to end up having another slab here so we can stack this whole thing up 14 more times because we already have two lamps and we want a total of 16 so take this whole thing stack oops stack 15 up take this part stack 15 up and then

**[28:38]** take uh this whole part and stack 15 up so 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16. so this is our this is our final output right here so we don't need to do anything past that point now for the actual locking mechanism we're gonna start with two repeaters on the first nine so stack eight up and then a repeater

**[29:09]** and a block on the other six stack five up so it should look like this now from the bottom i'm gonna go up like this and then our first repeater is right here for that uh for that special circuit again the one that um depowers it for one tick so let's build that real quick we have a one tick two ticks

**[29:41]** i need a torch torch here torch here and then you can continue this up with a slab tower so take this part stack six up and then right here we need another repeater into a block like this

**[30:12]** and then we're going to continue to have a slab tower all the way up until it powers all the repeaters so now if you go down here and press a button the whole idea is that all these repeaters should be unlocked synchronously now what we need to do is make the clear button so the clear button is going to open up all the registers and then it's

**[30:42]** also going to cut off the machine that and kills all the lines just like we did in the multiplier um the first step to this is making sure that we can unlock all these repeaters so put a piston here with a redstone torch and then do the exact same thing over here go to this block sticky piston and redstone torch now in order to cancel all the lines i'm actually gonna replace this slab

**[31:13]** with a redstone into uh blocks for all of these including this bottom one which means that we have to bring this guy up and then same exact thing down here just replace all these with blocks the reason i'm doing that is because now we can just easily put pistons right here expand one

**[31:46]** up stack seven up and then do the exact same thing up here now we have a way to retract all the lines and essentially kill them so that they uh run into nothing go to this third piston and put a repeater here bring this down into like a spiral thingy and just make sure it powers those

**[32:16]** pistons and we can test this while we're doing it by putting a torch here so the first three pistons are powered so far and then as usual we do a slab tower and we're going to stack this really high we're going to stack it like 15 up and whenever it runs out of signal strength we can just use a normal repeater extend it like this we don't have to worry about synchronization this time

**[32:46]** so now it's just a matter of connecting those three functions to make the clear button so the clear button is going to open up all these registers for to clear out the answer it's going to open up these registers to clear out our a input and it's also going to just pull back all these pistons to open up the machine i'll just connect these lines by first putting a torch here going

**[33:08]** out like this into a repeater into a block and then around like this bring it all the way to here you can start bringing this down and they should connect like this then just go the other way and put a repeater here bring it down like this

**[33:40]** whoops and we should be able to sneak under this machine by going like this and then just bringing it all the way up to here to connect with this line

**[34:17]** two three four five six 7 8 9 10 11 12 13 13 14 15 so just put another repeater there and that should be good now 16 bits is a lot for it to flow out and we're not going to have enough time with a normal button so i'm going to have to make a pulse extender for this guy so you're going to go one two three four

**[34:48]** and put um a bunch of repeaters on four ticks here this is just to make a massive pulse extender thing one block like this button redstone and now this should be our clear button so when we press this button the pulse gets extended it's pulling back all these pistons it's clearing out this line by retracting the piston and it's also clearing out this line

**[35:21]** by retracting the piston one thing i do want to mention is if you clear it with the b digit being zero so this entire column being a zero uh the output is all ones that's because it's continuing to subtract zero and it's saying yup yup yup i can always do that so in order to clear it properly you need to just at least put something down like a one over here that way when you hit this button the

**[35:52]** answer register gets fully cleared out the very last step is to just have a nice space for our calculate button we could just put a calculate button like right here and that would be fine it would work but i'm gonna i want to put it right next to the clear button like it was for the multiplier so to do that just put a button here uh repeater bring this all the way out uh make it into a

**[36:21]** another big slab tower and i'm going to test the signal strength while we go and that doesn't interfere

**[36:52]** good well okay and one last thing is we need to go down here to the second uh spiral tower and come down with a block

**[37:25]** go under here all the way across line up with this guy put a repeater on four ticks and then have this guy connect to depowering this torch

**[38:00]** and you will need another block of space and just a small correction make sure this bottom repeater is also getting locked by this same line here at this point we should have a working 16-bit divider with an answer right here and a remainder here so let's do a giant test with just some random numbers i'm gonna put in uh

**[38:33]** i'll put it on screen too and we'll do a smaller number over here and now i'll hit calculate now it does take a lot longer than any of the previous ones because these are 14 tick loops 14 plus 3 i'm sorry 4 plus 3 plus 4 plus 3 is 14

**[39:04]** and each of these 14 tick loops is 1.4 seconds and there's 16 total of them so yeah it takes like 24 25 seconds and this is correct we just did 60 779 divided by 725 and we got an answer of 83 1 0 1 0 zero one one remainder six hundred and four one zero zero one zero one one one zero zero so like i

**[39:35]** said before we're gonna multiply the top number by 100 but we're not going to use a multiplier for it we're gonna do something really similar to part two i think of this series where when i multiply by 10 i did a triple up shift multiply it by eight and then a single up shift to multiply it by two and then i put those together to give the multiplying by 10. we're going to do pretty much the exact

**[39:59]** same thing with 100 but instead of 8 and 2 we're going to use 64 32 and 4 because these three numbers put together equal 100 so to show you what i mean if the user types in 5 which is 101 what we want to do is we want to multiply it by 100 and so to do that we're going to first shift it up twice to multiply it by 4 which is this number then we're going to

**[40:31]** shift it up 5 times to multiply it by 32 which is this number and then we're going to shift it up six times to get this number to multiply it by the 64. and if you add these three numbers together you should get 500 because it's 5 times 100 so i'm going to start off with a 16-bit cca and copy the entire thing

**[41:09]** i'm going to copy it from right here and i'm going to go over here put a space of 3 and then paste dash a now what you want to do is put all the outputs from this guy and route them into the uh inputs on this guy should look something like this so now what i've done is i've taken three slices of eight all resembling the shifts that we want this first one is a shift up by

**[41:40]** four so it's a double shift you can see the first one is already going into the four which is two higher than it normally would all of these are going to higher than it normally would second one's going into the eight third one into the 16 and so yeah and then this middle one is a um you shift everything up by five so it's everything's being multiplied by 32 the first one is already going into the

**[42:02]** 32 second one into the 64 etc and then the last one is really similar just one higher because this one is a times 6 up shift which is multiplied by 64. so yeah first one's going into the 64 already second one into the 128. so now we just need to take our eight inputs and split it three times so that it goes into all three of these and i have a thing to do that right here

**[42:28]** and so you just connect them all with this block slab pattern so that they can stack so i'm going to copy this whole thing and i'll go right here slash copy paste and i'm going to undo because i actually want to paste it without error just so that we can keep the rest of

**[42:59]** those repeaters and if we line everything up right each level should be going into the level corresponding to each of these three so what i mean by that is this is this is bit 1 right so now bit 1 is going into the 4 the 32 and the 64. so we're essentially doing 1 times 100 and our final output should be 100 and i believe it is if we get a lamp

**[43:30]** 64 plus 32 plus four yep that's a hundred so now i'm just going to stack this whole thing um seven up for the rest of the eight inputs and now we can multiply whatever eight bit number we want by 100 just by using these adders so let's put a little bit more lamps here let's do the um five times 100 like we did in the example so five times 100

**[44:01]** let's grab a lever and this is 500. one one one one one zero one zero zero so now we have to take our multiply by one hundred and eighter and plug it into the input a of our divider so i lined up all 16 outputs of the multiplied by 100 thing i just took the top eight and shoved them down a little bit and now this directly lines up with the 16 over here so now i'm going to be

**[44:32]** extremely careful and copy this entire thing rotate it by 90 and put it onto here copy and paste dash a so there we go this giant thing which is literally bigger than our entire divider is just responsible for multiplying our a number by 100 before it goes into the machine that's kind of crazy now the other thing you can do is

**[45:02]** bring the b around so that it lines up right next to a so i'm going to take this move it around to here let me first expand this and stack this down so a comes out to here and then b i'm gonna line up all of uh all of b right here to line up with these first eight lamps these top half

**[45:35]** the top half of b is not going to be used because we're not doing anything to the second number it's just still a boring 8-bit number that they put in on the display but if you want to destroy these lamps make sure that you just replace them with a block instead because you don't want to get rid of these torches these torches are important the top half of b still needs to be

**[45:55]** inverted in order for this whole thing to be a subtractor all right so i took b and brought it all the way out here so that it lines up with a and now we have our two 8-bit inputs and just to remind myself that you don't want to mess with these honestly you can just grab like a redstone block and instead of lamps with torches here just put a bunch of redstone blocks along these

**[46:21]** so this giant weird looking thing should be our working divider and let's try it out so we're going to do 2 divided by 3 run all the way over here and hit the calculate button and while it's going i'll get my sign out again so 2 divided by 3 what this thing will do is it's going to do 200 divided by 3 and it's going to give us a 66 remainder

**[46:52]** 2 and yeah on the display it will show up as 0.66 and we won't care about the remainder at that point so let's see if that happens looks like it's still going and done so our answer is 66 this is 64 and a 2 66 remainder 2. so back at the calculator we're going to be doing the same thing that we always did we're going to bring a line out with a slab like this and we're going to bring the b line

**[47:24]** through a this time you don't actually have to go through because uh well this is the last operation so you can just bring this guy down with a slab as well and put some repeaters boom seven down

**[47:54]** seven down and seven down now we're ready to paste in the divider so copy it rotate it do whatever you need to do get to your repeaters paste dash a boom yeah this guy's a lot bigger than the other ones all right let's test addition subtraction multiplication and division all at the same time on the top i'm going to type in 109

**[48:25]** on the bottom i'll just do uh 236 all right now i'll fly around to each one i'll put on screen what we got and whether it was correct or not so over here this is our answer for addition this line and then this is our answer for subtraction i know i'm at least somewhat right because we got a 0 on the top which means it's a negative answer

**[48:57]** and for our calculate i'm sorry for our multiplication and division we have to hit the calculate button on both of them so let's hit calculate for multiplication and calculate for division and multiplication is already done and division is still chugging done

**[49:28]** thanks for watching
