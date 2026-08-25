# Data Memory - Let's Make a Redstone Computer! #9

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=KWkGW0lS2-0
- **Duration:** 11:39
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to let's make a redstone computer in the last episode we created a call stack today is a really exciting day we're going to add the last main component and finish the instruction set I hope you enjoy at this point in the series our computer is decently powerful you can make programs over 1,000 instructions long and these programs can have a wide variety of code

**[0:19]** structures like if statements loops and sub routines but it's not powerful enough if you watch the Showcase Video for this computer you know that the original reason I designed it was to run games like Tetris and to make games we're going to need a lot more memory so how should we add more memory one idea is to just make the register file bigger maybe instead of 16 registers there

**[0:40]** could be 100 or a th000 technically this is an option but it comes at a cost remember register operands are four bits long because four bits can address 16 different registers so even if you just added one more register making the total 17 4 bits wouldn't be enough anymore register operands would become 5 bits long and you'd have to completely redo the instruction set okay but then why

**[1:02]** did I spend all this time making the instruction set like this I mean if 16 registers isn't enough memory why didn't I just start with a giant register file and design the instruction set based on that well memory works best when it's not just one big register file but rather a pyramid let me explain memory is a balancing act we like when memory is big but we also like it to be fast

**[1:24]** this is problematic because as memory gets bigger it gets slower so how can you design memory to get the best Best of Both Worlds the answer is a pyramid or a hierarchy for example in the computer you're watching this on the memory hierarchy probably look something like this on the bottom you have a drive like a solid state drive or a hard disk drive this stores a lot of data so it's

**[1:45]** very slow above that you probably have Ram or main memory main memory can't store as much data but it's a lot faster above that there's the registers these hold very little data but they're extremely fast now of course this diagram is is not exact but no matter what the exact layers are your computer follows some sort of pyramid where the memory types get smaller and faster as

**[2:07]** you go up to understand why this setup works so well I like to use an analogy with a library let's say you're a big reader and there's a library that stores all the books you could ever want to read so whenever you finish a book one option is to just go to the library return it and get a new one which takes about an hour but a better option would be to have a bookshelf at home then you

**[2:27]** could go to the library grab 20 books and set them on the bookshelf now whenever you want a new book you'll only spend a few minutes getting it from the Shelf well until you finish them all and need to go to the library again but that'll only happen like once a week but even this is not as efficient as it could be you could also have a backpack that stores three books now whenever you

**[2:46]** want a new book you'll only spend a few seconds getting it out of your backpack you'll still have to go back to the Bookshelf sometimes but that'll only happen like once a day this is why a hierarchy is so great it makes most tasks very efficient and only slows down once in a while when you you go to a lower layer now for our computer a memory pyramid is a bit less useful than

**[3:05]** it is in real life remember our computer is single cycle meaning every instruction takes the same amount of time which means any memory we make is going to end up being the same speed in practice but there are actually more advantages to a pyramid than just speed so our computer is still going to have a pyramid it'll be a mini pyramid that looks like this the register is on the

**[3:24]** highest layer and a new component called the data memory below that the data memory will be much bigger than the Reg ERS and in theory it should be slower but again it's not actually slower because our computer is single cycle so how will the data memory work well just like the instruction memory there will be a list of addresses but instead of a 10-bit address it'll be an 8-bit address

**[3:44]** creating 256 possible slots and instead of storing an instruction at each address it'll store one bite of data this data will end up being whatever we want similar to the registers in fact if you want to think of the data memory as 256 new registers you can that's basically what it is to write data to an address just put the address here the data here set it to write enable it and

**[4:07]** clock it then to read data just put the address you want to read here set it to read enable it and whatever data is at that address will come out right here all right let's make this in Minecraft first we need to make an 8 to 256 decoder that way we can input an address and get a signal at the physical location next let's make this input a one bit signal to distinguish between a

**[4:29]** right write and a read I'll start by splitting every output into two one for writing and one for reading then I'll just make this signal control which one is allowed through if it's on then it's a right so when an address comes in it'll output a right at that address and if it's off it's a read so it'll output a read at that address then for the actual storage I'm just going to use the

**[4:50]** same design from the registers duplicated up to 256 bytes honestly this is a pretty lazy solution but it's fine for a single cycle computer so let's say you want to a five into the data memory input the five right here and it'll spread out in this tree formation now it's directly behind all the repeaters so it's ready to be written to any address to write to address 7 for

**[5:11]** example input a seven here and clock it thanks to the decoder this makes the bite at address 7 quickly unlock and relock grabbing the five now let's say you want to read the data memory if you look closely there's another tree formation for reading which ores all the outputs together so if you switch to read mode and input seven the five gets put onto this tree and it comes out on

