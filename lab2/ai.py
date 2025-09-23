import random
from typing import Tuple, Union

from game import AI, State, Objective


class Counter():
    """
    Counter:
    help class for counting
    """
    def __init__(self):
        self.count: int = 0
    
    def add(self, num=1):
        self.count += num
    
    def get(self) -> int:
        return self.count
    
    def __str__(self) -> str:
        return str(self.count)
    
    def clear(self):
        self.count = 0
class Random(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        state = current_state.copy()

        available_moves = state.available_moves()
        if not available_moves:
            return None

        return random.choice(available_moves)


class MinMax(AI):
    @staticmethod
    def opposite_objective(objective: Objective):
        return Objective.MIN if objective == Objective.MAX else Objective.MAX
    
    @staticmethod
    def next_state_and_objective(current_state: State, move:int, objective: Objective) -> Tuple[State, Objective]:
        next_state = current_state.next_state(move)
        next_objective = objective if (current_state.current_player == next_state.current_player) else MinMax.opposite_objective(objective)
        return (next_state, next_objective)

        

    @staticmethod
    def best_move(current_state: State, objective: Objective):
        candidates_pits = current_state.available_moves()
        if not candidates_pits:
            return None
        counter = Counter()
        next_states_and_objectives = [MinMax.next_state_and_objective(current_state, pit, objective) for pit in candidates_pits]
        utilities = [MinMax.get_utility(state, objective, counter) for state, objective in next_states_and_objectives]
        decider = max if objective == Objective.MAX else min
        best_move = decider(enumerate(utilities), key=lambda x: x[1])
        print(f'{objective}\'s turn, {counter} states expanded')
        print(f'current state: {current_state}, available moves: {candidates_pits}')
        return candidates_pits[best_move[0]]
    
    @staticmethod
    def check_victory(current_state: State, objective: Objective) -> Union[None, float]:
        victory = current_state.check_victory()
        if victory is not None:
            # finished
            if victory == -1:
                # tie 
                return 0
            elif victory == 0:
                # player 0 wins
                return 1 if objective == Objective.MAX else -1
            elif victory == 1:
                # player 1 wins
                return -1 if objective == Objective.MAX else 1
        return None
    
    @staticmethod
    def get_utility(current_state: State, objective: Objective, counter: Counter = Counter()) -> float:
        counter.add(1)
        result = MinMax.check_victory(current_state, objective)
        if result is not None:  
            return result
        
        candidate_moves = current_state.available_moves()
        if len(candidate_moves) == 0:
            print(f'No moves available, state: {current_state}, check_victory: {MinMax.check_victory(current_state, objective)}')
            return 0
        decider = max if objective == Objective.MAX else min
        next_states_and_objectives = [MinMax.next_state_and_objective(current_state, move, objective) for move in candidate_moves]
        utilities = [MinMax.get_utility(state, objective, counter) for (state, objective) in next_states_and_objectives]
        # if counter.get() % 100000 == 0:
        #     print(f'{counter} {objective}\'s turn, considering state: {current_state}, available moves: {candidate_moves}, utilities: {utilities}')
        return decider(utilities)


MAX_DEPTH = 8
class DepthMinMax(AI):

    @staticmethod
    def best_move(current_state: State, objective: Objective):
        candidates_pits = current_state.available_moves()
        if not candidates_pits:
            return None
        counter = Counter()
        next_states_and_objectives = [MinMax.next_state_and_objective(current_state, pit, objective) for pit in candidates_pits]
        utilities = [DepthMinMax.get_utility(state, objective, 1, counter) for state, objective in next_states_and_objectives]
        decider = max if objective == Objective.MAX else min
        best_move = decider(enumerate(utilities), key=lambda x: x[1])
        print(f'{objective}\'s turn, {counter} states expanded')
        print(f'current state: {current_state}, available moves: {candidates_pits}')
        return candidates_pits[best_move[0]]
    
    @staticmethod
    def check_victory(current_state: State, objective: Objective) -> Union[None, float]:
        victory = current_state.check_victory()
        if victory is not None:
            # finished
            if victory == -1:
                # tie 
                return 0
            elif victory == 0:
                # player 0 wins
                return 1 if objective == Objective.MAX else -1
            elif victory == 1:
                # player 1 wins
                return -1 if objective == Objective.MAX else 1
        return None
    
    @staticmethod
    def get_utility(current_state: State, objective: Objective, depth: int = 0, counter: Counter = Counter()) -> float:
        counter.add(1)
        result = MinMax.check_victory(current_state, objective)
        if result is not None:  
            return result
        
        # not ended, but deep enough
        if depth >= MAX_DEPTH: 
            return current_state.score
        
        candidate_moves = current_state.available_moves()
        if len(candidate_moves) == 0:
            print(f'No moves available, state: {current_state}, check_victory: {MinMax.check_victory(current_state, objective)}')
            return 0
        decider = max if objective == Objective.MAX else min
        next_states_and_objectives = [MinMax.next_state_and_objective(current_state, move, objective) for move in candidate_moves]
        utilities = [DepthMinMax.get_utility(state, objective, depth+1, counter) for (state, objective) in next_states_and_objectives]
        # print(f'{objective}\'s turn, considering state: {current_state}, utilities: {utilities}')
        return decider(utilities)





class AlphaBeta(AI):
    """
    Alpha-Beta pruning
    General Idea:
    - Prune the search tree by keeping track of the best move found so far
    - If we found a utility of a optimal path that can not give any benifits to the opponent, we can stop the exploration in current branch
    Alpha: the best utility found so far for Max
    Beta: the best utility found so far for Min
    """
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        candidates_pits = current_state.available_moves()
        if not candidates_pits:
            return None
        alpha, beta = -1, 1
        utilities = []
        counter = Counter()
        for move in candidates_pits:
            next_state, next_objective = MinMax.next_state_and_objective(current_state, move, objective)
            utility = AlphaBeta.get_utility(next_state, next_objective, alpha, beta, counter)
            alpha, beta = AlphaBeta.get_new_alpha_beta(alpha, beta, utility, objective)
            utilities.append(utility)
        decider = max if objective == Objective.MAX else min
        best_move = decider(enumerate(utilities), key=lambda x: x[1])
        print(f'{objective}\'s turn, {counter} branch(es) cut')
        return best_move[0]
   
    @staticmethod
    def get_new_alpha_beta(alpha: float, beta: float, utility: float, objective: Objective) -> tuple[float, float]:
        if objective == Objective.MAX:
            alpha = max(alpha, utility)
        else:
            beta = min(beta, utility)
        return alpha, beta
    @staticmethod
    def get_utility(current_state: State, objective: Objective, alpha: float = -1, beta: float = 1, counter: Counter = Counter()) -> float:
        """
        alpha: the best utility found so far for Max, default by -1, because it will never worse by Max Lose in our case
        beta: the best utility found so far for Min, default by 1, because it will never worse by Max Win in our case
        """
        if result := MinMax.check_victory(current_state, objective):
            return result
        
        candidate_moves = current_state.available_moves()
        better = (lambda x, y: x if x > y else y) if objective == Objective.MAX else (lambda x, y: x if x < y else y)
        for idx, move in enumerate(candidate_moves):
            next_state = current_state.next_state(move)
            utility = AlphaBeta.get_utility(next_state, MinMax.opposite_objective(objective), alpha, beta, counter)
            if objective == Objective.MAX:
                alpha = better(alpha, utility)
            else:
                beta = better(beta, utility)
            # pruning
            # we found a optimal path that can make this branch worse enough that our opponent won't adopt this branch.
            # so that we can return early
            if alpha >= beta:
                # number of cut branches
                # print(f'Cut branches: {len(candidate_moves) - idx - 1}')
                counter.add(len(candidate_moves) - idx - 1)
                return utility
        
        return alpha if objective == Objective.MAX else beta
