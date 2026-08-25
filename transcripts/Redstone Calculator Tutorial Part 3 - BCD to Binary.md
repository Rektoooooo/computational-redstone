# Redstone Calculator Tutorial Part 3 - BCD to Binary

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=cea9Pq_ZFq8
- **Duration:** 31:41
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** okay uh this is part three of the calculator tutorial um for this part we're going to be looking at how to convert the bcd digits that we type in into two separate 8-bit binary numbers that we can use to actually do math with the numbers that we type in so we're going to use a device over here that i made a schematic for um typically when i do schematics the blue is the input red is the output and

**[0:23]** orange is just a device or something in this case it's a binary adder so the adder has two inputs it's gonna add two binary numbers together and give an output and so this is how it's gonna work our input is gonna go into the right input over here and it says bcd input from the keypad so when we type it in let's say you type in one two three well this input is gonna get

**[0:44]** uh the one on the first round the two on the second round and then the three on the third round now over here this other input is routed to the output so the output gets routed back and on the way back it gets multiplied by 10 so i'll show you how this works so when we first type in the number 123 we type in a 1 and at this point there's nothing in this input so 0 plus 1 gives us a 1 in the output

**[1:13]** and if we stop if we stop typing at this point we just want to use a 1 we're fine however if we keep going and we press a 2 then what's going to happen is this 1 is going to get routed back multiplied by 10 so now it's a 10 and it gets added to the 2. so 10 plus 2 gives us a 12. again if we want to stop typing we're fine but we're typing in 123 so as soon as we press that 3

**[1:37]** 12 comes around here gets multiplied by 10 now the adder is adding 120 to 3 and we get an output of 123. so i'm going to show you a little bit more about binary addition so it uses logic gates just like real life real-life circuits and this i have a few examples of logic gates out these are the three logic gates that you need to make an adder this first one's an and gate

**[2:03]** this is just a really simplified version of it you have two inputs the output only goes on if both inputs are on and you have a xor gate which works by only letting one through at a time so if you have one on it goes through but if you have both nothing gets through and this is just an or gate it's literally just redstone wired up and it's always goes on as long as one of them is on so

**[2:31]** um the circuit we need to make a binary adder is called a full adder and i'll put this on screen now just using like tons of electronics i made a version of it out of these logic gates drawn out here so this green and blue is our two inputs and this one here is our carry in uh carry in can just be thought of as another input right now and this is our output and this is our carryout

**[3:01]** so let's play with it for a second so if you have one plus zero this circuit is going to give us a one as an output and same thing if we have it over here also gives us a one now if we have one plus one it's going to give us a 2 which is the carry outfit so this can be thought of as 2 right now if we add 1 plus 1 plus 1 we get a 3 which is a 1 and a 2.

**[3:32]** the idea is if you this is a great this is great for just two good addition but we want we need it to be bigger because these these are going to be potentially like 8-bit numbers if i'm typing in 255. so we need to connect uh multiple full adders together and the way we do that is we take the carry out from this guy and we plug it into the carry-in of the next guy

**[3:53]** so now you have to think about it a little bit differently the two greens is going to be input a and the two purples are input b so we can now add uh we now have a four bit adder we can add any combination so we can do three plus three we can do two plus three things like that so let's look at the green let's do let's start with three plus three so for green we'll put in a three

**[4:23]** because green both both of the green bits are lit up and for purple we'll also put in a three and so our output should be six and here it is a six we have a four which is the carry out of the second full adder and we have a two so one one zero is a six and we still have a carry-in bit but that's okay because if we add it it just fills in the last lamp and we have a perfect seven one one one

**[4:50]** so obviously this design is not the smallest or the most compact there's been a lot of adders in the minecraft community over the years my favorite one is the carry cancel adder which is only four ticks for any operation you do on it it's always the same speed it's vertical and that's because it's using some really cool tricks with like slabs and properties with it but

**[5:08]** it does the same thing it's just a full adder it's just a very optimized minecraft adder and i'll put a link for it in the description um credit goes to the magic gentleman and i'll put a tutorial for it in there too someone already made one but i'm just going to show how it works anyways so we have the output is vertical and it's in red here one two four etc as it goes up

