__author__ = 'Ethan Hill'
import nltk
from collections import namedtuple
from nltk.tokenize import sent_tokenize, word_tokenize

WordInfo = namedtuple('WordInfo', 'word, tag, sentence_id, index')


def split_into_sentences(text):
    return [word_tokenize(sentence) for sentence in sent_tokenize(text)]


def prepare_word_info(text):
    token_sentences = []
    for sentence_id, sentence in enumerate(split_into_sentences(text)):
        words = []
        for word_index, word_tag in enumerate(nltk.pos_tag(sentence)):
            word, tag = word_tag
            words.append(WordInfo(word, tag, sentence_id, word_index))
        token_sentences.append(words)
    return token_sentences
