import fs_serial

ser = fs_serial.stream(['COM5']).data()
while True:
    print(ser)

