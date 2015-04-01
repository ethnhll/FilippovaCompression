__author__ = 'Ethan Hill'
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


def tokenize_input(text):
    return [word_tokenize(sentence) for sentence in sent_tokenize(text)]


def pos_tag_sentences(tokenized_sentences):
    return [nltk.pos_tag(sentence) for sentence in tokenized_sentences]