**[5:29]** the two inputs are also vertical i i label them with the blue and the orange so for example we can do five plus three and it gives us an eight so like i said really fast synchronous which is important and so we're going to use that carry cancel ladder in making our design for this uh bcd to binary device that i talked about so what i've done is i i've taken it out here i took off all

**[5:54]** the labels and i made it so that the output is able to get locked so right now all the outputs have a repeater with them here and they're all being locked by a slab tower and so now we need to route them we need to route the output so that it gets multiplied by 10 on the first input so the way i'm going to do that is instead of building a whole multiplier there's a really easy way to

**[6:19]** do it by just shifting if you shift the number up once it gets multiplied by two that's just a property of binary and if you ship the number up three times it gets multiplied by eight which is another property of binary so we're going to do that we're going to take the output shift it up once and shift it up three times and add those two numbers together so just to show you what i mean here's

**[6:40]** the number one if we want to multiply this by 10 i'm going to first shift it up by one which gives us two and i'm also going to shift it up by three times which gives us eight so you see the one just went from being in the first slot to being in the second slot and then to being in the fourth slot and then of course add the add the single shift with the triple shift

**[7:06]** and we get 10. so this works with any number um so now we just have to replicate that in this device what i'm gonna do is i'm gonna go down to the fourth um bit here so one two three four i'm gonna make a block like this and then what you wanna do is you wanna start building like this which is kind of weird but you'll see why and you're gonna make a repeater here

**[7:40]** and then continue to build up like this like this put another repeater here redstone all along these and so now let's double check our work so we want it to go up by one and up by three so this is the one two three four fifth bit that we're talking about so the fifth bit needs to be shifted into the

**[8:11]** sixth and the eighth because the sixth is one higher and the eighth is three higher so we know the eighth is going to be the top one so that's good and is this the sixth eighth seventh sixth yep we're good and another thing you can do is you can keep these lamps on here um because it'll just act like a solid block and it'll be a good indicator for it'll be it'll make it way easier for

**[8:37]** you to see what's in the output at any time in fact i always recommend using lamps if you're debugging stuff it makes it way easier so the reason why we built it in this weird way is because this is going to be stackable for um for any of the ones under it so we need to stack this one two three four times under but we can't use the stack command because it will get

**[8:58]** all messed up so what i like to do is just build a tower like this slash copy uh paste dash a which means without air and is it doing it right well it's almost doing it right we can rebuild those uh i don't know why this got messed up but it's not too hard to to redo like this

**[9:30]** and like this and we need one more of them right here base dash a this redstone on these and then we need to do the same thing with this part so copy this module like this copy paste paste paste

**[10:02]** and paste okay so now we need to make the bcd input possible and what i've done is i've brought this out i think this block is like if you take this reference point right here one two three four five six seven eight and then that goes there i'm gonna label these as well they're gonna be kind of in reverse here i'm gonna make this one the eight

**[10:33]** four two [Music] and one and then i also want all of them to power a line under similar to the signal bit but this will just make it easier for us when we're typing it in like this for the one bit i'm just gonna go like this bring it out to here put a repeater here and redstone

**[11:03]** for the two bit i'm going to put a block like this get rid of this redstone here block like this bring it down until it lines up with the thing here out like this and then like this and then i'm also going to make this like this and so we have our signal bit line right next to everything else for the four bit i'm going to do it a little bit weird so

**[11:34]** one two four we need to take it from right here i'm gonna put a repeater here go out one two three four blocks and just bring it down until it lines up with the line here block this off now for the eight we have a little bit of an issue because both of the eight inputs are being taken right now

**[12:04]** let's see one two four eight yeah so on this level the right is being taken and the left is being taken so what we need to do is bring it like this and i'll kind of explain what's happening in just a second get like this slab slab

**[12:36]** bring a block out like this slab slab and slap make this a normal block so what's going on here is because we didn't have an 8 we can make use of the carry in to still input enough to make it add up to 8. so this eight is now connected to a one

**[13:09]** a carry in which is acts like a one so we have one plus one is two so far it's also connected to the two that we did earlier which will add two to it so one plus one plus two is four and then it's also connected to the four that we did earlier so it's it's essentially putting in a one a one a two and a four all at once which is the exact same thing as an eight

