# Redstone Displays - LRR #9

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=mDLfUbAK9T0
- **Duration:** 25:48
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to logical Redstone reloaded if you're new to the channel or you came from the Piston extender video Welcome I'm happy to have you here to catch you up to speed this is the ninth episode in a series about building digital logic circuits with just Redstone in the previous episode we covered sequential devices like registers and counters today we're going

**[0:17]** to cover displays both pixel displays and segment displays there is a lot to talk about today so let's get started let's start with pixel displays a pixel display is just a rectangular screen full of pixels but unlike the colorful pixels you're watching this on pixels in Minecraft typically only have two states on or off you can make these displays in many different ways I've seen them done

**[0:40]** with pistons to push out or pull in the pixels or even with dispensers and snow blocks but the most common way to make them and my personal favorite is with redstone lamps using a wall of redstone lamps you can simply power the lamp you want to turn on with a redstone signal and it's a completely flat screen which is really nice the only question is how big should each pixel actually be your

**[1:02]** first thought might be to make every lamp its own pixel in Minecraft terms we would call that a one by one density display because each pixel would be one block by one block unfortunately though one by one density displays are really annoying if you try to make one yourself even for something as small as a 4x4 screen you'll notice that it's kind of difficult to make even the best designs

**[1:24]** in the community tend to use complicated techniques and a lot of them are really laggy as well so in my opinion it's better to make a two by two density display where each pixel is two blocks by two blocks or four lamps each this is a stackable module that allows you to power a 2x2 pixel and you can stack these next to each other to make a display of any size for example this is

**[1:46]** an 8 pixel by 8 pixel display it's literally just 64 copies of this module every pixel now has a dust associated with it in the back that you can use to turn that pixel on for example to turn this pixel on I can just power it right here and we see it on the screen now that we have a basic display we can do a ton of stuff with it first up let's use it to show some images let's say that

**[2:08]** you want to show three different images a smiley face a sad face and a surprised face to do this we can use a technique shown in the encoder from episode 6. remember an encoder allows you to Output a unique binary string for each input this input might give you a certain string while this other input might give you do a different string and an image on a screen is just a bunch of binary so

**[2:29]** using this technique we can control for which image we want to send to the screen I'll start by spreading out the pixel lines like this creating more space above each row then I'll create perpendicular blue lines above them as well as a glass tower to ore them all together now to store an image we can put torches above the pixel lines that make up that image I'll just stack this

**[2:50]** two more times and store all three images okay there we go flipping the first lever turns on all the Torches attached to these blue lines which I coded to show the smiley face flipping the second lever shows the sad face and flipping the third lever shows the surprised face of course by changing the positions of these torches you can store whatever images you want very cool the one thing

**[3:15]** that kinda sucks about this design is the size compared to the screen it's actually twice as tall so here's a design by my friend RT which stays the same size as the screen instead of torches this design uses Target blocks to show the image when you want to show an image these four blue glass Towers actually get turned on from underneath using this lever if there are no target

**[3:37]** blocks then the towers won't do anything they're not connected to any of the pixel lines but by placing Target blocks at the pixel locations of the image it forces the glass Towers to power those pixels and you can store as many images as you want by stacking this backwards okay I just load this with these same three images as before and as you can see we can send whatever we want to the

**[3:59]** screen beautiful next let's try plotting pixels according to an x y coordinate I'll say that the bottom left pixel has the coordinate 0 0 then for every pixel to the right X will increase by one and for every pixel up y will increase by one for example this pixel right here is two three two an X and three in y to plot a pixel with just an x y coordinate we can use something called a matrix

**[4:23]** decoder a matrix decoder takes in two numbers X and Y and outputs the corresponding point right now the input is zero zero so that's why the bottom left torch is on but if we input say four five the torch at the coordinate 0.45 gets turned on this works by using a decoder for x a decoder for y and a grid of torches to detect the intersection between them notice that

