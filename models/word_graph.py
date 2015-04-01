# General Algorithm
# 1) Add a start node, followed by a linear path of the words in 
#    the first sentence as nodes, and an end node
# 2) For each word in additional sentences:
#      a) If stopword, include it only if there is some overlapping
#		  in non-stopword neighbors 
#      b) If (word, tag) node exists in graph and no part of that
#         sentence has already been mapped to node, add 1 to weight 
#         of edge and add the sentence id to the node’s list of seen sentences
#      c) If word node does not exist, create a new a new node for it and an 
#         edge with weight 1 from the previous node and add the sentence id to 
#         its seen sentences list


class word_graph:

	def __init__(sentence, stop_words=[]):
		# graph is just a list of nodes
		self.graph = []
		self.stop_words = stop_words
		# TODO(ethan or lizzy): Add first sentence to word graph


	# Adds a sentence to the word graph
	# Sentence is list of pre-tagged words that are represented as named tuples (word, tag)
	def add_sentence(sentence, sentence_id):
		

	# Returns the shortest path
	# TODO(jorge)
    def shortest_path(min_sentence_length, k):


