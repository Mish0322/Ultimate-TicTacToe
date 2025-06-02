from backend.game import Game
from backend.MCTSStrategy import MCTSStrategy, MCTSNode
from random import choice
from multiprocessing import Pool, cpu_count
import time


class RandomStrategy:
    def __call__(self, game):
        valid_moves = game.get_valid_moves()
        if valid_moves:
            game.make_move(choice(valid_moves))


class BestMoveOneStrategy:
    def __init__(self, depth=2):
        self.depth = depth

    def __call__(self, game):
        game.best_move(depth=2, eval_func=game.evaluate_one)


class BestMoveTwoStrategy:
    def __init__(self, depth=2):
        self.depth = depth

    def __call__(self, game):
        game.best_move(depth=2, eval_func=game.evaluate_two)


def simulate_game(_, p1_strategy, p2_strategy):
    game = Game()
    moves = 0

    while game.check_winner() == 0:
        if game.turn == 1:
            p1_strategy(game)
        else:
            p2_strategy(game)
        moves += 1

    return game.check_winner(), moves


def run_simulation(label, n, p1_strategy, p2_strategy):
    num_games = n
    num_processes = cpu_count()

    print(f"Starting {label} simulation with {num_processes} processes…")
    start_time = time.perf_counter()

    with Pool(processes=num_processes) as pool:
        results = pool.starmap(
            simulate_game, [(i, p1_strategy, p2_strategy) for i in range(num_games)]
        )

    end_time = time.perf_counter()
    total_time = end_time - start_time

    pOne = sum(1 for winner, _ in results if winner == 1)
    pTwo = sum(1 for winner, _ in results if winner == 2)
    ties = sum(1 for winner, _ in results if winner == 3)
    total_moves = sum(moves for _, moves in results)

    avg_game_time = total_time / num_games
    avg_move_time = total_time / total_moves

    print()
    print(f"Results for {label}:")
    print("Total games:", num_games)
    print("Player 1 wins:", pOne)
    print("Player 2 wins:", pTwo)
    print("Ties:", ties)
    print(f"Total simulation time: {total_time:.2f} seconds")
    print(f"Average time per game: {avg_game_time:.4f} seconds")
    print(f"Average time per move: {avg_move_time:.6f} seconds")
    print("-" * 40)
    return total_time


if __name__ == "__main__":
    run_simulation("Random vs Random", 1000, RandomStrategy(), RandomStrategy())
    run_simulation("DLMM1 vs Random", 1000, BestMoveOneStrategy(2), RandomStrategy())
    run_simulation("DLMM2 vs Random", 1000, BestMoveTwoStrategy(2), RandomStrategy())
    run_simulation("DLMM2+4 vs Random", 1000, BestMoveTwoStrategy(4), RandomStrategy())
    run_simulation(
        "DLMM1 vs DLMM2", 1000, BestMoveOneStrategy(2), BestMoveTwoStrategy(2)
    )
    run_simulation(
        "DLMM2 vs DLMM2+4", 1000, BestMoveTwoStrategy(2), BestMoveTwoStrategy(4)
    )
    run_simulation(
        "MCTS vs Random", 1000, MCTSStrategy(iterations=300), RandomStrategy()
    )
    run_simulation(
        "MCTS(100) vs MCTS(300)",
        1000,
        MCTSStrategy(iterations=100),
        MCTSStrategy(iterations=300),
    )
    run_simulation(
        "MCTS vs DLMM2", 1000, MCTSStrategy(iterations=300), BestMoveTwoStrategy(4)
    )
