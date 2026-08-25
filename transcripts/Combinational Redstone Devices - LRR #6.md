# Combinational Redstone Devices - LRR #6

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=34QSMj1wbe4
- **Duration:** 16:40
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to logical Redstone reloaded last episode we talked about negative numbers and subtraction today I have a really cool episode for you as circuits get larger and more complicated many common patterns and functionalities arise so in this episode we're going to build up what I like to call a toolbox of common logic devices for you to use in your circuits I hope

**[0:18]** you enjoy but first a bit of terminology all the logic devices in this video are called combinational a combinational circuit is independent of time there's no memory there are no internal States a combinational circuit is simply a function from input combinations to outputs in other words if you know what the input is you know what the output is for example a full adder is

**[0:39]** combinational it has three inputs two outputs and every combination is defined by a truth table if I input 1 1 1 I already know what the output will be without even looking at it it has to be 1 1. the other type of circuit we'll learn about later is called a sequential circuit but more on those later for now let's just focus on combination logic devices so far in this series we've already made

**[1:03]** a few of these devices we've made logic gates a half adder a full adder and 8-bit adder and an 8-bit subtractor the next combinational device I want to show you is called a magnitude comparator this has nothing to do with the Redstone comparator that's a completely different thing in this context the entire circuit is called the comparator a magnitude comparator takes in two numbers A and B

**[1:23]** and outputs three bits of information whether a is greater than b equal to b or less than b this circle is really useful because comparing numbers is a very common thing to do so how should we approach building this oh let's start with the equality check to see two binary numbers are equal to each other you can simply check each pair of bits and make sure they all

**[1:43]** match the easiest way to do that with redstone is a tower of xor gates with the outputs ored into a glass tower and a final knock gate on the end notice that an xor gate outputs zero if the bits match and a 1 otherwise so if all the bits match then every single xor gate will output 0 which allows the torch to turn on but if we get a mismatch on any layer that xor gate will

**[2:06]** output 1 causing the torch to turn off no matter where the signal came from alright perfect we have an equality Checker next let's focus on a greater than b to check if a is greater than b we can follow a relatively simple algorithm first check the highest bit if a has a 1 and B has a zero a must be greater than b no matter what's below so we can output 1 and we're done but if a

**[2:30]** has a 0 and B has a one the opposite is true there's no way a is greater than b so we can output 0 and be done and if the highest bits are equal to each other we don't know which one is bigger yet so we go down to the next highest pair and run the same checks again and yeah if you repeat this process potentially going down to the lowest bit you'll eventually figure out whether a is

**[2:52]** greater than b now the cool thing about building this with redstone is that we don't have to stick by that logic exactly there's actually a way to do the same thing using some Redstone specific properties this is an a greater than b circuit made by my friends ikandu and sloime it's pretty clever it uses a modified version of the carry cancel process from the edition episode but

**[3:12]** repurposed for comparisons as you can see if I input 10 versus 8 10 is greater than 8 so we get an output but if I input 6 versus 8 6 is not greater than 8 so the output is zero also I kinda lied this device has an output for equality check as well if you put a redstone torch right here this lamp will tell you whether a is equal to B so we actually don't need our own equality Checker this

**[3:38]** circuit outputs both a greater than b and a equal to B plus it only takes three ticks which is really cool notice that the equality lamp is on right now and that makes sense the input is zero and zero so a is not greater than b but a is equal to B so now that we have these two outputs the only thing left for our comparator is a less than b and the cool thing is we don't have to make

**[4:02]** another circuit for this we can actually derive it just by looking at the other two bits if a is not greater than b and a is not equal to B well the only other option is that it's less than B therefore I'll just put them into a nor gate and now we have the output for a less than b and that is the finished magnitude comparator we can now input Anything For A and B and get the three

**[4:25]** output bits of comparison now I should mention that you can also do this with a subtractor if you subtract a minus B and the output is zero well then you know that a equals b or if the output is greater than zero you know that a is greater than b in fact that's the more common way to do it in computers but I'm not building a computer here doing it this way still has its advantages like

**[4:47]** being smaller and faster than a subtractor the next logic device I want to show you is an encoder an encoder is a device that accepts one input at a time and outputs an encoding for that input for example this encoder has four potential inputs a b c and d and outputs a three bit encoding but in general you can have as many inputs as you want and the size of the encoding is up to you as

