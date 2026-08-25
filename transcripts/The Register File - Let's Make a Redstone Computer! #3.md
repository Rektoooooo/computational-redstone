# The Register File - Let's Make a Redstone Computer! #3

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=LUQZR8i_t-0
- **Duration:** 14:09
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer in the previous episode we created the ALU a device to perform operations on numbers today we're going to dive into the world of memory and build a fully working dual read register file I hope you enjoy but first let's get more specific about which Alou design we're going to use in the last episode I showed you three main

**[0:19]** designs for an Alou a simple design where you just allow one output at a time and a more complicated design with two versions this one is for a ripple carry adder and this one is for a carry cancel Adder for our computer we're going to use this last one the carry cancel lder design I like this one the best because the inputs are vertical and it's pretty small going to a diagram

**[0:37]** form this is our computer so far all we have is the ALU D1 and D2 are the two 8bit inputs which I refer to as a and b in the last episode the setting input is one of these 11 operations that our ALU can do and the output is the 8bit result remember this is a combinational component because once you put in the inputs the output is already predetermined you could even make a

**[0:59]** truth table with every possible combination but it would be thousands of lines long so an ALU can definitely do a lot on its own but it's still pretty limited the only Expressions it can evaluate are ones that have two numbers like 5 + 6 or 2X or 3 what if you wanted to evaluate an expression with more than two numbers like 1 + 4 + 7 for example well even though you can't do it in one

**[1:20]** step you can still do it right just add 1 + 4 which gives five and then add that five to 7 which gives 12 you only operated on two numbers at a time but since you remembered the five and brought it back you could still finish the evaluation using this same technique you could evaluate an expression of any size as long as you had enough memory to store the intermediate results so let's start

**[1:45]** building some memory with redstone because it seems like it would be kind of useful in lrr number 7 I showed you guys that repeater locks are a great way to make memory because they act as a natural data latch all you have to do to write a bit is unlock it and relock it to write a one just put a one behind it and unlock relock or to write a zero it's the same idea using a stone button

**[2:06]** like this works fine but it's actually a lot longer than it needs to be you only need a minimum of a two tick pulse which you can get from a two tick pulse generator this gives just enough time to write the new data one repeater lock Only Stores a single bit though so how would you store more information the easiest solution is to just use more of them here I have four repeater locks all

**[2:24]** hooked up to the same right line so you can put in any number like 0 1 01 press right and the whole thing gets written this is called a register a register just stores a number and it's usually made with a bunch of data latches specifically this is a 4-bit register because you can store any 4-bit number to it and although making horizontal registers works fine in my opinion it's

**[2:45]** more elegant to do it vertically this is an 8-bit register with all eight repeater locks stacked directly on top of each other I say this is more elegant because now the right line is just one glass tower that reaches all eight at once so you can put in any 8bit number and write it if you want to write a new number then you can just put it back here and write again now let's take this even

**[3:07]** further and combine multiple registers together here I took four registers and combined all the inputs into one main input right here so if you put in a number it gets duplicated to all of them then you can just press write on the register you want to write to for example to write a five to the second register just put a five here go to the second register and press right as you

**[3:27]** can see it received a five the only only downside with this circuit is that you can't write to multiple registers at once but in our case that's okay remember the overall job of the computer is to execute simple instructions so it's actually going to be better to write to one register at a time next let's give these registers some official names because calling them by the second

**[3:46]** one or the third one is kind of annoying I'll call this one on the left register zero then register 1 register 2 and register three and now that each one has a number we can use a decoder from lrr number 6 to address them this is a 2 to four decoder meaning it takes in a 2 bit binary number 0 1 2 or 3 and turns on the corresponding output if you put in one it decodes to one or if you put in

**[4:10]** two it decodes to two a decoder outputs a constant signal though so if you just hook this up to the right lines it makes the selected register constantly open notice how if you put a three into this decoder it comes over here gets decoded for and keeps register 3 completely unlocked it would be really nice if instead of this we could wait for a button press to write to the register

