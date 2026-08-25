# Redstone Calculator Tutorial Part 7 - Logistics

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=lp54Dwasg5k
- **Duration:** 27:32
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** all right this is part seven this is just a logistics episode we just have to go over a few things that we have to add to the calculator before it's ready to display its answer on the bottom first thing i want to go over is the leading zero logic what that means is well these don't look very natural right now they're three zeros when honestly you only need one and i think on the original calculator

**[0:19]** if you have just zero in there it just shows one uh so let's fix this and add a little bit of logic so that it looks normal the way we can do that is first we just need to cancel um the leading zeros on the top and bottom because they never need to be shown there's no number you can type in here where this number where this number needs to be shown as a zero it just never happens

**[0:46]** the other thing we need to do is i'm gonna put slabs all along here block this off block this off and i'm going to pour them all together into a torch and now this output should tell us whether it's a zero or not so as soon as we get any other signal that's not a zero this line gets powered and it turns it

**[1:17]** off and so now we just need to connect this and make it so that it cancels the second zero because if our leading zero is a zero then we have permission to also cancel the second one

**[1:48]** and there we go let's do the exact same thing on the bottom just bring some slabs out put redstone on them block it off where you need to make it go into a torch and then take signal from here

**[2:35]** okay so now no matter what we type in on the top and bottom it should look normal and you can test that by just putting in a one and then a zero yep so since this one is out here it allows this zero to be on and then it also allows the zero to be on and when we clear it it just goes back to being one zero cool now every number should look normal i'm also going to go around the back

**[3:06]** and put a bar like this all the way out to like here now you can take your bcd to seven segment display device from the very beginning and copy it five times on the bottom and when you're done it should look something like this all five modules right next to each other to make one giant line of bcd now we just need to do that same leading zero logic but for the entire answer

**[3:32]** so the first thing just like before is to cancel this zero because there's never a point where you want that zero to show the next thing i'm going to do is bring out slabs but behind it this time and still put a redstone like this and do this for the first three so this one this one and this one should look something like this and now you want to actually bring out the um

**[4:05]** zero from here and block this off and then block like this repeater and another block and another block and two redstone so do that for the three middle numbers so this one this one and this one not the ones on the end after you've done that it should look something like this with these three sticking out here now you want to take a repeater signal from here into a block

**[4:37]** into a torch into another block and line it up with this guy so that it powers it and cancels the second zero on the display then you want to take another signal from here and put this into another torch into a block have them line up like this into another dust into a torch and like this and then you're going to kind of repeat you're going to want to put another repeater here

**[5:09]** into this into the l shape thing torch block one more another torch and over like this so if i did everything correctly we should have the leading zero logic for the answer all working so let's say our third number is an eight so in other words we got an answer of um

**[5:39]** 800 or i think that might be a one yeah it's a one so the one stays and it keeps all the zeros that follow it if we have something in the very end one let's actually do an eight this time let's say our answer came out to be 80 000 you can see as soon as this eight goes in all the zeros that follow it pop up so now the answer should always look normal as well now we're going to connect all the

**[6:00]** outputs from all four of these addition subtraction multiplication division we're gonna connect all four of those outputs into one like master bus and that master bus will put itself into the answer so to start this i'm gonna just go on the first level of division that way division will line up properly go all the way out to like here it really doesn't matter redstone and stack 15 up

**[6:32]** and then you can take this whole thing there should be 16 of them and stack it this way by like 60. now your job is to connect the outputs from these four into the master bus at their corresponding levels the bottom one here resembles a 1 and then 2 4 8 16 etc all the way to the 32 000 or something and so you just want to take the output from addition put it accordingly subtraction put it

**[6:58]** accordingly and so on so i'll start with addition for example um you have to do the the going down with the slab block trick in order to make them all stack with each other so you're gonna have a lot of this until it finally gets to the same level as this level one and so this level one if i look at my top right it's at y 101 so we want this one here to go to 101. so we go down by two more

