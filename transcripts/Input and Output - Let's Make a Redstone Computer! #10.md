# Input and Output - Let's Make a Redstone Computer! #10

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=wpYU6Zvemck
- **Duration:** 16:22
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer in the last episode we finished the main part of the computer and the instruction set but even with all this hardware and software everything is still very contained the computer is basically just a box that changes its memory so today we're going to talk about input and output I hope you enjoy just like everything else in

**[0:18]** this series input and output introduces a ton of Freedom there are unlimited ways to connect a computer to the outside world but even with all this Freedom most approaches can fit into two main categories port-based IO and memory mapped IO let's talk about port-based IO first this approach also known as isolated IO is where you use ports to talk to external devices a port is

**[0:40]** basically just another register and you can think of it as separate from the main CPU in general you can have as many ports as you want but to keep things simple for this example let's say you have four ports now if you want to send some data to the outside world just write it to a port you can write a s to Port 1 or a three to Port two whatever you want then the devices on the outside

**[1:01]** can read the ports to access the data for example maybe one of your devices is a number display in that case you could just have it read Port one and display the seven and if a device wants to send data to the CPU like with the controller just do the reverse have the device write the data to a port and now the CPU can read it this approach is nice because the ports are a physical

**[1:21]** intermediate layer between the CPU and the devices the CPU can see the ports but it can't talk to the devices directly and the devices can see the ports ports but can't talk to the CPU directly but the downside of this approach is that you need extra instructions to talk to the ports for example if we added ports to our computer we would probably need at least one more instruction maybe an

**[1:41]** instruction called Port that takes in a register a port address and a bit to signify if you're loading from the port or storing to the port another idea is to have two instructions Port load and port store this works too the point is since ports are a separate piece of Hardware the instruction set needs separate instructions to talk to them or at the very least a separate argument

**[2:02]** within an existing instruction now let's talk about the other category memory mapped IO the idea behind memory mapping is to use the memory already in the CPU to directly talk to devices for example let's say you have a number display specifically it takes in an 8bit number and shows it on these three digits to connect this to the CPU using memory mapping you can take an address from

**[2:23]** data memory like address 255 and directly plug it in whatever is at that address will now show up on the this display for example if you store a 13 to address to 55 using this program the device shows 13 we've basically hijack this address as another example let's say you have an 8x8 screen it takes in any 8 by8 pattern in the back and shows it on these pixels you could hook this

**[2:47]** up to the computer by taking the last eight addresses of data memory 248 to 255 and plugging them in each column of the screen is now showing the data from each address for example if you store 1 through through eight using this program you can literally see the data or if you store these numbers using this program you'll get a smiley face memory mapping is nice because you don't need to change

**[3:10]** the instruction set whatsoever assuming the devices are directly connected to data memory you can just use load and store but the downside is that it takes up space in memory in this case with the screen these eight addresses are essentially reserved you can't use them for anything other than the screen because if you do it'll mess up what's on the screen so which strategy should

**[3:29]** we use should we create ports should we use memory mapping or should we do something else well when I made this computer the first time I thought about this a lot and I eventually decided to use memory mapping so that's what we're going to make in this series if you're making your own computer this might not be the best choice for you make sure to consider ports as well because that

**[3:47]** might be better for your situation but yeah for our computer we're going to create a memory mapped system specifically we're going to reserve the last 16 addresses of data memory 240 to 255 for input and output one cool thing about having 16 is that you can easily access all of them using offsets remember from last episode that the offset value for loads and stores is ne8

**[4:08]** to 7 so if you use 248 as a pointer then offset 8 will reach 240 all the way to offset 7 reaches 255 then in terms of devices we're going to add five a controller a random number generator a number display a character display and a giant 32x32 screen I just picked these devices because they seemed useful for making games to connect these devices to the computer

**[4:32]** we need to create a protocol or a system of rules so that everything knows how to talk to each other the protocol is something that you as the designer need to come up with there's really no right or wrong way to make a protocol all that matters is that it makes sense to you for our protocol we're going to keep track of it with another spreadsheet There are 16 rows one for each address

**[4:52]** and they're colorcoded according to the devices this column shows the devices and this column shows the address then there's a column called functionality which I need to explain as I've described memory mapping so far the CPU can both store to an address and load from an address as normal but in reality this is pretty difficult to wire so we're actually going to make each

