# Redstone Calculator Tutorial Part 4 - Addition and Subtraction

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=HiTeqnIxZaY
- **Duration:** 18:47
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** all right this is part four of the redstone calculator tutorial so far we've made a screen we've made an input system where we can switch between a and b type in any number on the top and bottom and we'll have those two numbers resembled in binary two eight bit numbers one for a and one for b on the side over here so now that we have our two eight bit numbers ready to

**[0:18]** go all of our inputting is done and now it's time to actually do math with them but before that we do that we have to make it easier to get these outputs out of here because it's really hard to reach these right now so what i'm gonna do for that is just build out um a little bit more of a staircase for the ones that aren't connected to anything just so that we can take an easier output i'm

**[0:36]** gonna take an output from this column right here once you've done that should look something like this i also replaced these lamps with just normal blocks because it's going to be way easier to just put lamps right here now so put lamps on this column and then also repeat the entire thing for the other one all right so now that it looks like this what i'm going to do is since this is our a number

**[0:55]** i'm going to pull it out like this and just give ourselves some room so just make this line go past the edge here and stack this seven down make sure it doesn't mess with anything down here okay and i'm going to do the exact same thing for b take this entire wall copy and paste so then what i'm going to do is i'm going to make b

**[1:26]** come over here to a i'm going to stack maybe 15 or so okay let's do a little bit more 20. and you want it to so that they are that there are two blocks in between them so in my case i'm gonna have to stack this 22 and then of course you will have to put um repeaters wherever you need to so now it should look like this and then what i'm going to do is i'm going to take this a line

**[1:54]** stack it out by another two blocks and then bring this just some amount this way it doesn't really matter right now this is just going to set us up for the future now go to the a line and on the end of this go out and put repeaters here the reason i'm doing this is because we want to make it so that b can go through a right here without actually interfering with it

**[2:23]** so the way i'm going to do that is putting a repeater here and then a block here and so now b can go through a without messing with anything so just stack this for everything else stack seven down stack seven down and then finally just bring a down by one so just take uh put slabs like this and copy them like that so seven down

**[2:54]** and now we have our inputs for where the adder is going to be so now we just need to take the carry cancel ladder that we were using in the previous episode and hook it up to those two inputs and slash slash paste and remember these have to be the exact same signal strength coming in on these corners so i got 15 and 15 because they're both repeaters right there

**[3:12]** we want to be pointing forward so we can eventually plug it into the display so i'm just going to remove this part and then put lamps on my output so i can test it so there should be nine lamps because we have eight bits and a carryout because when you have eight bits plus eight bits you have a max of nine bits coming out all right so let's test this thing out

**[3:32]** let's put in a hundred and i don't know 107. flip to b do 90 3 so our answer should be 200 this is the 128 bit 128 plus 64 is 192 192 plus a 8 is 200 so perfect we just did the first actual math with the calculator

**[4:03]** congratulations moving on to subtraction uh let's make the inputs for the subtraction and now you'll see why this output is kind of useful because what we can do is just do the exact same thing we did over here we'll take a out from like i don't know just go out from like here do it with slabs again and then make b go through the lines and again just have a space of uh

**[4:26]** two in between them so again a just drop down with a slab and b go through a so you have your two inputs here okay should look something like this and now let's move on to how we're actually gonna do subtraction the way we're gonna do subtraction is through something called two's complement two's complement is where we represent negative numbers by inverting them and adding one so for example

**[4:48]** if you have five which is one on one we would invert it like this changing all the zeros to ones and ones to zeros and then add one to it so five through two's complement would be zero one one the way we're going to use this for subtraction is by representing the second number the b number in a minus b um in two's complement so we're gonna change b by inverting it and adding 1

**[5:11]** and then from that answer we will be able to tell what the what the answer is from subtraction so for example let's do 6 minus three so six minus three we know is going to be three but let's see how we would do a two's complement so we take the second number which is the b number we're gonna invert it and add one so this is it when it's inverted and then we're gonna add one

**[5:42]** now we take these two numbers and we add them because we're technically adding negative numbers together so this looks like it's six plus five and six plus five would give us eleven and eleven is one zero one one so even though it doesn't look like it we just did subtraction because what we did is we did six minus three and we got an answer of one zero one one and i know it looks like eleven

**[6:11]** but really the first one doesn't mean is the is the sign bit that's just telling us whether it's positive or negative the only bits we care about from this answer is the same size as what we started with we started with only three bits in length so the only part we care about in the answer is the three bits in length the zero one one so six minus three is actually just

**[6:32]** three 0 1 1. the one out front is telling us that it's positive so let's do an example where we get a negative number so let's just do the reverse zero one one three minus six so we're gonna do the exact same thing three minus six we're gonna take the b number which is six this time we're gonna invert it and add one so three uh inverting a six gives us

**[7:05]** this adding one gives us this adding these negative numbers together it looks like it's three plus two which would give us five now our sign bit this time is a zero which tells us that it's negative so we're not done yet because this is negative we actually have to flip it back invert and add one again to get our final answer so remember we had three minus six so we should get a

