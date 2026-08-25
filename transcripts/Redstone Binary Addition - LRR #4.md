# Redstone Binary Addition - LRR #4

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=Hl1dHFOl3Zo
- **Duration:** 21:49
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to logical Redstone reloaded last episode we talked about Boolean algebra and logic gates today we're going to use those logic gates to build a binary Adder like I said last time if you haven't learned binary by now you're really going to want to there are a ton of resources in the description to do so including episode 2 of this series so without

**[0:16]** further Ado let's get started first let's define what the term binary Adder means a binary Adder is a circuit that takes two binary numbers as input and outputs their sum for example if I input 1 1 0 or 6 and 1 0 0 or 4 6 plus 4 is ten one zero one zero so how do you even approach something like this well I think the first step is to get super comfortable with binary Edition on paper

**[0:42]** we need to break down exactly what happens when two binary numbers get added together to do that let's first remind ourselves how to add numbers in decimal to add two numbers together you add the digits of each column together starting from the right for example if I have 43 plus 89 the first thing I do is three plus nine which is 12. so Mark a 2 here and carry the 10 to the next digit

**[1:04]** then we do 1 plus 4 plus 8 which is 13. so Mark a 3 and carry a 10 to the next digit again but there are no more digits to add it to only these invisible zeros so the carry can be directly written to the answer giving us a final sum of 132 okay easy enough now let's apply that same concept to Binary addition let's do five plus nine one zero one plus one zero zero one just like decimal we go

**[1:30]** column by column starting from the right for the First Column we have one plus one which is two but two in binary already takes up two digits it's one zero so let's mark a zero and carry over the one to the next column remember the next column is twice as valuable so this carried one is essentially worth two instead of ten now to add up the next column we just do one plus zero plus

**[1:54]** zero which is one next one plus zero is also one and finally zero plus one is one so five plus nine is one one one zero or fourteen let's do one more example this time I have seven plus six one plus zero is one one plus one is two so Mark a zero and carry and one plus one plus one is three three in binary is one one so let's mark a one and carry but once again we're carrying two

**[2:24]** invisible zeros so we can just write it on the output so seven plus six is one one zero one or thirteen perfect so that's how binary addition works as you can see it's pretty similar to decimal edition if you want more practice with binary Edition check out this video in the description it has great walkthroughs of more examples now let's make a binary Adder to to keep things

**[2:45]** simple let's start with the simplest possible adding circuit a circuit that just takes two binary bits A and B and outputs a single bit for their sum we have four cases for A and B the first three cases are zero plus zero equals zero zero plus one equals one and one plus zero equals one in other words the truth table with a b and sum looks like this now the fourth case is a special

**[3:06]** one one plus one is two but as I showed earlier this means the output is zero and we carry over to the next column so in our truth table the sum for one plus one is zero but that's only part of the story we need another output bit for the carry this new carry bit is one only when the input is one plus one let's also add that output to our little diagram and now this is the finished

**[3:30]** truth table for our Adder so to implement this with redstone which logic gates are going to be the most useful does the output for the carry or for the sum remind you of any logic gates in particular as it turns out the carry can be made with an and gate and the sum can be made with an xor gate the truth tables for these Gates match exactly what we want so let's grab those Gates

**[3:51]** and make this with redstone alright here it is as you can see we have an xor gate for the sum and an and gate for the carry and both inputs are just kind of going into both of them in digital logic this circuit is called a half adder a half adder takes in two bits and adds them together giving a sum and a carry just for good measure let's test out the half adder and make sure it works one

**[4:12]** plus zero is one zero plus one is also one and one plus one is two perfect okay so now we can add one plus one but what if we want to add bigger binary numbers together for that it's going to get a little more complicated but I think a good starting place would be to analyze exactly what happens in a column of binary addition at any individual column there are essentially three bits

**[4:38]** that you're adding up the top bit the bottom bit and the carry coming in from the previous column if there was one I'll call these three bits a b and carry in for example on this column A is zero B is 0 and the carry in is one but on this other column A is one B is 0 and carry in is zero once you add up these three bits you essentially produce two output bits the sum which is part of the

**[5:01]** final answer and sometimes a carry going out to the next column I'll call these output bits the sum and the carry out so if we could make a circuit that adds three bits together and produces a sum and a carry or you know the two bit result we could simulate a column of binary addition but the question is how well remember we have a half adder and a half adder can add two bits together so