**[4:49]** every torch in this grid is being powered from two places the row with these Redstone lines and the column with glass Towers in the back now since X is currently 4 the 4 line on the decoder gets unpowered which stops powering that column and since Y is 5 the 5 line on this decoder gets turned off which stops powering that row so the torch where the fourth column and the fifth row

**[5:14]** intersect is the only torch that turns on so by hooking this up to a display we can now plot pixels according to their coordinate if you want to plot pixel 1 4 then just put a 1 here a 4 here and pixel 1 4 is now on the screen pretty cool right next let's take this one step further and plot multiple pixels onto the same display to do this we need every pixel we plot to stay on the screen so let's

**[5:39]** put an Sr latch from episode 7 onto every single Pixel like this that way whenever a pixel is activated it will turn on and stay on until we reset it and turn the pixel back off okay I put the latches on the screen and now whenever we activate a pixel it will turn on and stay on we can literally activate as many as we want and whatever we put in that pattern will stay on the

**[6:03]** screen let's go ahead and connect the Matrix decoder to this and we should be able to continuously plot pixels alright there we go The Matrix decoder is going into Sr latches and then into the display now you'll notice that the latch for 0 0 is already on and that's because technically we're inputting zero zero right now but since we have latches now it would be nice to have a button that

**[6:24]** tells the screen when to plot the point instead of the screen just plotting the point constantly okay I made a little circuit in the front that just cancels everything until the button is pressed now we can actually start plotting pixels you can put in one two and plot and it shows up on the screen then you can put in something else like maybe five six and it'll plot that as well also I wired

**[6:50]** together all the reset signals from the latches into one button right here so when you press it it sets every pixel to zero which clears the screen next let's explore what happens when we use data latches again from episode 7 instead of Sr latches this right here is a very similar setup to what we had before we still have a matrix decoder in the back but this time every pixel has a repeater

**[7:12]** lock instead of an Sr latch now all the repeater locks on the entire screen are locked by default using these comparators but when a pixel gets decoded for by The Matrix decoder it quickly unlocks and relocks again for example if you input 77 and press the button you can see that the repeater at 7 7 opens and closes and the actual data going into the back of the repeaters is

**[7:37]** all or together using these magenta glass Towers into one single lever right here whatever this lever is set to zero or one that's what's trying to go into the back of all the repeaters so let's try this out if we set the data to 1 and decode the pixel 2 3 that pixel will be set to one because it grabbed the data let's decode another pixel like four five and as you can see that gets set to one

**[8:07]** as well then if we set the data to zero and put the pixel back to 2 3 we can essentially turn that pixel off because again it just grabbed the data so we now have the ability to set any pixel to one or zero which is super cool there's just one small problem which is that we lost the ability to reset the whole screen at once technically you could set every pixel to zero one by one but that's

**[8:34]** really time consuming luckily though there's actually a really clever way to add a reset function as well and it has to do with this decoder let me show you what I mean it turns out that with a little bit of added circuitry in Orange we can force a matrix decoder to turn on all the torches at once all you have to do is physically prevent all the rows and columns from being powered with

**[8:57]** comparators right here we can force all the rows to be unpowered and with this Redstone line down here we can force all the columns to be on powered as well so now when you press this button all the Torches turn on otherwise it's still a completely normal Matrix decoder you can still decode for two three for example and it'll still work okay great but how does this give us a reset function well

**[9:21]** remember whichever repeater gets decoded for that's the repeater that grabs the data so now that we can decode for every pixel at once we can make every repeater grab the data at once putting this all together the input now looks like this we have the data the x y coordinate the plot pixel button and the plot all pixels button if you press plot pixel then the data gets sent to that specific

**[9:45]** pixel just like before but if you press plot all pixels the data gets sent to every pixel if the data is zero every pixel receives a zero and if the data is one every pixel receives a one so now our screen has four functions we can set a pixel to zero set a pixel to one set every pixel to zero and set every pixel to one beautiful next what if you want to use a display

