# Redstone Binary Subtraction - LRR #5

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=_fZP-r2yhnY
- **Duration:** 14:05
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to logical Redstone reloaded last episode I covered binary Edition and showed off some really cool redstone adders today we're going to take it one step further and talk about subtraction I hope you enjoy just like last time with addition binary subtraction is really similar to decimal subtraction you can subtract binary numbers on paper using a pretty simple

**[0:18]** algorithm and if you want you can make a circuit that directly implements that algorithm just like the full ladder however I wouldn't recommend doing that you see subtraction can actually be viewed as just another form of addition as long as you consider both positive and negative numbers for example if I want to subtract 6 minus 4 this is equivalent to 6 plus negative four they

**[0:39]** both equal two in general a minus B is the same thing as a plus negative B notice how this isn't a subtraction it's an addition between a positive number and a negative number therefore if we could somehow represent negative numbers in binary then maybe we could just reuse an Adder to simulate subtraction so let's try to represent negative numbers in binary in math negative numbers are

**[1:02]** written with a negative sign in the front and although not as common positive numbers can have a plus sign that sign is one extra bit of information right it has two states and the state of it tells you the sign of the number so why not just copy that strategy in binary let's make the first bit of a number the sign bit 0 means positive and one means negative and the

**[1:23]** rest of the binary number will have the normal place values this format is called signed magnitude notation because the number consists of a sine and a magnitude the sign is the first bit and the magnitude is the rest of the number for example let's say I have 1 1 0 1 in sine magnitude notation the sine bit is 1 so it's negative and the magnitude is one zero one or five so one one zero one

**[1:46]** in this notation is negative five or let's say I have zero one one the sine is zero and the magnitude is seven so this is positive seven one important thing about this format is that you need to know how many bits you're working with one one zero one is only negative five if you're working with four bits if you were working with five bits this could be interpreted as positive 13 or

**[2:09]** if you were working with three bits it could be negative one but anyways this is a pretty solid way to represent negative numbers it's simple and it's kind of what we're already used to when we read numbers and here's a table that shows all the different four bit numbers and what each one represents in sine magnitude notation one weird thing about this is that we have two representations

**[2:28]** for zero both positive zero and negative zero but oh well maybe it doesn't matter what matters more is does this format work if you add positive and negative numbers together because that's our ultimate goal well let's try it out I've got a 4-bit CCA here if we add positive five plus negative five we get this remember we need to stay in four bits here so let's just ignore the carryout

**[2:53]** and it looks like we got positive two that's not great we wanted a zero not a two clearly adding positives and negatives together with sine magnitude does not always work so back to the drawing board I guess all right well even though this answer was not what we wanted I want you to notice something interesting that happened during that Edition we added two numbers together

**[3:15]** and the result got so big that it couldn't fit in the same number of bits anymore we got a carryout and in a way our Adder overflowed this idea of overflowing an Adder is actually the k key behind simulating subtraction with addition let me show you what I mean let's say I'm working with 4 bits and I want to subtract 6 minus two now six minus two is four but again we're trying

**[3:37]** to simulate this using addition so the question is can we add something to 6 that has the same effect as subtracting 2 as it turns out you can if you add 14 instead then 6 plus 14 is 20. but notice that it overflowed so we ignore the 16 bit and the answer is 4. therefore adding 14 has the same effect as subtracting 2. as long as you stay in four bits okay so let's just say that 14

**[4:07]** or 1 1 1 0 is the representation for negative two and now you can even test this on the CCA 6 plus negative two is four this representation for negative 2 is basically so big that it overflowed the adder and wrapped around to get give the correct answer again a really good analogy for this is a clock on a 12 hour clock instead of going two hours backwards you can also go 10 hours

**[4:35]** forwards both of those get you to the same time also if you go past 12 like maybe 13 o'clock that's the same thing as one o'clock this is called modular arithmetic you could say that a 12 hour clock has a modulus of 12. and in mathematics you can express this by saying 13 equals 1 mod 12 because 13 and 1 are both one past a multiple of 12. and since two hours backwards is the

**[5:02]** same as 10 forwards you can also say that negative 2 equals 10 mod 12. now since we're working with only four bits this is the same thing as mod 16 or a 16 hour clock if you want to look at it that way remember how 20 was the same thing as 4 well that's because 20 is 4 past a multiple of 16. 20 equals 4 mod 16. so vote to find a good representation for a negative number all

**[5:29]** you have to do is find an equivalent positive number in that modulus in mod 16 negative 2 is equal to positive 14. that's why 14 works really well as a representation for negative 2 when you're working with 4 bits and by the way a little shortcut to find it is to just take the modulus minus that number 16 minus 2 is 14. therefore 14 must be a good representation for negative two as

**[5:54]** another example let's say I wanted to do 7 minus 3 and I'm working with 5 bits working with 5 bits is the same thing as mod 32. in general working with n Bits is the same thing as mod 2 to the N so we can find a good representation for negative three by doing 32 minus 3 which is 29 and sure enough if you add 7 plus 29 or 7 plus negative 3 and ignore the Overflow you get four perfect alright

**[6:23]** we're making great progress let's design a notation for for negative numbers based on this new knowledge I'll make the positive numbers the same thing that they were inside magnitude no reason to change those but then for the negative numbers I'll make them all 16 minus the positive version because 16 is the modulus for 4 bits for example 16 minus 5 is 11 so with representation for