**[5:26]** if we want to add three bits we can simply do two additions for example if you have one plus two plus three you're adding three numbers but it's not being done directly first you add the one to the two then you add the result of that to the three notice how you just added three numbers using only operations that add two numbers at a time transposing to circuits we can have a half adder that

**[5:47]** adds the first two bits and then have another half adder that adds the sum of that with the third bit and the final sum is output right here this nearly works the only problem with this is that you might get a carry from the first half adder or from the second one but that can be fixed with a simple or gate and now this circuit is called a full adder a full adder takes in three bits

**[6:10]** and adds them together giving a sum and a carry that's exactly what we need for a column of binary addition and if you're interested in the truth table for a full adder here's what that looks like there are eight cases for the three inputs a b and carry in and the output is the result of adding the three bits together for example on this row we have one plus zero plus one so the full adder

**[6:31]** produces two a carry and no sum which by the way corresponds to this case during binary addition now of course this is not the only way to make a full ladder all that matters in the definition of a full ladder is that it matches this truth table however you want to implement it is up to you but doing it like this with the two half adders makes the most sense to me but anyways let's

**[6:52]** test this out if we input a single bit no matter where it is we should get just a sum if we put in any combination of two bits we get a carry and all three bits gives a carry and a sum beautiful and of course if you're making one yourself I recommend checking all eight cases before using it okay now using this full adder we can construct a multi-bit binary Adder to do that let's

**[7:16]** reorient the inputs and outputs to look like this you'll see why in a minute A and B are on the bottom the sum is on the top the carry in is on the right and the carry out is on the left also now that we know how it behaves let's transfer to a more compact version to save some space this is a super small design for a full adder that's been around for a long time if you want to

**[7:35]** look at it more closely the World download is in the description but it really implements the exact same logic that I've drawn out here we still have the exact same inputs and outputs a b carry in carry out and sum now notice how during addition the carry out of one column becomes the carry in of the next one so to mimic this with redstone let's chain full ladders together like this

**[7:58]** plug in the carry out of each one into the carry in of the next one and now this is a binary Adder it's typically it's a 4-bit binary Adder by using a chain of four full adders we can now add any two 4-bit binary numbers together the first input to the adder consists of the four a bits the second input consists of the four B bits and the output is made up of the four sum bits

**[8:22]** let's go ahead and try it out five plus nine gives us 14. nice and seven plus six gives us 13. beautiful this type of Adder is called a ripple carry Adder because as it's calculating the carries Ripple across the adder now because of the nature of these full ladders we still have a dangling carry in on the first one and a carry out on the last one so what do we do with those

**[8:52]** well this carry in is representing a carry on the very first column which of course never happens on paper but if it did happen it would just be worth one right I mean we're just adding another one to the First Column for example if I add five plus nine plus one we get 15. if we get a carry out that means that the final column carried over in which case it gets written directly

**[9:19]** on the output so if you want you can wire the carryout to be part of the answer now if we input large numbers like 11 plus 14 . the output is 25.11001 notice how the carryout is the fifth bit of the answer and in general adding two n-bit numbers produces a number up to n plus one bits long the plus one is because of that final carryout okay so we just made a 4-bit

**[9:47]** ripple carry adder or RCA for short using this technique of chaining the ladders together you can make an Adder as big as you want for example this is what a 32-bit RCA looks like I really like RCA's because they're the easiest and most straightforward type of Adder to understand however they have a fatal flaw that makes them very unlikable in digital logic as an RCA gets bigger it

**[10:10]** takes longer and longer on average to produce the answer the carries have to take more time to propagate across all the full ladders for example if you add this huge number with just one more one yeah it's gonna take a while it would be really cool to have a synchronous adder or an Adder that takes the same amount of time to compute no matter what you input a well-known type of synchronous

**[10:34]** Adder is called a carry lookahead adder or CLA these are used in real Electronics as a faster type of Adder a CLA essentially adds more logic in the back of the adder to compute the carries all at once of course that's a big simplification and if you want to learn more about how clas work check out these videos in the description they're actually really interesting however I'm

