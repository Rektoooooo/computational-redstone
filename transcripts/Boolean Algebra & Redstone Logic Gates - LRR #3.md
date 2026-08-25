# Boolean Algebra & Redstone Logic Gates - LRR #3

- **Channel:** mattbatwings
- **URL:** https://www.youtube.com/watch?v=J36WJHaFPGc
- **Duration:** 15:45
- **Transcript:** English (auto-generated)
- **Saved:** 2026-08-25

---

**[0:00]** hi guys and welcome back to logical Redstone reloaded today we're finally going to build our first Redstone Circuits but first let's talk about the fundamental idea behind every circuit we'll ever make logic what is logic why is it useful and how can we implement it with redstone if you're not already familiar with binary I highly recommend watching the previous episode binary and

**[0:19]** some hexadecimal will be extremely important for the rest of this series so without further Ado let's get started throughout history humans have always been eager to quantify logic whether it was to question things like morality or to reason about the laws of nature humans are always trying to gain a deeper logical understanding of the world around them as a result countless

**[0:36]** systems of logic Math and Science have been developed all over the world in the mid-1800s a system was published by a man named George Poole called Boolean algebra nowadays Boolean algebra is the foundation behind digital logic as well as many other applications so how does it work just like normal algebra Boolean algebra has variables but instead of taking on any possible value these

**[0:58]** variables can only have two values true or false one or zero Boolean algebra also has operations similar to addition or multiplication that you would see in normal algebra Boolean algebra has logical operations the three most basic ones are and or and not let's look at these in more detail first we have the not operation also referred to as negation in Boolean algebra it's

**[1:21]** signified with this negation symbol but in other notations like in programming you might also see it expressed as an exclamation point the not operation simply outputs the opposite of what it's given let's say I have this expression the negation of a a is a variable so I don't know what it is but I know it's either true or false so let's make a table to describe both possibilities as

**[1:43]** well as what the output would be we have two possibilities for a and the output in both scenarios is just the opposite of a because it's being negated this table is saying that if a is false not a is true and if a is true not a is false this type of table where you list all the possibilities is called a truth table one interesting property about negation is that if you do it twice

**[2:06]** you're back to where you started this means that the expression not not a is equivalent to a in other words they will always have the same truth value no matter if a is true or false next we have the or operation also referred to as disjunction in Boolean algebra it's signified with a V symbol or sometimes with what looks like addition and in programming it's often expressed with a

**[2:27]** vertical bar let's look at the expression a or b or outputs true if a or b is true A and B are variables and once again I don't know what they are so I'll make a truth table with a b and the output A or B this time our truth table needs four rows because we have four possibilities for A and B now according to the or operation we output true when at least one of them is true by looking

**[2:54]** at the table we can see that that corresponds to these three rows the only time that a or B is false is When A and B are both false and that's the truth table for the or operation finally we have the and operation also referred to as conjunction it's signified with an upside down V symbol or sometimes with what looks like multiplication and in programming it's often expressed with

**[3:14]** the and symbol sorry I do not have enough resolution here for a good and symbol this is terrible the expression A and B outputs true if both A and B are true so once again we can make a truth table with the four possibilities for A and B the only row that outputs true is the one on the bottom where both A and B are true the other three rows are false also if you didn't notice already these

**[3:37]** three operations work the same way that they do in conversation let's say Bob is a man wearing a blue shirt if I said the statement Bob is a man and Bob is wearing a red shirt you'd say that's false because even though he's a man he's not wearing a red shirt he's wearing a blue one both parts of the statement have to be true for the whole thing to be true but if I said Bob is a

**[3:56]** man or Bob is wearing a red shirt you'd say that's true because Bob is a man the other parts of the statement don't matter as long as at least one of them is true alright awesome so those are the three basic operators of Boolean algebra and once you have these operators you can also start to create what are called laws a law of Boolean algebra is just a small Boolean expression designed to

**[4:16]** show some property or fact for example if I have X or 0 this will always be equal to just X this is called the identity law or if I have X or 1 this will always be equal to 1 because the or operator doesn't care what x is it's going to Output true either way this is called the annihilator law and lastly one of the most important laws in all of Boolean algebra is called de Morgan's

