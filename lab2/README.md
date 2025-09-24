# Task1: 
- [x] implement recursive function which returns the utility of each available move
- [x] add counter for the number of expanded states, and output its value in the command line *assign to @duo*

# Questions1:
1. Suppose that we allow 5 seconds for the AI player to choose its next move.


    (a) What are the maximum dimensions of the board (number of pits and seeds) that allow this?
        
        3

    (b) How many nodes are then expanded?

        1 million+

2. For a small game, let the algorithm you implemented play against itself.

    (a) Which player won?

        player 0 won

    (b) What does it mean? Do you think that, as player 1, you could beat MinMax as player 0?

        MinMax player 0 can find a path to secure victory at the beginning. Absolutely player 1 can't beat MinMax player 0.

# Task2 depth-bounded:
- [x] Implement a function computing the score of each state, in class State, in file game.py. The more positive (resp. negative) the score is, the more the state should be favorable to player 0 (resp. player 1). *assign to @duo*
- [x] Modify your implementation so that each branch is explored up to a constant depth.  For now, we will set that maximum depth to 8. *assign to @duo, temporarily*

# Questions 2
1. What score function did you choose? Justify the intuition behind it.

        Compare the current seeds they gathered. If player 0 has more seeds than player 1, then returns 1. If player 1 has more seeds than player 0, then returns -1. If they have the same number of seeds, then returns 0.

        Intuition: The one that has more seeds right now is more likely to win.

2. Just like before, suppose that we allow 5 seconds for the AI player to choose its next
move.
    (a) What are the maximum dimensions of the board (number of pits and seeds) that allow this?

        6

    (b) How many nodes are then expanded?

        1 million (1180563)

3. Find some dimensions of the board such that, on your machine, the original (non- depth-bounded) algorithm takes 30 to 40 seconds to compute the first few moves.

        4*3 (4 pits for each player and 3 seeds in each pit) takes around 10 secs for the first step. any larger settings takes more than 2 minutes

    (a) At which (minimum) value should the cutoﬀ be set so that depth-bounded Min-Max achieves comparable results to MinMax?

        We've written a evaluate script, which simulate the game against random AI 10000 times to test the win rate.
        With depth bounded to 3, depth-bounded Min-Max can win 81% of the games. And with depth bounded to 8, it can win 96% of the games.

    (b) How many nodes do the algorithms then expand, respectively? How much faster is the depth-bounded algorithm?

        MinMax expanded 4166625 nodes, and takes 43.246 seconds for the first step.

        Depth-bounded Min-Max expanded 21137 nodes, and takes 48 milliseconds for the first step.

        Depth-bounded Min-Max is almost 900 times faster.

4. Suppose that we set the cutoﬀ to depth 1. How is that search then called?

        Greedy search.

# Task3
- [x] Starting from the code that you wrote previously, implement MinMax with Alpha-Beta
pruning in a separate class. *assign to @wenlin*
- [x] Add a counter that outputs the number of branches that have been cut during search. *assign to @wenlin*

# Questions 3
1. When the value for the depth cutoﬀ is the same for both algorithms, how do the outputs of Alpha-Beta compare to the ones of MinMax? Justify.
Slightly worse.

        Because if it's cutoff by depth, alpha-beta just got an estimated utility instead of the actual one, and it may apply pruning with the estimated alpha/beta, which may affect the choices in some cases.
        But Alpha-Beta is better in performance because of pruning.

2. Find some dimensions of the board such that, on your machine, depth-bounded Min-Max takes 30 to 40 seconds to compute the first few moves.

        7 * 8 (7 seeds in each pit and 8 pits per player) takes 20 seconds

    (a) How long does Alpha-Beta take to perform the same moves?

        34 ms

    (b) How many nodes are expanded?
    
        13332 nodes


## Bonus questions
1. How could the diﬃculty/strength of the AI should be tuned?

        depth cut: allow more depth to search will get more accurate utility result



2. Is it a good idea to simply limit the search time, and cut the search of the unbounded algorithm when it runs out of time?

        No. If we simply limit the search time, we still search deeply, but less branches. The expanded areas will be leaning to one side. By limiting the search depth, we can search averagely in each branch.