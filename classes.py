import numpy as np
import pandas as pd


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
        self.probs = np.array([.8, .1, .1])
        self.earnings = 0
        self.break_lock_chance = 0.3

    def mine(self):
        self.earnings = 1

    def lock(self):
        self.safe.locks += 1
        self.safe.money -= self.safe.lock_price
        self.earnings = 0

    def loss(self):
        while self.safe.locks > 0:
            chance = np.random.random()
            if chance <= self.break_lock_chance:
                self.safe.locks -= 1
            else:
                return 0

        loss_money = self.safe.money
        self.safe.money = 0
        return loss_money

    def steal(self, neighbor):
        gain = neighbor.loss()
        self.earnings = gain

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
                miner_probs = np.random.random(self.n_miners)
                miner_probs[i] = 0
                miner_to_steal = miner_probs.argmax()
                miner.steal(self.miners[miner_to_steal])

        self.update_stats()
        self.day += 1

    def update_stats(self):
        self.stats['Money in safe'] = pd.Series([miner.safe.money for miner in self.miners])
        self.stats['Money in hand'] = pd.Series([miner.earnings for miner in self.miners])
        self.stats['Total money'] = pd.Series([(miner.earnings + miner.safe.money) for miner in self.miners])
        self.stats['Locks'] = pd.Series([miner.safe.locks for miner in self.miners])
        self.stats['Last action'] = pd.Series([miner.action for miner in self.miners])
