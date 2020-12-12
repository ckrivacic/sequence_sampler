# sequence_sampler
A simulated annealing sampler for sequencing

Requires a csv file with user-defined scores for each song transition. Each column and 
each row contains a different song, and each box represents the score of transtioning 
from the column song to the row song. You should also score transitions from "start"
to each song (how well does each song work as an opener?), and from each song to "stop"
(how well does each song work as a closer?). It is easiest to take the example csv and 
modify it with your scores.  
Scores can be any number, including negatives, but between 0 and 10 seems to work well.

Requirements:  
numpy  
pandas  
docopt

Usage:
./sequence.py example_scores.csv