**[5:12]** address either store only where the CPU can only output data to it or load only where the CPU can only read the data as input and so that's what this column is for it'll just tell you which addresses are store only and which are load only then there's the name which is pretty self-explanatory there's a holds column to describe what this address is supposed to hold and then the last two

**[5:34]** columns describe what happens on a store and what happens on a load if this doesn't all make sense right now I think it'll be a little more clear when we start to fill it in so first let's make the controller since this computer is meant for games let's make the controller have a d-pad for up left down and right and four buttons for a b start and select I'll combine these signals

**[5:56]** into an 8bit wire 8 Bits is the perfect amount for just one address so let's Reserve address 255 for the controller and I'll just plug these eight bits directly into that address so now if you load from 255 the eight bits you get signify which things on the controller are being pressed if you load and get this string for example then you know that up and left are being pressed on

**[6:19]** the spreadsheet let's label address 255 as load only the name is controller input and it holds the controller info and on a load it simply loads that controller info it doesn't do anything on a store because it's load only if you try to store to it that store will go nowhere one problem with this though is that a button press is very short meaning when you load it can be

**[6:42]** difficult to actually capture it so I'm going to plug these four buttons into some Sr latches before they reach the address that way when you press a button it stays on once there's a load from 255 this wire will reset the latches this makes it much easier to capture button presses from the player trust me you'll have a very hard time without it next let's add a random number generator I

**[7:03]** chose to add this because Randomness is a huge part of making games in Tetris you want a random piece in snake you want a random Apple you get the idea in Minecraft one of the easiest ways to generate Randomness is with a binary randomizer this circuit will give a random one or zero when I press this button it's a 50/50 chance so if you have eight of them it'll create a random

**[7:24]** 8bit number however these randomizers use droppers and Hoppers which are usually fine but in the next episode we're going to use a special tool to speed up the game and that tool does not support these blocks so I'm going to use this circuit to create Randomness Instead This is called a linear feedback shift register it's 8 Bits tall so when I press this button a random 8bit number

**[7:45]** is generated the details of this circuit are not important for this video but the idea is that using a shift register and some exor gates you can generate decently good Randomness and those components are easily created with your basic dust repeaters and comparators no special blocks required so let's connect this circuit directly to address 254 just like the controller on address 255

**[8:06]** now when you load from 254 this wire will generate a random number and you'll receive it on the load so on the spreadsheet address 254 is load only again the name is RNG it holds a random 8bit number and on a load it loads that random 8bit number next up the number display this is similar to the device I was showing earlier it takes in any 8bit number and displays it but it also has

**[8:30]** another input to switch between sign mode and unsign mode for example if you input this and it's on unsigned mode it'll show 203 but if it's on signed mode it'll interpret it using tw's complement and show- 53 this device also has a switch to clear the number when you flick this lever it forces all the lamps to be off so I'm going to reserve these four addresses for the number

**[8:52]** display 250 to 253 and all four of them will be store only the CPU can store data to them but can't load the data back address 250 will be for storing the number you want to show and therefore the contents of address 250 will be directly connected to the display for example if you store a 7 to address 250 the display will show s now not all programs will need to use this display

**[9:16]** sometimes it's just better to have it turned off so I'm going to use address 251 as a way to turn off the number display if you store anything to address 251 it will detect that store and turn off the display notice that the holds column for this address is empty because the contents don't matter I'm just using this address for the store signal similarly I'm going to use the store

**[9:37]** signal of address 252 and 253 to switch between sign mode and unsign mode if you store anything to 252 it'll switch to sign mode and if you store anything to 253 it'll switch to unsign mode here's an example program to hopefully make this more clear it starts by storing a 200 to address 250 so the display shows 200 then it increments the 200 and stores to 250 again so the display

**[10:02]** updates to 201 then there's a store to 252 which changes it to sign mode so the display updates to 55 another store to 253 which changes it back to unsign mode a store to 251 which clears the display and then an increment and another storage to 250 so it turns back on and shows 202 okay but this is an annoying program to read right you basically have to memorize the protocol to understand

**[10:28]** what's going on so I'm going to add something called definitions to the assembler that way the programmer can make things more clear a definition is just a way to represent a number with a word in my Assembly Language if you say Define apple 3 then every time you write Apple it'll be replaced with a three so to clean this up let's define the word base pointer as 248 and let's define the

