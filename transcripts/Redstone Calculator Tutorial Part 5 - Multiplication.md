# Redstone Calculator Tutorial Part 5 - Multiplication

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=xbGEN6S0KCs
- **Duration:** 26:24
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** all right time for binary multiplication this one's really cool we're going to use a adder on a loop with some shifting and stuff it's going to be really cool this is one of my favorites uh so let's do it on on the table first like how you do it in elementary school you just take this bottom right digit and you multiply it by the first one up here and then the second one and then the third one in

**[0:20]** binary it makes it really simple because it's either going to be one times the whole number which means you're just copying the number or it's going to be zero times the whole number which means you're not adding anything at all so let's do this piece by piece so you start with the one you multiply it by this whole number and i'm literally going to copy and paste it because it saves time

**[0:42]** paste it here and this is the first part of our answer we did 1 times 1 gives the 1 1 times 1 1 etc and we copied the first answer now since we have a zero for the second one we do nothing but i'll draw it anyways just so it um so you can see what's happening we shift it over by one and we do all the multiplication which again gives us all zeros now since the third one is a one

**[1:09]** copy this number again and it gets shifted over again and then the fourth one is a one and it gets shifted over again with the exact same number and then you can just put another line here and you would add all these up so i'll just do the addition live and we'll

**[1:41]** double check that we get the right answer so one goes here just a one one plus zero is one zero plus zero plus one three ones gives us a three so a three is a one with a carry one plus one is two a two is a zero with a carry one plus one gives us

**[2:12]** another two which is again a zero with the carry one plus one gives us another two zero with a carry so let's see if we did this right so 1 0 1 1 is 11 1 1 0 1 is 13 13 times 11 is 143 this is 128 plus four ones four ones is 15. 128 plus 15

**[2:42]** is 143. so we did it so what we've shown here is that all it takes to to multiply two binary numbers is to take the first number shift it a bunch and maybe take some out as you go depending on where the zeros are in the second number because what i mean by that is if you go over here and you put a one wherever there was a number a zero wherever there wasn't a number you're gonna get this

**[3:08]** which is exactly our second number but in reverse because that's what we're using to decide whether we write it down or whether we don't write it down so i'm going to try my best to describe how this works uh this is the schematic for the actual multiplier the red is one number that we're multiplying the blue is the second number um i put a repeater and a comparator here to resemble the fact that

**[3:32]** as we shift blue to the right this lowest bit this rightmost bit is going to determine whether whether a this red is going to be cancelled or not so in other words if this lowest bit right here is a one then a is sent through no problem if it's a zero we're going to cancel a in other words it's just going to be all zeros now this output is sent back into the front of the machine and of

**[4:02]** course this orange is an adder and it's going to add this first row whoops with the second row it can't see this lowest bit here and this lowest bit is going to gradually give us our answer that's why i put a record here part of part of the step on each loop is to record the lowest bit and that will gradually give us our answer so let's try to do three times three so we have three right here

**[4:32]** our lo our lowest bit on the blue is a one so we're good to go three plus zero is three three comes around here gets put into here and we record the lowest bit like this so whatever this is i literally just copy it to here now we're gonna repeat so we shift this over to the right and our lowest bit is still a one so we still don't cancel or anything

**[5:05]** but now instead of our adder doing three plus zero it's going to do three plus one three plus one is a four four comes around and gets put into these four and there we have it our answer is one zero zero one which is nine so let's do another example i'm gonna do five times five we have five in the red and five in the blue when we go through the first time this

**[5:37]** is a one no canceling needed so five plus zero gives us a five five comes around gets put into here and we record the lowest bit so the first digit of our answer is a one again i'm just copying whatever this is and putting it here now before we do our next loop we of course need to shift this over now our lowest bit is a zero so for the first time we actually need to just

**[6:08]** turn this off completely cancel it it's equivalent to this second row right here when we were doing it out on paper so now the adder is going to do zero plus two and of course that's just two two gets sent around gets put into here and we're going to record the lowest one so bring this over copy it and you know shift this over now now we need to start our third and final loop

**[6:39]** this number gets shifted again this last bit has become a one again so now we can send in that five it no longer needs to be canceled five plus one is six six comes around to the back gets put into here and we are done five times five is 25 16 8 and a 1. now this is the 16 bit multiplier that i used in the calculator and i'm going to be trying to

**[7:10]** build this with the tutorial so because it's using loops now it's not as simple as just flicking the levers and watching the answer appear we do need a calculate button and a clear button just so that we can tell it to run and clear when we're done so i'm gonna show you the five times five we just did on an actual multiplier so five times five is inputted it's this blue and this

**[7:33]** orange and when you hit calculate notice how this bottom bit is getting saved every time and shifted over and eventually our answer shows up as 25 1 6 and 18. all right so we're going to start with our 8-bit adder as usual i get rid of all the carrying stuff it's just going to get in the way anyways just make sure to keep it off we're going to take these outputs and

