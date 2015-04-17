# General Algorithm
# 1) Add a start node, followed by a linear path of the words in 
# the first sentence as nodes, and an end node
# 2) For each word in additional sentences:
#      a) If stopword, include it only if there is some overlapping
#		  in non-stopword neighbors 
#      b) If (word, tag) node exists in graph and no part of that
#         sentence has already been mapped to node, add 1 to weight 
#         of edge and add the sentence id to the nodeâs list of seen sentences
#      c) If word node does not exist, create a new a new node for it and an 
#         edge with weight 1 from the previous node and add the sentence id to 
#         its seen sentences list
from filipova_compression.models.node import Node


class Word_Graph:
    def __init__(self, sentences, stop_words=[]):
        # graph is just a list of nodes
        self.graph = []
        self.start_node = Node()
        self.stop_node = Node()
        self.stop_words = stop_words

        for sentence in sentences:
            self.add_sentence(sentence)

    # TODO(ethan or lizzy): Add first sentence to word graph

    def add_sentence(self, sentence):
        # Adds a sentence to the word graph
        # Sentence is list of pre-tagged words that are represented as named tuples (word, tag)
        previous_node = self.start_node
        for i, word_info in enumerate(sentence):
            if word_info.word in self.stop_words:
                next_word = None
                if (i+1 < len(sentence)):
                    next_word = sentence[i+1]
                current_node = self.GetStopWordNode(word_info, previous_node, next_word)
            else:
                current_node = self.GetWordNode(word_info, previous_node)
            self.graph.append(current_node)
            previous_node = current_node
        pass
        self.stop_node.add_edge(previous_node)

    # Either
    # (1) Gets the existing word node
    # (2) Adds an additional word node
    def GetWordNode(self, word_info, previous_node):
        for node in self.graph:
            if node.can_map_word(word_info):
                node.map_word(word_info, previous_node)
                previous_node.add_edge(node)
                return node
        # If it doesn't exist yet
        new_node = Node(word_info)
        previous_node.add_edge(new_node)
        return new_node

    def GetStopWordNode(self, word_info, previous_node, next_word):
        for node in self.graph:
            if node.can_map_word_stopword(word_info, previous_node, next_word):
                node.map_word(word_info, previous_node)
                previous_node.add_edge(node)
                return node
        # If it doesn't exist yet
        new_node = Node(word_info)
        previous_node.add_edge(new_node)
        return new_node

    def Kshortest_path(self, min_sentence_length, k):
        # Use shortest path 
         pass

    def shortest_path(self, source, sink, visited=[], distances=defaultdict(int), previous_node=defaultdict(Node)):
        # if we reach the end build the path from previous_node
        if sink==source:
            path = []
            previous = sink
            while previous != None:
                path.append(previous)
                previous = previous_node.get(previous,None)
            distance = distances[sink]
        else:
            # If we are in the initial run initialize distance
            if not visited:
                distances[source] = 0
            # Go through the edges going out of the node if it's not visited
            # check whether it's the shortest way to reach the node
            for node in source.edges:
                if node not in visited:
                    distance = distances[source] + source.edges[node]
                    if distance < distances.get(node,float('inf')):
                        distances[node] = distance
                        previous[node] = source
            visited.append(source)
            # Call the function recursively to the node with the lowest distance
            # that has been touch (not visited)
            univisited={}
            for node in self.graph:
                if node not in visited:
                    unvisited[node] = distance.get(node,float('inf'))
            new_source = min(unvisited)
            shortest_path(self, new_source,sink,visited,distances,previous_node)

    def process_graph(self):
        self.graph.append(self.start_node)
        self.graph.append(self.stop_node)


