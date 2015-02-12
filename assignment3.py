def print_chart():
    """
    """
    print '\n\n\n\n'
    for i, col in enumerate(chart):
        print '\n--------------------------------------------------------------------------------'
        print 'col ', i
        print '--------------------------------------------------------------------------------'

        for j, row in enumerate(chart[i]):
            print row['key_rule'], ' --> ', row['rule'], '               [', row['input_pos'], ', ', row['global_dot_pos'], ']               ', row['who_added_it'], '\n'
            # print row['key_rule'], ' --> ', row['rule'], row['input_pos'], row['global_dot_pos'], row['dot_pos'], '               ', row['who_added_it'], '\n'


def incomplete(state):
    """
    """
    return state['dot_pos'] < len(state['rule'].split())


def next_cat(state):
    """
    """
    return state['rule'].split()[state['dot_pos']]


def enqueue(state, chart_pos):
    """
    """
    if state not in chart[chart_pos]:
        chart[chart_pos].append(state)
        print_chart()
    return


def earley_parser(words):
    """
    """
    chart[0].append({'key_rule': 'gamma',
                     'rule': 's',
                     'input_pos': 0,
                     'global_dot_pos': 0,
                     'dot_pos': 0,
                     'who_added_it': 'dummy start state'})

    for i, word in enumerate(words):
        for state in chart[i]:
            if incomplete(state) and next_cat(state) not in final_words:
                predictor(state)
            elif incomplete(state) and next_cat(state) in final_words:
                scanner(state, word)
            else:
                completer(state)
    return chart


def predictor(state):
    """
    """
    next_category = next_cat(state)
    for expansion in grammar[next_category]:
        new_state = {'key_rule': next_category,
                     'rule': expansion,
                     'input_pos': state['input_pos'],
                     'global_dot_pos': state['global_dot_pos'],
                     'dot_pos': state['dot_pos'],
                     'who_added_it': 'predictor'}
        enqueue(new_state, state['input_pos'])
    return


def scanner(state, word):
    """
    """
    # check that we are parsing a phrase that we know how to parse
    if state['rule'] in grammar and word in grammar[state['rule']]:
        new_state = {'key_rule': state['rule'],
                     'rule': word,
                     'input_pos': state['input_pos'],
                     'global_dot_pos': state['global_dot_pos'] + 1,
                     'dot_pos': state['dot_pos'] + 1,
                     'who_added_it': 'scanner'}
        enqueue(new_state, state['input_pos'] + 1)
    return


def completer(current_state):
    """
    """
    for state in chart[current_state['input_pos']]:
        # if len(state['rule'].split()) > state['dot_pos']:
        if state['rule'].split()[state['dot_pos']] == current_state['key_rule']:
            new_state = {'key_rule': state['key_rule'],
                         'rule': state['rule'],
                         'input_pos': state['input_pos'],
                         'global_dot_pos': state['global_dot_pos'] + 1,
                         'dot_pos': state['dot_pos'] + 1,
                         'who_added_it': 'completer'}
            enqueue(new_state, state['input_pos'] + 1)
            # enqueue(new_state, state['input_pos'])
    return


# phrase = "you need new permissions"

# final_words = ['pronoun', 'det', 'adj', 'n', 'md', 'v', 'prep']

# grammar = {'s': ['np vp'],
#            'np': ['pronoun', 'adj n'],
#            'vp': ['v'],
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
           'proper_noun': ['houston', 'twa'],
           'nominal': ['nominal pp']}

chart = [[] for x in range(len(phrase.split()))]
words = phrase.split()
earley_parser(words)
print_chart()