**[13:31]** small correction also put a block right here at this point it's just a matter of getting the timing right um first thing i'm going to do is i'm actually going to make this a little bit faster instead of having repeaters come out here i'm going to make these blocks instead okay and now what we need to do is have a way to de-power this in an easy way and then bring this out grab a sticky piston

**[13:59]** and in fact we have enough signal strength we can just do it like this okay one two three four we have plenty of signal strength so then you want to build this into this like this two ticks sticky piston block and another repeater for two ticks so now if we've done everything right we should have a finished device besides the clear

**[14:29]** button so let's test this out if we add in a one the machine saves the one and you can see the next time it gets it gets brought in it can shift it up once into the two and three times into the eight and if you look at this and put lamps next to it we can actually see we can predict what's gonna happen next time so look at that the next time it's gonna send in a ten one zero one zero

**[15:00]** and it's gonna add it to what's ever in it which is currently a one so let's type in another one and at this point we should have eleven which if we which we do we have an 8 a 4 i'm sorry 8 a 2 and a 1 and that is 11. so now for the final thing if we wanted 111 we would press one one more time and let's see if this is 111. so this is 64 plus 32

**[15:32]** which is 96 and 96 plus 8 is 104 104 plus 4 108 110 111 beautiful so the other thing i want to show you is this makes it really easy for me to show you why you can't type in a number bigger than 255 because if this is only eight bits tall let's look what happens when we type in 255 so we type in a two

**[16:03]** and then to do a five i'll have to just do a makeshift uh four and one real quick so five that gives us 25 and then 255 all the lamps are on and that's the max amount of information it can carry so that's why 255 is the max so the last thing we need to do with this guy is make a clear function for it um you might think it you can just clear

**[16:34]** it by de-powering this and letting it all flow out which honestly you can but it can get really slow sometimes so for example if you just plug in a one and then you depower it yeah i don't want to wait that long so let's make this a little bit faster what i'm going to do for that is i'm going to move this torch out to here um move this guy like this and also

**[17:05]** like this get rid of this torch we don't need it anymore uh reroute this so that it still connects and then you're going to want to put sticky pistons um lining ups that they look like they're about to grab the um the lamps so i think you need like five of them you'll need to do the ones that are connected to the redstone you don't need to go above that just go like this

**[17:37]** and then you want to connect them all with a slab tower like this whoops oh my gosh redstone and then make them powered like this so if they're just being powered right now it doesn't do anything because they're extended and they won't affect the lamp but as soon as we hit the clear button

**[18:08]** which i'll just put over here this is going to depower it and it's going to depower the pistons which will retract the lamps and instead of letting it flow through it will just flow out and die it won't have a chance to go back around any anymore so let's make this like this bring this down

**[18:42]** actually just make this all flat there we go it makes it easier and then we can just bring it up one here and then you're gonna want a redstone there so let's test this out here's our clear button if we type in one and let's type in more let's type in a 2 so now this is going to be 12.

**[19:13]** so now we'll watch it and we'll see if it still takes time to flow out and it doesn't they just kind of disappear so same thing if we just have a 1 remember last time it just took a long time now just disappears so it's a lot faster and it didn't take that much effort so there you go so we're gonna need two of these guys one to resemble the top number and one to resemble the bottom number

**[19:36]** uh but before we do that and copy them over here what i'm going to do is just for layout purposes you're going to want to take these digits and make them go to the side because we're going to we're going to paste it right here um so this is a was this the eight bit yeah i think this was the eight so remember the eight was on the right so let's have this one on the right

**[20:02]** and we're gonna need to have it go over all this stuff which is kind of annoying but just bring it up like this all the way like this back and then the four will go next to it like this the two

**[20:34]** and the one which we're going to need to do some fancy wiring for oh wait no we're not i'm just not building it in the right spot just bring it up like this nope still need fancy wiring oops that's why slabs are useful

**[21:06]** okay fill these all with redstone and then you're going to want to test to make sure that they all reach it and put repeaters where you need to and then as long as this has enough space we should be able to directly copy those four repeaters right here before i copy it you're actually going to want to split this line into two so take this and do this for all the pcd digits

**[21:38]** and then just expand these out like this copy this stack three okay now we're ready to copy and paste so let's take this bring this out take the first corner boom