**[7:31]** and yeah you get the idea so you put repeaters where you need to take all of these line them up plug them into the bus and do the exact same thing with subtraction multiplication and division all right so you can see here that's what i did addition drops down and just gets put into the first uh nine subtraction drops down and gets put into the first eight we'll worry about

**[7:51]** this bit later this is gonna be for our uh subtraction sign uh multiplication i took the l right here of the outputs and just line them all up with the 1 through 16 and then division i just connected it to the end right here and then this wall is all flowing to the right so they should all activate these lamps on the very end now now we need a cancellation line for each of these four so

**[8:23]** comparator on subtract mode stack 8 repeater stack 8 slap tower stack and then just put a torch here and now you want to do the exact same thing for the other three and you might have something like this where

**[8:54]** you need to um extend the signal now i have a cancellation tower for everything the divider the multiplier the subtractor and the adder and they're all being powered right now with the torch on the bottom so right now nothing is getting through to our answer now we have to build our mode selector the thing that allows us to switch between the four modes over here you're gonna start by putting four

**[9:21]** torches directly behind the buttons and then put four blocks on top of them four more torches four more blocks and then dust on top all these torches are going to power a line of repeaters all on one tick and do sticky pistons that go upwards into more blocks and then another line of repeaters and now we're gonna have sticky pistons facing outwards with redstone blocks and then out here

**[9:53]** you want a row of alternating redstone repeater to dust repeater to dust put blocks like this and then on the other side make it alternate the other way so dust in front of the repeaters repeaters in front of the dust up here you want more sticky pistons blocks on top of them more dust blocks on these and then connect these

**[10:25]** up and then bring it out further with a slab into [Music] a torch so now we should be able to select what we want and if you put lamps on these well actually just go out like this down like this all right now you should be good to put lamps on them if you want

**[11:02]** and this should be our mode selector so if we hit addition we get the addition lamp to turn on if we hit subtraction subtraction lamp turns on and yeah now i'll attempt to show you how to build this uh symbol switcher thing that i made it allows you to put the plus sign uh negative sign multiplication sign all in the same five by five area you're going to start with your five by five area of lamps

**[11:27]** and then you want torches on a 3x3 and then also on some extra blocks out here the top three lines you're going to first get rid of this block and put one here instead and then put redstone on top of these

**[11:57]** two redstone on these two repeater here and also repeater on these two blocks and then you can line them all up and these are going to be your top three segments so what these segments control for is specific parts of the display and the parts we're gonna code for with these nine uh rows are well the top row is this guy this guy and this guy the middle row is this guy

**[12:25]** this guy this guy and then the bottom row is this guy this guy and this guy so those are things we're going to control for and then using different combinations of them we're going to use an encoder to code for the four different symbols so then back to building you do have to go in here and get punch out these two and then just put blocks right here now for your middle row you first want

**[12:48]** to punch out this block so you can reach in here and put a repeater then you can replace it and put the torch back and then your middle segment is going to be your repeater here bring it out like this the other two on the middle row are going to be brought out with blocks like this and a slab here and you're going to put put two repeaters dust all the way same thing over here

**[13:09]** blocks out like this but this one's a slab two repeaters and dust all the way now for the bottom row the middle one you can just take with a repeater from right here the side ones are going to be a little bit different you're going to want to put another two torches kind of below these ones and now you have to link up redstone so that they can all connect so you're

**[13:33]** going to want to put a repeater here a block here and something like this so that you can put uh oh and block these off so you can put redstone all the way on here and same thing on this side another two torches a repeater into a block connect all the redstone now some of these are on to start so i'm

**[14:04]** actually gonna just change that to make it simpler uh what i'm gonna do so the top three are on the middle outside ones are on and the bottom middle one is on so uh we can just fix that by putting torches all here on these guys and on this guy and now they should all be off now you can bring all these lines back out again to make a three by three and then extend the top to go two up

