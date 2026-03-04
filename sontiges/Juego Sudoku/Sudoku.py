import sqlite3
import time
import copy
from typing import List

conn = sqlite3.connect("../solutions.db")
c = conn.cursor()

sudoku_empty = [[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]]

sudoku_easy = [[0,0,0,0,5,0,3,2,1],
               [2,0,0,0,0,0,0,0,0],
               [3,0,0,0,0,0,0,0,0],
               [4,0,0,0,0,0,0,0,0],
               [5,0,0,0,8,0,0,0,0],
               [6,0,0,0,0,0,0,0,0],
               [7,0,0,0,0,0,0,0,0],
               [8,0,0,0,0,0,0,0,0],
               [1,0,0,0,0,0,0,0,0]]

sudoku_hard = [[0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,3,0,8,5],
               [0,0,1,0,2,0,0,0,0],
               [0,0,0,5,0,7,0,0,0],
               [0,0,4,0,0,0,1,0,0],
               [0,9,0,0,0,0,0,0,0],
               [5,0,0,0,0,0,0,0,0],
               [0,0,2,0,1,0,0,0,0],
               [0,0,0,0,4,0,0,0,9]]

sudoku_extrem = [[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,3,0,8,5],
                 [0,0,1,0,2,0,0,0,0],
                 [0,0,0,5,0,7,0,0,0],
                 [0,0,4,0,0,0,1,0,0],
                 [0,9,0,0,0,0,0,0,0],
                 [5,0,0,0,0,0,0,0,0],
                 [0,0,2,0,1,0,0,0,0],
                 [0,0,0,0,4,0,0,0,0]]

runs = 0
version = "FILE"

def create_table() -> None:
    c.execute("""CREATE TABLE IF NOT EXISTS sudokus (before TEXT, after TEXT, runs INTEGER)""")


def sudoku_to_string(sudoku_obj: List[List[int]]) -> str:
    return ''.join(str(num) for row in sudoku_obj for num in row)


def string_to_sudoku(sudoku_str: str) -> List[List[int]]:
    sudoku_str = sudoku_str.strip()
    return [list(map(int, sudoku_str[i:i+9])) for i in range(0, len(sudoku_str), 9)]


def save_solution(before_solution: List[List[int]], after_solution: List[List[int]]) -> None:
    if version == "DB":
        c.execute("INSERT INTO sudokus VALUES (?, ?, ?)", (sudoku_to_string(before_solution), sudoku_to_string(after_solution), runs))
        conn.commit()

    if version == "FILE":
        with open("../solutions.txt", "a") as f:
            f.write(sudoku_to_string(before_solution) + "->" + sudoku_to_string(after_solution) + "\n")


def sudoku_has_solution(sudoku_obj: List[List[int]]) -> List[List[int]]|None:
    if version == "DB":
        c.execute("SELECT after FROM sudokus WHERE before=?", (sudoku_to_string(sudoku_obj),))
        result = c.fetchone()
        if result:
            return string_to_sudoku(result[0])
        else:
            return None

    if version == "FILE":
        try:
            with open("../solutions.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if sudoku_to_string(sudoku_obj) == line.split("->")[0]:
                        return string_to_sudoku(line.split("->")[1])
        except FileNotFoundError:
            return None


def solve_sudoku(sudoku_obj: List[List[int]]) -> bool:
    global runs
    runs += 1
    nff = next_free_field(sudoku_obj)

    if nff is None:
        return True

    for number in range(1, 10):
        if is_number_valid_at_position(sudoku_obj, nff[0], nff[1], number):
            sudoku_obj[nff[0]][nff[1]] = number

            if solve_sudoku(sudoku_obj):
                return True

        sudoku_obj[nff[0]][nff[1]] = 0

    return False


def is_number_valid_at_position(sudoku_obj: List[List[int]], row: int, col: int, number: int) -> bool:
    for i in range(9):
        if sudoku_obj[row][i] == number:
            return False

    for i in range(9):
        if sudoku_obj[i][col] == number:
            return False

    col_start = (col // 3) * 3
    row_start = (row // 3) * 3

    for i in range(3):
        for j in range(3):
            if sudoku_obj[row_start + i][col_start + j] == number:
                return False

    return True


def next_free_field(sudoku_obj: List[List[int]]) -> tuple|None:
    for row in range(9):
        for col in range(9):
            if sudoku_obj[row][col] == 0:
                return row, col

    return None


def view_sudoku(sudoku_obj: List[List[int]]) -> None:
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("-" * 21)

        for col in range(9):
            if col % 3 == 0 and col != 0:
                print("|", end=" ")

            print(sudoku_obj[row][col], end=" ")

        print()


if __name__ == "__main__":
    print('Welche Version soll ausgeführt werden? (DB/FILE)')
    print('1. DB')
    print('2. File')

    input_version = input()
    if input_version == "1":
        version = "DB"

    if version == "DB":
        create_table()

    print('Welches Sudoku soll gelöst werden?')
    print('1. Leeres Sudoku')
    print('2. Einfaches Sudoku')
    print('3. Schwieriges Sudoku')
    print('4. Extremes Sudoku')
    input_sudoku = input()

    match input_sudoku:
        case "1":
            sudoku = sudoku_empty
        case "2":
            sudoku = sudoku_easy
        case "3":
            sudoku = sudoku_hard
        case "4":
            sudoku = sudoku_extrem

    start_time = time.time()
    print(f"Versuche Sudoku zu lösen, bitte warten...")
    try:
        if sudoku_has_solution(sudoku):
            print(f"Eine Lösung des Sudokus ist:")
            print("#" * 21)
            sudoku = sudoku_has_solution(sudoku)
            view_sudoku(sudoku)
            print("#" * 21)
            print(f"Diese Sudoku wurde schon mal gelöst. {round(time.time() - start_time, 6)} Sekunden.")
        else:
            before_sudoku = copy.deepcopy(sudoku)
            solve_sudoku(sudoku)
            save_solution(before_sudoku, sudoku)
            print(f"Eine Lösung des Sudokus ist:")
            print("#" * 21)
            view_sudoku(sudoku)
            print("#" * 21)
            print(f"Aufrufe zum lösen des Sudokus: {runs}. Die Lösung hat eine Laufzeit von {round(time.time() - start_time, 6)} Sekunden.")

    except KeyboardInterrupt:
        print("Abgebrochen.")
        print(f"Aufrufe {runs}. Laufzeit {round(time.time() - start_time, 6)} Sekunden.")
    except RecursionError:
        print("Endlos. Es gibt keine Lösung?")
    finally:
        conn.close()