**[10:13]** for an animation well in that case the first thing I recommend doing is swapping out all the lamps for trap doors and using my texture pack to make them look like lamps this is because trapdoors respond instantly to a redstone signal whereas Redstone lamps take two ticks to turn off and when it comes to animations it's pretty important for your screen to respond

**[10:32]** instantly now if you want to make the frames of the animation yourself then you can probably just use RT's image display from earlier just make each image its own frame and then release them one after the other each frame will get to the screen slightly after the other which is exactly what you want but what if you want to display something that isn't handmade what if the frames

**[10:50]** are being drawn by another Redstone Contraption like a line drawer in that case you might want to use something called a buffer display the idea behind a buffer display is to let the contraption draw the whole frame first and then push the frame to the screen once it's done let's say I'm the contraption drawing this Frame so I'm going to draw something like a smiley

**[11:09]** face for example okay so even though I just drew this smiley face it doesn't show up on the screen yet once you press the button the frame is sent to the screen then let's say the next frame is a bigger smiley face so I'll go ahead and draw a bigger one okay there we go and now when we press this button it updates to the next frame the way this works is with Sr latches followed

**[11:31]** by d-latches as we draw a frame it gets saved into these Sr latches which are not connected to the screen then when we press this button two things happen first all the data latches unlock and re-lock which captures the frame that we just drew and second it resets all the SR latches so that it's ready for the next frame to be drawn and you can actually achieve this with just one

**[11:53]** glass tower for every column this dust on the left is flashing the d-latch and this dust on the right is resetting the SR latch this buffer technique is super cool if you combine this with something like a line drawer or a computer you can create some pretty cool animations next I want to show you an amazing Redstone technique called pass-through which was invented by these guys right

**[12:15]** here pass-through is the idea of using multiple Matrix decoders to plot to the same screen at once when I first learned about pass-through I was blown away because I didn't even think it was possible I mean how can you pass the result of one decoder through the other without interfering with anything it just seems like a logistical nightmare but it's completely possible and here's

**[12:35]** how it works first consider this new design for a matrix decoder even though it looks quite a bit different it has the exact same functionality as before if you turn on a specific column and a row you get the intersection between them it's just that this time we're using comparators instead of torches every output has one comparator associated with it which is getting

**[12:56]** canceled on both sides it it's being canceled from the row with these repeaters and the column with these glass Towers if the glass tower for that column and the repeater for that row both turn off then the comparator is not being canceled from either side and we get an output now the question is can you pass signals through this such that they connect to the outputs without

**[13:18]** messing with anything amazingly you can and it looks like this if I power one of these four lamps the corresponding lamp shows up on the final output what we're doing here is using a comparator to put a signal through this block into this dust and into the final output but you might be wondering doesn't that just mess with the Y decoder line well no because it's being forced to have a

**[13:41]** signal strength of one which does not get picked up by the other repeaters on this line that's the key behind this technique so now if you put another Matrix decoder behind this and plug the outputs into these inputs you can decode for multiple points at the same time you can decode for the bottom right with this one and for the top left with this one they both show up on the display so

**[14:06]** yeah that's the idea behind pass-through here's an 8x8 version instead of two by two using the exact same technique the only slightly weird thing about this is that the x-coordinate is on the right this time but in any case let's go ahead and plot two three on this one and four five on this one and they both show up on the screen nice so if you happen to watch my 3D renderer video hopefully the

**[14:31]** display makes a little bit more sense now it's essentially a giant pass-through display with six layers of pass-through as well as a buffer on the front this allowed me to draw many lines at once and push the frame to the screen when it finished finally I want to briefly talk about color displays so far in this video all the displays only use two colors but what if you want to add

**[14:50]** more is an RGB display possible in Minecraft well not really but over the years I've seen some color displays that I think deserve some attention the first type of color display is called a map display using an actual Minecraft map you see the color of a pixel on a map is decided by the majority of the colors in that region so let's say that a map is looking at this 4x4 region of blocks to

**[15:12]** decide which color the pixel should be currently there's no majority because every block is a different color but if you place a red block here red becomes the majority or if you place a Blue Block blue becomes the majority so yeah these displays typically use pistons to change the majority and change the color of a pixel you can you can color display with the help of a

