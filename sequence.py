#!/usr/bin/python3
import pandas as pd
import numpy as np
import sys, random
from copy import deepcopy
from decimal import Decimal


"""
Usage: python sequence.py <rankings_csv>
"""


class SeqSample(object):

    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.current = list(self.df.columns[1:-1])
        random.shuffle(self.current)


    def neighbor_move(self, num_moves=2):
        proposed = deepcopy(self.current)
        for i in range(0, num_moves):
            idx = range(len(self.current))
            i1, i2 = random.sample(idx, 2)
            proposed[i1], proposed[i2] = proposed[i2], proposed[i1]

        return proposed


    def score_sequence(self, sequence):
        score = 0
        idx = 0
        current = 'start'
        for song in sequence:
            nxt = sequence[idx]
            songscore = float(self.df[self.df['name']==nxt][current])
            score += songscore
            current = nxt
            idx += 1

        endscore = float(self.df[self.df['name']=='stop'][current])
        score += endscore

        return score


    def target(self, x):
        return np.exp(Decimal(x) / Decimal(self.temp))


    def accept(self, oldseq, newseq, t=1):
        old = self.score_sequence(oldseq)
        new = self.score_sequence(newseq)
        A = min(1, self.target(new - old))
        return random.uniform(0, 1) < A

    
    def main_loop(self, inner_i=100,
            start_moves=4, end_moves=1):
        temp_schedule = [20, 15, 10, 7, 5, 10, 5, 1, 5, 0.5, 0.1, 3, 1,
                0.1, 0.05]
        outer_i = len(temp_schedule)

        moves_increment = (start_moves - end_moves) / (outer_i - 1)
        moves = start_moves
        print('Initial num. moves: {}'.format(moves))
        for temp in temp_schedule:
            self.temp = temp
            print('Current temp: {}'.format(self.temp))
            print('Number of neighbor moves: {}'.format(round(moves)))
            accepted = 0
            for j in range(0, inner_i):
                self.proposed = self.neighbor_move(num_moves=round(moves))
                if self.accept(self.current, self.proposed):
                    accepted += 1
                    self.current = self.proposed
            print('Acceptance rate this round: {}'.format(
                accepted / inner_i
                ))
            moves -= moves_increment
            print('Current sequence:')
            print(self.current)
            print('Current score: {}'.format(self.score_sequence(self.current)))
            print('-----------------------------------------')

        print('FINAL SEQUENCE:')
        print(self.current)


def main():
    sampler = SeqSample(sys.argv[1])
    sampler.main_loop()

if __name__=='__main__':
    main()