**[4:31]** that we put in the decoder one way to do this is to just cancel the input until the button is pressed so now when you press right the address gets released for two ticks and you get the output for two ticks for example if you put in a one and press right you get a two tick pulse on one or if you put in a three and press right you get a two tick pulse on three but as you might have noticed

**[4:51]** already there's a subtle problem with this canceling the address is the same thing as setting the address to zero but zero is a perfectly valid address addess so the decoder is just going to constantly output zero while it's cancelled furthermore since the decoder decodes for all possible combinations there's no address we can put in to make it output nothing to solve this problem

**[5:11]** there are a few different approaches and we're going to choose the most naive one we're just going to remove register zero so instead of registers 0 1 2 and 3 we'll just have 1 2 and 3 and now all of them are off by default until we choose one two or three and press right let's go ahead and hook this up and try it out I'll put in a four select register 1 and press right then I'll put in a five

**[5:36]** select register 2 and press WR again and it worked register 1 got a four and register 2 got a five okay now that we can write to a specific address it would make sense to read a specific address as well to do this I'm going to wire all the outputs together and put in another decoder to only allow one of them at a time so when you put an address here only that register's output will be

**[5:58]** allowed and it'll show up on this out output I just filled the registers with these numbers so let's try reading them reading three gives six reading 2 gives five and reading one gives four but what about address zero what happens if you try to read that well it looks like it outputs zero because it decodes to nothing we removed the physical copy of register zero however that doesn't mean

**[6:24]** it doesn't exist register zero actually does exist if you think about it as only reading zero this is called a zero register so instead of thinking of this as decoding to nothing think of it as decoding for register zero which happens to be a zero register also notice that if you write to register zero the data doesn't get stored anywhere it essentially just gets thrown out that

**[6:45]** makes sense because why would you write to it if it's just going to read zero no matter what now having a zero register might sound stupid but we'll see later on that it's actually going to be pretty useful but anyways this is now a fully working register file a register file is just a collection of registers with the ability to write to any of them or read from any of them specifically this

**[7:04]** register file has four registers 0 1 2 and three with zero being a zero register if you're making your own computer and want the simplest design possible for a register file then this is what I recommend but this wouldn't be a video about register files without talking about one of the most common features dual read dual read is the ability to read two registers at once in

**[7:24]** Hardware there are two main strategies to do this true dual read and simulated dual read in true dual read you basically just duplicate all the output wires and read each one separately so in this example you can see that it lets you read register one with one set of wires and register two with the other set in simulated dual read you instead keep two copies of the registers and

**[7:45]** then just read each copy normally to read registers 1 and two for example just read one on the first copy and two on the second note that since you have two copies now this means you have to keep them in sync one easy way to do that is to just write to both copies whenever you execute a r so with redstone here's an example of true dual read there's only one copy of

**[8:04]** the registers but the output wiring gets really messy there are two read decoders now so you can put in any two addresses here and read them both at once and then here's an example of simulated dual read simulated dual read is actually a lot easier to make with redstone because you can basically just mirror the entire circuit to make the copy this is the first copy of registers one 2 and three

**[8:24]** and this is the other copy it's symmetrical to keep them in sync the right decoder now writes to both copies at once with this Redstone line so if you write to register one for example you can see that both register ones receive a right signal perfectly in sync and then there are just two separate read decoders one on each side so you can read any register here and any

**[8:43]** register here all right now let's build the register file that we're actually going to use in our computer again if you just want the simplest design I recommend this but the one we're going to use is going to be a bit fancier because it'll take advantage of some smart Redstone tricks we'll start by using this clever design for the right function if you didn't know you can also

**[9:00]** lock repeaters with a comparator so what we have here are comparators with signal strength One locking every repeater and when you power this Glass Tower it cancels all of them from the side which unlocks the entire register this design is great because it can be stacked every two blocks as long as you stagger them like this let's give our register file a total of 16 registers 0 through 15 with

