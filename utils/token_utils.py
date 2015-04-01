__author__ = 'Ethan Hill'
import nltk
from collections import namedtuple
from nltk.tokenize import sent_tokenize, word_tokenize

WordInfo = namedtuple('WordInfo', 'word, tag')


def tokenize_text(text):
    return [word_tokenize(sentence) for sentence in sent_tokenize(text)]


def pos_tag_text(text):
    tokens = tokenize_text(text)
    return [WordInfo(w, t) for sent in tokens for w, t in nltk.pos_tag(sent)]

