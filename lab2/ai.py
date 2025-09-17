import random

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
    def get_utility(current_state: State, objective: Objective) -> float:
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
        
        # print(f'{objective}\'s turn, considering state: {current_state}') 
        # not finished, continue the game
        candidate_moves = current_state.available_moves()
        decider = max if objective == Objective.MAX else min
        utilities = [MinMax.get_utility(current_state.next_state(move), MinMax.opposite_objective(objective)) for move in candidate_moves]
        return decider(utilities)





class AlphaBeta(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        pass
