from collections import defaultdict
from collections import namedtuple
from copy import deepcopy

WordInfo = namedtuple('WordInfo', 'word, tag, sentence_id, index')

class Node:
    # Represents a node on the word graph
    def __init__(self, word_info = None):
        self.word = word_info[0]
        self.tag = word_info[1]
        self.edges = defaultdict(int)

    def __eq__(self,other):
        return self.word == other.word

    def map_word(self, word_info):
        self.offset_positions[word_info.sentence_id] = word_info.word_index

    # Adds an edge from the previous word in the sentence
    def add_edge(self, node,weight):
        self.edges[node] = weight

    def remove_edge(self,node):
        return self.edges.pop(node,None)

    def print_children(self):
        print(self.edges)


        
class Word_Graph:
    def __init__(self, stop_words=[]):
        # graph is just a list of nodes
        self.graph = defaultdict(Node)
        self.start_node_info=WordInfo('<s>','<s>',0,0)
        self.add_node(self.start_node_info)
        self.stop_node_info = WordInfo('</s>','</s>',0,0)
        self.add_node(self.stop_node_info)

    def add_node(self, word_info):
        new_node = Node(word_info)
        self.graph[word_info[0]]=new_node


    def add_edge(self,source,target,weight):
        if target not in self.graph.keys():
            self.add_node((target,target,0,0))
        self.graph[source].add_edge(target,weight)

    def pop_edge(self,source,target):
        return self.graph[source].remove_edge(target)

    def printGraph(self):
        for node in self.graph.keys():
            print(node)
            self.graph[node].print_children()

    def add_group_edges(self, edges_removed):
        for edge in edges_removed:
            if edge[2]!=None:
                self.add_edge(edge[0],edge[1],edge[2])

    def Kshortest_path(self, min_sentence_length, K):
        paths=[]
        distances = []
        # Use shortest path 
        path, distance = self.shortest_path('<s>','</s>')
        distances.append(distance)
        paths.append(path)
        potential_paths = []
        for k in range(K-1):
            for i in range(len(paths[k])-1):
                edges_removed=[]
                spur_node = paths[k][i]
                root_path = paths[k][:i]
                for path in paths:
                    if root_path == path[:i]:
                        edges_removed.append((path[i],path[i+1],self.pop_edge(path[i],path[i+1])))

                for node in root_path:
                    if node != spur_node:
                        # cut out edges out of the node (effectively removing it
                        for word in self.graph.keys():
                            edges_removed.append((node,word,self.pop_edge(node,word)))

                spur_path, distance = self.shortest_path(spur_node,'</s>')
                self.add_group_edges(edges_removed)
                if spur_path!=None:
                    root_distance=0
                    for i  in range(len(root_path)-1):
                        root_distance+=self.graph[root_path[i]].edges[root_path[i+1]]
                    if root_path:
                        root_distance+=self.graph[root_path[-1]].edges[spur_path[0]]
                    final_path = root_path + spur_path
                    potential_paths.append((final_path,distance+root_distance))
            potential_paths.sort(key=lambda x: x[1])
            paths.append(potential_paths[0][0])
            distances.append(potential_paths[0][1])
            potential_paths.pop(0)
        #print(potential_paths)
        print (paths)
        print(distances)


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
            for node in self.graph[source].edges:
                if node not in visited:
                    distance = distances[source] + self.graph[source].edges[node]
                    if distance < distances.get(node,float('inf')):
                        distances[node] = distance
                        previous_node[node] = source
            visited.append(source)
            # Call the function recursively to the node with the lowest distance
            # that has been touch (not visited)
            adjacent_nodes=[]
            for node in visited:
                for adjacent_node in self.graph[node].edges.keys():
                    if adjacent_node not in visited:
                        adjacent_nodes.append(adjacent_node)

            if adjacent_nodes:
                unvisited={}
                for node in self.graph:
                    if node not in visited:
                        unvisited[node] = distances.get(node,float('inf'))
                new_source = min(unvisited,key=unvisited.get)
                path, distance = self.shortest_path(new_source,sink,visited,distances,previous_node)
                return path, distance
            else:
                return None, float('inf')

test = Word_Graph()
test.add_edge('<s>','d',3)
test.add_edge('<s>','e',2)
test.add_edge('d','f',4)
test.add_edge('e','d',1)
test.add_edge('e','f',2)
test.add_edge('e','g',3)
test.add_edge('f','g',2)
test.add_edge('f','</s>',1)
test.add_edge('g','</s>',2)
#path=test.shortest_path('<s>','</s>')
#print(path)
#test.pop_edge('<s>','e')
#path=test.shortest_path('<s>','</s>')
#print(path)
test.Kshortest_path(8,3)




