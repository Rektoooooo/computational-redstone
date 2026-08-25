# Introduction to Computing - Let's Make a Redstone Computer #1

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=osFa7nwHHz4
- **Duration:** 11:03
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome to the first episode of a brand new series building a redstone computer the ultimate goal for this series is to take you along with me as we make a programmable Redstone computer powerful enough to run complex programs like snake Tetris and more and hopefully along the way you won't just learn about Redstone you'll also learn a lot about computers and digital logic in

**[0:18]** general but first let's back up for a second why make a computer in the first place if you played around with redstone before you'll know that you can use it to make digital circuits within the game of Minecraft and most circuits you'll see whether they're on YouTube Reddit or wherever are single-purpose circuits meaning they only do one main thing a light switch a binary counter or even an

**[0:37]** Adder are all examples of single-purpose circuits in fact you could even argue that the Redstone games I've made like Tetris snake and Flappy Bird are also single purpose circuits sure they're extremely complex but they only run one thing my Tetris game for example only runs Tetris you can't modify it to run anything else at least not very easily so in this series we're going to change

**[0:57]** our way of thinking the larger goal is not to make a circuit that does one thing but instead to make a general purpose circuit or more accurately a general purpose computer but wait if it's possible to make a computer that can just play any game or run any program then why haven't I done this earlier why did I spend 3 years making games when I could have just done this

**[1:17]** all along well like anything in computer science there are trade-offs computers are great but they're extremely slow like orders of magnitude slower than Redstone games maybe a thousand times slower or more depending on the computer and what what you're doing with it Redstone games are faster because you can optimize for the task and use Creative Solutions for example when I

**[1:36]** made Flappy Bird I used a decaying signal strength circuit to make the bird fall in real time think of it this way if your goal is to play a bunch of games using only Redstone you have two options option one make each game with a single-purpose circuit and they'll be somewhat fast this is what I've done on my channel a lot and each game took me anywhere from a couple days to a couple

**[1:54]** weeks to make or option two spend a ton of time making a complex general purpose computer I did this recently and it took me 3 months to do but now that it's done making games for it is easy because you can just program them an experien programmer could code something as complicated as Tetris in like a day so option two is what we're going to be doing in this series we're going to make

**[2:14]** that initial investment to make a complex computer that way when we want to make a new game we can program it in a day instead of building it in a few weeks so now that we have the motivation why are we doing this in Minecraft I think a lot of people would tell you that if you want to make a computer you should just use a digital logic simulator like lism or make one in real

**[2:32]** life on a breadboard and I want to be super clear I don't disagree with that however I think Minecraft is a pretty good way to do it too the 3D nature of Minecraft makes it feel like you're physically in the world of the circuits I mean I'd be lying if I said there wasn't some Nostalgia keeping me playing as well but I swear it actually is a decent simulator plus computer tutorials in

**[2:52]** logismos already exist so why not do something unique right now let's talk about what you need to know before we start this series The First first and most important thing is to watch my previous tutorial series logical Redstone reloaded this series will introduce you to Binary logic gates and a bunch of fundamental circuits that are going to be really important for our

**[3:10]** computer I'm going to try my best to recap stuff whenever it's brought up but still I highly recommend watching logical Redstone reloaded so that you can get familiar with fundamental circuits and Concepts another thing I recommend especially if you're planning on making your own computer is to get familiar with fabric mods the most common mods I'll be using are world edit

**[3:26]** to help with building carpet to speed up the game and redstone tools for a bunch of other utility commands I'm also going to be using a tool called MCH PRS to run Redstone super fast but that's more complicated than a fabric mod so you don't have to worry about that right now for now I've left a bunch of links in the description for how to install the three fabric mods and how to use them

**[3:44]** also this entire series will be in version 1182 because that's the version the computer was built in I know that 121 has some useful new commands and features but the computer was built in 182 so I'm just going to stick to that version to make sure there's no issues plus at the time of recording this R stone tools still isn't updated to 121 okay almost done yapping the last

**[4:04]** thing I want to say before getting started is just some disclaimers I am not an expert on computers I am a recent college graduate who has never done real life Electronics I've only done software projects and obviously a lot of Minecraft so I'm probably going to be a biased learning Source because the best way to do something in Minecraft might not be the best way to do it in real

**[4:22]** life however this series will still teach you a lot that applies to real life and I think I have a ton of useful information to offer also there is unlimited Li mited Freedom when building a computer every design choice is a matter of pros and cons There is almost never a single correct answer when building any part of it so if you want to make your own computer play around

**[4:39]** with these choices by doing so you'll learn much more than just copying me plus this series is not going to be a block by block tutorial so it's really not intended for copying me instead I recommend using this series to Simply learn about computers and then with that knowledge make your own all right let's finally get started earlier I mentioned that our computer will be able to do

**[4:58]** anything but what is that actually mean back in 1936 a mathematician and computer scientist named Alan Turing thought about this question a lot he was one of the first people to wonder what a machine that could compute anything might actually look like and so he created the first mathematical model that could do this the turing machine the turing machine is basically an

