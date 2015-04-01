from collections import namedtuple

GraphEdge = namedtuple('GraphEdge', 'node, weight')


class Node:
    # Represents a node on the word graph
    def __init__(self, word_info, sentence_id, word_index):
        self.word_info = word_info
        self.sentence_ids = set()
        self.sentence_ids.add((sentence_id, word_index))
        # Children are stored as a GraphEdge namedtuple (node, weight)
        self.children = []
        self.parents = []

        # We need (1) a way to see if the node has been used
        # (2) a way to add the word to the node