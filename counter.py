import csv
import numpy as np
from string import punctuation
from collections import Counter
from nltk.corpus import stopwords


def extract_tweets(name):
    tweets = []

    with open(name, newline='') as f:
        tweet_reader = csv.reader(f)
        for line in tweet_reader:
            tweets.append(line[1].lower().split())

    return tweets


def remove_link_mention_hashtag(list):
    tweets = []

    for tweet in list:
        _tweet = [x for x in tweet if not x.startswith(
            'http') and not x.startswith('@') and not x.startswith('#')]
        if _tweet:
            for word in _tweet:
                tweets.append(word)

    return tweets


def remove_punctuation(list):
    keywords = []
    _punctuation = punctuation + '“”'

    for word in list:
        for symbol in _punctuation:
            word = word.replace(symbol, '')
            if word:
                keywords.append(word)

    return keywords


def remove_stopwords(list):
    stop_words = stopwords.words("english")
    stop_words.append('rt')
    stop_words.append('amp')

    tweets = [x for x in list if x not in stop_words]
    return tweets


def count_tweets():
    FILE = 'data/tweets.csv'

    tweet_list = extract_tweets(FILE)
    word_list = remove_link_mention_hashtag(tweet_list[1:])
    preprocessed_word_list = remove_punctuation(word_list)
    keyword_list = remove_stopwords(preprocessed_word_list)
    counter = Counter(keyword_list)

    return counter


def export_word_counts(counter):
    result = []
    for word, freq in counter.items():
        result.append((word, freq))
    result = sorted(result, key=lambda x: x[1], reverse=True)

    output = open('results/word_counts.txt', 'a')
    output.write(str(result))
    output.close()


def export_median(counter):
    result = []
    for _, freq in counter.items():
        result.append(freq)

    output = open('results/median_amount.txt', 'a')
    output.write(f'Median: {str(np.median(result))}')
    output.close()


export_word_counts(count_tweets())
export_median(count_tweets())