**[22:11]** hit the second corner boom pick a reference point i'm just going to pick right here copy and would you need to rotate it by 270. obviously it might be different for you and paste dash a because why not and there we go so we should be able to type in numbers and we should be able to have it resembled in binary right here as well as the display

**[22:42]** at this point so let's try that let's try fan favorite 123 one two three 123 on the display which perfectly matches with the 123 in the machine beautiful now we do need another one of these for the b number so this is why i brought these down here because what we're going to do is we're going to take these and just make them go under the entire

**[23:12]** machine so just literally take this stack it like 20 or so oh we need even more 30. and then bring it back up to the same level that um that these guys are on so up to uh up to 108 so bring these up so you get 2008 beautiful uh but you can do it quicker than that

**[23:44]** you can do it like right here beautiful take this go like this you know the drill expand one stack three and then of course we need to think about signal strength here so one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen

**[24:22]** one two three four five six seven eight nine ten eleven twelve thirteen fourteen and as soon as we paste the next one we should be good and i think i still have it in my clipboard yep i do so now that we have machines for both a and b the last thing we need to do is the logic for the lever and the button so the clear button is the easiest it's just going to clear both a

**[24:45]** and b so that's this outside line here and we just need to route it with the clear lines for both of our machines so make it branch off here get on the same level and i'm going to test the signal strength so i'm going to do it like this like this bring it up make it connect and repeater and then i don't know if i showed this earlier but you also need a repeater right here otherwise you have some

**[25:12]** issues bring this all the way out and connect with the other clear line and just make sure it has enough strength so get rid of this torch and now when we press clear it should clear both of our machines now for the lever that's going to be this line right here so we need this to cancel a when it's on b and cancel b when it's

**[25:44]** on a so i've already put in some comparators you need them on subtract mode just like before uh you might not have enough room down here uh i think what i did is i moved these back by a few blocks just so i had enough room to bring out the uh the cancel part under here and so i'll build that right now this is the cancellation for for a so you need repeaters like this repeaters on these blocks

**[26:13]** you need to block these out just like before and then line them up with a line like this and just bring it out for now do the exact same thing on b bring these down lock them out do a line

**[26:49]** and now we just need to make this line uh do what it's supposed to do so when it's on a and it is on a right now so when it's on a it needs to cancel b so right now it should be canceling b which it will do if you just connect these wires and make sure you have enough signal strength

**[27:20]** okay and we want to do the opposite thing to a and we can achieve that with a torch this torch will be the opposite and it will do the vice versa so now when we when we are on a a is being let through b is being cancelled and vice versa we do this bring it down to b a is being cancelled and b is being let through okay i lied there's one more thing we have to do

**[27:46]** these machines have no idea if we type in zero right now so the zero has to connect to the same line that everybody else does remember this signal bit that kind of gets activated when anyone gets activated the zero has to do that too so the easiest way to get the signal from the zero is right here off of this torch so take it like this bring it up and i'm gonna make it line up with that right there

**[28:11]** so let's start bringing it up right away and then just for single strength purposes again get rid of this bring it all the way up and it also has to be cancelled according to this logic as well so we're going to have to expand this by one bring this like this so just copy all of these parts and do the exact same thing over here

**[28:45]** and so now this has to be our zero and what i'm going to do for that is continue to try to connect it to this guy might get a little messy here but i should be able to just bring it up with a slab tower barely doesn't intersect and put it like this okay that should work let's just double check so fill in the redstone

**[29:19]** repeater there and i messed this up i messed that up too and there you go that looks good so this also has to power the uh the other one the zero all the way over here which is on

**[29:50]** this line so again just copy all these parts and you might have to look at the signal strength make sure it reaches all the way boom peter redstone peter bring this up just like the rest

**[30:22]** of them and it's going to connect to this guy oops i need it one higher there we go okay let's turn the zero back off uh double check this real quick okay and yeah turn the zero back off because we were just testing it for the signal strength also get rid of this part

**[30:55]** and that should be good so now it's time to give it a final test right now we should have two machines that accurately resemble what's on the display in an 8-bit number for the top i'll type in 200 and 7. for the bottom i'll just type in 90 eight and let's check it out so two hundred and seven one one zero zero one one one one

**[31:28]** that is accurate that's two hundred and seven over here this should be 98 let's see a 64 plus a 32 that gives us a 96 plus another two 98 beautiful thanks for watching
