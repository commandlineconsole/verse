#!/usr/local/bin/python
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn, CategorizedPlaintextCorpusReader, stopwords
from settings import base_emotions
import nltk
import urllib
import re


# Search in direct synonyms as well as the words themselves
emotions = [(s, em) for em in base_emotions for s in wn.synsets(em)[1].lemma_names]


# Creates files from the poems on poemhunter using urllib and beautiful soup
def create_entries():
    url = 'http://www.poemhunter.com'
    searchdir = '/poems/'
    poem_id = 0
    cat_file = open('./data/cats.txt', 'a')

    # Search for each emotion
    for (sentiment, emotion) in emotions:
        print sentiment
        search_page = BeautifulSoup(urllib.urlopen(url + searchdir + sentiment))

        # Main scraping loop
        while True:
            poems_list = search_page.find('ul', {'class', 'poems-about-list'})

            # Find individual poems
            for p in poems_list.findAll('li'):
                title = p.a.get_text().strip().encode('utf-8')
                link = p.a['href']
                poem_page = BeautifulSoup(urllib.urlopen(url + link))
                poem_body = poem_page.find('div', {'class', 'KonaBody'}).find('p')

                filename = 'poems_' + str(poem_id)
                poem_file = open('./data/' + filename, 'a')
                poem_file.write(title.upper() + '\n')

                for s in poem_body.strings:
                    s = re.sub('(.*)<\s*br\s*>(.*)', '\1\2', s)
                    # get rid of 'by' tag at the bottom, also get rid of copyright
                    ignore_line = r'(?:^|\W)(?:[Cc]opyright|\\xa9)(?:\W|$)'
                    if re.sub(ignore_line, '', s) != s:
                        continue

                    # remove spam: duplicate words that repeat
                    spam_line = r'(?: |^)([^ ]*)( \1){3,}(?= |$)'
                    if re.sub(spam_line, '', s) != s:
                        continue

                    poem_file.write(s.strip().encode('utf-8') + '\n')

                cat_file.write(filename + ' ' + emotion + '\n')
                poem_file.close()
                poem_id += 1

            # If there is a next page in the search results, go to it
            next_page = search_page.find('li', {'class': 'next'})
            if next_page:
                search_page = BeautifulSoup(urllib.urlopen(url + next_page.a['href']))
            else:
                break

    cat_file.close()
    print poem_id


# create vocabularies for each emotion
def create_vocabularies():
    poem_corpus = CategorizedPlaintextCorpusReader('./data', 'poems.*',
        cat_file='cats.txt')

    for emotion in base_emotions:
        words = poem_corpus.words(categories=[emotion])
        words = [w.lower() for w in words if w.isalpha() and w not in stopwords.words('english')]
        fdist = nltk.FreqDist(words)
        vocabulary = fdist.keys()[:200]

        vocab_file = open('./opinion-lexicon-English/%s-words.txt' % emotion, 'w')
        vocab_file.write('\n'.join(vocabulary))
        vocab_file.close()


if __name__ == '__main__':
    create_vocabularies()