**[9:22]** zero being a zero register then for the read function we're going to use another clever design notice that you can create a read function with just two Inver iions right now the output is reading the input because the double inversion cancels out but if you want to stop reading you can just power it here which forces it to be off this design uses that strategy but just in a fancier way

**[9:42]** the first inversion is done with these comparators and the second inversion is done with these torches when the Glass Tower is powered it forces all the Torches to be off and stops reading the register just like how over here powering the dust stops reading the bit but when it's not powered any comparators that are on will have a signal strength of two two which is just

**[10:00]** barely enough to only affect one output and get inverted again for example right now there's a five in the register but the Glass Tower is being powered so it's not being read to read it you just unpower the Glass Tower and you can see that the comparators just barely reach their outputs and read a five this probably seems like the most over complicated read function in the world

**[10:20]** and it is but it's all for a reason it's all to make it too wide stackable using the Staggering technique again so let's go ahead and add this to all 16 registers now let's add some decoders Since There are 16 registers we can address them using some 4-bit decoders here's the right decoder with the right button already hooked up and here's the read decoder and finally let's mirror

**[10:40]** this entire thing to make it simulated dual read now the right decoder is hooked up to both copies and there are two read decoders one on each side and that's it this is the final register file 16 8bit registers dual read and register zero is a zero register in diagram form the register file looks like like this R1 and R2 are the two read addresses and these are the two

**[11:03]** outputs W is the WR address and data is the 8bit data you want to write now remember in episode 1 when I said that sequential components will update using the clock signal while the right button I've been using this whole time is what updates the register file it literally controls when the register values change so the right button is the clock signal I've just been calling it a different

**[11:24]** name the only thing we don't have from this diagram is the enable input when enable is one it behaves the exact same way I showed you in Minecraft so far but when enable is zero you can't read from it or write to it it's completely disabled this will be a really useful feature later on so let's go ahead and add this signal to the Minecraft build the nice thing is it's pretty simple to

**[11:43]** completely disable this you can do it by just canceling all three of the address inputs this forces it to read register zero on both read ports which again always outputs zero and it forces any rights to register zero which just get thrown away so now when this lever is off off it's disabled and when it's on it's enabled and just like that we are completely matching the diagram here's

**[12:05]** R1 R2 W data clock enable and the two outputs which are on the other side let's go through some final examples to make this really solid I'll put the diagram on screen too everything is zero right now including the enable signal so let's start by enabling it then I'll put in a seven for data a one for the right address and press clock this writes a s to register one on the first Port

**[12:33]** Reading address one reads 7 and on the second Port Reading address one also read seven now let's change the data to four the right address to two and press clock this writes a four to register two switching the first read port to two will switch the first output to four and switching the second read port to two we'll switch the second output to four and then if we disable it both outputs

**[12:57]** switch to zero note that the registers aren't reset or anything it's just reading and writing is disabled if you enable it later you can continue where you left off memory is going to be an essential part of our computer later in this series we'll see how upgrading the memory even further makes our computer a lot more powerful but in the meantime if you want to upgrade your brains memory

**[13:16]** then check out brilliant the sponsor of this video brilliant is the best way to learn about all things computer science and math all of their online lessons use Hands-On problem solving which sticks to your brain much better than a lecture by getting hands-on experience instead of memorizing you'll become a better thinker while also gaining knowledge on top of that it'll help you develop a

**[13:34]** powerful learning habit learning a little bit with brilliant every day is a thousand times better than mindless scrolling you can even learn right on your phone with fun lessons you can do whenever you have time we'll touch on programming later in this series but if you want to get a head start then check out the creative coding course this course will teach you all the essential

**[13:50]** coding elements and get you to really think like a programmer to try everything brilliant has to offer for free for a full 30 days visit brilliant.org slmap batwings or click the link in the subscription you'll also get 20% off an annual premium subscription [Music]
