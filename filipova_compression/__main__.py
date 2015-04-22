__author__ = 'Ethan Hill'
import token_utils
from word_graph import Word_Graph

def main():
    test = token_utils.make_test_sentences()
    f = open('stoplist')
    stop_words = f.read().split()
    word_graph = Word_Graph(test, stop_words)
    word_graph.process_graph()
    word_graph.print_graph()


if __name__ == '__main__':
    main()