from flask import Flask, render_template, request, url_for
from classify import classifier, classify, test_set, poem_set, get_errors
import nltk
import urllib
import json


# Flask initialization
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/_classify/<poem>')
def get_classification(poem):
    poem = nltk.word_tokenize(urllib.unquote(poem))
    print poem, classify(poem)
    return json.dumps({'category': classify(poem)})


@app.route('/_learning')
def learning():
    accuracy = str(nltk.classify.accuracy(classifier, test_set))
    errors = get_errors(poem_set[:500])
    print len(errors)
    return render_template('learning.html', accuracy=accuracy, errors=errors)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
