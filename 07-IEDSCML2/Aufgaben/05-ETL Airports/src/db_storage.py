import sqlite3
from models import FlightRecord

class FlightStorage:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        conn= sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;") # activate foreign keys
        return conn

    def _create_tables(self) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS airlines
                           (
                               id   INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT NOT NULL UNIQUE
                           )
                           """)

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
                    
                    UNIQUE(destination_airport, flight_number, year, month, day, hour, minute), 
                    
                    FOREIGN KEY (airline_id) REFERENCES airlines(id)                    
                );
            """)

            conn.commit()

    @staticmethod
    def get_or_create_airline(cursor, airline_name: str) -> int:
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
        return cursor.lastrowid

    def add_flights(self, records: list[FlightRecord]) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()

            rows_to_insert = []
            for record in records:
                airline_id = self.get_or_create_airline(cursor, record.airline_name)

                rows_to_insert.append(
                    (
                        record.destination_airport,
                        record.origin_country,
                        record.origin_iata_airport,
                        record.flight_number,
                        airline_id,
                        record.year,
                        record.month,
                        record.day,
                        record.hour,
                        record.minute,
                        record.second,
                    )
                )

            cursor.executemany("""
                               INSERT OR IGNORE INTO flights (destination_airport,
                                                    origin_country,
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
                               """, rows_to_insert)

            conn.commit()

            return len(rows_to_insert)