**[7:58]** shift them down by one by the time they come around i'm going to hug it really close to the adder with no space in between i'm just going to put a repeater here one two three blocks down one with the slab and then two and then one up repeater here redstone dust on the rest block this off block this off and then i'm gonna do something a little weird i'm gonna take

**[8:21]** this one by one part of the actual adder and one this way it won't affect the adder at all it'll just reduce uh these lines interfering with anything because see right here we need to block another one off right there now we can actually stack this whole thing seven down so this part seven down actually let's just do eight down because we're starting from the carryout uh take this part

**[8:48]** actually take uh this entire part stack eight down there we go now what you want to do is get rid of this bottom one put a repeater here starting on this bottom bit bring it up by one cancel it with a repeater make it like this and then you're gonna stack this part seven

**[9:20]** times and you can just put a torch right here for now to lock all of these and then we're gonna do something similar over here we're gonna build starting from here more repeater locks so i'm gonna put a slab like this i'm sorry block like this and i'm just going to power it for now using a redstone block and now you can just stack this whole thing up you can stack this part stack 7 up slab tower

**[9:54]** stack seven up you might have extra that's okay get rid of that and then make sure the top one is locked now we can also build part of the clearing mechanism this is going to use sticky pistons and you're going to build up like this and make another slab tower thingy and you can just stack these seven up take this span one up uh stack seven up and there we go get

**[10:25]** rid of these and then you can also just power this for now with a torch right here now since one of these inputs is pretty much either always either gonna just be sent in or nothing at all aka the red one over there in the schematic we're just gonna control for that using some pistons over here so uh grab a sticky piston and you're actually going to build it right

**[10:47]** here and you can already put a lamp for one of your inputs this is where uh input a or whatever is going to be expand one down stack seven down there you go you can also go ahead and put lamps for the rest of your inputs so we know that this is going to be the top one 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16. when we're multiplying to eight bit numbers we get a max of an 18-bit number

**[11:15]** and as you can see i think from the other one i had signs but i'll just put some signs here too this is the lowest one this is one it goes all the way up to like something crazy i don't know 32 000 or something yup 32 768 is your top bit and it goes in an l shape all the way down like this we want a bunch of repeaters as if they were going into these blocks so take this stack seven up and i'm

**[11:38]** going to make a tower like this so i'm gonna put the clear button nine blocks out from this so one two three four five six seven eight nine and then an extra block and put a repeater here you can get rid of all these and then grab a lamp and you can put it here so i want to make this clear button split like this it's gonna come down like this one and one

**[12:09]** two three four bring it all the way across out to here and then you can start going up like this and just keep bringing it up and then this is going to have to be a sticky piston here and then there's going to be a slab here and a slab here block here and then we actually want um another

**[12:39]** piston here and then you're actually gonna have to bring all these blocks up block here repeater on two ticks redstone under these and then redstone on the entire thing and you'll probably need another repeater along the way here yep and then the clear also has to do one other thing it has to open up the machine so we're

**[13:10]** gonna go like this and so now when we press this button it's going to pull back all these pistons killing all these lines and it unlocks all these repeaters by making this piston pull back the redstone block and i almost forgot we also have to clear the ones that are down here so to do that just make a repeater put it on three ticks go like that and now these will all be

**[13:39]** unlocked as well to let everything flow out all right so i'm gonna label it so i don't forget get a sign clear and then let's also make the calculate button so that one's going to be here grab a button but also label this repeater here block here

**[14:11]** another block uh yeah you're gonna want to do a pattern like this where you have like four blocks coming out and then bring these over here and then put some blocks in between here one in between here and one in between here as well

**[14:42]** now pistons sticky pistons go under this block and this block and another block here whoops and then you want a repeater on three ticks here or peter on three ticks three ticks and a repeater on two ticks right here and then the rest can be filled in with redstone and now you need a comparator here

**[15:13]** and a block and redstone so this is essentially going to create the loop that we're going to use to count how many times we ship this through and it's going to shift a total of eight times before it gets to its final answer now we also need a way to stop it when it's done so that's that's what i'm gonna build here so right here build a redstone like this down three one two three four five

**[15:40]** six and this is all going to be normal redstone and then one two three four five six seven eight and a slab and these are all going to be repeaters on the max link which is four ticks and then this is going to flip itself around like this three ticks right here and we're gonna make an

**[16:11]** extender this is a pulse extender one two three four put it like that build this all the way out redstone all over it and then go up like this make looks like this and we're gonna make a um torch tower out of these so

**[16:45]** like i'm sorry not one there one here here here here and here and then this is going to power a repeater into a block into redstone dust which is next to a extended piston here and so that is one giant loop that's going to basically come down here wait a lot of repeaters until it gets

**[17:16]** back and the repeaters are exactly time for how long this machine is going to take to do one calculation and then when it's all done this will turn off which retracts the piston and closes the loop and i also forgot to make these two blocks right here and these two redstone it's really important ones because that makes the loop um unlock and lock these repeaters every

