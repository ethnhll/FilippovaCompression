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
from node import Node
from collections import defaultdict
import networkx as nx
from networkx.readwrite import json_graph
import json


class Word_Graph:
    def __init__(self, sentences, stop_words=[]):
        # graph is just a list of nodes
        self.graph = defaultdict(Node)
        self.start_node = Node(0)
        self.stop_node = Node(1)
        self.counter = 2
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
            self.graph[current_node.hash_counter] = current_node
            previous_node = current_node
        pass
        previous_node.add_edge(self.stop_node)

    # Either
    # (1) Gets the existing word node
    # (2) Adds an additional word node
    def GetWordNode(self, word_info, previous_node):
        for node in self.graph.values():
            if node.can_map_word(word_info):
                node.map_word(word_info, previous_node)
                previous_node.add_edge(node)
                return node
        # If it doesn't exist yet
        new_node = Node(self.counter, word_info, previous_node)
        self.counter = self.counter + 1
        previous_node.add_edge(new_node)
        return new_node

    def GetStopWordNode(self, word_info, previous_node, next_word):
        for node in self.graph.values():
            if node.can_map_stopword(word_info, previous_node, next_word):
                node.map_word(word_info, previous_node)
                previous_node.add_edge(node)
                return node
        # If it doesn't exist yet
        new_node = Node(self.counter, word_info, previous_node)
        self.counter = self.counter + 1
        previous_node.add_edge(new_node)
        return new_node

    def invert_weights(self):
        for node in self.graph.values():
            for node2, edge in node.edges.items():
                node.edges[node2] = 1/edge

    def add_group_edges(self, edges_removed):
        for edge in edges_removed:
            if edge[2]!=None:
                self.add_edge(edge[0],self.graph[edge[1]],edge[2])

    def add_edge(self,source,target,weight):
        self.graph[source].add_new_edge(target,weight)

    def pop_edge(self,source,target):
        return self.graph[source].remove_edge(self.graph[target])

    def Kshortest_path(self, min_length, K):
        paths=[]
        distances = []
        # Use shortest path 
        path, distance = self.shortest_path(0,1)
        distances.append(distance)
        paths.append(path)
        potential_paths = []
        for k in range(K-1):
            for i in range(len(paths[k])-1):
                edges_removed=[]
                spur_node = paths[k][i]
                root_path = paths[k][:i+1]
                for path in paths:
                    if root_path == path[:i+1]:
                        edges_removed.append((path[i],path[i+1],self.pop_edge(path[i],path[i+1])))
                for node in root_path:
                    if node != spur_node:
                        # cut out edges out of the node (effectively removing it)
                        for ID in self.graph.keys():
                            edges_removed.append((node,ID,self.pop_edge(node,ID)))

                spur_path, distance = self.shortest_path(spur_node,1)
                self.add_group_edges(edges_removed)
                if spur_path!=None:
                    root_distance=0
                    for i  in range(len(root_path)-1):
                        root_distance+=self.graph[root_path[i]].edges[self.graph[root_path[i+1]]]
                    if root_path:
                        root_distance+=self.graph[root_path[-1]].edges[self.graph[spur_path[0]]]
                    final_path = root_path[:-1] + spur_path
                    potential_paths.append((final_path,distance+root_distance))
            if not potential_paths:
                break
            potential_paths.sort(key=lambda x: x[1])
            #print('print potential paths')
            #print(potential_paths[:3])
            while(potential_paths[0][0] in paths):
                potential_paths.pop(0)
            paths.append(potential_paths[0][0])
            distances.append(potential_paths[0][1])
            potential_paths.pop(0)
        #print(potential_paths)
        final_paths = list(zip(paths,distances))
        print(str(final_paths))
        i=0
        while i<len(final_paths):
            if len(final_paths[i][0])<min_length:
                final_paths.remove(final_paths[i])
            elif not self.contains_verb(final_paths[i][0]):
                final_paths.remove(final_paths[i])
            else:
                i+=1
        if final_paths:
            for i in range(len(final_paths[0][0])-1):
                self.graph[final_paths[0][0][i]].shortest=final_paths[0][0][i+1]
        return final_paths


    def shortest_path(self, source, sink, visited=None, distances=None, previous_node=None):
        if visited==None:
            visited=[]
            distances=defaultdict(int)
            previous_node=defaultdict(Node)

        # if we reach the end build the path from previous_node
        if sink==source:
            path=[]
            previous = sink
            while previous != None:
                path.insert(0,previous)
                previous = previous_node.get(previous,None)
            distance = distances[sink]
            return path, distance
        else:
            # If we are in the initial run initialize distance
            if not visited:
                distances[source] = 0
            # Go through the edges going out of the node if it's not visited
            # check whether it's the shortest way to reach the node
            for node in self.graph[source].edges.keys():
                if node.hash_counter not in visited:
                    distance = distances[source] + self.graph[source].edges[node]
                    if distance < distances.get(node.hash_counter,float('inf')):
                        distances[node.hash_counter] = distance
                        previous_node[node.hash_counter] = source
            visited.append(source)
            # Call the function recursively to the node with the lowest distance
            # that has been touch (not visited)
            adjacent_nodes=[]
            for node in visited:
                for adjacent_node in self.graph[node].edges.keys():
                    if adjacent_node.hash_counter not in visited:
                        adjacent_nodes.append(adjacent_node.hash_counter)

            if adjacent_nodes:
                unvisited={}
                for node in self.graph.keys():
                    if node not in visited:
                        unvisited[node] = distances.get(self.graph[node].hash_counter,float('inf'))
                new_source = min(unvisited,key=unvisited.get)
                path, distance = self.shortest_path(new_source,sink,visited,distances,previous_node)
                return path, distance
            else:
                return None, float('inf')

    def process_graph(self):
        self.start_node.word = '<s>'
        self.start_node.tag = ''
        self.stop_node.word = '</s>'
        self.stop_node.tag = ''
        self.graph[0] = (self.start_node)
        self.graph[1] =(self.stop_node)

    def print_graph(self):
##        for node in self.graph.values():
##            print "\nCounter: %d  Word : %s  Tag: %s" %(node.hash_counter, node.word, node.tag)
##            print "EDGES"
##            for edge in node.edges.keys():
##                print "\t %s   :  %d" %(edge.hash_counter, node.edges[edge])
        g = self.convert_to_networkx()
        d = json_graph.node_link_data(g)
        json.dump(d,open('graph.json','w'))

    def convert_to_networkx(self):
        g = nx.DiGraph()
        g.add_nodes_from(self.graph.keys())
        for ID, node in self.graph.items():
            g.node[ID]['word'] = node.word
            g.node[ID]['tag'] = node.tag
            g.node[ID]['shortest'] = node.shortest
            g.node[ID]['sentences'] = str(node.offset_positions)
            
            for edge_node,weight in node.edges.items():
                g.add_edge(node.hash_counter, edge_node.hash_counter,weight=weight)
                
        return g

    def contains_verb(self, path):
        for id in path:
            print(self.graph[id].tag[:2])
            if self.graph[id].tag[:2].upper() == 'VB':
                return True
        return False