**[14:34]** like this and the bottom to go two down like that all right should look something like this then you wanna put your four vertical lines or i mean uh four lines going the other way the redstone on them and then you can copy this whole layer and place it above um the other two as well so copy from here face dash a and paste sha now you can connect each column of three

**[15:05]** with a slab tower here that way when we go down here and power with the torch it powers all parts of the line so all the way to here all the way to here and all the way to here and then stack this three more times out so it covers all four now you want to snake these guys under with a few more torches so take it like this and stack this guy expand one stack three

**[15:31]** and now after you code for your lines these will represent your um addition subtraction multiplication and division so put blocks like this grab a lever and now we can test for each one so when we hit addition this line is going to turn off meaning all the torches attached to it will turn on so we want all the torches attached to this first line to resemble the plus so that means we want this one

**[15:59]** uh all the ones on the middle row and one down here in the middle and that gives us a plus sign so that's good we can turn it off and then go to subtraction subtraction we just want the middle three so boom boom boom all right yeah subtraction sign and then multiplication is going to be the corner ones so it's going to be like these two

**[16:30]** outside ones and then the middle and then these two outside ones that gives us an x perfect and then finally for division we just want to slash cool now you can copy this whole module and paste it uh somewhere on your display i'm going to take it from

**[17:00]** this row and then go one up and i'm also going to line it up with the middle of the second digit so this column right here case dash a it doesn't really matter where you put it but the important thing is is that it doesn't interfere with anything going on over here as you can see we just barely don't mess with the lines underneath and we also don't mess with the leading zero

**[17:25]** logic that we built over here so now you can see as we press these we can put symbols on the screen so i just hit the division one you can hit the addition one so now what i'm going to do is i'm going to take these four lines i'm going to sneak them all the way back through here and have them somewhere out here so it's easier to line up with the four modes and that's

**[17:49]** what i did i took those four lines put them through here and now they're easier to reach all right i made a logic map for all the remaining things we have to do each row resembles when each mode is turned on and the signs next to it are all the things that has to happen when that mode gets turned on so for addition mode we have to do these three things we have to turn on the addition sign

**[18:08]** which is uh that first one right there that we just made uh we have to unlock the addition answers which means we have to uh turn off this tower from these towers we made earlier and that will let the addition answer come through and then the third thing we have to do is we have to clear m d m d stands for the multiplier and then divider this is just so that people can

**[18:32]** switch between the modes at their will without having issues with the divider and stuff so when addition mode is turned on we just have to also clear the multiplier and divider subtraction mode we have to turn on the sign we have to unlock their answers we have to also enable the negative sign if if we need to and then we also have to clear the multiplier and divider

**[18:51]** multiplication mode we have to do the sign the answers we have to press calculate on the multiplier otherwise it won't do anything and then we have to clear the divider division mode turn on the division sign unlock the answers press calculate on the divider enable the decimal point so the decimal point will come after the first two and then clear the multiplier

**[19:12]** but before we do any of that though i want to change these calculate and clear buttons for the multiplier and the divider because right now they're just meant to work with stone buttons which is great but a stone button is really specific it's a it's a dentic redstone pulse and these modes when they're turned on they're not 10 ticks they just stay on for as long as you have the mode

**[19:31]** so we need to create a 10 tick pulse uh generator on these guys so i'm going to get rid of these lamps i'm going to extend them down with the torch there you go and then you can create your first 10 tick thingy out here this is the only one i'm going to build on camera just to show you how to make it

**[20:03]** so this is for and then you go like this with uh i'm sorry you go like this with a sticky piston a block and redstone like this so now let's say this is multiplication mode coming in we turn this on and it generates a 10 tick pulse right into the calculate button so i'm going to make three more of these another one for the clear on this guy and then two more for