**[4:43]** law it states that the negation of an and operator is equivalent to Distributing the negation and switching it to an or operator and the reverse is true as well so de Morgan's tells us that you can distribute a negation as long as you swap the operator this is a really powerful law and it's used all the time of course you can always just prove it with a truth table and I

**[5:04]** encourage you to do so but another way to think about it is like this if a and b are not both true then that means either a is false or B is false there are a bunch of other laws I could go over but I'll save that for you to look at in the description if you're interested what I do want to go over though is analyzing a Boolean expression because now we have the tools to do so

**[5:26]** let's take a look at this Boolean Expression A or B N not C our truth table needs eight rows to cover the eight possibilities of a b and c and by the way the number of rows we need is always 2 to the power of how many different variables there are in this case two to the third is eight okay now let's start to think about when this equation would be true the first thing I

**[5:48]** notice is that when a is true the whole thing is true right we know that from the annihilator law the or gate doesn't care what this second quantity is as long as a is true the whole thing will output true so let's mark true on all the rows where a is true which is just these bottom four rows because on these rows a is one now for the other four rows a is false but that's not enough to

**[6:13]** conclude what the or gate will evaluate to we still have to look at the second part because the second part might make the or gate become true again so the question is when is B and not see true well I kind of just said it it's true when we have B and not C in other words when B is true and C is false and if we look at the four remaining rows there's only one row where that's the case b is

**[6:40]** one C is zero so right on this row we need this to be true the last three rows have to be false because we've shown that both sides of the or are false and that is our finished truth table now we know what this expression will evaluate to for any combination of a b and c if you have any doubts about this or if you're brand new to Boolean Algebra I highly recommend going through each row

**[7:04]** one at a time plugging in the truth values and seeing if the output makes sense and if you want more practice try filling out the truth table for these Expressions I'll put the Solutions in the description alright awesome now before we start building circuits I want to talk about one more operation the exclusive or also known as xor even though it's 10 technically not one of

**[7:24]** the three basic operations it's still extremely useful and used everywhere here's the symbol for it it's like a circle with a plus sign on it and in programming it's often expressed with the carrot symbol the way it works is it outputs true if only one of the inputs are true here's the truth table for it it's pretty similar to or the only difference is that when both inputs are

**[7:46]** true xor outputs false because you can't have both it's exclusive okay now let's finally talk about circuits to use Boolean algebra to its fullest potential we should build circuits that mimic these logical operators these types of circuits are called logic gates there are four logic gates that correspond to the operations I've talked about so far the not gate the or gate the and gate

**[8:08]** and the xor gate all of these Gates essentially just Implement their operation on real binary signals and they follow the exact same truth table so let's check out each one and how to build them with redstone first not Gates these are represented in logic diagrams with a trying angle and a DOT on the end of it they literally just take a binary input negate it and give a binary output

**[8:29]** and lucky for us there's a redstone component that's specifically designed for not Gates the redstone torch if I have a wire connected to a redstone torch the output is the negation of the input this is a not gate and although this is the most common way to make one there are plenty of other ways for example I can make one with a comparator on subtract mode that's being powered

**[8:49]** from the back the input to the not gate is the side of the comparator as you can see when the side is not being canceled the output is one but when you cancel the side the output is zero next let's make an or gate here's the symbol for it in logic diagrams it takes two binary inputs and gives one binary output the funny thing is with redstone or gates are stupidly easy because they're

**[9:11]** already built into how Redstone wire behaves if I take two wires and connect them into a single wire then as long as at least one of the inputs are on the output is on so technically this is an or gate yeah not very complicated and just in case you want some other variations here are some examples you can play around with them in the World download in the description next let's

**[9:32]** make an and gate this is the symbol for one and of course it just outputs one when both inputs are one unfortunately in Redstone there's no super easy way to make an and gate it's not built directly into any components however if you have not Gates and or Gates you can actually construct an and gate out of them that being said this is a perfect opportunity to try to make one yourself if you don't

**[9:53]** want to do it in Redstone you can also just draw it as a logic diagram as a hint you need at least three not Gates and one or gate pause the video now if you want to try it all right welcome back and here it is we have not Gates on the inputs then they go into an or gate and then one more knock gate on the end so to check our work let's build this with redstone and

**[10:12]** see if it actually behaves like an and gate okay here's a super small version of it these torches pointing up are the first two not Gates this dust in the middle is the or gate and this final torch is the last not gate and as you can see the output is only on when both inputs are on awesome it's an and gate but why exactly does this work well the easiest way to see why it works is

