# sequence_sampler
A simulated annealing sampler for sequencing

Requires a csv file with user-defined scores for each song transition. Each column and 
each row contains a different song, and each box represents the score of transtioning 
from the column song to the row song. You should also score transitions from "start"
to each song (how well does each song work as an opener?), and from each song to "stop"
(how well does each song work as a closer?). It is easiest to take the example csv and 
modify it with your scores.  

For example, the 4th row of the 3rd column in example_scores.csv rates
the transition from "LittleBlank" to "Temper" as 3, a moderate score,
whereas the 3rd row of the 4th column rates the transition from "Temper"
to "LittleBlank" as a 6, a significantly "better" transition.

Scores can be any number, including negatives, but between 0 and 10 seems to work well.
Note that this is not a deterministic algorithm, and it is not
parameterized to always find the highest scoring sequence; I didn't want
to over-fit to scores that are subjective and fuzzy to begin with.

Requirements:  
numpy  
pandas  
docopt

# Usage:

`./sequence.py example_scores.csv`  
If you want to save a playlist with the final sequence, just point the. 
script to a folder that contains audio files of your songs:  
`./sequence.py example_scores.csv -f /path/to/songfiles`
