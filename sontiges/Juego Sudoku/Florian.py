# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from typing import List


# 0 = casilla vacía
sudoku_easy = [[0,0,0,0,5,0,3,2,1],
               [2,0,0,0,0,0,0,0,0],
               [3,0,0,0,0,0,0,0,0],
               [4,0,0,0,0,0,0,0,0],
               [5,0,0,0,8,0,0,0,0],
               [6,0,0,0,0,0,0,0,0],
               [7,0,0,0,0,0,0,0,0],
               [8,0,0,0,0,0,0,0,0],
               [1,0,0,0,0,0,0,0,0]]

sudoku_hard = [[1,0,0,0,0,0,0,0,0],
               [0,2,0,0,0,0,0,0,0],
               [0,0,3,0,0,0,0,0,0],
               [0,0,0,4,0,0,0,0,0],
               [0,0,0,0,5,0,0,0,0],
               [0,0,0,0,0,6,0,0,0],
               [0,0,0,0,0,0,7,0,0],
               [0,0,0,0,0,0,0,8,0],
               [0,0,0,0,0,0,0,0,9]]

sudoku_extrem = [[9,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,8,0],
                 [0,0,0,0,0,0,7,0,0],
                 [0,0,0,0,0,6,0,0,0],
                 [0,0,0,0,5,0,0,0,0],
                 [0,0,0,4,0,0,0,0,0],
                 [0,0,3,0,0,0,0,0,0],
                 [0,2,0,0,0,0,0,0,0],
                 [1,0,0,0,0,0,0,0,0]]


class SudokuSolver:
    def __init__(self) -> None:
        self.runs = 0

    def solve_sudoku(self, sudoku_obj: List[List[int]]) -> bool:
        self.runs += 1
        pos = self.next_free_field(sudoku_obj)
        if pos is None:
            return True

        r, c = pos
        for number in range(1, 10):
            if self.is_number_valid_at_position(sudoku_obj, r, c, number):
                sudoku_obj[r][c] = number
                if self.solve_sudoku(sudoku_obj):
                    return True
                sudoku_obj[r][c] = 0

        return False

    @classmethod
    def is_number_valid_at_position(cls, sudoku_obj: List[List[int]], row: int, col: int, number: int) -> bool:
        # fila
        for i in range(9):
            if sudoku_obj[row][i] == number:
                return False
        # columna
        for i in range(9):
            if sudoku_obj[i][col] == number:
                return False
        # bloque 3x3
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if sudoku_obj[row_start + i][col_start + j] == number:
                    return False
        return True

    @classmethod
    def next_free_field(cls, sudoku_obj: List[List[int]]) -> tuple | None:
        for r in range(9):
            for c in range(9):
                if sudoku_obj[r][c] == 0:
                    return r, c
        return None


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        # --- ttk style (tema + estilos) ---
        self.style = ttk.Style(self.root)
        # Puedes probar: "clam", "alt", "default", "vista" (depende del SO)
        self.style.theme_use("clam")

        self.style.configure("Side.TFrame", padding=10)
        self.style.configure("Board.TFrame", padding=10)
        self.style.configure("TButton", padding=6)
        self.style.configure("Info.TLabel", padding=(0, 6))

        # Entry style (campo sudoku)
        self.style.configure(
            "Cell.TEntry",
            padding=2
        )

        self.entries: List[List[ttk.Entry]] = [[None for _ in range(9)] for _ in range(9)]
        self.build_gui()

    def build_gui(self) -> None:
        # Layout principal (2 columnas)
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.left_frame = ttk.Frame(self.root, style="Side.TFrame")
        self.left_frame.grid(row=0, column=0, sticky="nsw", padx=(15, 10), pady=10)

        self.sudoku_frame = ttk.Frame(self.root, style="Board.TFrame")
        self.sudoku_frame.grid(row=0, column=1, sticky="nsew")

        # --- Panel izquierdo (ttk) ---
        ttk.Button(self.left_frame, text="Lösen", command=self.solve, width=12).pack(fill="x")
        self.runs_label = ttk.Label(self.left_frame, text="Versuche: 0", style="Info.TLabel")
        self.runs_label.pack(fill="x")

        ttk.Button(self.left_frame, text="Leeren", command=self.clear, width=12).pack(fill="x")

        ttk.Separator(self.left_frame).pack(fill="x")

        ttk.Label(self.left_frame, text="Vorlagen").pack(anchor="w")
        ttk.Button(self.left_frame, text="Einfach", command=lambda: self.fill_sudoku(sudoku_easy)).pack(fill="x", pady=2)
        ttk.Button(self.left_frame, text="Schwer", command=lambda: self.fill_sudoku(sudoku_hard)).pack(fill="x", pady=2)
        ttk.Button(self.left_frame, text="Extrem", command=lambda: self.fill_sudoku(sudoku_extrem)).pack(fill="x", pady=2)

        ttk.Separator(self.left_frame).pack(fill="x")
        ttk.Button(self.left_frame, text="Beenden", command=self.root.destroy, width=12).pack(fill="x")

        # --- Tablero sudoku (truco visual con “bloques” 3x3 usando Frames) ---
        # Creamos 9 frames: cada frame es un bloque 3x3 con padding interno.
        block_frames = [[None for _ in range(3)] for _ in range(3)]
        for br in range(3):
            for bc in range(3):
                f = ttk.Frame(self.sudoku_frame, padding=6)
                f.grid(row=br, column=bc, padx=6, pady=6)
                block_frames[br][bc] = f

        # Validación: permitir solo "" o un dígito 1..9
        vcmd = (self.root.register(self._validate_cell), "%P")

        for r in range(9):
            for c in range(9):
                br, bc = r // 3, c // 3
                local_r, local_c = r % 3, c % 3

                e = ttk.Entry(
                    block_frames[br][bc],
                    width=2,
                    justify="center",
                    font=("Arial", 18),
                    style="Cell.TEntry",
                    validate="key",
                    validatecommand=vcmd,
                )
                e.grid(row=local_r, column=local_c, padx=3, pady=3, ipadx=6, ipady=6)
                self.entries[r][c] = e

        # Atajo: Enter = resolver
        self.root.bind("<Return>", lambda _evt: self.solve())

    @staticmethod
    def _validate_cell(proposed: str) -> bool:
        # proposed = texto que quedaría en el Entry
        if proposed == "":
            return True
        if len(proposed) == 1 and proposed in "123456789":
            return True
        return False

    def clear(self) -> None:
        for row in self.entries:
            for e in row:
                e.delete(0, tk.END)
        self.runs_label.config(text="Versuche: 0")

    def solve(self) -> None:
        solver = SudokuSolver()

        sudoku_current = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                val = self.entries[r][c].get()
                sudoku_current[r][c] = int(val) if val.isdigit() else 0

        if solver.solve_sudoku(sudoku_current):
            for r in range(9):
                for c in range(9):
                    self.entries[r][c].delete(0, tk.END)
                    self.entries[r][c].insert(0, "" if sudoku_current[r][c] == 0 else str(sudoku_current[r][c]))
        else:
            print("Keine Lösung gefunden!")

        self.runs_label.config(text=f"Versuche: {solver.runs}")

    def fill_sudoku(self, sudoku_obj: List[List[int]]) -> None:
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)
                self.entries[r][c].insert(0, "" if sudoku_obj[r][c] == 0 else str(sudoku_obj[r][c]))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sudoku (ttk)")
    root.geometry("700x560")
    App(root)
    root.mainloop()
