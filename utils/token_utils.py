import os
import string
import subprocess

__author__ = 'Ethan Hill'
import nltk
from collections import namedtuple
from nltk.tokenize import sent_tokenize, word_tokenize

WordInfo = namedtuple('WordInfo', 'word, tag, sentence_id, word_index')


def cluster_sentences(sentence_file, stop_word_file, centroid_width=16,
                      similarity_threshold=0.06):

    clusterer_path = os.path.join(
        'FilipovaCompression', 'utils', 'cluster', 'bin')

    output = subprocess.check_output(
        ['java', '-cp', clusterer_path, 'sentenceCluster.SimClusterMain', sentence_file, stop_word_file,
         str(centroid_width), str(similarity_threshold)])
    cluster_strings = output.splitlines()
    clusters = []
    for i in cluster_strings:
        clusters.append([int(cluster) for cluster in i.split(',')])

    return clusters


def prepare_word_info(sentence, sentence_id):
    words = []
    sentence = ' '.join(i.strip(string.punctuation) for i in sentence.split())
    sentence = word_tokenize(sentence)
    # Start the index at 1, we will use 0 index for start symbol
    for word_index, word_tag in enumerate(nltk.pos_tag(sentence), start=1):
        word, tag = word_tag
        words.append(WordInfo(word, tag, sentence_id, word_index))
    return words


def make_test_sentences():
    token_sentences = []

    sentence1 = []
    sentence1.append(WordInfo('the', 'dt', 0, 0))
    sentence1.append(WordInfo('really', 'adv', 0, 1))
    sentence1.append(WordInfo('fat', 'adj', 0, 2))
    sentence1.append(WordInfo('cat', 'nn', 0, 3))
    sentence1.append(WordInfo('sat', 'vb', 0, 4))
    sentence1.append(WordInfo('on', 'prep', 0, 5))
    sentence1.append(WordInfo('the', 'dt', 0, 6))
    sentence1.append(WordInfo('mat', 'nn', 0, 7))

    token_sentences.append(sentence1)

    sentence2 = []
    sentence2.append(WordInfo('the', 'dt', 1, 0))
    sentence2.append(WordInfo('cat', 'nn', 1, 1))
    sentence2.append(WordInfo('and', 'cc', 1, 2))
    sentence2.append(WordInfo('the', 'dt', 1, 3))
    sentence2.append(WordInfo('dog', 'nn', 1, 4))
    sentence2.append(WordInfo('sat', 'vb', 1, 5))
    sentence2.append(WordInfo('on', 'prep', 1, 6))
    sentence2.append(WordInfo('the', 'dt', 1, 7))
    sentence2.append(WordInfo('mat', 'nn', 1, 8))

    token_sentences.append(sentence2)

    sentence3 = []
    sentence3.append(WordInfo('the', 'dt', 2, 0))
    sentence3.append(WordInfo('cat', 'nn', 2, 1))
    sentence3.append(WordInfo('sat', 'vb', 2, 2))
    sentence3.append(WordInfo('on', 'prep', 2, 3))
    sentence3.append(WordInfo('the', 'dt', 2, 4))
    sentence3.append(WordInfo('mat', 'nn', 2, 5))
    sentence3.append(WordInfo('and', 'cc', 2, 6))
    sentence3.append(WordInfo('the', 'dt', 2, 7))
    sentence3.append(WordInfo('other', 'dt', 2, 8))
    sentence3.append(WordInfo('cat', 'adj', 2, 9))

    token_sentences.append(sentence3)

    sentence4 = []
    sentence4.append(WordInfo('the', 'dt', 3, 0))
    sentence4.append(WordInfo('mat', 'nn', 3, 1))
    sentence4.append(WordInfo('was', 'vbd', 3, 2))
    sentence4.append(WordInfo('sat', 'vb', 3, 3))
    sentence4.append(WordInfo('on', 'prep', 3, 4))
    sentence4.append(WordInfo('by', 'prep', 3, 5))
    sentence4.append(WordInfo('the', 'dt', 3, 6))
    sentence4.append(WordInfo('fat', 'adj', 3, 7))
    sentence4.append(WordInfo('cat', 'nn', 3, 8))

    token_sentences.append(sentence4)

    return token_sentences


if __name__ == '__main__':
    cluster_sentences(''
                      'test.txt')
