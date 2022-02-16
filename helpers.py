import pandas as pd


def change_probs(probs, ind, amount):
    x = probs.copy()
    x[ind] += amount
    x /= x.sum()
    return x


def build_dataset(n_miners):
    return pd.DataFrame([{
        'Money in safe': 0,
        'Money in hand': 0,
        'Total money': 0,
        'Locks': 0,
        'Break ins': 0,
        'Successful break ins': 0,
        'Steal attempts': 0,
        'Successful steals': 0,
        'Last action': None
    } for _ in range(n_miners)])
