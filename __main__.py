import sys
import argparse
from services.parking_management import ParkingManagement
from services.command_parser import CommandParser
import logging
from utils.logger import setup_logging

if __name__ == "__main__":
    setup_logging(level=logging.INFO)

    parking_management = ParkingManagement()
    parser = CommandParser(parking_management)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--input_file", required=True, help="Input File")
    arg_parser.add_argument("--output_file", required=False, help="Output File")
    args = arg_parser.parse_args()

    if args.output_file:
        sys.stdout = open(args.output_file, "w")

    with open(args.input_file) as f:
        for line in f:
            parser.parse(line)
