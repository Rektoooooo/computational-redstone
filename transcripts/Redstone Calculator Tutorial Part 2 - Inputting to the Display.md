# Redstone Calculator Tutorial Part 2 - Inputting to the Display

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=2SMJFs4Rm-0
- **Duration:** 44:52
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** all right this is part two of the redstone calculator tutorial um originally i said it's not going to be a block by block tutorial but i'm kind of changing my mind a little bit just because i want to show especially when it comes to input i want to show how the numbers show up on the screen and all that stuff so today we're just going to look at how this works

**[0:19]** and how the numbers are shown on the on the first and second rows of the screen and if you haven't seen part one yet you should that goes over the two things you need to know before starting this which is just world edit and binary i'm just going to assume you already know those two things at this point so we're going to start with how this works uh what it's going to do

**[0:38]** is it's an encoder what encoder does is it takes any time you select one single button which is one input it it codes for a line of multiple inputs because obviously if you have seven you have multiple lamps turning on at once so you want these four lines to be resembling your 1 2 4 and 8 bits and you want each button to show up with the corresponding number so i'm going to show you how to make a

**[1:08]** basic encoder with torches and then we're going to apply it to this so what's going to happen is you're going to code for it using torches that are connected to this block because as the line turns off every torch that's connected to these lines also turns on when the line goes off because since they're already powered it's inverted so it doesn't do anything right now

**[1:28]** until you press the button and then it codes for it so if this is one and this is our one bit over here we're going to code one to just show us one so one to one now whenever i press one our output gives us one and i'm also going to make these levers just so i can make it more permanent as i go over there now two is also just one line so i'm gonna code the two line

**[2:00]** for two and then three is where it gets interesting because there's no three bit you need to use a two and a one so we're gonna code for a two and a one and now when we hit three we get a three so that's how an encoder works with that basic idea down all you need to do is if you want to use a keypad system like i have you just need to make it so that each button

**[2:25]** has its own corresponding line and each line is coded with torches to light up uh its bcd digit when it gets when it gets activated all right so we're finally going to start with the actual calculator um so i'm going to start with the platform you can use slash up 0 to give you a glass block wherever you're standing i'm just going to set it to an iron block you can obviously use whatever blocks

**[2:48]** you want i'll just make a platform like i have on the other one and this platform will have walls on it like this so we'll do this set iron block stack four up i think you needed at least four uh actually the one i had was only yeah the one i had was was four tall like this so we'll do that and then you can make your keypad and you can make your uh input switch

**[3:19]** you can make your clear button and then you can make your four buttons for the four different types of operations and you're going to want to leave some space on the side too so now we basically just need to copy the input to bcd thing so i'm just gonna and as you know they're gonna be powered by default so the easiest way to do that is to just have a torch behind every button

**[3:43]** so that way you know if you have a line right here and you want to connect to this torch it's already powered you're good to go um so just to make space we're going to have these three top ones connect to the uh each torch is going to power the block above it these ones are going to take signal like this and then this one's going to take signal like this this middle one is going to take signal

**[4:11]** normally it's gonna just go out like that these side ones are gonna be brought out from the side side middle and then the um this middle one here is actually going to be brought out like that i'll deal with the one on the bottom in a second so that's going to be brought out like that and actually we can make these go like this we don't have to be we can we can make it a little bit more compact

**[4:46]** like that and so what are we missing we're missing this torch and what we can do for that is we can have it go out like this block it off from here and then have this be a slab so that it can flow under it and meet up with this guy like that so we're gonna do the exact same thing on this side this guy's gonna go like this we're gonna put a slab here lock it off

**[5:16]** and bring it under like this so now we have one through nine if you want to check them you can always just put lamps on them and as you press each button the lamp that corresponds to it should turn off and okay so i'm pretty sure that's all working and then the zero the zero down here also needs to have a a way of getting it so what i'm gonna do for that is i'm gonna

**[5:44]** take it in kind of a weird way i'm gonna like because i'm kind of out of room down there and i spent a lot of time trying to try to do this but what you're going to want to do is just something like this where you have um where you have a redstone that's activated by it and make sure it's not powering that one and put a slab here put a torch here and then this is your signal

**[6:17]** so it's really important so there's a lot of different ways to do the zero one and honestly there's a lot of different ways to do this in general but what you want to make sure you keep consistent is the timing so as each as you add a torch a torch takes one uh redstone tick to to power on or power off i'm pretty sure so you need to have every line be the same whether that's two ticks or one tick

