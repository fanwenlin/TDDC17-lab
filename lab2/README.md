# Task1: 
- [x] implement recursive function which returns the utility of each available move
- [ ] add counter for the number of expanded states, and output its value in the command line *assign to @duo*

# Questions1:
1. Suppose that we allow 5 seconds for the AI player to choose its next move.
(a) What are the maximum dimensions of the board (number of pits and seeds) that
allow this?
(b) How many nodes are then expanded?
2. For a small game, let the algorithm you implemented play against itself.
(a) Which player won?
(b) What does it mean? Do you think that, as player 1, you could beat MinMax as
player 0?

# Task2 depth-bounded:
- [ ] Implement a function computing the score of each state, in class State, in file game.py. The more positive (resp. negative) the score is, the more the state should be favorable to player 0 (resp. player 1). *assign to @duo*
- [ ] Modify your implementation so that each branch is explored up to a constant depth.  For now, we will set that maximum depth to 8. *assign to @duo, temporarily*

# Questions 2
1. What score function did you choose? Justify the intuition behind it.
2. Just like before, suppose that we allow 5 seconds for the AI player to choose its next
move.
(a) What are the maximum dimensions of the board (number of pits and seeds) that
allow this?
(b) How many nodes are then expanded?
3. Find some dimensions of the board such that, on your machine, the original (non-
depth-bounded) algorithm takes 30 to 40 seconds to compute the first few moves.
(a) At which (minimum) value should the cutoﬀ be set so that depth-bounded Min-
Max achieves comparable results to MinMax?
(b) How many nodes do the algorithms then expand, respectively? How much faster
is the depth-bounded algorithm?
4. Suppose that we set the cutoﬀ to depth 1. How is that search then called?

# Task3
- [x] Starting from the code that you wrote previously, implement MinMax with Alpha-Beta
pruning in a separate class. *assign to @wenlin*
- [ ] Add a counter that outputs the number of branches that have been cut during search. *assign to @wenlin*

# Questions 3
1. When the value for the depth cutoﬀ is the same for both algorithms, how do the
outputs of Alpha-Beta compare to the ones of MinMax? Justify.
2. Find some dimensions of the board such that, on your machine, depth-bounded Min-
Max takes 30 to 40 seconds to compute the first few moves.
(a) How long does Alpha-Beta take to perform the same moves?
(b) How many nodes are expanded?
## Bonus questions
1. How could the diﬃculty/strength of the AI should be tuned?
2. Is it a good idea to simply limit the search time, and cut the search of the unbounded
algorithm when it runs out of time?