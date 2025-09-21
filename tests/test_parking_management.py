import pytest
from services.parking_management import ParkingManagement


@pytest.fixture
def parking_management():
    pm = ParkingManagement()

    # Clear tables before each test
    pm.db.cursor.execute("DELETE FROM cars")
    pm.db.cursor.execute("UPDATE slots SET occupied = 0")
    pm.db.commit()

    pm.create_parking_slots(3)
    yield pm

    # Cleanup after test
    pm.db.cursor.execute("DELETE FROM cars")
    pm.db.cursor.execute("UPDATE slots SET occupied = 0")
    pm.db.commit()


def test_create_parking_slots(parking_management):
    assert parking_management.capacity == 3
    assert len(parking_management.available_parking_slots) == 3


def test_allocate_and_deallocate(parking_management):
    slot = parking_management.allocate_parking_slot("CAR-0000")
    assert slot == 1

    slot2 = parking_management.allocate_parking_slot("CAR-1111")
    assert slot2 == 2

    # Deallocate slot 2
    result = parking_management.deallocate_parking_slot(2)
    assert result["vehicle_registration"] == "CAR-1111"

    # Slot 2 should now be available again
    slot3 = parking_management.allocate_parking_slot("CAR-2222")
    assert slot3 == 2


def test_all_parked_vehicles(parking_management):
    parking_management.allocate_parking_slot("CAR-1111")
    parking_management.allocate_parking_slot("CAR-2222")
    vehicles = parking_management.get_all_parked_vehicles()
    assert "CAR-1111" in vehicles
    assert "CAR-2222" in vehicles


def test_get_parking_slot_by_vehicle(parking_management):
    parking_management.allocate_parking_slot("CAR-3333")
    slot = parking_management.get_parking_slot_by_vehicle("CAR-3333")
    assert slot == 1
    assert parking_management.get_parking_slot_by_vehicle("CAR-9999") == -1


def test_full_parking_lot(parking_management):
    parking_management.allocate_parking_slot("CAR-A")
    parking_management.allocate_parking_slot("CAR-B")
    parking_management.allocate_parking_slot("CAR-C")
    # Lot is full now
    slot = parking_management.allocate_parking_slot("CAR-D")
    assert slot == -1
