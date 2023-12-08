import random
import string

def check_seat_availability(seat_row, seat_column):
    try:
        # Open the reservations file to read current reservations
        with open("data_files/reservations.txt", "r") as file:
            for line in file:
                # Split each line to extract reserved seat details
                _, reserved_row, reserved_column, _ = line.strip().split(',')
                # Check if the requested seat matches any reserved seat
                if int(reserved_row) == seat_row and int(reserved_column) == seat_column:
                    return False  # Seat is already reserved
    except FileNotFoundError:
        # If the reservations file doesn't exist, assume all seats are available
        return True
    except Exception as e:
        # Print any other exceptions that might occur
        print(f"An error occurred: {e}")
    # Default return value, assuming the seat is available if no match is found
    return True

def generate_reservation_code(first_name, last_name, seat_row, seat_column, filename):
    # Read existing codes from the file
    try:
        with open(filename, 'r') as file:
            existing_codes = file.read().splitlines()
    except FileNotFoundError:
        existing_codes = []

    # Generate a unique reservation code
    while True:
        # Extract initials from the first and last name
        initials = (first_name[0] + last_name[0]).upper()

        # Convert seat row to a string with zero padding (if necessary)
        seat_row_str = str(seat_row).zfill(2)

        # Generate a random string of 4 alphanumeric characters
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

        # Combine initials, seat row, seat column, and random part to form a reservation code
        new_code = f"{initials}{seat_row_str}{seat_column}{random_part}"

        # Check for uniqueness
        if new_code not in existing_codes:
            return new_code

def calculate_cost(seat_row, seat_column):
    try:
        # Define a cost matrix for the seat pricing
        cost_matrix = [[100, 75, 50, 100] for _ in range(12)]
        # Adjust for 1-based indexing to 0-based indexing
        row_index = seat_row - 1
        column_index = seat_column - 1
        # Return the cost from the cost matrix
        return cost_matrix[row_index][column_index]
    except IndexError:
        # Raise a ValueError if the seat row or column is invalid (out of range)
        raise ValueError("Invalid seat row or column")
    except Exception as e:
        # Print any other exceptions that might occur
        print(f"An error occurred while calculating cost: {e}")

def generate_seating_chart():
    rows = 12  # Define the number of rows
    cols = 4   # Define the number of columns

    # Initialize a seating chart with all seats marked as 'Available'
    seating_chart = [['Available' for _ in range(cols)] for _ in range(rows)]

    try:
        # Open the reservations file to read current reservations
        with open("data_files/reservations.txt", "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    # Adjust for 1-based indexing to 0-based indexing
                    row, col = int(parts[1]) - 1, int(parts[2]) - 1

                    if 0 <= row < rows and 0 <= col < cols:
                        # Mark the seat as 'Reserved' in the seating chart
                        seating_chart[row][col] = 'Reserved'
                    else:
                        # Print a message for out-of-range entries
                        print(f"Out of range entry in reservations.txt: Row {row+1}, Column {col+1}")
    except FileNotFoundError:
        # Handle the case where the reservations file is not found
        print("reservations.txt file not found.")
    except Exception as e:
        # Print any other exceptions that might occur
        print(f"An error occurred: {e}")

    return seating_chart

def save_reservation(first_name, last_name, seat_row, seat_column, reservation_code):
    try:
        # Open the reservations file in append mode to add a new reservation
        with open("data_files/reservations.txt", "a") as file:
            # Write the reservation details to the file
            file.write(f"\n{first_name},{seat_row},{seat_column},{reservation_code}")
    except Exception as e:
        # Print any exceptions that occur while saving the reservation
        print(f"An error occurred while saving the reservation: {e}")
