"""
data base for SQLite
"""

import sqlite3
from datetime import datetime


class PredictionRepository:
    def __init__(self, db_path):
        self.db_path = db_path  # verification
        self._create_table()  # create table

    def _connect(self):
        return sqlite3.connect(self.db_path)  # conect with SQL

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    area INTEGER NOT NULL,
                    predicted_price REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()  # create table if doesn´t exist

    def save_prediction(self, area: int, predicted_price: float):
        timestamp = datetime.now().isoformat(timespec="seconds")  # stamp a time/data

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO predictions (area, predicted_price, created_at)
                VALUES (?, ?, ?)
            """,
                (area, predicted_price, timestamp),
            )
            conn.commit()  # save/insert info in to the table

    def get_all_predictions(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, area, predicted_price, created_at
                FROM predictions
                ORDER BY id DESC
            """)
            return cursor.fetchall()  # show/consult all the table
