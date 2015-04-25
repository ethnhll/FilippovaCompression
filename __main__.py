import os

from graph.word_graph import Word_Graph


__author__ = 'Ethan Hill'
from utils import token_utils
import argparse


def setup_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'text_file', action='store', help='text file to summarize')
    parser.add_argument(
        'stop_words', action='store', help='a list of stop words')
    return parser.parse_args()


def main():
    arguments = setup_argument_parser()

    with open(arguments.text_file) as text_file:
        unprocessed = ''.join(text_file.readlines())
        unprocessed = unprocessed.replace('\n', ' ')

        split_sentences = token_utils.sent_tokenize(unprocessed)
        with open('split_tmp', 'w') as temp_file:
            temp_file.write('\n'.join(split_sentences))
        temp_file_path = os.path.join(os.getcwd(), 'split_tmp')
        clusters = token_utils.cluster_sentences(temp_file_path, arguments.stop_words)
        os.remove(temp_file_path)

        sentence_clusters = []
        for cluster in clusters:
            sentence_clusters.append(
                [token_utils.prepare_word_info(split_sentences[index], index) for index in cluster])
    with open(arguments.stop_words) as stop_word_file:
        stop_word_list = stop_word_file.readlines()
        for sentences in sentence_clusters:
            word_graph = Word_Graph(sentences, stop_word_list)
            word_graph.process_graph()
            word_graph.reweight_edges('baseline')
            paths = word_graph.k_shortest_path(9,50)
            word_graph.print_graph()



if __name__ == '__main__':
    main()