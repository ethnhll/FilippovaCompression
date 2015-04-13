# General Algorithm
# 1) Add a start node, followed by a linear path of the words in 
# the first sentence as nodes, and an end node
# 2) For each word in additional sentences:
#      a) If stopword, include it only if there is some overlapping
#		  in non-stopword neighbors 
#      b) If (word, tag) node exists in graph and no part of that
#         sentence has already been mapped to node, add 1 to weight 
#         of edge and add the sentence id to the node’s list of seen sentences
#      c) If word node does not exist, create a new a new node for it and an 
#         edge with weight 1 from the previous node and add the sentence id to 
#         its seen sentences list


class Word_Graph:
    def __init__(self, sentence, stop_words=[]):
        # graph is just a list of nodes
        self.graph = []
        self.start_node = Node()
        self.stop_node = Node()
        self.stop_words = stop_words

    # TODO(ethan or lizzy): Add first sentence to word graph

    def add_sentence(self, sentence):
        # Adds a sentence to the word graph
        # Sentence is list of pre-tagged words that are represented as named tuples (word, tag)
        previous_node = self.start_node
        for word_info in sentence
            current_node = GetWordNode(word_info, previous_node)
            previous_node = current_node
        pass
        self.stop_node.add_edge(previous_node)

    # Either
    # (1) Gets the existing word node
    # (2) Adds an additional word node
    def GetWordNode(word_info, previous_node)
        for node in self.graph:
            if node.can_map_word(word_info):
                node.map_word(word_info)
                node.add_edge(previous_node)
                return node
        # If it doesn't exist yet
        new_node = Node(word_info)
        new_node.add_edge(previous_node)
        return new_node




    def shortest_path(self, min_sentence_length, k):
        # Returns the shortest path
        # TODO(jorge)
        pass

