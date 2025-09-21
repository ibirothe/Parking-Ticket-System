from heapq import heappush, heappop
from datetime import datetime
from db.database import Database
from models.car import Car


class ParkingManagement:
    def __init__(self):
        self.db = Database()
        self.capacity = self._get_capacity()
        self.available_parking_slots = self._load_available_slots()

    # ---------------- Helper Methods ----------------
    def _load_available_slots(self):
        self.db.cursor.execute("SELECT slot_number FROM slots WHERE occupied = 0")
        slots = [row[0] for row in self.db.cursor.fetchall()]
        heap = []
        for slot in slots:
            heappush(heap, slot)
        return heap

    def _get_capacity(self):
        self.db.cursor.execute("SELECT COUNT(*) FROM slots")
        return self.db.cursor.fetchone()[0]

    # ---------------- Parking Slot Management ----------------
    def create_parking_slots(self, max_capacity):
        try:
            for i in range(1, max_capacity + 1):
                self.db.cursor.execute(
                    "INSERT OR IGNORE INTO slots(slot_number) VALUES (?)", (i,)
                )
            self.db.commit()
            self.capacity = max_capacity
            self.available_parking_slots = [i for i in range(1, max_capacity + 1)]
            return True
        except Exception as e:
            print(e)
            return False

    def get_nearest_empty_slot(self):
        if not self.available_parking_slots:
            return -1
        return heappop(self.available_parking_slots)

    def allocate_parking_slot(self, vehicle_registration):
        if len(self.available_parking_slots) == 0:
            return -1
        slot = self.get_nearest_empty_slot()
        entry_time = datetime.now().isoformat()
        car = Car(vehicle_registration)
        self.db.cursor.execute(
            "INSERT INTO cars(vehicle_registration, "
            "slot_number, entry_time) VALUES (?, ?, ?)",
            (car.vehicle_registration, slot, entry_time),
        )
        self.db.cursor.execute(
            "UPDATE slots SET occupied = 1 WHERE slot_number = ?", (slot,)
        )
        self.db.commit()
        return slot

    def deallocate_parking_slot(self, slot_number):
        self.db.cursor.execute(
            "SELECT vehicle_registration FROM cars WHERE slot_number = ?",
            (slot_number,),
        )
        row = self.db.cursor.fetchone()
        if not row:
            return False
        vehicle_registration = row[0]
        self.db.cursor.execute("DELETE FROM cars WHERE slot_number = ?", (slot_number,))
        self.db.cursor.execute(
            "UPDATE slots SET occupied = 0 WHERE slot_number = ?", (slot_number,)
        )
        heappush(self.available_parking_slots, slot_number)
        self.db.commit()
        return {
            "vehicle_registration": vehicle_registration,
            "slot_number": slot_number,
        }

    # ---------------- Queries ----------------
    def get_parking_slot_by_vehicle(self, vehicle_registration):
        self.db.cursor.execute(
            "SELECT slot_number FROM cars WHERE vehicle_registration = ?",
            (vehicle_registration,),
        )
        row = self.db.cursor.fetchone()
        return row[0] if row else -1

    def get_all_parked_vehicles(self):
        self.db.cursor.execute("SELECT vehicle_registration FROM cars")
        return [row[0] for row in self.db.cursor.fetchall()]