**[6:38]** so right now all of our lines are one tick because every line only requires one torch obviously redstone is instant so that doesn't count but even this this is also just one torch and the rest is redstone so all of these lines are activated within one tick and it's all synchronized it's important to have them synchronized that's what i'm trying to say you want to bring these up by two first

**[7:00]** and i'll show you why in just a second so you're gonna bring these up like this just two blocks and you're gonna bring these down two blocks like this now you can bring these out and honestly don't worry about the zero right now we'll deal with that later now you can select this and bring it out

**[7:31]** so we'll just do like eight i don't think we need very much yeah these are still powered um now we need to put the output lines underneath them so as i said before you only need four because we're doing it we're converting it to bcd which is just the one two four and eight bits um so you're gonna just wanna do something like this make four lines i don't know why i made this

**[8:02]** just make four lines like this and then you're also going to want a fifth line this is going to be called the signal bit and it's just basically going to activate no matter what number we press and that's for two reasons one it's going to activate when a zero is pressed so that the machine knows we pressed a zero because if you think about it zero means none of these four lines is lit up so

**[8:28]** how does the machine know that we pressed a zero well that's what the signal bit is for um and so you're gonna copy this and you're gonna put it below um this second row and the third row so make let's just copy this again so let's do let's let's build out from here choose a reference point copy and paste and paste okay so now we have to connect

**[9:01]** these three rows because each column is going to resemble each bit so just go up like this and make kind of a slap tower here like this hit connect on here one higher and then redstone oops repeater fill this all in with redstone and then

**[9:31]** connect it to the other two lines like this so now wherever this any of these three lines get powered um the entire thing should be powered so whether it's from down here they all reach up to this block so you're gonna do the same thing for the other four lines take this guy expand one stack three and now we need to code for whoops stack four actually now we need to code for the digits so

**[10:02]** i'm gonna label them to make it easier so just put lamps on them like this and get a sign and this is going to be the eight this is going to be four two one and signal so let's start with signal because it's the easiest so every single line is going to power the signal bit including the zero so what you're gonna wanna do is expand

**[10:33]** these by one put torches here and then also take the zero line and bring him down under like this and then put a block here and a torch

**[11:04]** okay signal bit's done so the way to check that is if you press any number now on the entire keypad the signal bit should light up now we need to code for each digit so let's start with one right here so one is this line and all we needed to power is the one so done two is this middle top line and all it needs to power is two three is this line and it just needs to power

**[11:32]** the one and the two and you're going to repeat this for all the rest of the numbers so four come down here one two four it's gonna be this one five we need four and a one and you get the idea so just copy this pattern for the rest of the digits all right so now in order to display the top number and the bottom number we actually have to use this device which is at the end of the line here

**[12:04]** the reason i had at the end of the line is because it's used to display the answer but it's also used to display the top two numbers so we're gonna have to build it right now uh all it does is it converts the bcd digits that we just coded for into the actual display itself in a seven segment display so like when you had an eight and one this will make it show a nine or if you had a

**[12:24]** four and a one it will show you a five so it's just another version of a decoder i'm really proud of it because of how compact i got it to be but i'm basically gonna i can't really do it for memory that well so i'm gonna try to just look at it as a reference right here and build it as best i can so i know that each segment uh each horizontal segment has three blocks on it like that with

**[12:49]** three more going down like this and they have repeaters and they have an output that goes like this so as soon as it gets powered it's in charge of that segment only same thing up here but we're actually going to put a slab here and then we're going to put another slab there a block there a block there and a block

**[13:19]** there and we're gonna put redstone on top of all those and these side ones you put one in the middle and then you put two like this and you make it into a torch tower and then you put another torch on the side like this and that is where your output's going to be so it's the exact same thing on this side just flipped so we're going to do a torch tower and

**[13:51]** redstone like this like this and maybe make all these line up because why not and then same thing over here torch tower and one of these with a torch same thing here

**[14:26]** and let's see actually how i did that one okay so so far we have it like this i might need to change it in just a second yep i was right it needs to be changed a little bit uh what you're going to want to do is put this down like this three more and then have it hop over like this and then put a block here to block that off

**[14:57]** and then you can bring all of these out to uh line up with it so when you're done you should have four on the bottom and three here and again if you want to test them you just power each one individually and they all should be coded for a specific segment so this one is the side segment and so on now we're going to want to do is stack this row right here out by 20.

