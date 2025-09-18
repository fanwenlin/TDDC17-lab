import random
from typing import Union

from game import AI, State, Objective


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
    def best_move(current_state: State, objective: Objective):
        candidates_pits = current_state.available_moves()
        if not candidates_pits:
            return None
        next_states = [current_state.next_state(pit) for pit in candidates_pits]
        utilities = [MinMax.get_utility(current_state, MinMax.opposite_objective(objective)) for current_state in next_states]
        decider = max if objective == Objective.MAX else min
        best_move = decider(enumerate(utilities), key=lambda x: x[1])
        return best_move[0]
    
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
    def get_utility(current_state: State, objective: Objective) -> float:
        if result := MinMax.check_victory(current_state, objective):
            return result
        
        # print(f'{objective}\'s turn, considering state: {current_state}') 
        # not finished, continue the game
        candidate_moves = current_state.available_moves()
        decider = max if objective == Objective.MAX else min
        utilities = [MinMax.get_utility(current_state.next_state(move), MinMax.opposite_objective(objective)) for move in candidate_moves]
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
        for move in candidates_pits:
            next_state = current_state.next_state(move)
            utility = AlphaBeta.get_utility(next_state, MinMax.opposite_objective(objective), alpha, beta)
            alpha, beta = AlphaBeta.get_new_alpha_beta(alpha, beta, utility, objective)
            utilities.append(utility)
        decider = max if objective == Objective.MAX else min
        best_move = decider(enumerate(utilities), key=lambda x: x[1])
        return best_move[0]
   
    @staticmethod
    def get_new_alpha_beta(alpha: float, beta: float, utility: float, objective: Objective) -> tuple[float, float]:
        if objective == Objective.MAX:
            alpha = max(alpha, utility)
        else:
            beta = min(beta, utility)
        return alpha, beta
    @staticmethod
    def get_utility(current_state: State, objective: Objective, alpha: float = -1, beta: float = 1) -> float:
        """
        alpha: the best utility found so far for Max, default by -1, because it will never worse by Max Lose in our case
        beta: the best utility found so far for Min, default by 1, because it will never worse by Max Win in our case
        """
        if result := MinMax.check_victory(current_state, objective):
            return result
        
        candidate_moves = current_state.available_moves()
        better = (lambda x, y: x if x > y else y) if objective == Objective.MAX else (lambda x, y: x if x < y else y)
        for move in candidate_moves:
            next_state = current_state.next_state(move)
            utility = AlphaBeta.get_utility(next_state, MinMax.opposite_objective(objective), alpha, beta)
            if objective == Objective.MAX:
                alpha = better(alpha, utility)
            else:
                beta = better(beta, utility)
            if alpha >= beta:
                return utility
        
        return alpha if objective == Objective.MAX else beta
