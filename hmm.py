import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from hmmlearn import hmm
    
def viterbi(observe, state, start_prob, transition_prob, emit_p): #defines the variables used 
    V = [{}]

    for st in state:
        V[0][st] = {"prob": start_prob[st] * emit_p[st][observe[0]], "prev": None}

    # Start the viterbi algorithm when t >0

    for t in range(1, len(observe)):
        V.append({})

        for st in state:
            max_tr_prob = max(V[t-1][prev_st]["prob"]*transition_prob[prev_st][st] for prev_st in state)

            for prev_st in state:
                if V[t-1][prev_st]["prob"] * transition_prob[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][observe[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break

    for line in dptable(V):
        print(line)

    opt = []

    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None

    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break

    # Follow the backtrack till the first observeervation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print('The steps of state are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)


def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))
    
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)


observe = ('Sunny', 'Snowy', 'Rainy')
state = ('Go to class', 'Skip class')


start_prob = {'Go to class': 0.6, 'Skip class': 0.4}

transition_prob = {
   'Go to class' : {'Go to class': 0.7, 'Skip class': 0.3},
   'Skip class' : {'Go to class': 0.4, 'Skip class': 0.6}
   }
   
emit_p = {
   'Go to class' : {'Sunny': 0.5, 'Snowy': 0.4, 'Rainy': 0.1},
   'Skip class' : {'Sunny': 0.1, 'Snowy': 0.3, 'Rainy': 0.6}
   }
   
viterbi(observe,state,start_prob,transition_prob,emit_p)