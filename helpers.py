import numpy as np


def change_probs(probs, ind, amount):
    x = probs.copy()
    x[ind] += amount
    x = x/x.sum()
    return x
