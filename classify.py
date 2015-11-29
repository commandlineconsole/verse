from nltk.corpus import CategorizedPlaintextCorpusReader
from settings import base_emotions
import nltk
import random


# Annotate poems with features
def poem_features(text):
    text = [w.lower() for w in text if w.isalpha()]
    pos_count = len([word for word in text if word in positive_words])
    neg_count = len([word for word in text if word in negative_words])
    pos_ratio = float(pos_count) / float(len(text))
    neg_ratio = float(neg_count) / float(len(text))
    print pos_ratio, neg_ratio
    features = {'positive_ratio': pos_ratio, 'negative_ratio': neg_ratio}

    return features


# Return errors in order to improve algorithm
def get_errors(poemset):
    errors = []
    for (fileid, category) in poemset:
        poem = poem_corpus.words(fileids=[fileid])
        features = poem_features(poem)
        guess = classifier.classify(poem_features(poem))

        if guess != category:
            errors.append((category, guess, poem, \
                    features['positive_ratio'], features['negative_ratio']))

    return errors


# Classifies a poem
def classify(poem):
    return classifier.classify(poem_features(poem))


# Get words from positive and negative files
pos_file = open('./opinion-lexicon-English/positive-words.txt', 'rU')
neg_file = open('./opinion-lexicon-English/negative-words.txt', 'rU')
positive_words = [word.strip() for word in pos_file.readlines() if not \
        word.startswith(';')]
negative_words = [word.strip() for word in neg_file.readlines() if not \
        word.startswith(';')]
pos_file.close()
neg_file.close()


# Words for all emotions
lexicon = {}
for emotion in base_emotions:
    f = open('./opinion-lexicon-English/%s-words.txt' % emotion, 'rU')
    words = [word.strip() for word in f.readlines()]
    lexicon[emotion] = words
    f.close()

# Make a classifier based on the feature sets of the poems
poem_corpus = CategorizedPlaintextCorpusReader('./data', 'poems.*',
        cat_file='cats.txt')

poem_set = [(fileid, category) for fileid in poem_corpus.fileids() \
        for category in poem_corpus.categories(fileid)]
random.shuffle(poem_set)

feature_set = [(poem_features(poem_corpus.words(fileids=[fileid])),
        category) for (fileid, category) in poem_set]

train_set, test_set = feature_set[2000:], feature_set[:2000]

# Initialize the classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)

# For improving the algorithm
classifier.show_most_informative_features(20)
