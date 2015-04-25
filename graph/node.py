from collections import defaultdict


class Node:
    # Represents a node on the word graph
    def __init__(self, node_count=0, word_info=None, parent=None):
        self.offset_positions ={}
        if word_info is not None:
            self.word = word_info.word
            self.tag = word_info.tag
            self.offset_positions = {word_info.sentence_id: word_info.word_index}
                # Children are stored as a dictionary of {node: weight}
        
        self.hash_counter = node_count
        self.edges = defaultdict(float)
        self.shortest=-1
        self.parents = {parent} if parent else set()

    def __eq__(self,other):
        return self.hash_counter == other.hash_countier
        
    def __hash__(self):
        return self.hash_counter

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

    def can_map_stopword(self, word_info, previous_node, next_word):
        if self.word.lower() != word_info.word.lower():
            return False
        if self.tag != word_info.tag:
            return False
        if word_info.sentence_id in self.mapped_sentences:
            return False
        ## One of these conditions needs to be true
        if previous_node in self.parents:
            return True
        for child in self.children:
            if child.can_map_word(next_word):
                return True
        return False

    def map_word(self, word_info, parent):
        self.offset_positions[word_info.sentence_id] = word_info.word_index
        # Should always have a parent node, because if it is the first node,
        # the parent is the start node.
        self.parents.add(parent)

    # Adds an edge from the previous word in the sentence
    def add_edge(self, node):
        self.edges[node] = self.edges[node] + 1

    def remove_edge(self,node):
        return self.edges.pop(node,None)

    def add_new_edge(self, node,weigth):
        self.edges[node] = weigth

