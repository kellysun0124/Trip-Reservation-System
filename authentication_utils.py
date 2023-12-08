# Function to read admin credentials from passcodes.txt and validate them
def validate_admin_credentials(username, password):
    try:
        # Open the passcodes.txt file to read stored admin credentials
        with open("data_files/passcodes.txt", "r") as file:
            for line in file:
                # Split each line into stored username and password, and strip whitespace
                stored_username, stored_password = [item.strip() for item in line.split(',')]
                # Check if the provided credentials match the stored credentials
                if stored_username == username and stored_password == password:
                    return True  # Return True if credentials are valid
    except FileNotFoundError:
        # Print an error message if passcodes.txt is not found
        print("passcodes.txt file not found.")
    except Exception as e:
        # Print any other exceptions that occur
        print(f"An error occurred: {e}")
    # Return False if credentials are not valid or an error occurs
    return False
