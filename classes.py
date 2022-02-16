import numpy as np
import pandas as pd
from helpers import change_probs


class Safe:
    def __init__(self):
        self.money = 0
        self.locks = 0
        self.lock_price = 3


class Miner:
    def __init__(self):
        self.safe = Safe()
        self.actions = ['mine', 'lock', 'steal']
        self.action = None
        self.probs = np.array([0.8, 0.1, 0.1])
        self.earnings = 0
        self.steal_gains = np.array([])
        self.breakins = 0
        self.successful_breakins = 0
        self.steals = 0
        self.locks_cracked = 0
        self.successful_steals = 0
        self.steal_from_probs = None
        self.break_lock_chance = (1 + np.tanh(-1))/2

    def mine(self):
        self.earnings = 1
        self.probs = change_probs(self.probs, 0, 0.1)

    def lock(self):
        self.safe.locks += 1
        self.safe.money -= self.safe.lock_price
        self.earnings = 0

    def loss(self):
        self.breakins += 1
        locks_lost = 0
        while self.safe.locks > 0:
            chance = np.random.random()
            if chance <= self.break_lock_chance:
                self.safe.locks -= 1
                locks_lost += 1
            else:
                self.probs = change_probs(self.probs, 1, 0.01*self.safe.money*locks_lost/self.safe.locks)
                return 0, locks_lost

        self.successful_breakins += 1
        loss_money = self.safe.money
        self.safe.money = 0
        self.probs = change_probs(self.probs, 1, 0.1*loss_money)
        return loss_money, locks_lost

    def steal(self, neighbor):
        self.steals += 1
        gain, locks_cracked = neighbor.loss()
        self.locks_cracked += locks_cracked
        self.break_lock_chance = (1 + np.tanh(self.locks_cracked - 1)) / 2
        if np.random.random() > 0.85:
            gain = 0
        self.steal_gains = np.append(self.steal_gains, gain)
        self.probs = change_probs(self.probs, 2, 0.1*self.steal_gains.mean())
        if gain > 0:
            self.successful_steals += 1

    def add_earnings(self):
        self.safe.money += self.earnings


class Game:
    def __init__(self, miners=2):
        self.miners = [Miner() for _ in range(miners)]
        self.n_miners = miners
        self.day = 0
        self.stats = pd.DataFrame([{
            'Money in safe': 0,
            'Money in hand': 0,
            'Total money': 0,
            'Locks': 0,
            'Break ins': 0,
            'Successful break ins': 0,
            'Steal attempts': 0,
            'Successful steals': 0,
            'Last action': None
        } for _ in range(miners)])

    def good_morning(self):
        for miner in self.miners:
            miner.add_earnings()
            miner.action = np.random.choice(miner.actions, p=miner.probs)

        for miner in self.miners:
            if miner.action == 'mine':
                miner.mine()
            elif miner.action == 'lock':
                if miner.safe.money >= miner.safe.lock_price:
                    miner.lock()
                else:
                    miner.action = 'mine'
                    miner.mine()

        for i, miner in enumerate(self.miners):
            if miner.action == 'steal':
                if miner.steal_from_probs is None:
                    miner.steal_from_probs = np.array([1/(self.n_miners-1) for _ in range(self.n_miners)])
                    miner.steal_from_probs[i] = 0
                miner_to_steal = np.random.choice(self.n_miners, p=miner.steal_from_probs)
                miner.steal(self.miners[miner_to_steal])
                if miner.earnings == 0:
                    miner.steal_from_probs[miner_to_steal] *= 0.5
                    miner.steal_from_probs /= miner.steal_from_probs.sum()

        self.update_stats()
        self.day += 1

    def update_stats(self):
        self.stats['Money in safe'] = pd.Series([miner.safe.money for miner in self.miners])
        self.stats['Money in hand'] = pd.Series([miner.earnings for miner in self.miners])
        self.stats['Total money'] = pd.Series([(miner.earnings + miner.safe.money) for miner in self.miners])
        self.stats['Locks'] = pd.Series([miner.safe.locks for miner in self.miners])
        self.stats['Break ins'] = pd.Series([miner.breakins for miner in self.miners])
        self.stats['Successful break ins'] = pd.Series([miner.successful_breakins for miner in self.miners])
        self.stats['Steal attempts'] = pd.Series([miner.steals for miner in self.miners])
        self.stats['Successful steals'] = pd.Series([miner.successful_steals for miner in self.miners])
        self.stats['Last action'] = pd.Series([miner.action for miner in self.miners])
