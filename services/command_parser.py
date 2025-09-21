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
            return

        cmd = tokens[0]
        handler = self.commands.get(cmd)
        if handler:
            try:
                handler(tokens)
            except Exception as e:
                print(f"Error in Query - {query} : {e}")
        else:
            print("Query not recognized.")

    def handle_create_parking_lot(self, tokens):
        capacity = int(tokens[1])
        if self.pm.create_parking_slots(capacity):
            print(f"Created parking of {capacity} slots")

    def handle_park(self, tokens):
        vehicle_registration = tokens[1]
        slot = self.pm.allocate_parking_slot(vehicle_registration)
        if slot == -1:
            print("Sorry, Parking Lot is full, No Parking Slots Available.")
        else:
            print(
                f'Car with registration number "{vehicle_registration}" '
                f"has been parked at slot number {slot}"
            )

    def handle_leave(self, tokens):
        slot_number = int(tokens[1])
        result = self.pm.deallocate_parking_slot(slot_number)
        if result:
            print(
                f'Slot number {result["slot_number"]} vacated, '
                f"the car with registration number "
                f'"{result["vehicle_registration"]}" left the space'
            )
        else:
            print(f"Slot number {slot_number} cannot be vacated.")

    def handle_slot_for_car(self, tokens):
        vehicle_registration = tokens[1]
        slot = self.pm.get_parking_slot_by_vehicle(vehicle_registration)
        print(slot if slot != -1 else "No parked car matches the query")

    def handle_all_parked_vehicles(self, tokens):
        vehicles = self.pm.get_all_parked_vehicles()
        print(",".join(vehicles) if vehicles else "No cars parked")
