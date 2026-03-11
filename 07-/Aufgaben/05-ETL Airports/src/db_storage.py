import sqlite3
from datetime import datetime
from data_transform import FlightRecord

class FlightStorage:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_or_create_airline(self, airline_name: str) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM airlines WHERE name = ?",
                (airline_name,)
            )
            row = cursor.fetchone()

            if row:
                return row[0]

            cursor.execute(
                "INSERT INTO airlines (name) VALUES (?)",
                (airline_name,)
            )
            conn.commit()
            return cursor.lastrowid

    def _create_table(self) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    destination_airport TEXT NOT NULL,
                    origin_country TEXT NOT NULL,
                    origin_iata_airport TEXT NOT NULL,
                    flight_number TEXT NOT NULL,
                    airline_id INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    hour INTEGER NOT NULL,
                    minute INTEGER NOT NULL,
                    second INTEGER NOT NULL,
                    FOREIGN KEY (airline_id) REFERENCES airlines(id)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS airlines (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL UNIQUE
                )
            """)
            conn.commit()

    def add_flights(self, records: list[FlightRecord]) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.executemany("""
                               INSERT INTO flights (origin_country,
                                                    destination_airport,
                                                    origin_iata_airport,
                                                    flight_number,
                                                    airline_id,
                                                    year,
                                                    month,
                                                    day,
                                                    hour,
                                                    minute,
                                                    second)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               """, [
                                   (
                                       record.origin_country,
                                       record.destination_airport,
                                       record.origin_iata_airport,
                                       record.flight_number,
                                       record.airline_name,
                                       record.year,
                                       record.month,
                                       record.day,
                                       record.hour,
                                       record.minute,
                                       record.second,
                                   )
                                   for record in records
                               ])
            conn.commit()