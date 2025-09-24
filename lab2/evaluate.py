#!/usr/bin/env python3
"""
Evaluation script for Kalah AI agents.
Pits a specified AI against a random AI for n games and collects statistics.
"""

import argparse
import time
import random
from typing import List, Tuple
from collections import defaultdict

from game import State, Objective
from ai import Random, MinMax, DepthMinMax, AlphaBeta
from settings import SEEDS, PITS_PER_PLAYER, PLAYER_0_STORE, PLAYER_1_STORE, TOTAL_PITS


class GameStats:
    """Statistics collector for a single game."""
    
    def __init__(self):
        self.move_times = []  # Time for each move in milliseconds
        self.winner = None
        self.total_moves = 0
        self.first_three_move_times = []  # Times for first 3 moves
        
    def add_move_time(self, move_time_ms: float):
        """Record the time taken for a move."""
        self.move_times.append(move_time_ms)
        self.total_moves += 1
        
        # Keep track of first 3 moves
        if len(self.first_three_move_times) < 3:
            self.first_three_move_times.append(move_time_ms)
    
    def get_avg_first_three_moves(self) -> float:
        """Get average time for first 3 moves."""
        if not self.first_three_move_times:
            return 0.0
        return sum(self.first_three_move_times) / len(self.first_three_move_times)


class AIGameEngine:
    """Engine for running AI vs AI games without GUI."""
    
    def __init__(self):
        self.ai_classes = {
            'random': Random,
            'minmax': MinMax,
            'depth_minmax': DepthMinMax,
            'alphabeta': AlphaBeta
        }
    
    def get_ai_class(self, ai_name: str):
        """Get AI class by name."""
        if ai_name not in self.ai_classes:
            raise ValueError(f"Unknown AI: {ai_name}. Available: {list(self.ai_classes.keys())}")
        return self.ai_classes[ai_name]
    
    def create_initial_state(self) -> State:
        """Create the initial game state."""
        pits = [SEEDS] * TOTAL_PITS
        pits[PLAYER_0_STORE] = 0
        pits[PLAYER_1_STORE] = 0
        return State(pits, 0)
    
    def play_game(self, ai0_class, ai1_class, starting_player: int = 0) -> Tuple[GameStats, int]:
        """
        Play a single game between two AI agents.
        
        Args:
            ai0_class: AI class for player 0
            ai1_class: AI class for player 1  
            starting_player: 0 for player 0 starts, 1 for player 1 starts, -1 for random
            
        Returns:
            Tuple of (GameStats, winner)
        """
        # Determine starting player
        if starting_player == -1:
            starting_player = random.randint(0, 1)
        
        # Create initial state
        state = self.create_initial_state()
        state.current_player = starting_player
        
        stats = GameStats()
        
        # Play the game
        while state.check_victory() is None:
            available_moves = state.available_moves()
            if not available_moves:
                break
                
            # Determine which AI to use
            if state.current_player == 0:
                ai_class = ai0_class
                objective = Objective.MAX
            else:
                ai_class = ai1_class
                objective = Objective.MIN
            
            # Get move from AI and time it
            start_time = time.perf_counter()
            move = ai_class.best_move(state, objective)
            end_time = time.perf_counter()
            
            if move is None:
                break
                
            # Record move time
            move_time_ms = (end_time - start_time) * 1000
            stats.add_move_time(move_time_ms)
            
            # Apply the move
            state = state.next_state(move)
        
        # Determine winner
        victory = state.check_victory()
        if victory == -1:
            stats.winner = -1
        elif victory:
            stats.winner = 1
        else:
            stats.winner = 0
        # print(f'Winner: {stats.winner}, pits: {state.pits}, player 0 store: {state.pits[PLAYER_0_STORE]}, player 1 store: {state.pits[PLAYER_1_STORE]}')
        
        return stats, stats.winner


def evaluate_ai(ai_name: str, n_games: int, starting_player: int = -1) -> None:
    """
    Evaluate an AI against random AI for n games.
    
    Args:
        ai_name: Name of the AI to evaluate
        n_games: Number of games to play
        starting_player: 0 for AI starts, 1 for random starts, -1 for random
    """
    engine = AIGameEngine()
    
    # Get AI classes
    eval_ai_class = engine.get_ai_class(ai_name)
    random_ai_class = engine.get_ai_class('random')
    
    print(f"Evaluating {ai_name} vs Random AI")
    print(f"Number of games: {n_games}")
    print(f"Starting player: {'Random' if starting_player == -1 else ('AI' if starting_player == 0 else 'Random AI')}")
    print("-" * 50)
    
    # Collect statistics
    game_stats = []
    wins = defaultdict(int)
    first_three_times = []
    
    for game_num in range(1, n_games + 1):
        print(f"Game {game_num}/{n_games}...", end=" ", flush=True)
        
        # Play game
        stats, winner = engine.play_game(eval_ai_class, random_ai_class, starting_player)
        
        # Record results
        game_stats.append(stats)
        wins[winner] += 1
        if stats.first_three_move_times:
            first_three_times.extend(stats.first_three_move_times)
        
        # Print game result
        if winner == 0:
            print(f"AI wins")
        elif winner == 1:
            print(f"Random wins")
        else:
            print(f"Tie")
    
    print("\n" + "=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50)
    
    # Calculate and print win rates
    total_games = len(game_stats)
    ai_wins = wins[0]
    random_wins = wins[1]
    ties = wins[-1]
    
    ai_win_rate = (ai_wins / total_games) * 100
    random_win_rate = (random_wins / total_games) * 100
    tie_rate = (ties / total_games) * 100
    
    print(f"Total games played: {total_games}")
    print(f"{ai_name} wins: {ai_wins} ({ai_win_rate:.1f}%)")
    print(f"Random AI wins: {random_wins} ({random_win_rate:.1f}%)")
    print(f"Ties: {ties} ({tie_rate:.1f}%)")
    
    # Calculate timing statistics
    if first_three_times:
        avg_first_three = sum(first_three_times) / len(first_three_times)
        print(f"\nTiming Statistics (First 3 moves):")
        print(f"Average time per move: {avg_first_three:.2f} ms")
        print(f"Min time: {min(first_three_times):.2f} ms")
        print(f"Max time: {max(first_three_times):.2f} ms")
    
    # Calculate overall move time statistics
    all_move_times = []
    for stats in game_stats:
        all_move_times.extend(stats.move_times)
    
    if all_move_times:
        avg_move_time = sum(all_move_times) / len(all_move_times)
        print(f"\nOverall Move Timing:")
        print(f"Average move time: {avg_move_time:.2f} ms")
        print(f"Total moves analyzed: {len(all_move_times)}")


def main():
    parser = argparse.ArgumentParser(description='Evaluate Kalah AI against Random AI')
    parser.add_argument('ai', help='AI to evaluate (random, minmax, depth_minmax, alphabeta)')
    parser.add_argument('-n', '--games', type=int, default=10, help='Number of games to play (default: 10)')
    parser.add_argument('-s', '--starting-player', type=int, choices=[-1, 0, 1], default=-1,
                       help='Starting player: -1=random, 0=AI first, 1=Random first (default: -1)')
    
    args = parser.parse_args()
    
    # Set random seed for reproducibility
    random.seed(42)
    
    try:
        evaluate_ai(args.ai, args.games, args.starting_player)
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
