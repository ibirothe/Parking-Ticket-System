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

| Command                      | Description                              |
| ---------------------------- | ---------------------------------------- |
| `create_parking_lot <n>`     | Create a parking lot with `n` slots      |
| `park <registration_number>` | Park a car in the nearest available slot |
| `leave <slot_number>`        | Vacate the given parking slot            |
| `status`                     | Show current parking status              |

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