**[10:50]** names of the four ports as the four offsets now when you put these definitions into the program it's much easier to read and it assembles to the exact same thing next is the character display in a typical character display the characters show up one by one as you type them and that's fine for most things but when it comes to games it would be nice to write a message

**[11:09]** instantaneously so this character display is special when you send characters to it they don't get written to the screen instead they get written to a secret buffer behind the screen which the player can't see then when you want to display it you can press this button to copy the buffer to the screen making the entire message appear at once for example let's write the message

**[11:29]** subscribe as you can see it's not on the screen it's in the buffer it's only visible once you press this button to push the buffer now there's also a button to clear the buffer so if you want to display a new message you can do the following clear the buffer write the new message and push the buffer again the screen will immediately update to the new message and if you ever want to

**[11:48]** clear the display completely just clear the buffer and push it on the spreadsheet there will be three addresses for the character display 247 to 249 and they're all store only address 247 will hold the 8bit code for the character and on a store it'll write the character to the buffer now the types of characters you can write depends on what character set you're

**[12:09]** using for our computer I just made this simple character set with 30 characters you can use a different character set if you're making your own computer and to make programming easier I made some inbuilt definitions for them in the assembler if you type A Single Character and wrap it in quotes it'll automatically assemble to that character code ldi R1 quote a will put the code

**[12:28]** for a into register one then address 248 will be for pushing the buffer and address 249 will be for clearing the buffer let's go ahead and make a program to write something I'll write the message hello First grab 247 for the pointer then load H into register one and store it do the same thing for e l l and O and then store to 248 to push the buffer last but not least let's add the

**[12:54]** screen this screen has an x coordinate a y-coordinate a draw pixel button and a clear pixel button and just like the character display the draws and clears are done in a buffer not the actual screen for example if you input 2 3 and press draw it'll turn on that pixel at that coordinate in the buffer and then just like before there's a signal to push the buffer and a signal to clear

**[13:16]** the buffer if you push it right now you'll see the pixel we wrote at 23 then if you clear the buffer and push it again the screen gets cleared so the screen will Reserve seven memory addresses 240 to4 46 and this time they're not all store only I'll get to that in a second addresses 240 and 241 are to hold an x coordinate and a y-coordinate and since the coordinates

**[13:39]** are five bits each only the bottom five bits will be plugged in then address 242 will use the right signal to draw a pixel in the buffer and address 243 will use the right signal to clear a pixel in the buffer then address 245 will push the buffer and address 246 will clear the buffer let's look at a quick example Le this program stores two for x and three for Y into the coordinates then it

**[14:04]** stores to draw pixel which will draw the pixel at 2 three in the buffer then it pushes the buffer then it updates y to four and draws that pixel then it pushes the buffer again and finally it clears the buffer and pushes it again the only other address 244 you'll notice is load only that's because it's an input we're going to take the pixel at these coordinates from the screen buffer and

**[14:29]** and plug it back into the bottom bit of this address for example if these are the current coordinates and the buffer looks like this then when you load address 244 the bottom bit will be on it might seem weird to do this but reading pixel values is super useful especially when making games if you're making Tetris for example it's nice to read the pixels underneath the piece because if

**[14:50]** they're on the piece hit the ground another way to think about this is that the screen buffer has now become another piece of memory for the computer you can write data to it it or read from it so what makes it different from any other piece of memory and with that the protocol is done and all the devices are hooked up I know I went over a lot in this video but I want to stress once

**[15:10]** again that this protocol is just how I personally designed it there are many other ways to do this and on top of that there are many different devices and features you could potentially add you could add a Sprite drawer to the screen you could add a keyboard you could even connect another computer why not as long as the protocol makes sense to you and the devices know how to use it you're

**[15:28]** good to go our computer is just one example of a working system if you want more examples then check out the links in the description especially the top link for brilliant the sponsor of this video brilliant is a platform to learn all things math data analysis programming and AI just like Redstone they make learning fun the lessons are filled with Hands-On activities which

**[15:46]** are both more engaging and more beneficial than just watching a video whether you're a student or someone who just wants to learn in their free time brilliant makes it easy the lessons are available 24/7 recently I did a lesson on a case study for Airbnb and it actually gave me a lot more insight for how to visualize real data sets to try everything brilliant has to offer for

**[16:04]** free for a full 30 days visit brilliant.org slmap wings or scan the QR code on screen or you can click the link in the description you'll also get 20% off an annual premium subscription
