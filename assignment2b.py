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

    def create_graph(self):
        """
        """

        # create networkx graph
        graph = nx.DiGraph()

        # add nodes
        graph.add_node('offer_help', text='Hello! How can I help you?')
        graph.add_node('ask_if_found', text='You should ask to the campus reception in case someone has found your card and has returned it there.')
        graph.add_node('ask_for_new_one', text='You should then ask for a new one, you can ask for a meeting in order to renew the student card following this link: http://fluvia.upf.edu/citescarnet/login.php. For more information you can always visit: www.upf.edu/carnetupf')
        graph.add_node('you_are_welcome', text='No problem. That is why I''m here :)')
        graph.add_node('goodbye', text='Goodbye!')
        graph.add_node('error', text="Sorry, I don't understand. Do you have any problem with your student card?")

        # add edges
        # todo: dos listas, una con posibilidades y otra con cosas que deben aparecer para ejecutar esa transicion?
        graph.add_edge('offer_help', 'ask_if_found', text=["can't find", 'lost'])
        graph.add_edge('offer_help', 'ask_for_new_one', text=["broken", 'not working', "doesn't work"])
        graph.add_edge('offer_help', 'error', text=[])

        graph.add_edge('ask_if_found', 'you_are_welcome', text=["thank you", 'thanks'])
        graph.add_edge('ask_if_found', 'goodbye', text=['bye', 'goodbye'])
        graph.add_edge('ask_if_found', 'ask_for_new_one', text=["already", 'done', 'asked'])
        graph.add_edge('ask_if_found', 'error', text=[])

        graph.add_edge('ask_for_new_one', 'you_are_welcome', text=["thank you", 'thanks'])
        graph.add_edge('ask_for_new_one', 'goodbye', text=['bye', 'goodbye'])
        graph.add_edge('ask_for_new_one', 'error', text=[])

        graph.add_edge('error', 'ask_if_found', text=["can't find", 'lost'])
        graph.add_edge('error', 'ask_for_new_one', text=["broken", 'not working', "doesn't work"])
        graph.add_edge('error', 'you_are_welcome', text=["thank you", 'thanks'])
        graph.add_edge('error', 'goodbye', text=['bye', 'goodbye'])
        graph.add_edge('error', 'error', text=[])

        self.graph = graph

    def parse_answer(self, node, answer):
        """ return number of the node to which we should transition, given that we
        are in 'node' and the user typed 'answer'
        """
        
        # get edges connecting 'node' with other nodes
        edges = [a for a in self.graph.edges() if a[0] == node]
        
        # get first edge that contains any of the words on 'answer'
        for edge in edges:
            text = self.graph.edge[edge[0]][edge[1]]['text']
            if set(text).intersection(answer.lower().split(' ')):
                return edge[1]

        # if no edge found, transition to 7
        return 'error'

    def create_dialog(self):
        """ starting on node 'offer_help', prints the machine answers according with
        the user questions, until no more transitions are possible
        """

        answer = raw_input("You enter Bea's virtual office. Welcome!\n>> ")  # 'hello' expected
        node = 'offer_help'
        while self.graph.successors(node):
            answer = raw_input(self.graph.node[node]['text'] + '\n>> ')
            edge = self.parse_answer(node, answer)
            node = edge
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
