from collections import defaultdict


class Node:
    # Represents a node on the word graph
    def __init__(self, word_info=None, parent=None):
        if word_info is not None:
            self.word = word_info.word
            self.tag = word_info.tag
            self.offset_positions = {word_info.sentence_id: word_info.word_index}
                # Children are stored as a dictionary of {node: weight}
        self.edges = defaultdict(int)
        self.parents = {parent} if parent else set()

    def __eq__(self,other):
        return self.word == other.word
        
    @property
    def mapped_sentences(self):
        return set(self.offset_positions.keys())

    @property
    def children(self):
        return set(self.edges.keys())

    def can_map_word(self, word_info):
        if self.word.lower() != word_info.word.lower():
            return False
        if self.tag != word_info.tag:
            return False
        if word_info.sentence_id in self.mapped_sentences:
            return False
        return True

    def map_word(self, word_info, parent):
        self.offset_positions[word_info.sentence_id] = word_info.word_index
        # Should always have a parent node, because if it is the first node,
        # the parent is the start node.
        self.parents.add(parent)

    # Adds an edge from the previous word in the sentence
    def add_edge(self, node):
        self.edges[node] += 1

