import logging

logger = logging.getLogger(__name__)


class CommandParser:
    def __init__(self, parking_management):
        self.pm = parking_management
        self.commands = {
            "Create_parking_lot": self.handle_create_parking_lot,
            "Park": self.handle_park,
            "Leave": self.handle_leave,
            "Slot_number_for_car_with_number": self.handle_slot_for_car,
            "All_parked_vehicles": self.handle_all_parked_vehicles,
        }

    def parse(self, query):
        tokens = query.strip().split()
        if not tokens:
            logger.warning("Received empty query")
            return

        cmd = tokens[0]
        handler = self.commands.get(cmd)
        if handler:
            try:
                handler(tokens)
            except Exception as e:
                logger.error("Error in query '%s': %s", query, e)
        else:
            logger.warning("Query not recognized: %s", query)

    def handle_create_parking_lot(self, tokens):
        try:
            capacity = int(tokens[1])
            if self.pm.create_parking_slots(capacity):
                logger.info("Created parking of %d slots", capacity)
        except (IndexError, ValueError) as e:
            logger.error("Invalid input for creating parking lot: %s", e)

    def handle_park(self, tokens):
        try:
            vehicle_registration = tokens[1]
            slot = self.pm.allocate_parking_slot(vehicle_registration)
            if slot == -1:
                logger.warning(
                    "Sorry, Parking Lot is full. No Parking Slots Available."
                )
            else:
                logger.info(
                    'Car with registration number "%s"'
                    "has been parked at slot number %d",
                    vehicle_registration,
                    slot,
                )
        except IndexError as e:
            logger.error("Missing vehicle registration number: %s", e)

    def handle_leave(self, tokens):
        try:
            slot_number = int(tokens[1])
            result = self.pm.deallocate_parking_slot(slot_number)
            if result:
                logger.info(
                    "Slot number %d vacated, the car with"
                    'registration number "%s" left the space',
                    result["slot_number"],
                    result["vehicle_registration"],
                )
            else:
                logger.warning("Slot number %d cannot be vacated.", slot_number)
        except (IndexError, ValueError) as e:
            logger.error("Invalid input for leaving slot: %s", e)

    def handle_slot_for_car(self, tokens):
        try:
            vehicle_registration = tokens[1]
            slot = self.pm.get_parking_slot_by_vehicle(vehicle_registration)
            if slot != -1:
                logger.info("Car '%s' is at slot number %d", vehicle_registration, slot)
            else:
                logger.info("No parked car matches the query: %s", vehicle_registration)
        except IndexError as e:
            logger.error("Missing vehicle registration number: %s", e)

    def handle_all_parked_vehicles(self, tokens):
        vehicles = self.pm.get_all_parked_vehicles()
        if vehicles:
            logger.info("All parked vehicles: %s", ",".join(vehicles))
        else:
            logger.info("No cars parked")
