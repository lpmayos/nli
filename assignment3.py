import ipdb


def print_chart():
    """
    """
    print '\n\n\n\n'
    for i, col in enumerate(chart):
        print '\n--------------------------------------------------------------------------------'
        print 'chart[', i, ']'
        print '--------------------------------------------------------------------------------'

        for j, row in enumerate(chart[i]):

            rule = row['rule']
            rule = rule.split(' ')
            try:
                rule[row['dot_pos']] = '. ' + rule[row['dot_pos']]
            except:
                rule.append('.')

            if 'pointer_to_parent' in row:
                print row['key_rule'], ' --> ', ' '.join(rule), '               [', row['begin'], ', ', row['end'], ']               ', row['who_added_it'], ', ', row['pointer_to_parent'], '\n'
            else:
                print row['key_rule'], ' --> ', ' '.join(rule), '               [', row['begin'], ', ', row['end'], ']               ', row['who_added_it'], '\n'


def next_cat(state):
    """
    """
    return state['rule'].split()[state['dot_pos']]


def next_cats(state):
    """
    """
    return state['rule'].split()[state['dot_pos']::]


def enqueue(state, chart_pos):
    """
    """
    if chart_pos < len(chart) and state not in chart[chart_pos]:
        chart[chart_pos].append(state)
        print_chart()
    return


def earley_parser(words):
    """
    """
    chart[0].append({'key_rule': 'gamma',
                     'rule': 's',
                     'begin': 0,
                     'end': 0,
                     'dot_pos': 0,
                     'who_added_it': 'dummy start state',
                     'complete': False})

    for i in range(len(chart)):
        if i < len(words):
            word = words[i]

        for k, state in enumerate(chart[i]):
            if not state['complete'] and next_cat(state) not in final_words:
                predictor(state)
            elif not state['complete'] and next_cat(state) in final_words:
                scanner(state, word)
            else:
                completer(state, i, k)

    return chart


def predictor(state):
    """
    """
    next_categories = next_cats(state)
    for next_category in next_categories:
        if next_category in grammar:
            for expansion in grammar[next_category]:
                new_state = {'key_rule': next_category,
                             'rule': expansion,
                             'begin': state['end'],
                             'end': state['end'],
                             'dot_pos': 0,
                             'who_added_it': 'predictor',
                             'complete': False}
                enqueue(new_state, state['end'])
    return


def scanner(state, word):
    """
    """
    rule = state['rule'].split()[state['dot_pos']]
    if rule in grammar and word in grammar[rule]:
        new_state = {'key_rule': rule,
                     'rule': word,
                     'begin': state['begin'],
                     'end': state['end'] + 1,
                     'dot_pos': state['dot_pos'] + 1,
                     'who_added_it': 'scanner',
                     'complete': state['dot_pos'] + 1 >= len(word.split())}
        enqueue(new_state, state['end'] + 1)
    return


def completer(current_state, column, row):
    """
    """
    for state in chart[current_state['begin']] + chart[current_state['end'] - 1]:
        if not state['complete'] and state['rule'].split()[state['dot_pos']] == current_state['key_rule']:
            new_state = {'key_rule': state['key_rule'],
                         'rule': state['rule'],
                         'begin': state['begin'],
                         'end': current_state['end'],
                         'dot_pos': state['dot_pos'] + 1,
                         'who_added_it': 'completer',
                         'complete': state['dot_pos'] + 1 == len(state['rule'].split()),
                         'pointer_to_parent': [[column, row]]}
            enqueue(new_state, current_state['end'])
    return


# ------------------------------------------------------------------------------
# parsing_trees = []


# def _extract_paring_trees_helper(states_list, position):
#     """
#     """
#     for state in states_list:

#         try:
#             parsing_trees[position].append(state)
#         except:


#         if state['pointer_to_parent']:
#             _extract_paring_trees_helper(state['pointer_to_parent'], position + 1)
#     return


# def extract_parsing_trees():
#     """
#     """
#     for i, state in enumerate(chart[len(words)]):
#         if state['key_rule'] == 'gamma' and state['end'] == len(words):
#             final_state = state

#     _extract_paring_trees_helper([final_state], 0)

#     # ipdb.set_trace()

#     return
# ------------------------------------------------------------------------------


# phrase = "you need new permissions"

# final_words = ['pronoun', 'det', 'adj', 'n', 'md', 'v', 'prep']

# grammar = {'s': ['np vp'],
#            'np': ['pronoun', 'adj n'],
#            'vp': ['v np'],
#            'pronoun': ['you'],
#            'v': ['need'],
#            'adj': ['new'],
#            'n': ['permissions']}


phrase = "book that flight"

final_words = ['verb', 'det', 'noun', 'proper_noun', 'prep', 'aux']

# pag 381 pdf
grammar = {'s': ['np vp', 'aux np vp', 'vp'],
           'np': ['det nominal', 'proper_noun'],
           'nominal': ['noun', 'noun nominal'],
           'vp': ['verb', 'verb np'],
           'det': ['that', 'this', 'a'],
           'noun': ['book', 'flight', 'meal', 'money'],
           'verb': ['book', 'include', 'prefer'],
           'aux': ['does'],
           'prep': ['from', 'to', 'on'],
           'proper_noun': ['houston', 'twa']}

chart = [[] for x in range(len(phrase.split()) + 1)]
words = phrase.split()
earley_parser(words)
print_chart()
# extract_parsing_trees()
