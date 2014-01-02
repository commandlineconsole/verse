verse
=====

## Sentiment classification
* This program attempts to classify the main sentiment behind poems (love, joy, sadness, surprise, anger, fear) by evaluating the number of [positive and negative words](http://www.cs.uic.edu/~liub/publications/kdd04-revSummary.pdf) in a poem
* This program was trained on poems from [poemhunter](http://www.poemhunter.com/), many of which are tagged by the main emotion contained in them
* Much of this data is subjective, but using a large sample size, it is able to make an educated guess about the primary emotion of a poem


## NLTK
* This program uses the python nltk for many supporting function including:
    - synonyms from wordnet
    - Naive-Bayes classifier
    - corpus utilities


## Running
* Download all of the python dependencies (listed below)
* run `poems.py` from the root directory IF there are no poems in the 'data' directory
    - this should take ~30 minutes, because it takes a long time to scrape the web to get all of the necessary poems to compose a corpus
    - after running this once, you need not run it again
* run `python app.py` from the root directory
* It may take ~5 minutes to load the corpus and to create a classifier
* open [localhost](http://localhost:5005) and input a poem


## Dependencies
* flask
* nltk
* urllib
* bs4 (Beautiful soup)
