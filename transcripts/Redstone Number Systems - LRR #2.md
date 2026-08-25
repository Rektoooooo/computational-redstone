# Redstone Number Systems - LRR #2

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=fV8nrZo-o4s
- **Duration:** 9:27
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome to episode 2 of logical Redstone reloaded last episode I went over the basics of every Redstone component you'll need and how to use fabric mods now as much as I want to start building cool circuits we have to cover a few more fundamentals first specifically we need to learn about number systems if I were to describe logical Redstone in one word it would

**[0:18]** probably be numbers numbers make so many things possible from calculators to game systems to fully fledged CPUs but how much about numbers do you really need to learn for Redstone I mean assuming you're about five years old you already know what numbers are and how to use them well as it turns out the way you learn to think about numbers as a kid is not the only way to do it it's just the

**[0:39]** most popular one at some point you were probably told that there are 10 digits 0 through 9 but why are there 10 digits what if you only had five or seven would that break things and if it doesn't break things how can we exploit it to become better redstoners to explore these questions let's go back to school for a second and take a deeper look at how our number system works our number

**[1:01]** system is called base 10 or decimal it's a positional number system which means that the value of any digit depends on its position if a digit is all the way to the right on a number it's in the ones place but every place value to the left gets 10 times more valuable and if you go to the right even beyond the decimal point the place values get 10 times less valuable for example the

**[1:22]** number 321 literally represents three times one hundred plus two times ten plus one times one but why do we do this why do place values have this relationship well I think the easiest way to see why is by counting let's say that all you have is the ones place and you want to count up as high as possible so you start at zero and start counting up one two three all the way to nine and

**[1:45]** at this point you've counted up nine times you've stayed completely in the ones place so there's no problem but if you want to count up one more time you have an issue there's no symbol you can put in the ones place to signify a ten so without making a new symbol how do you signify that you've counted up 10 times I mean you can make another one's place but then what's gonna happen when

**[2:05]** you get to 30 or 40 that strategy won't scale very well the genius of our number system is to instead create a new column with more value the tens place by doing so I can package up all the work I did in the ones place into a single digit in the tens place this one is all I need to show that I counted up 10 times and that's why place values have this relationship in base 10 every 10 counts

**[2:30]** of work you do in one place value is equal to one count of work in the next place value okay now that we have a good understanding of base 10 let's go back to my earlier question what if you don't have 10 symbols well let's try it out let's say we're using a new number system where there are only four symbols zero one two and three just like before I'll start with a zero in the ones place

**[2:52]** and count up one two three and I ran into a similar problem there's nothing I can put in the ones place to make to four at least not with these symbols so a good solution would be to make a Four's place and put a one there to be super clear what we're saying here is that the number one zero represents four in this new system because it's one four and zero ones and that's pretty weird

**[3:18]** right we're so used to seeing one zero and automatically thinking that it means 10 but that's only true in base 10. in this new system that I just created one zero means four and naturally we'll keep multiplying the place values by 4 as they go to the left 4's Place sixteenths place 64's place Etc as you might have guessed already this number system is called Base Four

**[3:41]** and the amazing thing is nothing broke there's nothing wrong with expressing numbers in base four instead of Base 10. in fact every number in base 10 has a base 4 equivalent for example 3 2 in base 10 or 32 is 2 0 0 in base four three tens and two ones is equivalent to two sixteens and speaking even more generally you can express numbers in whatever base you want let's say I

**[4:09]** wanted to express 123 in base 7. the base 7 place values are going to multiply by seven so one seven Forty Nine Etc and I can only use seven symbols zero through six as it turns out 123 is made up of 249s three sevens and four ones so two three four is 123 in base 7. okay now we know how bases work and it's clear that every base is an equally valid number system so if our

**[4:39]** goal is to express numbers with redstone which base should we use well if we pick a base that naturally resembles the state of redstone it'll probably make things a lot easier there are two common ways to view the state of redstone you can view it as just on or off giving you two different states or you can view it in terms of its signal strength which gives you 16 different states zero all

**[5:02]** the way to 15. as a result the most common basis to use with redstone numbers are base 2 and base 16. let's talk about base 2 first base 2 is also called binary it uses two symbols zero and one typically Redstone that's off is used to represent zero and on represents one just like every other base we start with the ones place and then the place values scale by the base in this case

**[5:25]** they go one two four eight sixteen Etc as a quick example let's convert 25 into binary I I can make 25 with 116 1 8 and 1 1. I don't need anything else so let's fill these in with zeros and there we go 25 in binary is one one zero zero one if you're brand new to Binary and want some more practice try these conversions out getting comfortable with binary is really important for logical Redstone so

**[5:53]** I highly recommend it for some terminology a single 0 or 1 can also be referred to as a bit therefore 25 and binary is 5 bits long just be a little careful with that though because for example 25 can also be an 8-bit number all you have to do is add three more zeros to the left and now you have an 8-bit representation for the number 25. and by the way 8 Bits is so commonly

**[6:18]** used in computer science that it actually has a special name it's called a byte with that being said let me ask you a question how many different numbers can you represent with one byte of information pause the video now if you'd like to try to find the answer all right welcome back the correct answer is 256. there's a few different ways you could have gotten that answer

**[6:39]** you could have looked at it as a combinatorics problem I have two choices for each bit and so two times two times two eight times or two to the power of 8 is 256. you could have also noticed that the smallest number we can represent with eight bits is zero while the biggest number is 255 and the range from 0 to 255 has 256 values either way is equally valid the point is in general n

**[7:06]** Bits of binary can represent 2 to the N unique values now let's talk about hexadecimal hexadecimal has 16 symbols because it's base 16. 0 through 9 and then a b c d e f you don't usually see letters in numbers so this can be kind of weird to get used to but the most natural way to view it is that a means 10 b means 11 all the way to f means 15. and as expected our place values go 1 16 256

**[7:35]** Etc so as an example let's figure out what the hexadecimal value 9bf is in decimal we have 9 times 256 plus 11 times 16 because B is 11 plus 15 times 1 because f is 15. after doing the math we can see that 9bf in hexadecimal is equal to 2495 and yeah there's not a ton I can say about hexadecimal other than saying it's really useful to know in my experience I don't use hex as often as

**[8:06]** binary but considering that signal strength values are literally made to be hexed digits it can be a really useful tool the last thing I want to show you in this video has to do with the relationship between binary and hex because it's really cool you see since 16 is a power of 2 converting from binary to hex or from hex to Binary is really easy so easy that you don't even

**[8:28]** need a calculator let's say I have this long binary number I don't even know what the number is but to convert it to hex I don't have to all I have to do is split it into groups of 4 bits starting from the right like this each group of four bits is exactly representative of one hex digit if you look at this first group we have 0 1 1 0 which is binary for six the middle Group 1 1 1 1 is 15

**[8:53]** or F and the last group is four therefore this binary number in hexadecimal is six F4 and that's it for me about number systems like I said binary and hex are super important for logical Redstone I highly recommend getting comfortable with them next episode we'll start talking about logic and build our first Redstone Circuits I'll see you there I hope you learned something I hope you

**[9:16]** enjoyed peace out guys foreign
