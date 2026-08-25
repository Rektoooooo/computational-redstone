# Can you write a Sorting Algorithm with Redstone?

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=x3p6hdUEGU4
- **Duration:** 4:58
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:01]** [Music] sorting algorithms if you're into computer science chances are you've heard of these before a sorting algorithm is an algorithm that takes a bunch of items and sorts them according to some property given a list of numbers a sorting algorithm could sort them from lowest to highest or given a bunch of colors a sorting algorithm could sort them into a rainbow there are infinitely

**[0:21]** many ways a sorting algorithm can be coded some are more efficient than others one popular and efficient sorting algorithm is called quicksort which uses pivots to sort in a divided conquer type of style another sorting algorithm is called bubble sort bubble sort uses repeated swapping to sort the list no matter the application sorting comes up all the time in programming but what

**[0:38]** about in minecraft can you make a sorting algorithm with redstone i recently studied sorting algorithms for school and that's what prompted my interest on this given a bunch of signal strength values can you sort them with just redstone so just for fun i started trying to make a bubble sorter with redstone a bubble sort uses one mechanic over and over again it compares two

**[0:57]** different values that are right next to each other and swaps them if they're in the wrong order if you repeat this enough times in enough places you'll end up with a sordid list of signal strengths i thought this would be a pretty easy mechanic to do with redstone because you can compare two signal strengths with a comparator right all you need to do is switch on subtract

**[1:11]** mode and compare the back value with the side value then you can use the output of the comparator to tell you whether or not you need to swap and after a few hours i finished this guy this is a signal strength bubble sorter it's actually pretty fun to watch i was proud of it and sent it to my buddies on the ore discord and of course someone already made it way faster and way better

**[1:28]** come on guys you can't be good at everything this is oscar 91's bubble sorter it takes 17 ticks from input to output and it's 5 hertz which means it can sort five sets per second where a set is eight signal strengths this thing is absolutely insane but how does it work well the way it works is with this magic circuit right here this circuit inverts both the signal strengths which means it

**[1:51]** takes 15 minus what they used to be and then it puts the lower value on the left and the higher value on the right all in just two takes for example if you input 2 and 4 it will invert them making them 13 and 11 and then the 11 goes on the left because it's lower and the 13 goes on the right because it's higher the first stage of this sorter uses four of these magic circuits so now our list

**[2:10]** gets a little bit more sorted however now the list is inverted so what now well inverted signal strengths can still be sorted it's just that now the priority is opposite of what it used to be for example if you have five and three and you ask which one's bigger obviously it's five but when you invert them now they become ten and twelve and so an inverted three is actually bigger

**[2:31]** than an inverted five in fact any number that's smaller in the normal realm becomes bigger in the inverted realm so if we attach another row of these magic circuits which face the opposite direction to account for the inversion it will just continue sorting the list gets inverted for a second time which means that you're back to your normal list if you repeat that setup three more

**[2:50]** times your list will come out fully sorted again huge thanks to oscar 91 for showing this to me this is pretty genius so genius that the man said yeah it's impossible to make it any faster and i thought no way let's prove him wrong and make a faster one after hours and hours and hours i was beginning to lose hope no matter what i did it seemed like the magic circuit couldn't get any faster unless i

**[3:14]** completely redesigned the sorter there's just no way i could wait redesign there's other types of sorts and then i realized counting sort could be faster accounting sort is pretty simple you count up how many of each type you have and then you reconstruct the list based on those counts for example if i have the list four three five four three i count two threes two

**[3:36]** fours and one five then i can just go through those counts and reconstruct the list in order i had seen circuits that count things in minecraft before they're called unary counters so i thought let's give it a try and after a couple of days and some help from my buddies fearless and slow me we did it this is a 5 hertz sorter that takes 11 ticks from input to output this circuit generates random

**[3:55]** signal strength lists at 5 hertz and the output is all of the sorted lists coming out 11 ticks later so although i didn't make a faster bubble sorter i definitely made a faster sorter and after spending way too much time on this i was satisfied is any of this actually useful for redstone builds probably not but i learned a lot about sorting algorithms and it helped me pass

**[4:17]** my final in school too i would explain the details of how it works but instead i'm going to leave you with a little bit of a challenge i want to see if you guys can make a sorter that's even faster using any method that you want the requirements are that the input and output both look like this you can use any components you want just not command blocks it would be really cool for it to

**[4:34]** be 5 hertz as well but then you can't use torches so don't worry about that if that's what's stopping you from making one if you make one that's faster than 11 ticks i'll show it off and shout you out in a video that's all i got i hope you learned something i hope you enjoyed peace out guys if they show love imma show it back if the catch is too small imma throw it

**[4:52]** back i've done a lot but i ain't gotta lock the show for that all right let's do that
