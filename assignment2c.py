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

Todos:
    - i si no té username U...?
    - i si vol demanar hora més tard, etc? millorar funció ask_availability_function

"""

import sys
import random
import datetime
import networkx as nx
import matplotlib.pyplot as plt


class Graph():
    """
    """

    def __init__(self):
        """ create the necessary class variables and compute the initial phrases
        """
        # state graph
        self.graph = None

        # user information
        self.user_name = ""
        self.user_id = ""
        self.user_availability = None
        self.proposed_date = None
        self.proposed_date_str = ""

        # state transition information
        self.current_node = 'ask_name'
        self.last_node = ''

        # compute the phrases for each state
        self.compute_phrases()

    def draw_graph(self):
        """ draws the graph, without any label
        """
        # draw graph
        pos = nx.shell_layout(self.graph)
        nx.draw(self.graph, pos)

        # show graph
        plt.show()

    def draw_graph_with_labels(self):
        """ draws the graph, with labels on the nodes and on the edges
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
            edge_labels[edge] = self.graph.edge[edge[0]][edge[1]]['required_words']
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, label_pos=edge_text_pos)

        # show graph
        plt.show()

    def choose_phrase(self, node):
        """ given a node name 'node', returns a valid random phrase from the
        available phrases
        """
        if self.last_node in self.states_phrases[node]['last_node']:
            # last_node was a special case for the node where we are
            options = self.states_phrases[node]['last_node'][self.last_node]
        elif self.current_node == self.last_node and self.states_phrases[node]['recurrent']:
            # we are coming back to the same node
            options = self.states_phrases[node]['recurrent']
        else:
            # choose betwen regular options
            options = self.states_phrases[node]['options']

        return options[random.randint(0, len(options) - 1)]

    def compute_phrases(self):
        """ stores in self.state_phrases the valid phrases for every state.
        For each state, stores a dictionary with the regular options in
        'options', the phrase to show in case we couldn't find a transition and
        are repeating the state in 'recurrent', and special phrases to show in
        case we came from concrete states in 'last_node'
        """
        self.states_phrases = {'ask_name': {'options': ["Hi! What's your name?",
                                                        "Hello, could you remind me your name please?",
                                                        "Hi! I can't recall your name. It was...?"],
                                            'recurrent': ["Sorry, I couldn't get your name. What's your name again?"],
                                            'last_node': {'offer_help': ["Excuse me. I didn't get your name. Would you repeat it for me, please?"]}},
                               'offer_help': {'options': ["Of course! Sorry for my poor memory ;) How can I help you " + self.user_name + "?",
                                                          "Sure " + self.user_name + ". How can I help you?",
                                                          "Oh! How could I forgot if that's my cat's name? Tell me " + self.user_name + ", what can I do for you?"],
                                              'recurrent': ["Sorry " + self.user_name + ", I don't understand what you said. How can I help you with your student card?"],
                                              'last_node': {}},
                               'ask_problem': {'options': ["What kind of problem do you have?",
                                                           "Oh, what happened?"],
                                               'recurrent': ["Sorry, I don't understand. What kind of problem do you have (lost it, doesn't work, permission issues...)?"],
                                               'last_node': {}},
                               'ask_check_in_reception': {'options': ["Oh, I'm sorry to hear that. Have you asked in the campus reception?",
                                                                      "Really? Oh... Have you asked in the campus reception?",
                                                                      "Oh, I'm sorry, but you'll be expelled from the university... \n\n...\n\nJust kidding! Have you asked in the campus reception?"],
                                                          'recurrent': ["Sorry, I dont understand what you said. Did you check if they have found it in the campus reception?"],
                                                          'last_node': {}},
                               'check_in_reception': {'options': ["Then that's the first thing you have to do.",
                                                                  "You should go there first, to check if they found it."],
                                                      'recurrent': ["Sorry, I didn't hear you. What did you say?"],
                                                      'last_node': {}},
                               'goodbye': {'options': ["Bye " + self.user_name + "!",
                                                       "Glad to help you, " + self.user_name + "!",
                                                       "Goodbye " + self.user_name + ". Have a nice day!"],
                                           'recurrent': [],
                                           'last_node': {}},
                               'get_new_card': {'options': ["Oh, if it isn't working you should ask for a new one.",
                                                            "I see... Then you need a new one."],
                                                'recurrent': ["Sorry, I couldn't get what you just said. How can I help you?"],
                                                'last_node': {}},
                               'check_permissions': {'options': ["Oh, if the permissions are wrong you should ask for an update.",
                                                                 "I see... Then you need new permissions."],
                                                     'recurrent': ["Sorry, I couldn't get what you just said. How can I help you?"],
                                                     'last_node': {}},
                               'meeting_pie': {'options': ["You need to ask for a meeting at PIE. If you want I can do it for you.",
                                                           "You need to go to the library and arrange a meeting at the PIE. However, as I'm a machine (ba dum tssssss) I can do it for you."],
                                               'recurrent': ["Sorry, I couldn't get what you just said. How can I help you?"],
                                               'last_node': {}},
                               'explain_pie': {'options': ["PIE stands for Punt d'Informació de l'Estudiantat. Do you want me to arrange a meeting for you there?",
                                                           "Oh, it's the Punt d'Informació de l'Estudiantat. I can arrange a meeting for you if you want."],
                                               'recurrent': ["Sorry, I couldn't get what you just said. How can I help you?"],
                                               'last_node': {}},
                               'ask_userid': {'options': ["Ok. Can you give me your username? The one that starts with U...",
                                                          "Perfect. I need you username, the one starting with U..."],
                                              'recurrent': ["Sorry, I couldn't get what you just said. How can I help you?"],
                                              'last_node': {'ask_availability': ["Sorry, can you type again your username? Something went wrong..."]}},
                               'ask_availability': {'options': ["Ok " + self.user_id + ". Do you prefer the meeting to be in the morning or in the afternoon?",
                                                                self.user_id + ", got it. Would you like the meeting to be in the morning or in the afternoon?"],
                                                    'recurrent': ["Sorry, I couldn't get what you just said. How can I help you?"],
                                                    'last_node': {}},
                               'check_date': {'options': ["The next possible appointment could be " + self.proposed_date_str,
                                                          "If it is alright, I'll arrange you a meeting on " + self.proposed_date_str],
                                              'recurrent': ["Sorry, I couldn't get what you just said. How can I help you?"],
                                              'last_node': {}}}

    def parse_user_name(self, answer):
        """ finds the user name on the answer, by deleting all the dummy words;
        if after deleting them more than 3 words remain, no name has been found.
        """
        dummy_words = ['my', 'is', 'name', "i'm", 'am', 'i', 'hello', 'hi', ',', '.']
        array_answer = [a for a in answer if a not in dummy_words]
        if len(array_answer) > 0 and len(array_answer) < 4:
            self.user_name = ' '.join([a.capitalize() for a in array_answer])
            self.compute_phrases()  # recompute phrases because some of them contain self.user_name
        return

    def parse_user_id(self, answer):
        """ finds the user id on the answer by looking for a 7 letters word
        starting with 'u' followed by 6 digits, and stores it on self.user_id
        """
        for word in answer:
            if word[0] == 'u' and len(word) == 7 and word[1:7].isdigit():
                self.user_id = word
                self.compute_phrases()  # recompute phrases because some of them contain self.user_id
        return

    def ask_name_function(self, answer):
        """ finds the user name on the answer and stores it on self.user_name.
        returns a transition to offer_help if we found it, a recurrent
        transition otherwise
        """
        self.parse_user_name(answer)
        # return to ask_name
        if self.user_name == "":
            return (self.current_node, self.current_node)
        else:
            return ('ask_name', 'offer_help')

    def ask_userid_function(self, answer):
        """ finds the user id on the answer and stores it on self.user_id.
        returns a transition to ask_availability if we found it, a recurrent
        transition otherwise
        """
        self.parse_user_id(answer)
        if self.user_id == "":
            return (self.current_node, self.current_node)
        else:
            return ('ask_userid', 'ask_availability')

    def ask_availability_function(self, answer):
        """ identifies if the user would prefer a meeting in the morning or in
        the afternoon, and saves a proposed date on self.proposed_date.
        If it is not the first proposed date, it proposes a date on the next day
        """
        if 'morning' in answer:
            self.user_availability = 'morning'
        elif 'afternoon' in answer:
            self.user_availability = 'afternoon'

        # if user had not decided before and doesn't say anything now, 'morning' by default
        if not self.user_availability:
            self.user_availability = 'morning'

        hours = ['15:00', '16:00', '17:00', '17:30', '18:00']
        if self.user_availability == 'morning':
            hours = ['09:00', '10:00', '11:00', '11:30', '12:00']

        if not self.proposed_date:
            self.proposed_date = datetime.datetime.now() + datetime.timedelta(days=2)
        else:
            self.proposed_date = self.proposed_date + datetime.timedelta(days=1)

        self.proposed_date_str = self.proposed_date.strftime("%B %d") + " at " + hours[random.randint(0, len(hours) - 1)]

        self.compute_phrases()  # recompute phrases because some of them contain self.proposed_date_str
        return

    def create_graph(self):
        """ creates the graph with all possible nodes and transitions; saves it
        on self.graph
        """
        # create networkx graph
        graph = nx.DiGraph()

        # add regular nodes
        graph.add_nodes_from(['offer_help', 'ask_problem',
                              'ask_check_in_reception', 'check_in_reception',
                              'goodbye', 'get_new_card', 'check_permissions',
                              'meeting_pie', 'check_date'])

        # add nodes that need special ways of choose_next_node
        graph.add_node('ask_name', function=self.ask_name_function)
        graph.add_node('ask_userid', function=self.ask_userid_function)
        graph.add_node('ask_availability', function=self.ask_availability_function)

        # add edges
        graph.add_edge('ask_name', 'offer_help', required_words=[])
        graph.add_edge('ask_name', 'ask_name', required_words=[])

        graph.add_edge('offer_help', 'ask_problem', required_words=['problem', 'issue', 'question'])
        graph.add_edge('offer_help', 'ask_check_in_reception', required_words=['lost', 'find'])
        graph.add_edge('offer_help', 'get_new_card', required_words=['work', 'wrong', 'broken'])
        graph.add_edge('offer_help', 'check_permissions', required_words=['permission', 'permissions', 'access', 'rights'])
        graph.add_edge('offer_help', 'ask_name', required_words=[self.user_name, 'name'])
        graph.add_edge('offer_help', 'offer_help', required_words=[])

        graph.add_edge('ask_problem', 'ask_check_in_reception', required_words=['lost', 'find'])
        graph.add_edge('ask_problem', 'get_new_card', required_words=['work', 'wrong', 'broken'])
        graph.add_edge('ask_problem', 'check_permissions', required_words=['permission', 'permissions', 'access', 'rights'])
        graph.add_edge('ask_problem', 'ask_problem', required_words=[])

        graph.add_edge('ask_check_in_reception', 'check_in_reception', required_words=['no', 'not', "haven't", "didn't"])
        graph.add_edge('ask_check_in_reception', 'get_new_card', required_words=['yes', 'already', 'did', 'have'])
        graph.add_edge('ask_check_in_reception', 'ask_check_in_reception', required_words=[])

        graph.add_edge('check_in_reception', 'goodbye', required_words=['thank', 'thanks', 'bye', 'goodbye', 'perfect', 'great', 'awesome'])
        graph.add_edge('check_in_reception', 'get_new_card', required_words=['but', 'what', 'if', 'next', 'how'])
        graph.add_edge('check_in_reception', 'check_in_reception', required_words=["can't find", 'lost'])

        graph.add_edge('get_new_card', 'goodbye', required_words=['thank', 'thanks', 'bye', 'goodbye', 'perfect', 'great', 'awesome'])
        graph.add_edge('get_new_card', 'meeting_pie', required_words=['how', 'where', 'who'])
        graph.add_edge('get_new_card', 'get_new_card', required_words=[])

        graph.add_edge('check_permissions', 'goodbye', required_words=['thank', 'thanks', 'bye', 'goodbye', 'perfect', 'great', 'awesome'])
        graph.add_edge('check_permissions', 'meeting_pie', required_words=['how', 'where', 'who'])
        graph.add_edge('check_permissions', 'check_permissions', required_words=[])

        graph.add_edge('meeting_pie', 'goodbye', required_words=['no', 'not', 'myself'])
        graph.add_edge('meeting_pie', 'ask_userid', required_words=['yes', 'please', 'sure'])
        graph.add_edge('meeting_pie', 'explain_pie', required_words=['pie', 'sorry', 'explain'])
        graph.add_edge('meeting_pie', 'meeting_pie', required_words=[])

        graph.add_edge('explain_pie', 'ask_userid', required_words=['yes', 'please', 'sure'])
        graph.add_edge('explain_pie', 'goodbye', required_words=['no', 'not', 'myself'])
        graph.add_edge('explain_pie', 'explain_pie', required_words=[])

        graph.add_edge('ask_userid', 'ask_availability', required_words=[])
        graph.add_edge('ask_userid', 'ask_userid', required_words=[])

        graph.add_edge('ask_availability', 'ask_userid', required_words=['no', 'mistake', 'error', 'wrong', 'sorry'])
        graph.add_edge('ask_availability', 'check_date', required_words=['afternoon', 'morning', 'care', 'soon', 'sooner', 'same'])
        graph.add_edge('ask_availability', 'ask_availability', required_words=[])

        graph.add_edge('check_date', 'ask_availability', required_words=['no', 'change', 'wrong', 'impossible'])
        graph.add_edge('check_date', 'goodbye', required_words=['thank', 'thanks', 'bye', 'goodbye', 'perfect', 'great', 'awesome'])
        graph.add_edge('check_date', 'check_date', required_words=[])

        self.graph = graph

    def parse_answer(self, answer):
        """ cleans the answer to be able to split it into words, by separating
        punctuation marks and deleting '.', ',' and ':'.
        """
        answer.replace('!', ' !').replace('?', ' ?').replace(',', '').replace('.', '').replace(':', '')
        return answer.lower().split(' ')

    def choose_next_node(self, answer):
        """ returns the edge to which we should transition, given that we are in
        self.current_node and the user typed 'answer'
        """
        # parse user answer
        answer = self.parse_answer(answer)

        # special cases

        if 'function' in self.graph.node[self.current_node]:
            edge = self.graph.node[self.current_node]['function'](answer)
            if edge:
                return edge

        # normal cases

        # get edges connecting 'node' with other nodes
        edges = [a for a in self.graph.edges() if a[0] == self.current_node]

        # get edge that contains more keyword coincidences with 'answer'
        max_required_words = 0
        best_edge = None
        need_recheck = False
        for edge in edges:
            required_words = self.graph.edge[edge[0]][edge[1]]['required_words']

            num_required_words = len(set(required_words).intersection(answer))

            if num_required_words > max_required_words:
                max_required_words = num_required_words
                best_edge = edge
                need_recheck = False
            elif num_required_words == max_required_words:
                need_recheck = True

        if need_recheck:
            return (self.current_node, self.current_node)
        elif best_edge:
            return best_edge
        else:
            # if no edge found, transition to current node again
            return (self.current_node, self.current_node)

    def create_dialog(self):
        """ starting on self.current_node, keeps printing the current node text,
        waits for a user answer and chooses a transition to the next node
        according to user answer, until no more transitions are possible.
        """
        # initial situation explanation
        answer = raw_input("\n'KNOCK KNOCK!!' \n\n... \n\n'Please come in!!' \n\n... \n\nYou enter Bea's virtual office; please be nice and say hello :)\n\n>> ")  # 'hello' expected

        # main loop
        while self.graph.successors(self.current_node):
            answer = raw_input(self.choose_phrase(self.current_node) + '\n>> ')
            edge = self.choose_next_node(answer)
            self.last_node = self.current_node
            self.current_node = edge[1]

        # show last node text
        if not self.graph.successors(self.current_node):
            print self.choose_phrase(self.current_node) + "\n"
        return


def main():
    graph = Graph()
    graph.create_graph()
    graph.create_dialog()
    # graph.draw_graph_with_labels()

if __name__ == '__main__':
    status = main()
    sys.exit(status)