**[15:32]** texture pack in display created by torb every pixel has a red green and blue slice where each slice can be covered up by a certain number of trapdoors this gives you up to 64 different colors the texture pack to go along with it makes open trapdoors invisible and closed trap doors completely black this lets you control how much red green and blue is visible similar to RGB pixels in real life

**[15:54]** and finally in this display by mod punchtree each Redstone Dust signal strength has been re-textured to a separate color giving you up to 16 colors to use this one is personally my favorite color display it looks really clean and you can change which colors you want to use by just changing the texture pack now I also want to mention that any display you see in this video can be

**[16:15]** made bigger than 8x8 however it probably won't be as simple as just running stack in many cases signal strength will become an issue especially if you have glass Towers so if you need to extend a glass tower beyond the normal 8 Bits here are my two favorite techniques you can use a repeater going backwards like this and make sure to make this block a solid block or you can use two torches

**[16:37]** like this and once again make sure this block is a solid block I can't tell you how many times I've forgotten that and wondered why this specific repeater wasn't working also it's a good idea to keep your glass Towers synchronized notice that these repeaters in Gray are going to take one more tick to power than the bottom eight so I recommend adding one tick of delay to the bottom

**[16:57]** eight repeaters now when you power it they all get there at the exact same time and if you use torches you should add two ticks of delay to the bottom eight repeaters because this torch Tower takes two ticks as you can see this keeps it nice and synchronized but yeah honestly I I highly recommend sticking with an 8x8 screen unless absolutely necessary a working screen is infinitely

**[17:17]** more impressive than a big screen alright let's switch gears and talk about the world of segment displays segment displays use specialized segments instead of pixels they're typically used to show numbers or letters the most common segment display is called the seven segment display they use you guessed it seven segments to display anything from 0 to 9 as well as

**[17:38]** a through F and these are actually the only segment displays I'm going to cover in this video check out the links in the description if you want to learn about displays with other numbers of segments so to start us off let's make a circuit that goes from any number 0 to 9 to a seven segment display we'll talk about a through F later when you input three it should show three or when you input nine

**[17:59]** it should show a 9 and if you input something greater than 9 it should show nothing the first step is to figure out which value is being input because each one is going to show something different so let's use a decoder to decay code for every value from 0 to 9. if you input 3 the torch for number three will turn on then let's hook up a wire to every segment and arrange them like this above

**[18:21]** the decoder and finally let's make a glass tower for every number and encode the segments with repeaters and that's pretty much it so now if you input a 5 for example the torch for number 5 turns on which activates this Glass Tower powering the segments for five and as you can see we get a nice 5 on the display if you input an 8 instead you get an eight perfect is one of my favorite designs because

**[18:47]** it's extremely fast and you can stack them really close together horizontally but of course there are many other ways to make this here's another design that I've used quite a bit in the past this time we have a flat decoder on the top which decodes into a green line then on both of these layers the green line encodes the segments using these torches and as you can see it does the same

**[19:08]** thing just keep in mind that unlike this guy this design is completely unsynced when you input a number you'll probably get some random garbage on the output until it finishes however this design has a much more natural shape so you can stack it decently close horizontally and vertically so that's pretty cool so using many copies of these converters you can now display any number if you

**[19:30]** have three of them you can input one two three and you get 123 on the display this notation where each decimal digit is a four bit binary number actually has a special name it's called BCD which stands for binary coded decimal for example the number 347 in BCD looks like this 4 bits for three four bits for four and four bits for seven so this device is called a BCD to

**[19:58]** seven segment converter because it takes a single BCD digit and displays it on seven segments but this begs the question what if you want to convert a binary number larger than 9 into BCD in other words how could you go from a binary number like 123 to a BCD number so that you can actually display it on a seven segment display well I've actually covered this in a previous video called