**[5:10]** well now you can encode the inputs however you want it depends on what you want to use the encoder for in our case let's just make the encodings for a b c and d one two three and four respectively but I could have chosen anything here if I input a the output should be the encoding for a which is 0 0 1 or if I input C the output should be the encoding for C which is 0 1 1. so

**[5:36]** let's build this encoder for real first I'll start with four lines for a b c and d with a torch on each one to make them inverted the then underneath I'll have three output wires going this way then to make the encodings we can put torches on the sides of these lines such that they're above the output lines underneath a is one B is 2 C is three and D is four and that is the finished

**[6:00]** encoder you can now input A B C or D and get the encoding for it for example if I input D we get D's encoding which is one zero zero and by changing the positions of these torches you can make the encodings whatever you want of course there are way more designs for an encoder as well the classic design I just showed you goes from horizontal to horizontal but here's an encoder that

**[6:23]** goes from horizontal to Vertical instead each input Powers a glass tower and you can make the encodings using these repeaters and here's another design it's pretty similar to the classic one all I did here was add another layer on top so that the inputs and outputs are perfectly aligned and finally here's a design that goes from vertical to Vertical using spirals in case you

**[6:43]** didn't know 2x2 barrels are a great way to send data both up and down from anywhere on a wire and they're stackable directly next to each other as long as you Orient them correctly so that's the strategy being used here of course if you want to take a closer look at any of these designs or try them out yourself the World download is in the description now because only one input is supposed

**[7:02]** to be on at a time encoders can give you weird Behavior if something accidentally breaks that rule so if you want to enforce that rule on a hardware level you can attach a circuit like this to the front of an encoder this circuit will guarantee that only one input is allowed if multiple inputs are on it'll just pick the rightmost one and by the way an encoder with this circuit on the

**[7:22]** front has a special name it's called a priority encoder next let's talk about the opposite of an encoder a decoder as you can see by this table the inputs and outputs are swapped a decoder takes an encoding and outputs the corresponding signal for example if you input the code for C which is 0 1 1 then the output for C should come on just like an encoder a decoder is extremely customizable

**[7:46]** depending on what you're using it for but let's go ahead and build the decoder that matches this table the key to making a decoder is to understand how to detect a certain binary sequence because that's what a decoder is all about the a output is detecting a sequence the B output is detecting B sequence Etc so as an example let's say I want to detect the sequence 1 0 1. in other words when

**[8:08]** these lamps are one zero one the output is on in any other scenario the output is off your first instinct might be to make an and gate on the first and third bit and that's a great idea let's do that okay I put not Gates on the input and or them into another not gate now if I turn on the first and third bit the lamp is on but the problem is if you turn on the second bit the lamp is still

**[8:32]** on even though this is not the correct sequence anymore so let's put a repeater here to force the final torch to be off when the second bit is on and now this is the detection circuit for 1 0 001 the output will be on if and only if the input is one zero one in general if you want to detect a specific sequence this is the way to do it simply put torches on the correct bits repeaters on the

**[8:56]** incorrect bits and ore them all into a final torch for example to detect one one zero zero just go torch torch repeater repeater and there you go this circuit will output one if and only if the input is one one zero zero anything else will not work so back to our decoder let's use this strategy I'll start by having the input lines vertical like this then for each output let's

**[9:22]** have a glass tower going into a torch then let's place the Torches a is one B is two c is three and D is four and then put repeaters everywhere else and just like that we have a decoder if I input three I get C or if I input 4 we get D notice how each Glass Tower is essentially the exact same circuit that we were doing over here torches for the ones repeaters for the zeros and then

**[9:50]** all ored into a final torch this allows each Glass Tower to detect a specific sequence pretty cool right honestly as far as designs go this is pretty much the only one I use if you download the computer I made recently you'll notice that literally every decoder I made was in this style it's just the best design I don't call things the best design very often but I will for this one I mean you

**[10:11]** can power the input lines from either end or even in the back if you and you can decode on both sides as well but of course there are a lot of other designs so let's take a look at a few of them here's a similar design that uses spirals instead of glass Towers this allows you to go from vertical to Vertical in a decently nice way and here's a design that goes from horizontal to horizontal whenever

**[10:31]** there's a torch you just put it on the side of the block and whenever there's a repeater you just kind of use this formation to power the line underneath I will warn you though this design can be really annoying for example if you want to have a lot of repeaters in a row then there might not be enough space for this formation you'll just have to get creative with how you power the output