**[7:35]** negative three if this is correct so again the zero out out front tells us it's negative and the 101 is the number we is the negative number then we need to convert back so we can read our answer so 101 invert add one and you see it's three so our final answer is negative three so you saw in that case that we had to invert and add one twice throughout the process so that means we're actually

**[8:02]** going to need two adders for this um so i'm gonna start by copying this first one okay so here's our normal 8-bit adder our a input is just going to look normal and our b input is going to be inverted so let's start with the b input over here to invert them you're just going to want to put a torch like this and then a repeater like this and to keep it on the same level over here

**[8:31]** just put something like this and block like that so now copy this whole thing stack 7 down and now we have our a input going in normally our b input going in inverted and the last thing we need to do is we need to automatically add one to this answer so i think you can just do that by cutting this out and now the carry in is being powered and you should be good to go so this is

**[9:03]** actually a working subtractor if you only get positive answers so let me just take these lamps expand one up stack seven up and i'll show you what i mean so let's get some levers if we're doing what we did before and we did uh what was it six minus three we get a three and the one on the top tells us that it's positive so there you go

**[9:33]** now we need to copy this and paste it in front of it so that we can use a second adder in case we need to we need to when this is negative because when it's negative we need to invert and add one to the answer again and i'll show you what i mean by that if we have three minus six our carryout is zero in other words our sign bit is zero and that's telling us that our answer is negative

**[9:57]** and of course when that's the case we're going to use this second adder to invert this answer again and add one and you can tell that so this is three minus six we would want negative three you can tell that this is going to be a negative three because if you were to invert this then this lamp is going to be the only one that's on and then if you add one to that well now

**[10:15]** you have one one which is three negative three which is our answer so let's turn these off and then copy this adder so that we can use it again so go out here take a corner pick another corner copy go out by two make it line up because why not paste and then if we're going to use this

**[10:46]** adder it's going to be inverted so just put a repeater like this and now copy this whole setup stack it seven down and we do need to add one as well but i think because we copied this adder this one was already adding one so this one is also already adding one so we're good there now we need to just control for which output's going to be correct and actually let's test if this is working

**[11:17]** so normally 6 minus 3 this one's going to be our correct answer and it's going to be a 3. positive 3. if we have three minus six we have negative three our second answer is one that's correct if we do two minus seven we're gonna get a five and our second answer is correct again negative five so yeah like i said now it's just a matter of controlling for

**[11:48]** which one's correct way we can do that is by first getting rid of these lamps bringing this second answer out with a space and then a comparator and then another space and then another redstone like this stack seven up and then you can stack this this way

**[12:19]** stack like 17 or so and that was too much stack 14. make this answer also connect to the line so you could probably just do that with a slab yeah um if you want to be actually careful just put a repeater here and then let's hope this has enough strength 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 perfect so this is going to be our answer

**[12:52]** right here and then chop this off and stack this down and now we just need to control for when we want to cancel this guy so just make a repeater tower here stack seven down bring this up with a slab tower

**[13:29]** redstone on it now we need to think a little bit because when do we want to cancel this we want to cancel this when this is positive in other words this is on so this is already set up correctly we just need to connect this carryout line to the cancellation over here um easiest way to do that is probably just a spiral to be honest i i think we have room for it

**[13:57]** yeah just go right here and make a uh a downward spiral like this and i'm gonna use the i'm gonna connect the redstone live just so if we run out of signal strength we know how to handle it so continue to build down this yeah right here just do something like that and continue to

**[14:31]** oops build this down and repeater here hopefully it reaches all the way up and it does and you also need to bring out this carryout line as our uh as our signal bit and we're

**[15:02]** going to label it as well so we don't forget what it means let's bring this out oh of course and then stack this part of the uh of the output down as well step seven down so let's put a sign on this if i remember right one equals positive zero equals negative and then i almost forgot we also need to be able to cancel this line in the opposite case

**[15:35]** so stack seven down do the exact same thing make a torch tower so i'm going to copy this guy's torch tower rotate 180 and slash paste and since it's just the opposite we can take a uh we need a redstone torch and we can just take this signal

**[16:12]** and go like this and that hopefully no it doesn't reach all the way up we need to be one more block out and there so this should be a working subtractor now let's try this out right now i have uh 3 minus 7 and that is giving us a negative four beautiful let's try uh five minus seven

**[16:43]** should also give us a negative two let's try seven minus three this should give us a positive four and yeah seems to be working so just like before with the adder we can uh just copy this entire thing actually i'm gonna copy it from right here put the other corner

**[17:14]** right here and pick a reference point slash oh wait i need to choose this one flash copy uh in my case i need to rotate 180 and then over where the subtractor thing is slash slash paste and that was a horrible idea and this is why world that it has undo perfect demonstration of why you need to do slash paste

**[17:45]** dash a now we can test addition and subtraction at the same time so reset it let's try 1 20 3 minus uh two fifty one twenty three minus two fifty should be one twenty 127

**[18:15]** and our subtractor gave us 0 means it's negative 127 perfect 1 1 1 1 1 1 1 7 1's is negative 127 and just for good measure we can test if our adder is still working which is this line right here 123 plus 250 should be 373. 1 0 1 1 1 0 1 0 1 i'm going to check that real quick and it is correct so now we have addition add subtraction both working

**[18:45]** thanks for watching