**[10:35]** literally just by looking at the Redstone this final torch can only turn on if the dust turns off but the only way for the dust to turn off is for both of these torches to turn off which you can only do by powering both inputs another way to make an and gate is by using a comparator in subtract mode all you have to do is put one input in the back and a negated input in the side

**[10:58]** this works because the comparator will output a signal only if it has power in the back back and it's not being canceled from the side any other combination and you won't get an output so I guess I kinda lied when I said no component implements it directly you can fake it pretty well with comparators last up we have the xor gate the symbol for it is basically an or gate with a

**[11:19]** bar on the back just like the and gate there's no super easy way to make one with redstone but once again you can make it with just knots and ores and here's the diagram for it now I would build this but over the years people have created some clever designs that don't exactly follow this diagram the most common design is this one it uses two comparators on subtract mode as you

**[11:38]** can see it will output one if only one of the inputs are on if you input both it'll output zero the way this works is by abusing symmetry if both inputs are on then both comparators are receiving 14 signal strength in the back and in the side which means that they're both going to Output a zero but if only one of the inputs are on then one of the comparators is going to receive less

**[12:01]** strength in the side and then in the back notice how this one receives 14 and 14 still but this one on the right receives 13 and 11. 14 minus 14 is 0 but 13 minus 11 is 2. and when you combine both signals together the two trumps the zero so we get an output and this works the other way too because it's symmetrical the only bad thing about this design is that the output is a very

**[12:26]** low signal strength only two which basically forces you to use another repeater so another configuration you could use is this one this xor gate has a much higher signal strength on the output and yeah I've genuinely never had the need to use any other type of xor but just in case you're looking for more designs there's going to be more in the World download at this point you might

**[12:46]** be wondering why did I explain all that Boolean algebra stuff if we're just going to be using logic gates at the end of the day the reason is because as circuits get more complicated it gets harder to understand what they're doing just by looking at them Boolean algebra provides a language for you to stop thinking about Redstone and in instead think directly about the logic problem

**[13:05]** you're trying to solve also there are a bunch of Boolean algebra simplifiers online where you can type in an expression and it'll give you an equivalent expression as simplified as possible that is extremely useful because it can literally show you that you don't need as much Redstone the shorter your expression is the fewer Gates you need to implement it right for example let's say I'm designing a

**[13:25]** redstone game and I find out I need a circuit to implement this expression I get really sad because it looks super complicated but after plugging it into a simplifier turns out it's equivalent to Just A and B so yeah that's why I'm going to keep mentioning Boolean algebra throughout this series because it's a really nice tool before I end this video there are three more logic gates I want

**[13:45]** to talk about and don't worry they're extremely easy to remember the logic gates or and an xor have negated versions named nor nand and xnor the symbols for them are the same as the original symbols but with a DOT on the end to signify negation each of these Gates is equivalent to just taking the normal version and putting a not gate on the output for example this is the or

**[14:07]** gate from earlier and this is a nor gate if you want to make a truth table for a nor gate just take the or gate truth table and invert the output column change the ones to zeros and zeros to ones similarly to make a nand gate you can take the and gate from earlier and put a redstone torch on it like this although if you look at this carefully we have two torches in a row

**[14:29]** that's a double negation which cancels out so technically you can also just remove a torch instead of adding one that works too this is also a nand gate and lastly xnor of course you can always just slap a torch on the end like we did for the other ones that's an easy way to do it but another cool way to make an x-nor is by inverting one of the inputs of xor this is kind of unintuitive and

**[14:52]** it definitely does not work the same way for Nora and nand but it's a cool property that I learned recently you can prove it to yourself by testing it out or also by using Boolean algebra I'll put the Boolean algebra proof on screen right now if you want to take a look at it I think that's it for nor nand and xnor and with that we've covered the basics of Boolean algebra and the Seven main

**[15:12]** logic gates a lot of this video is essential to understand for the rest of this series so please check out the links in the description if you want more resources about these topics next episode we'll start using logic gates to create a redstone adder and some other cool circuits as well you definitely won't want to miss it if you'd like to support me in these videos consider

**[15:29]** subscribing or even checking out my patreon page in the description I hope you learned something I hope you enjoyed peace out guys all right foreign [Music]