**[10:50]** lines underneath however if you give the output lines a two wide Gap instead of a one wide Gap you won't have any of those problems this design right here is always nice and pretty no matter what your decodings are because there's plenty of space alright before moving on to the next combinational device let's look at some cool things you can do with encoders and decoders first you can use

**[11:10]** them to transfer data in less space with this setup if I turn on a specific lamp the corresponding lamp shows up over here which is really cool when you realize that there's only three wires between them what I'm doing here is encoding each input into a three bit number and then decoding it back out of course this doesn't work with multiple inputs at the same time because you

**[11:31]** can't encode two things at once but it's still pretty neat another cool thing is that with encoders and decoders you can essentially Implement any function you want using a kind of Brute Force type of approach for example let's say I want to make something that takes a 4-bit number and simply adds one to it four bits gives us 16 possibilities for the input so first let's decode for every single

**[11:53]** possibility using a decoder then once we know which scenario we're in we can use an encoder to customize what the output should be since our goal with this circuit was to add one I just encoded it so that it does that and now this is our plus one function if I input 5 then the 5 gets detected right here and it just gets encoded into a six because that's how I programmed it or if I input 3 the

**[12:17]** 3 line gets detected and it gets encoded into a four in a way this circuit is not even really adding one I mean functionally it is but there's no Adder here instead we just decoded for every possible scenario and program the output in every single case that's why I call this The Brute Force approach but of course this approach has a downside it gets way bigger with more bits if you

**[12:40]** wanted to brute force a function from 8 Bits to 8 Bits then you would need a 256 line decoder and a 256 line encoder so yeah try to use logic gates and Boolean algebra first the next combinational device is called a multiplexer don't be scared by the crazy name it's actually incredibly simple a multiplexer or a mux is basically a selector it allows you to select which input you want to allow

**[13:05]** through here's an example of a mux we have two inputs one output and one selector bit when the selector bit is zero the left input is allowed through but the right one isn't when the selector bit is one it's the opposite the right one is allowed through but the left one is not of course canceling comparators is not a thing in real life so in logic diagrams you might see a mux

**[13:29]** implemented like this using and Gates I recommend pausing the video and imagining yourself using this circuit to understand why it works but yeah in Minecraft I always just use comparators for muxes also multiplexers can have as many inputs as you want this right here is a mux that lets you select from four different inputs notice that there are now two selector bits instead of one

**[13:49]** this is because you need two bits to describe four possible selections this decoder underneath simply decodes for those four possibilities and unlocks the corresponding input 0 0 unlocks the first one zero one unlocks the second one one zero unlocks the third one and one one unlocks the fourth one beautiful next we have the opposite of a mux a d-mux a D-Max has one input and it

**[14:15]** allows you to Route it to one of the outputs using the selection bits I tend to think of d-muxes like a train track where you can choose where the tracks are going here's a small demox it looks extremely similar to the mux when the selection is zero it gets routed to the left otherwise it gets routed to the right and of course d-moxus can have as many outputs as you want using the same

**[14:35]** decoder technique I showed with the mux finally let's talk about some combinational devices that use signal strength or hexadecimal this device is called a red coder it takes in a signal strength value and it lights up the corresponding lamp inputting 7 will light up the seventh lamp or inputting 15 will light up the 15th lamp the way this works is actually really clever

**[14:57]** first it splits your input into two lines where the top line has one less strength than the bottom for example if I input a 6 the bottom line starts with six and decays but the Top Line starts with five ndks notice that when you do this the sixth column is special it's the only one where the bottom line is powered but the top one isn't and this works for any number if you input a

**[15:21]** three now the third column is the one that's special so really all a red coder does is detect that special column and depending on the design it might detect it in a few different ways to me the most obvious way to detect it would be with xor Gates on every column if you did that then these columns and these columns would all output 0 but the special column would output one oh and

**[15:43]** red coders can be vertical as well here's a super small vertical design I actually use this in my Flappy Bird game to show the bird and while we're on the topic of hexadecimal here's a converter from hex to Binary and from binary to hex I've actually covered these in a previous video so check that out if you're interested in more detail but in summary this one takes a hex number and

**[16:02]** outputs the binary equivalent while this one takes a binary number and outputs the hex equivalent and both of these designs only take two ticks which is honestly really cool next episode is another fun one we'll be taking a look at latches and flip-flops if you enjoy these videos subscribe and consider checking out my patreon page in the description I also have a redstone

**[16:21]** Discord server so come join us if that sounds interesting I hope if you learned something I hope you enjoyed peace out guys [Music] foreign [Music]