**[10:56]** not gonna build a CLA with redstone instead I'm gonna dive into the world of redstone specific synchronous adders see over the years the logical Redstone Community has developed some really clever types of adders that abuse the weird quirks of redstone these adders are not replicable in real life they don't actually exist anywhere outside of Minecraft so let's briefly go over a few

**[11:18]** of these Redstone specific adders and then I'll go over my favorite one in more detail first we have the carry look everywhere Adder these adders were really common in the early days of logical Redstone being first popularized by a YouTuber named nuomaster this is an 8-bit carry look everywhere adder and it has a speed of 4 ticks meaning that no matter what inputs I give it the output

**[11:38]** will always arrive exactly four ticks later completely synchronized the Redstone mechanic being abused here is glass Towers these glass towers are used to combine carry signals from multiple places at once and to control how far they propagate I'm not an expert on this type of Adder so I'm not going to go into any more detail but you can play around with it yourself in the World

**[11:58]** download the inputs and outputs are diagonal which is kind of weird but let's go ahead and see what it looks like to add five plus three the five goes here the three goes here and we get eight one zero zero zero another type of redstone specific Adder is called an instant carry Adder these were also really common in the early days this is an 8-bit instant carry Adder made by

**[12:23]** q2ck it has a speed of 4 ticks and this time the inputs and outputs are horizontal the Redstone mechanic being abused here is Pistons blocking signals for example let's say I have a setup like this where a carry is coming in from the right and I want to control how far it propagates if I lift this piston it instantly travels to the rest of the outputs but if I want to stop the

**[12:43]** propagation at a certain point I can just block it off stopping it from reaching any future outputs again this is a huge simplification because I'm not an expert on this type of Adder either once again let's add the classic five plus three and we get eight okay so both of these are great and at one time these adders along with a few other types were pretty common but in 2015 a

**[13:05]** revolutionary new type of redstone Adder was invented by magical gentlemen called the carry cancel adder or CCA and even today ccas are still one of the most common adders to use in logical Redstone here's an example of what a CCA might look like the cool thing about ccas is that they're vertical which makes them easier to work with and feel more Compact and they're completely

**[13:26]** pistonless unlike the instant carry adder and that removes any chance of weird timings as you can see if I add seven plus one we get an 8 completely synchronized I use ccas for everything now and a lot of people view them as the Holy Grail of redstone adders so let's dive into how they work just like most fast adders the first thing a CCA does is it computes all the

**[13:52]** carries at once what I mean by that is it calculates all the little numbers that you would write above the columns during an addition problem for example let's say I have five plus three definitely haven't used these numbers in this video yet if you go ahead and add these the normal way then after you're done you had to carry a one three times here here and here

**[14:10]** they didn't carry to any other columns let's mark those with zeros so when I say the carries I'm referring to this top row now like I said a CCA computes all the carries first and I'll explain how it does that in just a bit what's more important to understand here is that if you are somehow magically given these carries the rest of the addition problem is really fast for a circuit to

**[14:32]** compute this is because you don't have to start at the rightmost column anymore if you're already given the carries you can calculate the sum for every column all at once in other words the problem is parallelizable there's no more dependencies between the columns if we go back to the full ladder and look at how the sum is calculated we can see that it's calculated by taking a X or B

**[14:54]** X or C which is the same thing as just adding three bits together and only looking at the rightmost bit therefore if we apply a X or B X or C to each column we get our final answer we didn't even have to think about carrying or anything the carries were already given for example in this First Column we have 0 xor one xor 1 which is zero so clearly if you want to make a fast Adder all of

**[15:19]** your energy should be devoted to just figuring out what those carries are and that's really what these Redstone specific adders work so hard to do they all use some special trick to generate the carries alright so how exactly does a CCA figure out those carries a CCA generates the carries by a process called carry cancel that's why it's in the name let me show you how that

**[15:40]** process works let's say we want to generate the carries for five plus three anytime you see a column with two ones you know for sure that it's going to create a carry so create a signal of ones going to the left forever called a carry signal then anytime you see a column with two zeros you know that the carry will not be able to continue so create a signal of zeros going to the

**[16:02]** left forever called the cancel signal which trumps any previous carry signals now if you get another carry signal later it creates once again because carries have priority over previous cancel signals but of course eventually you'll hit another zero zero which once again cancels it forever after this process you're left with a string of ones and zeros amazingly this string is

