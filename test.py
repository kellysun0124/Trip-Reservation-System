#this file is just for testing stuff


def data_files_write(filename, content):
    try:
        passcodesFile = open("data_files/passcodes.txt", "a")  
        reservationsFile = open("data_files/reservations.txt", "a")  
    except:
        print("file does not exsist")
    if filename == "passcodes":
        passcodesFile.write(f"{content}\n")
    elif filename == "reservations":
        reservationsFile.write(f"{content}\n")
    else:
        print("filename should be passcodes or reservations")
    passcodesFile.close()
    reservationsFile.close()

data_files_write("passcodes", "whats, up")

# passfile, reserv = get_files_read()

# for line in passfile:
#     print(line)
# print(reserv)