final_words = ['pronoun', 'det', 'adj', 'n', 'md', 'v', 'prep']

grammar = {'s': ['np vp'],
           'np': ['pronoun', 'adj n'],
           'vp': ['v'],
           'pronoun': ['you'],
           'v': ['need'],
           'adj': ['new'],
           'n': ['permissions']}

# matrix with N +1 columns (N is the number of words);
# each column contains M rows;
# each row contains a list with: [rule, words position in the sentence, dot position]
chart = []


def incomplete(state):
    """
    """
    return bool


def next_cat(state):
    """
    """
    return bool


def enqueue(state, chart_pos):
    """
    """
    if state not in chart[chart_pos]:
        chart[chart_pos].append(state)


def earley_parser(words):
    """
    """
    # add dummy state
    chart[0][0] = ['gamma', ['s'], 0, 0]

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
    state = state[1].split()
    for next_state in state:
        for rule in grammar[next_state]:  # grammar[s] = ['np vp']
            new_state = [next_state, rule, state[2], state[3]]
            enqueue(new_state, state[2])
    return


def scanner(state, word):
    """
    """
    if word in grammar[state[1]]:
        new_state = [state[1], word, state[2], state[3] + 1]
        enqueue(new_state, state[2])
    return


def completer(state):
    """
    """
    return

phrase = "you need new permissions"
words = phrase.split()
earley_parser(words)