**[20:36]** the calculate and clear for division okay so i made another one for the clear button on the multiplier and then i made two more over here for the divider calculate and clear since addition is fairly straightforward i'm just going to show you what you need to connect it to and then i'll cut to when i did it so this addition line right here the one that gets powered when we hit

**[20:56]** edition this line needs to connect to our addition symbol so this guy and needs to connect to this guy to let our answers through and then it needs to clear our multiplication and division so clear division and clear multiplication all right edition mode is all set up it comes out here it turns on the addition sign so pops up on the display it lets the addition answers through

**[21:26]** from right here it clears the divider with this line and it clears the multiplier all the way over here with this line so for subtraction you're going to want to connect it to here and your tower to let the subtraction answers through and then as usual the clearing for the um divider and the clearing for the multiplier and then after connecting those we have to do one more thing for subtraction

**[21:57]** okay subtraction's all wired up to those four things and now we need to grab the signal for where we want the negative sign and i think we can just grab it from out here if you go one two to the second number and you grab this guy i think that will just show up as our where we want the negative sign yeah okay so we're just reusing one of the segments of the numbers that we don't use in

**[22:26]** subtraction uh so yeah this is our line for it and the carry out from subtraction remember we want the negative sign to show up when the carry out is a zero so we need to first invert this signal and then connect it to the negative sign all the way down there that's what i've done with this line here connects them like that and now when we test subtraction if we get zero minus zero is a zero

**[22:59]** which is positive but if we put something in the bottom then we're going to get a negative answer and the negative sign pops up perfect now i'm also going to just disable this negative sign whenever any other mode is on in other words i only want it to show up if it's subtraction mode so you can just put a comparator here a cancellation and then connect uh the inverse of subtraction mode

**[23:26]** to the cancellation so in other words when subtraction mode is on this line will always be off meaning that no canceling is going to happen but as soon as any other mode is on and subtraction mode gets turned off this line gets powered and if you connect it all the way here it will cancel the negative sign all right multiplication mode this line needs to connect to here to turn the x on

**[23:54]** needs to allow your uh multiplication answers through which is over here it needs to hit calculate on the multiplier which is this guy and then it also needs to clear the divider so as always this guy right here all right multiplication is all wired up for division i'm going to do the easier parts first we have to enable the division sign

**[24:24]** we have to let the giant stack of division answers through we have to hit calculate on the divider which is this guy and we have to clear the multiplier which is this guy all right those four parts of division are lined up and now the last thing we have to do is worry about the decimal point so for the decimal point i'm gonna go right after the first two digits and

**[24:50]** then in between the second and the third right here i want it to be this block so i'm gonna put a block like this repeaters here so it doesn't interfere with anything and then a torch and yeah that looks like the decimal point we want another torch to disable it for right now and then bring this line out and then the other thing we want to do is adjust the um

**[25:21]** the leading zero logic a little bit because it's going to work a little bit differently with the decimal point now and all you actually need to do for that is just power this guy right here so i just made two more lines to finish up the vision you want to power this and you want to power this and that pretty much wraps it up for logistics so we are almost done the only thing we have to do

**[25:48]** is connect our final answer which is all the way over here in a vertical form these are 16 bits and we need to convert them into the six digits of bcd down here to display into our answer other than that let's just give this a giant test um so i'm going to flip it into addition mode we should get our symbol and our division stuff goes away let's do 120

**[26:24]** three i already have a two on the bottom let's make it two hundred and forty seven so we can head over and check our answer and our answer over here is correct it's 370. now we can go back and switch to subtraction mode so 23 minus 247 and we got our negative sign and we got our subtraction sign we go all the way back here and it's

**[26:54]** correct negative 124 and we can switch it to multiplication live this is correct 30 381 and finally let's switch it live to division mode and we got 49 in the output and like i said lots of times before as soon as this gets plugged into the display it'll look normal because our decimal

**[27:27]** point popped up and it will look like 0.49 perfect thanks for watching
