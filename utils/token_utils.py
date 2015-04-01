__author__ = 'Ethan Hill'
import nltk
from collections import namedtuple
from nltk.tokenize import sent_tokenize, word_tokenize

WordTag = namedtuple('WordTag', 'word, tag')


def tokenize_text(text):
    return [word_tokenize(sentence) for sentence in sent_tokenize(text)]


def pos_tag_text(text):
    tokenized = tokenize_text(text)
    return [WordTag(w, t) for sent in tokenized for w, t in nltk.pos_tag(sent)]