**[15:23]** oh and if you get visual bugs like this don't worry they they go away and they don't do anything so now we need to build the input lines that are going to code for the segments themselves so you're going to start with a block here build out to here you're going to do the same thing down here and you're actually going to put a torch on the side of it like this this is

**[15:50]** actually just to conserve some space you're gonna put another one here like that and so what i've done is i've made a a downward torch tower this just makes it so that when this gets powered this line under here also gets powered so you can think of them as connected as long as you start on the top and then we're just gonna need to stack this thing so we're gonna stack it out nine more times

**[16:15]** i'm gonna do this really carefully go like this and like this stack nine take this guy stack nine and take this guy and stack nine that is not what i wanted to do expand one and then stack nine so now all of these lines are doing the same thing as before

**[16:46]** so at this point we need the btd that's coming in to decode into a specific digit because each of these lines is going to resemble specific digits so if this one resembles seven then that means when it's when it gets depowered all the torches attached to it are going to code for the segments of seven so but we need to like i said we need to decode the bcd first which is the opposite of an encoder

**[17:12]** what a decoder does it takes multiple lines and if you get a certain combination of lines it will give you one output each and that's exactly what we want because we have different combinations of bcd coming in if we have a seven coming in which is four two and one then as you can see the only line that gets depowered is right here and as you can see this line is coded for a seven

**[17:37]** and so we get a seven so i'm honestly just gonna go one line at a time um this first one well we can start with these these four blocks here and then they all have a slab connected to them whoops and they all have repeaters this first line out here goes all the way forward with a repeater at the end and two torches attached to it at the

**[18:08]** end so we're gonna do another slab one repeater bring this all the way out two torches and one repeater at the end like this okay the next line is going to be

**[18:39]** three repeaters four torches and two more repeaters so we're gonna go like this uh two three three repeaters and then what four torches yeah

**[19:15]** we're just starting on the next ones out here one two three four and then two more repeaters and these have to be slabs right here uh slap slap okay redstone dust right here

**[19:47]** all right the third line we have one repeater two torches two repeaters two torches so it's repeating that actually makes perfect sense because as you count up the two line um has that pattern so uh start with start with one repeater yeah this is gonna be the most annoying one be honest two torches which i think are here and

**[20:18]** here yep and then redstone two more repeaters which are probably yeah right next to it which means it's going to be right here so two more repeaters like this and like this oh we don't need to rest on block our redstone dust there and then

**[20:50]** two more torches and two more repeaters so like this two torches redstone dust and two more repeaters uh that is not i don't want to do it all two more repeaters all right and then this last one is

**[21:21]** another pattern this is gonna go out by uh alternating by one so it's gonna be uh dust torch repeater block dust porch repeater block dust torch repeater block yeah pretty sure that just yeah should be good so we start with uh dusts dust torch

**[21:52]** repeater block and since we know how to use world edit we can go like this expand one stack like probably three times yeah nearly perfect we just need one more dust and one more let's see does it end in a torch yeah it ends in a torch perfect so zero is already powered it's it's see how it's the only one that's depowered

**[22:23]** that's because when nothing's in it's gonna display zero because zero is in so we need to code for the zero bit so it's going to be every segment except for the middle and which line is the middle segment this line right here is the middle segment so we need all the other lines to code for that oh and another thing signal strength we need to put some repeaters down here

**[22:50]** as well so i'm going to put some under this block and some under here as well and we get a zero perfect so we put a one in and now you can see that the only one line that gets c powered is the one so we need to have this line decode for the one so the one is this segment and this segment which are the two ones on the outside so that makes it really easy you just

**[23:21]** put one here and here and now it's showing a one so if you turn this back off and it goes back to coding for a zero it's showing the zero so yeah you're going to repeat the same thing for all 10 digits so now it's time to copy this guy and paste them six times for the a and b numbers um it's not really a great spot to do this but i'll just choose this corner

**[23:53]** and i will also choose this corner and remember you got to pick a reference point so i will just choose uh standing on the middle segment as my reference point so slash copy so our reference point was right in the middle with one out like this slash paste and there you go so now we have a decoder all set for the first digit and you're

**[24:25]** going to do the exact same thing over here slash paste one two three is the space in between them and then like that and so paste if you want to you can copy this and just paste it one down but i'm feeling lazy so i'm just going to do this and i think this we should have enough

