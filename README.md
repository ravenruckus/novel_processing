#Novel Processing 

## Question
How 
to predict which novels will be popular? 

What are the patterns of popular novels when taking into consideration certain elements such as tone, emotion, the variance of sentence length, and structure?

## Known Data - Exploritory Stage

### Sentiment Pattern
The first novel I chose to explore using data science methods is the *Wizard of Oz*. It is the novel that Christopher Vogler uses as an example in his book *The Writers Journey*. He explains how the story follows the hero's journey as taught by mythologist Joseph Campbell. 

After breaking the *Wizard of Oz* up into twenty pieces and running a sentiment analyses on the individual pieces I discovered that there are five major dips in sentiment landing around the same location in the novel as the turning points in Michael Hauge's Six Stage Plot Structure. 

![Six Plot Structure](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/six-plot.jpg)
### Wizard of Oz Sentiment Pattern
![Wizard of Oz](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/wizard_of_oz_sentiment.png "Wizard of Oz")

For example the 75% mark of the Wizard of Oz and fourth major dip in sentiment corresponds with Turning Point #4 and Major Setback on Michael's diagram. 

"We have lost our way," said Dorothy.

In this section Dorothy learns that the cap on her head has a charm that gives three wishes to the wearer. The flying monkeys must fulfil the wishes. While the monkeys are fulfilling Dorothy's wish by carrying her and her friends back to the Emerald City they tell Dorothy the sad yet beautiful story of how the golden cap came to be. 

Towards the end of this section after they finally arrive to the Emerald City we read "They thought the Great Wizard would send for them at once, but he did not. They had no word from him the next day, nor the next, nor the next. The waiting was tiresome and wearing, and at last they grew vexed that Oz should treat them in so poor a fashion, after sending them to undergo hardships and slavery."

Not all novels share this same pattern.  
##Examples of Novel Sentiment Patterns

### Alice in Wonderland
![Alice Wonderland](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/alice_wonderland.png)
### Pride and Prejudice
![Pride and Prejudice](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/pride_prejudice.png)
### Ulysses
![Ulysses](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/ulysses.png)
### Tale of Two Cities
![Taleof Two Cities](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/tale_two_cities.png)
### Sherlock Holmes
![Sherlock Holmes](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/sherlock_holmes.png)
### Dracula
![Dracula](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/dracula.png)
### Jungle Book
![Jungle Book](https://github.com/ravenruckus/novel_processing/blob/master/novel_processing/images/jungle_book.png)




In addition to sentiment patterns I've also developed python code that extracts additional data from the novels on the [Gutenberg Project](https://www.gutenberg.org/browse/scores/top) website. The code generates CSV files that contain syllable count per word and sentence, the character count per sentence, the sentiment score for each sentence and cluster groups for each sentence. 


##Clusters

I found generally when I excluded the syllable count that most novels followed a pattern of sentence length to sentiment score.  
 
* Short Sentences to Low Sentiment  
* Long Sentences to Medium Sentiment  
* Medium Length Sentences to High Sentiment  

Frankenstein and Sherlock Holmes were two that didn't follow this pattern. However, Sherlock's sentiment values did not have a wide range and Frankenstein's sentence length did not have a wide variance.

I am in the process of exploring more novels. 

## Next Step - Visual Exploratory Stage 

I spent this last summer learning d3.js, the JavaScript library, and I am really excited to start displaying the novels interactively using what I've been learning. My first step is to display the sentiment patterns of the novels via bar charts. When the user clicks on a bar they will be able to read the sentences that correspond with that section of the novel. It's really fun to read the highs and lows of the different novels. I will have this up on  my website soon. 

When looking at Alice in Wonderland's bar chart I became curious to read the section whose sentiment mean dipped far below any section in all of the novels I was looking at. The first few lines of this section read: 

>"Oh, don't bother ME,' said the Duchess; 'I never could abide figures!'
And with that she began nursing her child again, singing a sort of lullaby to it as she did so, and giving it a violent shake at the end of every line:     'Speak roughly to your little boy,     And beat him when he sneezes:    He only does it to annoy,     Because he knows it teases.'"

This whole section is really strange. 
 
After I finish this part of the project I will create code to generate an individual web page for each novel based on their data where users can interact with the novels in ways that they may not have been able to do before. 



## In the Future

After I finish this exploratory stage of the project I will then, with the aide of the data science lessons I acquired through General Assembly figure out which features predict popularity and create a model that I can use to predict whether a novel will be popular or not. 

## Why This Project?

I chose this topic for my data science project because I have been attempting to write novels for a long time and have read and studied a decent amount about it and still feel overwhelmed with the process of novel creation.

I would like to create a model that I can run my novels through to predict whether they will be popular and then possibly make changes to help them fit the model more closely. 

After studying and thinking about story structure for over a decade as a hobby, looking at novels through the lens of data science is a whole knew experience and as a side benefit I think it is engraining into me the natural flow and structure that novels take on. It will be exciting if this shows in my natural writing flow.

This project also brings together my newer love of web design and coding.