import random
import app
import board

from itertools import chain 

def get_best_moveset(board_string, iterations, min, max):
    best_path = None
    max_combo = 0
    min_moves = 100
    #matches = ()
    for i in range(iterations):
        for start_index in range(len(board_string)):
            for path in range(min, max):
                index = start_index #random.randint(0, 29)
                #path = random.randint(min, max)
                rand_path = board.generate_random_path(
                    index , path)
                #matches[index, path] = True
                followed_path = board.follow_path(board_string, rand_path)

                combo = board.count_matches(followed_path)
                moves = len(rand_path[1])
                if combo >= max_combo:
                    if combo > max_combo:
                        min_moves = max
                    max_combo = combo
                    if min_moves > moves:
                        print(f"Moves: {moves}, Combos: {combo}, path: {path}")
                        min_moves = moves
                        best_path = rand_path

    return best_path


def solve():
    board_string = app.generate_board_string()
    move_set = get_best_moveset(board_string, 10, 10, 50)
    #res = list(chain.from_iterable(move_set)) 
    

    for key in move_set:
        index = key
        for val in move_set[1]: 
            print(val)
        print(f"index: {index}, key: {key}, total move: {len(move_set[1])}")
        app.solve_window(board_string, index, move_set[1])
        


if __name__ == "__main__":
    solve()
