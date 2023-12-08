import random
import string

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for _ in range(12)]
    return cost_matrix

def check_seat_availability(seat_row, seat_column):
    try:
        with open("data_files/reservations.txt", "r") as file:
            for line in file:
                _, reserved_row, reserved_column, _ = line.strip().split(',')
                # Convert reserved_row and reserved_column to integers before comparison
                if int(reserved_row) == seat_row and int(reserved_column) == seat_column:
                    return False
    except FileNotFoundError:
        # If the file doesn't exist, all seats are available
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
    return True

def generate_reservation_code(first_name, last_name, seat_row, seat_column):
    # Take the first letter of the first and last name
    initials = (first_name[0] + last_name[0]).upper()

    # Convert seat row to string and pad with zero if necessary
    seat_row_str = str(seat_row).zfill(2)

    # Generate a random string of 4 alphanumeric characters
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # Combine all parts
    reservation_code = f"{initials}{seat_row_str}{seat_column}{random_part}"

    return reservation_code

def calculate_cost(seat_row, seat_column):
    try:
        cost_matrix = get_cost_matrix()
        # Adjusting indices as they are now both numeric
        row_index = seat_row - 1
        column_index = seat_column - 1
        return cost_matrix[row_index][column_index]
    except IndexError:
        raise ValueError("Invalid seat row or column")
    except Exception as e:
        print(f"An error occurred while calculating cost: {e}")

def generate_seating_chart():
    rows = 12  # Total number of rows
    cols = 4   # Total number of columns

    seating_chart = [['Available' for _ in range(cols)] for _ in range(rows)]

    try:
        with open("data_files/reservations.txt", "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    row, col = int(parts[1]), int(parts[2])
                    row_index = row - 1
                    col_index = col - 1

                    if 0 <= row_index < rows and 0 <= col_index < cols:
                        seating_chart[row_index][col_index] = 'Reserved'
                    else:
                        print(f"Row or column index out of range: Row {row}, Column {col}")
                else:
                    print(f"Unexpected line format: '{line}'")
    except FileNotFoundError:
        print("reservations.txt file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return seating_chart

def save_reservation(first_name, last_name, seat_row, seat_column, reservation_code):
    """
    Save the reservation details to the reservations.txt file.

    Args:
    first_name (str): The first name of the person making the reservation.
    last_name (str): The last name of the person making the reservation.
    seat_row (int): The row number of the seat being reserved.
    seat_column (int): The column number of the seat being reserved.
    reservation_code (str): The unique reservation code.
    """
    try:
        with open("data_files/reservations.txt", "a") as file:
            file.write(f"{first_name},{last_name},{seat_row},{seat_column},{reservation_code}\n")
    except Exception as e:
        print(f"An error occurred while saving the reservation: {e}")