**[5:32]** the final output if you read any other addresses the output will be zero because all the other addresses currently have zero okay so as you might have guessed these last two instructions are how we're going to communicate with this new memory one instruction will be for loading data from the data memory into a register which is called load this will have op code 14 and demonic LOD the

**[5:54]** other instruction will be for storing data from a register to the data memory which is called store this will have op code 15 and neonic Str Str let's focus on load first load has three operands register a register B and an optional third operand called offset I say optional because if you don't include it the assembler will just make it a zero register a is the pointer and register B

**[6:18]** is the destination meaning it'll look at the contents of register a and go to that number as an address in data memory then it'll take whatever is at that address and load it into register B for example load R2 R3 assembles to this and when it's executed it'll use register 2 as a pointer and load the data into register 3 if register 2 has a one in it and the data at address one is say six

**[6:44]** then register 3 will get loaded with that six but this is all assuming you have an offset of zero the 4-bit offset value is sign 2's complement so it can be anything from8 to 7 I talked about two's complement in lrr number five and so actually instead of using just register a for the pointer it'll use register a plus the offset for example load R2 r31 we'll use register 2 + 1 as

**[7:10]** a pointer and load the data into register 3 note that this does not change register 2 the offset is only used for the pointer let's make a simple program with loads to make this really solid let's say that addresses 1 through four of data memory look like this and you want to load this data into the first four registers there are kind of two ways to do this one way is like this put a one

**[7:33]** into register one and then do load R1 R1 this uses register one as a pointer which points to address one and loads the data into register one then you can just do the same thing for register 2 3 and four another way to do it is like this put a zero into an extra register like register 15 and just use offsets to reach all four the first load uses register 15+ one as a pointer which

**[7:59]** points to one and loads it into register 1 the next load uses register 15 + 2 as a pointer which points to two and loads it into register 2 and similar story for three and four as you can see using offsets saves instructions it allows you to reach data in a small area without having to change the pointer in Hardware we can support loads by hooking up the data memory like this on a load the ALU

**[8:24]** will calculate register a plus the offset and plug that in for the address whatever is that address will come out and get selected on this MX and register B will be selected on this MX so it gets written to register B now let's transition to the final instruction store store has the exact same oper ends as load so it can be kind of confusing just remember load is loading a register

**[8:48]** from the data memory and store is storing a register to the data memory so in a store register a plus the offset is still the pointer but register B is not the destination register B is the data you want to store to that pointer for example store R2 r31 assembles to this and when it's executed it'll use register 2+ one as a pointer and store whatever is at register 3 to that

**[9:13]** address if register 2 has a one in it and register 3 has a six it'll store the six to address two and in Hardware all we have to do to support store is take register B and plug it into the data input once again the Alou will calculate register a plus the offset and the contents of register B will be written to that address you know the drill let's go ahead and connect the data memory to the

**[9:36]** computer following the diagram and that looks like this everything should be connected now let's run a test program to Showcase load and store I think a perfect test program is bubble sort this program will use the bubble sort algorithm to sort the list of numbers at the first eight addresses for example if the addresses look like this at the start of the program they'll look like

**[9:55]** this at the end if you're interested here's the equivalent pseudo code so you can pause the video to learn how it works I'll just manually put in some data at the first eight addresses paste it in and run after many trips back and forth between the data memory and the registers the list is sorted even though this is not the end of the series the main part of the computer is completely done and the

**[10:17]** instruction set is finished we have all 16 instructions but from an outside perspective it still doesn't do much it can run programs But ultimately it's just a box changing its memory so in the next episode we'll talk about how to connect this to the outside world like a screen or a controller and then after that the final episode will be about programming because even after the

**[10:36]** computer is hooked up to stuff there's still a lot to talk about when it comes to complicated programs but yeah at this point in the series you've learned how all the essential parts of a computer work so go out there and try to make your own and if you want more information on how to do that then check out brilliant the sponsor of this video brilliant is a great place to learn

**[10:52]** about computers math and many other engineering topics they have thousands of online lessons each with an interactive activity so instead of watching a video or just memorizing you'll play with the concepts yourself just like you would with redstone the lessons are available 24/7 and even with just a few minutes a day these lessons will help you build real knowledge if

**[11:09]** you want to learn more about programming before the final episode then check out the thinking and code course you'll learn all the essential coding elements and you'll start to think more like a programmer to try everything brilliant has to offer for free for a full 30 days visit brilliant.org slmap batwings or scan the QR code on screen or you can click the link in the description you'll

**[11:26]** also get 20% off an annual premium subscription
