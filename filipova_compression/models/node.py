from collections import defaultdict


class Node:
    # Represents a node on the word graph
    def __init__(self, word_info = None):
        if word_info is not None:
            self.word = word_info.word
            self.tag = word_info.tag
            self.offset_positions = {word_info.sentence_id: word_info.word_index}
                # Children are stored as a dictionary of {node: weight}
        self.edges = defaultdict(int)
        
    @property
    def mapped_sentences(self):
        return set(self.offset_positions.keys())

    def can_map_word(self, word_info):
        if self.word.lower() != word_info.word.lower():
            return False
        if self.tag != word_info.tag:
            return False
        if word_info.sentence_id in self.mapped_sentences:
            return False
        return True

    def map_word(self, word_info):
        self.offset_positions[word_info.sentence_id] = word_info.word_index

    # Adds an edge from the previous word in the sentence
    def add_edge(self, node):
        self.edges[node] += 1
