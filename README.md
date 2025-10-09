# Parking Lot Ticket System

A simple Python CLI app to manage parking slots with an SQLite database.

---

## Installation

```
git clone https://github.com/ibirothe/Parking-Ticket-System.git
cd Parking-Ticket-System
python -m venv venv
venv\Scripts\activate   # Windows  
source venv/bin/activate   # Linux/Mac  
pip install -r requirements.txt
```

---

## Usage

Run with an input file of commands:

```
python __main__.py --input_file example_input.txt
```

---

## Commands

| Command                                 | Description                                                                 |
| --------------------------------------- | --------------------------------------------------------------------------- |
| `Create_parking_lot <n>`                | Create a parking lot with `n` slots                                         |
| `Park <registration_number>`            | Park a car in the nearest available slot                                    |
| `Leave <slot_number>`                   | Vacate the given parking slot                                               |
| `Slot_number_for_car_with_number <reg>` | Find which slot a car with the given registration number is parked in       |
| `All_parked_vehicles`                   | List all currently parked vehicle registration numbers                      |
| `Generate_report <type>`                | Generate a report (`occupancy` or `clusters`) and save it as a `.png` image |
| `Clean_parking_lot`                     | Remove all cars and reset all parking slots to empty                        |

---

## Example

**Input (`example_input.txt`):**

```
create_parking_lot 5
park CAR-A
park CAR-B
leave 2
status
```

**Output:**

```
Created parking of 5 slots
Car with vehicle registration number "CAR-A" has been parked at slot number 1
Car with vehicle registration number "CAR-B" has been parked at slot number 2
Slot number 2 vacated, the car with vehicle registration number "CAR-B" left the space
1 CAR-A
```

---

## Testing

```
pytest -v
```
