# Represents a node on the word graph
class node:

	def __init__(word, tag, sentence_id, word_id):
		self.word = word.lower()
		self.tag = tag
		self.sentence_ids = set()
		self.sentence_ids.add((sentence_ids, word_id))
		# Children are stored as a tuple (weight, node)
		self.children = []
		self.parents = []

	# We need (1) a way to see if the node has been used
	#         (2) a way to add the word to the node

	


