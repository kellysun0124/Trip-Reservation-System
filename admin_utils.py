# Importing the calculate_cost function from reservation_utils
from reservation_utils import calculate_cost

def calculate_total_sales():
    # Define a cost matrix representing the cost of seats in each row and column
    cost_matrix = [[100, 75, 50, 100] for _ in range(12)]
    total_sales = 0  # Initialize total sales to 0

    try:
        # Open the reservations file to read reservation data
        with open("data_files/reservations.txt", "r") as file:
            for line in file:
                # Split each line into parts (name, row, column, code)
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    # Convert the row and column from 1-based to 0-based indexing
                    row, col = int(parts[1]) - 1, int(parts[2]) - 1

                    # Check if the row and column numbers are within the valid range
                    if 0 <= row < 12 and 0 <= col < 4:
                        # Add the cost of the reserved seat (from the cost matrix) to total sales
                        total_sales += cost_matrix[row][col]
                    else:
                        # Print a message if a reservation has out-of-range row or column
                        print(f"Out of range entry in reservations.txt: Row {row+1}, Column {col+1}")
    except FileNotFoundError:
        # Handle the case where the reservations file is not found
        print("reservations.txt file not found.")
    except Exception as e:
        # Handle any other exceptions that occur
        print(f"An error occurred: {e}")

    # Return the total sales calculated
    return total_sales

def validate_admin_credentials(username, password):
    try:
        # Open the passcodes file to read admin login credentials
        with open("data_files/passcodes.txt", "r") as file:
            for line in file:
                # Split each line into stored username and password
                stored_username, stored_password = line.strip().split(',')
                # Uncomment the following line if using hashed passwords
                # hashed_password = hashlib.sha256(password.encode()).hexdigest()
                # Check if the provided credentials match the stored credentials
                if stored_username == username and stored_password == password:  # Replace with hashed_password if using hashed passwords
                    return True
    except FileNotFoundError:
        # Handle the case where the passcodes file is not found
        print("passcodes.txt file not found.")
    except Exception as e:
        # Handle any other exceptions that occur
        print(f"An error occurred: {e}")

    # Return False if credentials are not validated
    return False
