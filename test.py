#this file is just for testing stuff


def get_passcode():
    reservations = []
    try:
        reservationsFile = open("data_files/reservations.txt")  
        for line in reservationsFile:
            reservations.append(line.removesuffix('\n'))
    except:
        print("file does not exsist") 
    reservationsFile.close()

    return reservations

print(get_passcode())