**[5:16]** infinitely long memory tape divided into cells and a head that always points to one of these cells then based on a set of states the head will either right to the cell move left or right or halt computation Turing proved mathematically that even with this incredibly simple design a touring machine could indeed compute anything from calculating the digits of pi to running Minecraft okay

**[5:37]** but why does this matter well if you were making a computer and wanted to prove that it could compute anything how would you do it one way to do it is to just ask can your computer simulate a turing machine if so then yes your computer can also compute anything because anything you could possibly want to do you can just do on the simulated turing machine Any model that can

**[5:56]** simulate a turing machine is called Turing complete so so a turning machine itself is turning complete virtually all programming languages are Turing complete and the computer you're watching this on is also turning complete and when it comes to Minecraft computers they tend to be so simple that they're not always tur complete our computer though definitely will be I'm

**[6:14]** not going to be proving it though or talking any more about it really I I just thought it was a good thing to bring up a lot of times when someone makes a new computer the first question people ask is is a turning complete so now you know what that is all right enough talk about Theory what is our computer actually going to look like well here's a diagram of all the

**[6:31]** hardware these are almost all the things we're going to build with redstone depending on how much you've seen before you might not understand everything here or maybe nothing at all and that's completely okay by the end of this series you'll understand all of this diagram and why it looks like this for now let's just talk about some of the key features these rectangular colored

**[6:48]** blocks are the main components each one has one or more inputs with the arrows going into it and outputs with the arrows going out of it for example this right here is the ALU which stands for arithmetic logic unit the Alou will be doing most of the actual computation in our computer it has two 8bit inputs an 8bit output and a setting input if the inputs are 1 and two and the setting is

**[7:12]** ADD then the output is three we'll talk a lot more about alus in The Next Episode so it's okay to think about this as a magical black box right now the main point is that the ALU is a combinational component remember from lrr number six combinational means that there's no memory or state it's simply a function from input to Output so when we put in one two and add there was no

**[7:34]** question what the output was going to be the output was predetermined to be three now let's look at a component that isn't combinational this is the PC or program counter it has a main input a main output and a special input called clock the job of the program counter is to hold a single number in its memory so let's say it's holding a seven right now if I input a different number like three

**[7:57]** nothing will happen but if I hold that three and send a pulse to this clock input then it will refresh its memory with the new number so the clock input allows you to choose when the program counter should update we'll go over why the program counter holds a single number in later episodes but the point is the output depends on what's in the memory so it's not a combinational

**[8:17]** component instead it's a sequential component in this diagram if a component has a clock input it's sequential and if it doesn't it's combinational that is not true in all diagrams but it's true in this one all right so like I said this is all the hardware and it's what we're going to be building in Redstone but that's only part of the story we're also going to be writing software for

**[8:37]** the computer specifically we're going to be writing programs in a custom language but why write programs in a custom language why not program in a language that already exists like C++ well you could do that but it would be more complicated before you can run a C++ program on a computer it gets compiled to an assembly program which is basically a new version of the program

**[8:59]** that's easier for the computer to understand then the assembly program gets assembled to machine code and that's what actually gets run on a computer the compiling stage is complicated and it's out of scope for this series so we're going to forget about compiling instead we're going to make a language in this realm so when I say custom language I really mean custom

**[9:17]** Assembly Language it's going to take on a similar syntax and feeling as a real Assembly Language but it'll be simplified because this is a Minecraft computer then to run a program we're going to assemble it to machine code which in our case is just a Minecraft schematic of zeros and ones and once that schematic is pasted into the computer we can run the program all

**[9:36]** right that was a lot so let's summarize throughout this series we're going to be building a programmable Redstone computer that has a lot of Hardware most of which is in this diagram some components are combinational but others are sequential and rely on a clock signal on top of that we're going to develop a custom Assembly Language to write programs in and to run a program

**[9:55]** will'll assemble it to a Minecraft schematic that can be pasted into the computer this is a very broad overview and we're going to dive into a lot more detail coming up but if you want to get ahead of the game and learn about computers before then then check out the links in the description especially the top link for the sponsor of this video brilliant brilliant is an amazing

**[10:12]** resource for learning about math data analysis programming and AI through thousands of interactive lessons it's designed to get you Hands-On with problem solving so by letting you play with Concepts visually you'll build critical thinking skills that you wouldn't get from a regular lecture learning every day is one of the best ways to grow both personally and profession professionally brilliant

**[10:30]** helps you do this with just minutes a day and the lessons are available 24/7 whenever you have time one of the best examples of learning Concepts visually is from a course called scientific thinking this course takes you on an interactive tour of the world and with no heavy math it's great for all Learners to try everything brilliant has to offer for free for a full 30 days

**[10:47]** visit brilliant.org slmap batwings or click the link in the description you'll also get 20% off an annual premium subscription [Music]
