# Redstone Calculator Tutorial Part 8 - Binary to BCD

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=D0lOzDvhPUo
- **Duration:** 11:28
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** all right welcome to part eight this is the final part of the calculator series there is one thing i forgot to do in the last episode but it's kind of optional i'm gonna go over it anyways because it does make it nicer and this is what this is what was included in the original calculator so we have this clear button here and what this clear button should also be doing is clearing the mode

**[0:18]** so we can do that with just a torch here and a redstone and now when we press this clear button it resets the mode to nothing so and then this clear button should also clear the multiplier and divider just like the modes were doing earlier so you can do that to take this clear line follow it out and make it so that when it's pressed it activates the clear for the

**[0:40]** multiplier here and divider over there so again that part is optional but it does make it a little bit cleaner so that uh when you hit the clear button everything goes away and you can start from the beginning instead of just having to switch off of a mode every time so with that out of the way the only thing we have left to do on this calculator is convert this 16-bit binary answer

**[0:58]** into the five digits of vcd on the display and to do that we're going to use an algorithm called the double dabble algorithm so a guy named newer master i was watching on youtube had a really good video on this and i'm pretty much going to go over his exact video he has a schematic for it which has a really good explanation and all that stuff so i'm gonna go over it myself really quick

**[1:17]** but if you have any questions at all i highly recommend checking his video out it's really cool and this is the schematic for it so all it is is the blue is your binary input and then the red is going to be your bcd output this black bar is separating the digits so this first four red is your first digit and then the next one is your next digit so uh 1684 i have them labeled here so

**[1:40]** let's see what happens when we put in a 16. this orange guy says hey if my input is greater than 4 add 3 to it otherwise do nothing so this goes into here and this orange guy is seeing an 8. i know it's actually putting in a 16 but to him it looks like it's an 8 according to his inputs so 8 is greater than 4 so we're going to add 3 to it 8 plus 3 is 11 and 11 is an 8 a 2 and a 1.

**[2:13]** and so we just converted 16 in binary to bcd because this digit right here is a 6 and this digit right here if you were to expand this out with all these being 0 this digit is a 1. 1 6 and you can see how that would line up perfectly on our display then once you expand it to 16 bits which is what we need it looks like this and you can see all these oranges are the exact same

**[2:40]** they all do if it's greater than four it adds three and you have five digits of bcd in your output so starting from the right this would be 1 2 4 etc so we go to 8 16 32 64. i'm just going to show you 64 as an example but obviously you can put in any combination of this any 16 bit number you want and it should accurately show its bcd digits so 64 we follow this up and it gets put into

**[3:12]** here this guy is just seeing a one because if you just look at him his only input is its rightmost one and to him that's just a one so it outputs a one this guy sees a two so it just outputs a two this guy sees a four so he just outputs a four and then finally this guy sees an eight and eight is greater than four so he's gonna spout 11 which is an eight a two and a one so now

**[3:40]** we have two guys going at the same time this guy sees a six and six plus 3 is 9 because 6 is greater than 4 so we need to add 3 to it and then over here we have just a 1 so you're just going to output a 1. this guy sees a 3 and a 3 is fine it just outputs a three this guy sees a two and so you're just going to output a two now if we look at our bcd we got sixty four this digit right here

**[4:11]** zero one one zero this is a six zero one zero zero this is a four so our display would show 64. so according to this all we need to make this device is to make one of these orange guys copy it a bunch of times and make sure it's lined up correctly according to the schematic and then we're good to go so i would do a tutorial for it but no master already has a really good tutorial for

**[4:32]** just one of these orange pieces it's pretty much as fast as it gets i'm going to show you what it looks like when it's done just to show you how big this thing gets but even though it is really big each of these devices these all resemble the orange things in the schematic each of these devices is only two ticks which is insane so it's still really fast and we can try

**[4:55]** the thing over here with the example if you put in 64. it goes through and it comes out with 64. if you're not worried about speed you can just i've showed a lot about like decoders and encoders in this tutorial so i'm sure you could make your own device and it would be bigger and slower but as long as you follow the schematic it would still work so you can just do that or

**[5:19]** you can follow newer master but those are your two options at this point in the tutorial i'm just going to assume you made it and i'm going to start getting these outputs and inputs ready for us to paste it in so for the one in the display we're going to have to annoyingly we have to reverse all of these because if you remember when i did the 16 and it looked like this if we plug that into here

**[5:44]** it shows up backwards it shows up as 61 000. so it doesn't really matter how you do this but in some way you have to reverse all of these so make it so that uh all the way on the left there's uh it connects to that outpost input and all the way on the right it connects to this leftmost input okay so what i did is i just took them all out i stacked it back here and then had them all like

**[6:11]** flip up on top of each other and so that way now you can look at them from the side here and the one all the way on the right it lines up to being the one all the way on the left when it gets put in and yeah so that successfully reverses them but unfortunately have another problem because this lowest one on the very end is supposed to be the one and if you look it is going into the right number

**[6:39]** but the bcd is reversed as well like each individual packet of four is also reversed because instead of a one it's giving us an eight so on top of the reversing i already have i also need to build a mini like one through four reverser thing for each bcd digit so this makes it so that uh the one goes into the four two goes into the three and yeah just this four gets flopped and we need to do that

**[7:08]** for each digit so now this is the highest bit this should be the eight on the highest digit and it is so we're going to copy this reversing device and stack here bring it up spin it down spin

**[7:39]** one stack four so finally this is our vcd input in the right orientation all that was just getting it into the orientation that we want so now if you um put separators between here which i honestly like to do and i like to keep them because it helps with debugging if you ever need to later now you can input your bcd digits so let's say we get 16 as an output which is one

**[8:09]** six we go over here on the display and we get 1 6 16. so now i'm going to paste in our giant binary to bcd thing paste and yep doesn't interfere with this okay all we have to do now is line up these with these so remember this bottom one down here is a one and the one on the very right over here

**[8:40]** is a one but first i want to test this out because it's really cool and i'm just doing this so let's try like i don't know 100 or something 64 32 and 4. plug those in through this machine it gets converted into bcd and then it shows up as 100 or if you do the highest one over here 32 768 you just flick one lever it goes to this whole machine

**[9:12]** 32 768. all right i got them all lined up the bottom one goes into the very right and the top one goes into the very left and i highly highly recommend testing each one individually because this is a really stupid part to have a mistake on especially with all this crazy wiring so what i mean by that is like test the top one make sure it only lights up that leftmost repeater and then go one down

**[9:38]** make sure it only lights up that second repeater three down and so on all the way but with that we're done now we can test the calculator everything should show up on the screen so let's try some out let's do uh 25 and 73.

**[10:08]** first put it into addition mode we get our plus sign and then we get our answer 98 now you can switch it live into subtraction mode negative 48 switch it into multiplication mode 1825 finally switch it into division mode 0.34 dude

**[10:41]** this is incredible all right i really hope you enjoyed this i know that not a lot of people will actually take their time to build this whole thing and i don't blame you it's not really what this is for i really just wanted to show off how each part worked and hope that people learn something in case they're doing something similar computer whatever and yeah just helping

**[10:58]** people get to know stuff because like a lot of times when i was making this i would need one specific component and i just searched everywhere no one had made it before and uh it took a lot of engineering a lot of a lot of these builds were made by me first the symbol switcher the bcd to binary device the multiplier i that that multiplier is one of the fastest ones out there

**[11:20]** and so yeah i'm probably gonna make a few more videos just highlighting a few of those builds but other than that we're done and yeah thanks for watching