**[24:56]** room here right yeah man i love how compact this thing is and it's seriously as close as it gets there is one block of space in between these twos so we're gonna go down here line these up like this paste line these up paste destroy all these and then you can just fill in the lamps with world edit

**[25:30]** redstone lamp and let's not worry about this right now okay another way to check if you get everything right is each of these bcd sections should be right next to each other so it should look like one long line so now we're going to build uh shift registers for the digits and what i mean by that is we're going to have to keep the memory of the digits as we as we type them in um so as you type a

**[26:00]** one you're gonna want it to show up right here as you press another number you're gonna want that one to get shifted over and you want that next number to be displayed so and i know this looks weird but it's just a glitch from world edit they just need to be updated so what we're going to do for that is we're going to pull all these out and we're going to line them up

**[26:21]** vertically so i'm going to make this guy up here i'm gonna make this guy down here uh make this guy go down even further yeah something like that actually just do this yeah just do this make it like that and this guy can go nicely under and this guy will have to go

**[26:54]** on top like this cover it all with redstone and put blocks like this right no one lower you're going to want to build this redstone out one more then you can put blocks like this and then you need to put repeaters

**[27:25]** in a tower connecting to these so what we're going to use to ship these over is something called repeater locking if you have a repeater and you have another repeater into the side of it and you power it the repeater gets locked with its current state so since this got locked with nothing in it i can't power this it doesn't get powered and at the same time if you if it's on

**[27:47]** and you power it now it's locked now if i get rid of this torch it's still powered so it's a form of memory it's it's one bit memory um so we're going to copy this and put it on the other five areas uh we'll do something like this maybe expand four expand five down stack two did i do it right i think i

**[28:18]** did it right that's really surprising once you've somehow figured out how to copy those you need to copy uh or you need to connect these uh you need to connect these lines so uh it's gonna be like that then of course this is gonna be connected to boom boom stack three up and there we go now the mechanism to

**[28:49]** lock them also has to be connected to everything so we're gonna take this stack three down uh copy it bring it over here bring it over here too and then we need to connect them all so i'm gonna like stack maybe 12 or something nope not long enough that is way too long holy

**[29:20]** stack uh 15 good enough and this is going to have to be a block because 15 is the max uh take this guy stack three down and now we have a way of locking everything uh we still need to connect it into just

**[29:51]** one single line though so what i'm gonna do is since this is already 15 long actually let me double check that does this go all the way no it doesn't look at that so we need to have another block right here and we need to have all of these be uh repeaters so take this sec three up and you're gonna want to make a torch tower again that is just not i'm all over the place

**[30:25]** take slabs put them like this so okay this device is going to do all the magic with the shifting so what it's going to do is it's going to keep it powered until i send a signal bit remember we made that signal bit and the signal bit is going to unpower it for just enough time so that everything gets shifted over by only one

**[30:55]** uh so we're gonna go like this this gets a torch here and this is this is one tick and this is two ticks and you go like this and you go like this and now just to test it let's get a button and this should be our shifter working so right now in its default date everything is locked in place you don't want to just be shifting on its own now if we send in

**[31:29]** uh what is this bottom one this bottom one is an eight yeah so it goes one two four eight starting from the top so let's just send in a one right if we do that and we don't shift it at all we get nothing but if we send in the one and we shift it now our first digit is a one and really still going to glitch i don't understand that

**[32:03]** yeah i guess it's just weird you might have to like do something like this where you you paste a bunch of blocks to to update all the lamps yeah that worked look at that i'm so smart so now if we want to shift it over again let's say this time we typed in a zero so nothing is right here we shift it over again and we get a 10. so now we just virtually typed in a 10.

**[32:33]** oh and the clearing mechanism let's build that real quick to clear it the easiest way i found to do it is just put a piston here put a uh a torch here and put a button here maybe does it have to be one block out i'm guessing it has to be like that yep there you go so that will clear it because what it will do it will unlock all the repeaters for long enough to everything

**[33:05]** for everything to just flow out of it by the time it's done so bring these vertical lines and bring them back to uh let's see yeah just bring them back to uh being horizontal like this whoops

**[33:36]** last one make sure they don't interfere with each other here there we go a redstone all over them because we just have to move it out to line up with these now all right so i lined them up and i connected them all you're gonna end up with an extra one here for the signal bit and the signal bit goes right into the thing that i was playing with earlier to shift it over

**[34:06]** and at this point you're ready to start typing in numbers but you probably will have to make some adjustments to the timing um i'm actually not sure so i'll just test it live if we try to type one wow it just works that's actually insane all right let's type zero that's it so obviously you can only type

