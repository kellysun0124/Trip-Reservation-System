# Function to read admin credentials from passcodes.txt
def read_admin_credentials():
    admin_credentials = []
    #match admin credentials to the passcodes.txt file
    try:
        with open("data_files/passcodes.txt", "r") as passcodes_file:
            for line in passcodes_file:
                username, password = map(str.strip, line.split(','))
                admin_credentials.append((username, password))
    except FileNotFoundError:
        print("passcodes.txt not found")

    return admin_credentials

#function to get a list of passcodes
def get_passcodes():
    passcodes = []
    try:
        passcodesFile = open("data_files/passcodes.txt")
        for line in passcodesFile:
            passcodes.append(line.removesuffix('\n'))
    except:
        print("file does not exsist") 
    passcodesFile.close()

    return passcodes