**[20:21]** binary to BCD in that video I made this really cool device that converts a binary number into its BCD form for example if you input 69 in binary and go ahead and press this button you get 6 9 in BCD you can then plug that BCD into some converters and now you can see the number on a screen so yeah check out that video if you want to learn more about this device and apologies for the

**[20:46]** lower quality it's from about two years ago okay let's show some letters now as I said earlier seven segment displays can also show a through F this means that a single seven segment display can show a hex digit remember from episode 2 that in hexadecimal 10 represents a 11 represents B all the way to 15 which represents F so we can literally just add six more lines to our converter for

**[21:09]** a through F and now this is a hex to 7 segment converter and what's really cool is we don't have to add any more bits to the input four bits of binary has the exact same range as one hex digit zero zero zero zero is zero and one one one one is f and of course you can also add six more lines to the other design as well another thing you can do is hook up a signal strength to Binary converter

**[21:34]** from episode 6 and now you can display signal strength if you put in a strength of four you get four or if you put in a 12 you get C which is 12 in hexadecimal additionally if you want to display a large binary number in hack extremely straightforward you can just plug each 4-bit chunk of the number into its own converter for example let's say you wanted to display the binary number

**[21:57]** one zero zero zero one zero one one in hexadecimal this number is equal to 139 by the way I'll put the first 4-bit chunk one zero one one into the first converter and the second 4-bit chunk one zero zero zero into the second converter this gives us 8B on the display therefore this binary number or 139 is equal to 8B in HEX so in summary showing a binary number in decimal that's kind

**[22:24]** of hard first you have to convert to BCD and then convert each BCD digit into seven seg but showing a binary number in HEX that's easy just plug each four bits directly into a hex to 7 seg converter and finally I want to show you some of the most interesting seven segment displays from the community this right here is a seven segment counter designed by mizuma games every time this Observer

**[22:45]** receives an update the display counts up by one and whenever it goes from 9 to 0 it gives an output on the other side which means that if you stack these next to each other you now have a multi-digit counter this is super useful especially for keeping score in a redstone game I used it for my Flappy Bird game and also in Dance Dance Revolution and now the last family of devices in this video and

**[23:08]** trust me when I say I save the best for last this is an incredible piece of technology designed by pausi and amino in essence it's a hex to 7 segment converter with a signal strength input so you can put in a three in the back and you get a three on the screen however the number is way smaller than the one on my design but why is that isn't the size of this thing just gonna

**[23:31]** make the numbers spread out anyways when it Stacks well if you take this entire module and paste it so that there's just one block of space between the numbers both modules still work you can put a 3 here and a 7 here and they'll both show up on the screen and not only horizontally but vertically too making this display incredibly tiny also notice that the numbers are kind of fancy these

**[23:58]** don't really look like segments anymore they look like they were drawn on by hand this is because there are actually no segments each display is a tiny pixel display so the way that every number and letter looks has been customized by the creators also here's a slightly smaller design but this one will only show zero through nine anything above 9 will just show up blank and it gets even smaller

**[24:21]** if you don't care about it being fully lamps as well this tiny thing can still decode for any number from zero to nine the numbers are completely out of order this time but it's still really impressive so how in the world do these work well if you look at them you'll see that they all use a repeating diagonal pattern of comparators and barrels as it turns out by changing the number of

**[24:43]** items in these barrels you can get it to produce many many different patterns so the creators of this literally brute forced millions of different Barrel combinations using software which allowed them to find the exact combination that produces the patterns they want that's how the creators were not only able to go from 0 to F but customize how each one looks as well so

**[25:04]** yeah I thought I'd show you this because it's both the smallest and nicest looking display I've ever seen and the technology behind it is just fascinating there's also a Discord server centered around this type of Technology if you're interested in learning more I'll put it in the description next episode will be the finale I'll be putting everything together and making some Redstone games

**[25:22]** from scratch I'll see you there if you enjoyed this video subscribe and check out my patreon page in the description I also have a redstone Discord server so come join us if that sounds interesting I hope you learned something I hope you enjoyed peace out guys thank you [Music]
