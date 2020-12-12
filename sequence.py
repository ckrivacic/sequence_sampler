"""
Usage: 
    sequence.py <rankings_csv> [options]

Options:
    -f, --folder=[PATH]
        Look for files that match the song names in the provided folder and
        create an m3u playlist from the final sequence.
"""


import pandas as pd
import numpy as np
import docopt
import sys, random, os
from copy import deepcopy
from decimal import Decimal
from difflib import get_close_matches


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


def match_files(sequence, folder):
    # filelist = glob.glob(os.path.join(folder, '*.wav'))
    folder = os.path.expanduser(folder)
    filelist = os.listdir(folder)
    match_dict = {}
    for song in sequence:
        match = get_close_matches(song, filelist, n=1, cutoff=0.1)
        match_dict[song] = match[0]


    with open(os.path.join(folder, 'sequence.m3u'), 'w') as f:
        for song in sequence:
            f.write(match_dict[song] + '\n')

    print('Sequence written to {}'.format(
        os.path.join(folder, 'sequence.m3u')
        ))

def main():
    args = docopt.docopt(__doc__)
    sampler = SeqSample(args['<rankings_csv>'])
    sampler.main_loop()

    if args['--folder']:
        match_files(sampler.current, args['--folder'])


if __name__=='__main__':
    main()
