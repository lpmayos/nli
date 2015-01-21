# -*- coding: utf-8 -*-

"""
Natural Language Interaction, MIIS, UPF
January 2015
Authors: Laura Pérez & Víctor Casamayor
Description: todo

Installation:
    $ pip install networkx
    $ pip install matplotlib

Troubleshooting:
    "ValueError: failed to convert font family name to ASCII"
        Another solution is to change the backend in your matplotlibrc file.
        Find your matplotlibrc file:
            import matplotlib
            matplotlib.matplotlib_fname()
        Open the file and change the graphics back-end, e.g.:
            "backend: macosx" -> "backend: TkAgg"

References:
    - http://en.wikipedia.org/wiki/Dialog_tree
    - https://networkx.github.io/documentation/latest/reference/index.html
"""

import sys
import random
import networkx as nx
import matplotlib.pyplot as plt


class Graph():
    """
    """

    def __init__(self):
        """
        """
        self.graph = None
        self.user_name = None
        self.current_node = 'ask_name'
        self.last_node = ''

    def draw_graph(self):
        """
        """
        # draw graph
        pos = nx.shell_layout(self.graph)
        nx.draw(self.graph, pos)

        # show graph
        plt.show()

    def draw_graph_with_labels(self):
        """
        """
        # graph configuration
        pos = nx.shell_layout(self.graph)
        node_size = 1600
        node_color = 'blue'
        node_alpha = 0.3
        node_text_size = 12
        edge_color = 'blue'
        edge_alpha = 0.3
        edge_tickness = 1
        edge_text_pos = 0.3
        text_font = 'sans-serif'

        # graph drawing
        nx.draw_networkx_nodes(self.graph, pos, node_size=node_size, alpha=node_alpha, node_color=node_color)
        nx.draw_networkx_edges(self.graph, pos, width=edge_tickness, alpha=edge_alpha, edge_color=edge_color)

        # draw node labels
        nx.draw_networkx_labels(self.graph, pos, font_size=node_text_size, font_family=text_font)

        # draw edge labels
        edge_labels = {}
        for edge in self.graph.edges():
            edge_labels[edge] = self.graph.edge[edge[0]][edge[1]]['text']
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, label_pos=edge_text_pos)

        # show graph
        plt.show()

    def text_ask_name(self):
        """
        """
        if self.current_node == self.last_node:
            return "Sorry, I couldn't get your name. What's your name again?"

        options = ["Hi! What's your name?",
                   "Hello, could you remind me your name please?",
                   "Hi! I can't recall your name. It was...?"]

        return options[random.randint(0, len(options) - 1)]

    def text_offer_help(self):
        """
        """
        return "text_offer_help"

    def text_ask_problem(self):
        """
        """
        return "text_ask_problem"

    def text_ask_check_in_reception(self):
        """
        """
        return "text_ask_check_in_reception"

    def text_check_in_reception(self):
        """
        """
        return "text_check_in_reception"

    def text_goodbye(self):
        """
        """
        return "text_goodbye"

    def text_get_new_card(self):
        """
        """
        return "text_get_new_card"

    def create_graph(self):
        """
        """
        # create networkx graph
        graph = nx.DiGraph()

        # add nodes
        graph.add_node('ask_name', text=self.text_ask_name)
        graph.add_node('offer_help', text=self.text_offer_help)
        graph.add_node('ask_problem', text=self.text_ask_problem)
        graph.add_node('ask_check_in_reception', text=self.text_ask_check_in_reception)
        graph.add_node('check_in_reception', text=self.text_check_in_reception)
        graph.add_node('goodbye', text=self.text_goodbye)
        graph.add_node('get_new_card', text=self.text_get_new_card)

        # add edges
        graph.add_edge('ask_name', 'offer_help', text=[])
        graph.add_edge('ask_name', 'ask_name', text=[])

        graph.add_edge('offer_help', 'ask_problem', text=["can't find", 'lost'])
        graph.add_edge('offer_help', 'ask_check_in_reception', text=["can't find", 'lost'])
        graph.add_edge('offer_help', 'get_new_card', text=["can't find", 'lost'])
        graph.add_edge('offer_help', 'offer_help', text=["can't find", 'lost'])

        graph.add_edge('ask_problem', 'ask_check_in_reception', text=["can't find", 'lost'])
        graph.add_edge('ask_problem', 'get_new_card', text=["can't find", 'lost'])
        graph.add_edge('ask_problem', 'ask_problem', text=["can't find", 'lost'])

        graph.add_edge('ask_check_in_reception', 'check_in_reception', text=["can't find", 'lost'])
        graph.add_edge('ask_check_in_reception', 'get_new_card', text=["can't find", 'lost'])
        graph.add_edge('ask_check_in_reception', 'ask_check_in_reception', text=["can't find", 'lost'])

        graph.add_edge('check_in_reception', 'goodbye', text=["can't find", 'lost'])
        graph.add_edge('check_in_reception', 'get_new_card', text=["can't find", 'lost'])
        graph.add_edge('check_in_reception', 'check_in_reception', text=["can't find", 'lost'])

        self.graph = graph

    def parse_user_name(self, answer):
        """
        """
        dummy_words = ['my', 'is', 'name', "i'm", 'am', 'i', 'hello', 'hi', ',', '.']
        array_answer = [a for a in answer.lower().split(' ') if a not in dummy_words]
        if len(array_answer) > 0 and len(array_answer) < 4:
            self.user_name = ' '.join([a.capitalize() for a in array_answer])
            print 'self.user_name: ', self.user_name
        return

    def parse_answer(self, answer):
        """ return number of the node to which we should transition, given that we
        are in 'node' and the user typed 'answer'
        """
        
        if self.current_node == 'ask_name':
            self.parse_user_name(answer)
            # return to ask_name
            if self.user_name is None:
                return (self.current_node, self.current_node)
            else:
                return ('ask_name', 'offer_help')

        # get edges connecting 'node' with other nodes
        edges = [a for a in self.graph.edges() if a[0] == self.current_node]
        
        # get first edge that contains any of the words on 'answer'
        for edge in edges:
            text = self.graph.edge[edge[0]][edge[1]]['text']
            if set(text).intersection(answer.lower().split(' ')):
                return edge[1]

        # if no edge found, transition to 7
        return (self.current_node, self.current_node)

    def create_dialog(self):
        """ starting on node 'offer_help', prints the machine answers according with
        the user questions, until no more transitions are possible
        """
        answer = raw_input("You enter Bea's virtual office. Welcome!\n>> ")  # 'hello' expected
        while self.graph.successors(self.current_node):
            print 'current_node: ', self.current_node
            print 'last_node: ', self.last_node
            answer = raw_input(self.graph.node[self.current_node]['text']() + '\n>> ')
            edge = self.parse_answer(answer)
            self.last_node = self.current_node
            self.current_node = edge[1]
        print self.graph.node['goodbye']['text']
        return


def main():
    graph = Graph()
    graph.create_graph()
    graph.create_dialog()
    graph.draw_graph_with_labels()

if __name__ == '__main__':
    status = main()
    sys.exit(status)