**[34:38]** into the top number right now we do need to copy this whole thing and put it down here so that's what i'll do right now don't worry about connecting these wires uh right now just copy um everything including this mechanism okay so i copied it down to the b number and it should look something like this i just cut it off at the repeaters here now what you want to do is bring these lines

**[35:02]** down so that they line up like here ish and i'll show you why okay so here's what i've done these repeaters power this block and the redstone below it so they're going to effectively split this line and kind of copy it to both a and b now obviously you don't want to type on both a and b at the same time so we're going to use that lever to control for which one is actually allowed to go through um

**[35:30]** so just take output from this lever somehow i think the torch is right here yeah the torch is right there so maybe grab it from like here and block this off now that doesn't work just grab it from here and bring it down like this yeah that works

**[36:02]** and then you're gonna sneak this guy around it doesn't really matter where you put it uh honestly i might just save space and put it above the signal bit line so why don't we do that go up like this go like this and just right on top of this guy yeah i don't see an issue with that

**[36:32]** so bring this all the way out and you can start building the redstone for it one two three four five six seven eight nine ten eleven twelve thirteen fourteen uh so we need something three four five six seven eight nine ten eleven and we can just cop the redstone locations for this bring this guy all the way out and then start copying these so stack one up

**[37:11]** so remember this is our lever and if we want it to let a in when it's pointing up then that's what we have to let it do right now because it's pointing up right now which means that this is powered so in other words when this is powered we want only the a1 to go in um so that means we have to cancel b all right so to cancel it we're going to use a little comparator trick

**[37:36]** so on any of these rows put a bunch of comparators all on subtract mode and then put blocks in between them all with redstone like this go underneath put redstone repeaters uh yeah and then put

**[38:09]** actually you can just do this just bring these out by another block like this block all these off and then bring it down boom boom boom bring them all down connect them all and then so as of right now it's just sending signal

**[38:41]** through as normal but when we power this assuming it actually gets to all the repeaters whatever tries to get through here is blocked so that's perfect with what we're going for so what do we say when this is powered we want b to be blocked so this is perfect if this is powered we'll just connect it right here and

**[39:12]** i think we're gonna run out of uh yeah we're gonna run out of signal strength so you can just do something funky like this and make sure it reaches and it does so that's perfect so now we need to do the exact same thing but for the inverse we need it so that when this line is off a gets cancelled so instead of going diagonal here you can build these up with slab towers

**[39:43]** and then make it go straight and then on the straight part have uh have another comparator cancel thingy i think i'm gonna do that alright so that's what i did and now when this line is off we want it to cancel a so we're going to do almost the exact same thing make some comparators put blocks in between them oops redstone on top repeaters underneath

**[40:15]** with redstone block these off bring it down by one and connect them now this line has to be powered again when this is off so when this is off this torch is going to be on so i can use this as our uh as our power

**[40:46]** and i doubt that's going to be enough signal strength so we'll just put a repeater here so now no matter what one of these is being canceled if you look right now b is being cancelled because the redstone in between the comparators is on if we flip the lever down then b is being let through and a is being cancelled this is perfect now we can type on whatever one we want if we select b we can type

**[41:19]** one two three and if we're on a we can type there nine okay so the last thing is the clear function and i'm going to use this button for the clear function i'll put up signs soon to make it less confusing but um again you can just bring it out like this if you want to save space bring this down onto the same level that

**[41:50]** the original bcd digits were so like this now we can go like this and like this and then we can just copy this line so take this entire line something like that and just

**[42:24]** expand one stack one to bring it out and this is just going to activate the uh the clear button from earlier so these this button and this button make sure to have it clear both uh so just bring it around let's power it so we can test uh the signal strength as we go so we're gonna need one right here bring it up to about

**[42:56]** here yeah bring this guy up we're just gonna this is just lining up the the thingies so make them on the same level bring them out like this we don't need a button anymore

**[43:27]** and continue to bring power to it so that's good and then we can just have this split off right here with a slap tower and make it go up like this and do

**[43:57]** this guy that's not going to reach is it nope so we need one right here okay and remember we powered it because we were testing so let's undo that and now we should have a clear function so if we type in 37. type something in on the bottom two

**[44:27]** let's just do 84 80 87 clear nice all right so that wraps it up for today next time we're going to go over how to uh convert these bcd into the two binary numbers that you actually need to do math thanks for watching
