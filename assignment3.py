def print_chart():
    """
    """
    print '\n\n\n\n'
    for i, col in enumerate(chart):
        print '\n----------------------------------------------------------------------------------------------------------------'
        print 'chart[', i, ']'
        print '----------------------------------------------------------------------------------------------------------------'
        aux = 0
        for j, row in enumerate(chart[i]):

            rule = row['rule']
            rule = rule.split(' ')
            try:
                rule[row['dot_pos']] = '. ' + rule[row['dot_pos']]
            except:
                rule.append('.')

            if 'pointer_to_parent' in row:
                print aux, '   ', row['key_rule'], ' --> ', ' '.join(rule), '               [', row['begin'], ', ', row['end'], ']               ', row['who_added_it'], ', ', row['pointer_to_parent'], '\n'
            else:
                print aux, '   ', row['key_rule'], ' --> ', ' '.join(rule), '               [', row['begin'], ', ', row['end'], ']               ', row['who_added_it'], '\n'
            aux+=1


def next_cat(state):
    """
    """
    return state['rule'].split()[state['dot_pos']]


def next_cats(state):
    """
    """
    return state['rule'].split()[state['dot_pos']::]


def state_in_chart_pos(new_state, chart_pos):
    """
    """
    for state in chart[chart_pos]:
        if state['key_rule'] == new_state['key_rule'] and state['rule'] == new_state['rule'] and state['begin'] == new_state['begin'] and state['end'] == new_state['end'] and state['dot_pos'] == new_state['dot_pos'] and state['who_added_it'] == new_state['who_added_it'] and state['complete'] == new_state['complete']:
            return True
    return False


def enqueue(state, chart_pos):
    """
    """
    try:
        if not state_in_chart_pos(state, chart_pos):
            chart[chart_pos].append(state)
    except:
        return
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

    for chart_pos in chart[int(current_state['begin']):int(current_state['end']) + 1]:  # VIK MOD
        for state in chart_pos:
            if not state['complete'] and state['rule'].split()[state['dot_pos']] == current_state['key_rule']:
                if 'pointer_to_parent' in state:
                    col1 = state['pointer_to_parent'][0][0]
                    row1 = state['pointer_to_parent'][0][1]
                    new_state = {'key_rule': state['key_rule'],
                                 'rule': state['rule'],
                                 'begin': state['begin'],
                                 'end': current_state['end'],
                                 'dot_pos': state['dot_pos'] + 1,
                                 'who_added_it': 'completer',
                                 'complete': state['dot_pos'] + 1 == len(state['rule'].split()),
                                 'pointer_to_parent': [[column, row]]}
                    new_state['pointer_to_parent'].append([col1,row1])

                else:
                    new_state = {'key_rule': state['key_rule'],
                                 'rule': state['rule'],
                                 'begin': state['begin'],
                                 'end': current_state['end'],
                                 'dot_pos': state['dot_pos'] + 1,
                                 'who_added_it': 'completer',
                                 'complete': state['dot_pos'] + 1 == len(state['rule'].split()),
                                 'pointer_to_parent': [[column, row]]}
                enqueue(new_state, current_state['end'])
            if state == current_state:
                break
    return


def extract_parsing_trees():
    """
    """
    for i, state in enumerate(chart[len(words)]):
        if state['key_rule'] == 'gamma' and state['end'] == len(words):
            final_state = state

    final_set = []

    row = 99
    col = 99

    while True:
        if final_state["key_rule"] + " --> " + final_state["rule"] not in final_set: 
            final_set.append(final_state["key_rule"] + " --> " + final_state["rule"])
        if row == 0:
            for state in chart[col - 1]:
                if 'pointer_to_parent' in state:
                    final_state = state
                    if final_state["key_rule"] + " --> " + final_state["rule"] not in final_set: 
                        final_set.append(final_state["key_rule"] + " --> " + final_state["rule"])
                    break
        if row == 0 and col == 1:
            break
        else:
            row = final_state['pointer_to_parent'][0][1]
            col = final_state['pointer_to_parent'][0][0]
            if len(final_state['pointer_to_parent']) == 2:
                row1 = final_state['pointer_to_parent'][1][1]
                col1 = final_state['pointer_to_parent'][1][0]
                if chart[col1][row1]["key_rule"] + ' --> ' + chart[col1][row1]["rule"] not in final_set:
                    final_set.append(chart[col1][row1]["key_rule"] + ' --> ' + chart[col1][row1]["rule"])
            final_state = chart[col][row]

    print final_set

    return


phrase = "you need new permissions"
# phrase = "I can arrange a meeting for you"
# phrase = "the next possible appointment could be tomorrow"

final_words = ['pronoun', 'det', 'adj', 'n', 'md', 'v', 'prep']

grammar = {'s': ['np vp'],
           'np': ['pronoun', 'adj n', 'np pp', 'det n', 'n', 'det adj adj n'],
           'pp': ['prep pronoun'],
           'vp': ['v np', 'md vp'],
           'pronoun': ['you', 'I'],
           'det': ['a', 'the'],
           'prep': ['for'],
           'v': ['need', 'be', 'arrange'],
           'adj': ['new', 'next', 'possible'],
           'md': ['can', 'could'],
           'n': ['permissions', 'meeting', 'appointment', 'tomorrow']}

# testing data from http://www.inf.ed.ac.uk/teaching/courses/inf2a/slides/2007_inf2a_L18_slides.pdf
# phrase = "fish swim in the soup"
# final_words = ['verb', 'det', 'noun', 'relpro', 'prep']
# grammar = {'s': ['np vp'],  # 's': ['np vp', 'aux np vp', 'vp'],
#            'np': ['det nominal', 'nominal'],
#            'nominal': ['noun srel', 'noun'],
#            'vp': ['verb pp', 'verb np', 'verb'],
#            'pp': ['prep np'],
#            'srel': ['relpro vp'],
#            'det': ['the', 'a'],
#            'noun': ['fish', 'frog', 'soup'],
#            'verb': ['saw', 'eat', 'swim'],
#            'relpro': ['that'],
#            'prep': ['in', 'for']}


# testing data from the book (page 381 of the pdf)
# phrase = "book that flight"
# final_words = ['verb', 'det', 'noun', 'proper_noun', 'prep', 'aux']
# grammar = {'s': ['np vp', 'aux np vp', 'vp'],
#            'np': ['det nominal', 'proper_noun'],
#            'nominal': ['noun', 'noun nominal'],
#            'vp': ['verb', 'verb np'],
#            'det': ['that', 'this', 'a'],
#            'noun': ['book', 'flight', 'meal', 'money'],
#            'verb': ['book', 'include', 'prefer'],
#            'aux': ['does'],
#            'prep': ['from', 'to', 'on'],
#            'proper_noun': ['houston', 'twa']}

chart = [[] for x in range(len(phrase.split()) + 1)]
words = phrase.split()
earley_parser(words)
print_chart()
extract_parsing_trees()