**[6:45]** negative five is eleven or one zero one one this notation has a special name it's called two's complement two's complement is the most popular notation for negative numbers in computers and for good reason it has a ton of advantages the first and most important Advantage is that it allows us to reuse adders to perform subtraction for example let's do five plus negative four

**[7:07]** according to the table five is zero one zero one and negative four is one one zero zero and we get one beautiful the other Advantage is that it's really easy to go from a number to its negative version or its complement to take the complement of a number all you have to do is invert all the bits and add one for example let's go from positive three to its complement negative three in four

**[7:33]** bit two's complement positive three is zero zero one one inverting all the bits gives us one one zero zero and then adding one gives us one one zero one so negative three is one one zero one and sure enough if we invert all the bits and add one again we're back to positive three that makes sense because the complement of a compliment cancels out also what's kind of cool is zero is its

**[7:56]** own complement if you take the complement of zero you just get zero back inverting gives you all ones and adding one rolls over to zero again now this invert and add one trick can feel very magical and honestly you can go your entire career without understanding why it works and you'll probably be just fine but I like understanding why things work so let me show you why inverting

**[8:17]** and adding one actually works remember that we got the negative version of a number by taking the modulus minus that number and because we're in binary the modulus is always some 2 to the N like 16 for example now if I have 16 minus X this is the same thing algebraically as 15 minus X plus one fifteen in binary is all ones so 15 minus X has the same effect as inverting x one minus zero

**[8:43]** flips the zero to a one one minus one flips the one to a zero and then of course you can just add one therefore any 2 to the N minus X is equivalent to inverting the bits of X and adding 1. with this in mind we can now make a binary subtractor let's modify this Adder to make it do a plus negative b instead of a plus b I'll invert all the bits of B by adding a bunch of torches

**[9:08]** or not Gates and then I'll add one by turning on the carry in and now if we put in seven minus three we get four or two minus five is one one zero one that is negative three by inverting the B input and adding one with the carrion this Adder is now a subtractor it computes a plus negative b instead of a plus b and another amazing property of two's complement is that we still have a

**[9:39]** sine bit notice how the positive numbers start with zero and the negative numbers start with one so that's pretty useful okay so this subtractor is great but it can kind of only do some subtraction what if we still want to add sometimes as well is it possible to modify this in such a way that it could toggle between addition and subtraction well yeah I mean in that case you would need a

**[10:01]** circuit that just allows you to toggle between inverting D and adding one to not doing that anymore one way to toggle the inversion of B is to use xor Gates an xor gate can also be used as a conditional inverter if you imagine that there's a wire going from this lamp to this lamp then the other input controls whether or not the wire acts like an inverter for example if this is zero

**[10:25]** then there's no inversion the signal just goes through the wire as normal just like a normal wire would but if you set the control to 1 now there's an inversion 0 becomes one and one becomes zero just like a redstone torch so if you stack a bunch of xor gates on top of each other and or all of the control signals together into a tower you can now conditionally invert a binary number

**[10:48]** when the control is 0 0 the number just passes through normally when the control is 1 the number becomes inverted so if we add that to the B input we can now conditionally invert B and then to add one let's just look up the control signal to the carry in as well and now when this lever is on it's a subtractor the B input becomes negated and we add one using the carrion but when the lever

**[11:12]** is off it's back to being a completely normal Adder for example let's put in five and two when the lever is off it's Computing 5 plus 2 which gives us seven when the lever is on it's Computing 5 minus two which gives us three that is beautiful one really important thing I want to stress here is that notations only exist for the developer the hardware like an Adder does not know

**[11:38]** whether or not you're using signed numbers like twos complement or unsigned numbers like the normal binary we used last episode an Adder is just a logic circuit and it will do what it's told it's up to you to keep track of of what notation you're using and how to interpret the results additionally if you're not careful it's possible to land way outside the range of two's

**[11:57]** complement I mean the range of 4-bit 2's complement is only negative 8 to positive 7. that's all you can represent so if you try to do something like negative seven plus negative seven which is negative 14 that's way outside your range and the answer you end up getting will obviously be incorrect this type of error can be detected with proper circuitry but I'm not going to get into

**[12:20]** that in this video check out the links in the description if you want to learn more about overflow detection in two's complement but anyways this is really cool by using a tower of conditional inverters we can essentially switch between an adder and a subtractor another really cool thing about two's complement is something that I actually didn't know about until the comments in

**[12:38]** my last series pointed it out the sign bit of a two's complement number can be viewed as having a negative place value for example 1101 can be thought of as negative eight plus four 4 plus 1 that equals negative 3 and sure enough one one zero one is negative three this works for any two's complement number positive or negative and any bit size as well if I was working with 8-bit 2's

**[13:04]** complement then the sign bit would be the negative 128th place real quick the last thing I want to mention in this video is another notation for negative numbers called one's complement historically this was used in computers before two's complement became more popular it's very similar to two's complement the difference is that instead of inverting and adding one to

**[13:23]** take the complement you only invert however due to its long list of disadvantages it's rarely used in computers anymore only in rare scenarios but it's a good thing to know about because it'll still come up from time to time if you go into computer science next episode will be a really fun one it's about all sorts of combinational logic and all the best designs for them

**[13:42]** with redstone you do not want to miss it if you'd like to support me in these videos subscribe and consider checking out my patreon page in the description I also have Redstone Discord server so come join us if that sounds interesting I hope you learned something I hope you enjoyed peace out guys [Music]