**[17:35]** time which is essentially capturing this last bit and shifting it over it's responsible for half of our answer and since this circuit already times how long it is for us we can also use it to just lock the repeaters at the very end which we need to do in order to save the answer so i'm just going to make three more like this all with four ticks um yeah block here another repeater

**[17:59]** redstone sticky piston block repeater block block dust dust there you go so at this point what this multiplier is doing is it's multiplying your a number with all ones because we haven't coded for whether it's sent in or not every time right now it's just being sent in no matter what so that's the equivalent as just doing all ones so let's try uh three times eight ones uh let's clear it first

**[18:29]** make sure the lamps are off hit the calculate button and there you go one zero six ones zero one and i've already checked that that is three times eight ones one correction is this sticky piston pushes up on this block so you're gonna have to uh move all these up here like this so in order to make a system to block this uh whenever there's a zero in the

**[19:00]** other number i'm first going to make a big spiral tower right here starting from this repeater and then going up like this and it's going to be 14 blocks in length it's going to reach nearly the top so i'll just build it up here but i think it stops around here let's see one two three four five six seven eight nine ten eleven twelve thirteen and the fourteenth one goes out like

**[19:30]** this now i'm gonna make our second input it'll just make it easier to line up so put this here put a um lever and then there's going to be a sticky piston right here and a torch here so now you can take this whole thing stack seven down and there you go so what i'm going to build right here this is really hard to explain but i'm making a tower right and each level

**[20:01]** of the tower is our each bit in our second number as this goes through the eight loops so let's say loop one loop two loop three those are gonna be synced up with level one level two and level three now each level is obviously coded with our second number and as it goes through these loops it's going to look at each level and if that level is a zero it cancels it if that level is a one

**[20:25]** lets it go through that's why we're connecting this spiral here to all the levels and this whole spiral is connected to a comparator to cancel it because if it's a zero at any level it will power this line and cancel the number if it's a one in any level it won't do anything with this line and the number will go through as normal um it's kind of hard to describe how to

**[20:46]** build this so just bear with me i'm gonna do it uh column by column here obviously first put blocks on these then you want to put a repeater block two repeaters another block take this whole thing stack it seven down and then put redstone on every other one so it's going to start with a repeater at the top redstone here redstone here redstone here then you want to take this guy

**[21:18]** and stack it seven down and alternate all of these to be repeaters until your last one is all the way down here barely powering this block which still reaches the end of the loop then you want to take in between these blocks and build like this build like this and then build two arches like this dust here repeater here and then a torch on the inside of this and then torches like this as well

**[21:49]** and then you want to take this pattern and stack seven down and then you don't need this top one but what you do need is to continue these torches all the way on the bottom here and then obviously you can uh get rid of this and then you actually don't need these two and you also don't need these blocks here then in order to start the tower from the bottom you just take this line which is from

**[22:19]** the calculate button into a block with a torch going up block like this portion of the side and another small change all of these have to be two ticks instead of one so with the tower done and the canceling being done accordingly we should now have a 16 bit multiplier really cool so let's try it out let's do let's do something huge i'm just gonna test something really big out

**[22:47]** and then i'll put it on screen all right make sure there's nothing in there calculate and this is correct we just did 173 times 223 equals 38 579 awesome all right before we copy it to the calculator i'm gonna just bring these two inputs out to the front so it fits

**[23:18]** uh easier i took this one and did a dot and a redstone repeater and then this one just has a repeater and a line all the way out i'm just gonna copy this whole thing uh one here one here stack seven down and these should be our inputs put repeaters on it to line it up better when we copy it actually we're gonna need to bring it up more bring it up to about here

**[23:50]** then put dust and then stack this up again so keep the calculate and clear button where they are when we copy it and let's take a corner this should be fine other corner all the way down here there's a bunch of lines underneath so got to make sure to go as far down as

**[24:23]** the lowest line and then my reference point is going to be on the top here just try this copy and then just like before bring the a line out front bring it down with some slabs and then put b through a paste dash a everything fits cool all right i say we test addition

**[24:54]** subtraction and multiplication all at one time eventually we're gonna get to switching between these modes and all the cool automatic stuff like that but i'm gonna save that until after the division episode there's gonna be just be a there's a whole lot of little logistics like that that i'm just gonna cram into one giant like logistics episode and so let's do a hundred and eighty two

**[25:24]** i don't know man two hundred and 210 minus 182 should be 28. and that is right here we have 16 8 and 4. i'm sorry yeah 16 8 and 4 that gives us 28. 210 plus 182 is 392.

**[25:54]** 392. you know what i'm going to trust that's 392. i think our adder is working that's typically the most the most reliable out of all these all right multiplier time so the inputs are in but we still have to hit the calculate button and while it's going 210 times 182 is 38 220 and i just checked it with this number and it all works so now we've done math with three different operations

**[26:23]** thanks for watching
