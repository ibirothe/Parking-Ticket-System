import sqlite3

DB_FILE = "parking_lot.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS slots (
                slot_number INTEGER PRIMARY KEY,
                occupied INTEGER DEFAULT 0
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cars (
                vehicle_registration TEXT PRIMARY KEY,
                slot_number INTEGER,
                entry_time TEXT,
                FOREIGN KEY(slot_number) REFERENCES slots(slot_number)
            )
        """
        )
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