**[16:25]** the carries it's just shifted over by one so yeah that's how a CCA works it runs the carry cancel process to generate all the carries and then computes a X or B X or C on each column at the same time to get the sums pretty cool right at this point if you want to just download the world and use the CCA feel free I totally respect that but for the people that want a greater understanding

**[16:49]** let's go over how all the Redstone of a CCA works it's actually really clever first the carry cancel process this is done using two glass towers with comparators on subtract mode the tower in the back is for the carry signals and the one in the side is for the cancel signals as you can see if we get a carry signal it travels up forever but not down because that's how glass towers

**[17:11]** work since this is a vertical Adder that's the same thing as traveling left but not right on paper and if we get a cancel signal later on it cancels it forever this is because at every layer the side has a higher signal strength than the back which means all the competitors on subtract mode will output zero then if we get another carry signal later it's able to generate again

**[17:33]** because all the signal strengths are higher than the cancel below it but if you get another cancel of course it cancels it forever one thing to note here is that this only works for up to eight bits beyond that the signal strength might run out and this thing doesn't work anymore in fact most Redstone specific adders are only 8 Bits for similar reasoning it all comes

**[17:54]** down to signal strength but anyways this is really cool by putting in the carry signals here and the cancel signals here we can generate all the carries of the addition problem at the same time and it only takes one tick to calculate because all these competitors are working in parallel that's why it's so fast the next part of a CCA is these two input Towers A and B and an xor gate at every

**[18:17]** single layer now remember we want a carry signal when both bits are one and a cancel signal when both bits are zero for the cancel signal we can implement it with a torch like this this torch will only be on if both bits are zero in other words it's a nor gate then for the carry signal since we're detecting both bits being one ideally we would Implement that with an and gate instead

**[18:43]** though I'm gonna do something a little weird I'm going to invert the output of this xor to make it an x-nor instead and use that for the carry this is almost an and gate except for when both bits are zero but when both bits are zero we get a cancel signal anyways so it doesn't actually matter we're good okay perfect real quick let's try generating the carries if we input five plus three the

**[19:09]** carry signals are one one that is perfect the last thing to do is for each bit compute a X or B X or C we already have an xor gate in the back so we can just grab a X or B from right here then let's make another X or gate to xor that with the corresponding carry and that is the finished CCA Adder you can probably see why people like them so much now they're just elegant oh and by the way

**[19:36]** just like most adders ccas have a carry in and a carry out the carry-in is all the way down here it's powering the very bottom of the carry Tower and the carryout is right here it's the highest output of the carry Tower this also means that if you want to have a CCA with more than 8 Bits you technically can all you have to do is stack two 8-bit modules on top of each other and

**[19:57]** connect the carry out to the next carry in you're going to lose some speed though and the synchronization gets all weird so honestly I don't recommend this unless you really know what you're doing 8 Bits is absolutely plenty for 99 of redstone applications but it's cool that it's an option because of the way I built this CCA the speed is five ticks and that's plenty

**[20:17]** fast enough for me in most cases however just because I think it's interesting I want to show you just how crazy optimized ccas have become recently this is a CCA made by my friend Don and it's only three ticks that might not seem very different from five but when you're using an Adder over and over and over again the time save is huge I'm not even going to pretend to understand how this

**[20:37]** works all I know is that a lot of really smart engineering went into making this and here's another three tick CCA made by my friend Fearless this one is special because not only is it pistonless like the other ones it's also torchless this has the advantage that you never have to worry about torches burning out if you're Computing many additions in succession which is

**[20:55]** attractive for something like a computer where you really want it to be 100 reliable and finally this is a hexadecimal CCA made by yellow bunny the inputs are two four-digit hexadecimal numbers using signal strength and the output is a five digit HEX number also shown in signal strength great job guys you should be proud of these and thanks for letting me show them off with that I

**[21:17]** think I've covered pretty much all I know about Redstone Edition dude it doesn't even fit in render distance anymore next episode we'll be talking about negative numbers and how to use them if you want to support me in these videos subscribe and consider checking out my patreon page in the description I also have a Discord server full of redstone nerds so come join us if that

**[21:34]** sounds interesting I hope you learned something I hope you enjoyed peace out guys [Music] foreign
