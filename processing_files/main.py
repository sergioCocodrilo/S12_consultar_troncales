


from os import listdir 
import serial
import re

def connect():
    """Connects to serial through USB"""
    ser = serial.Serial()
    # parameters
    ser.port = '/dev/ttyS0'
    ser.baudrate =  9600
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1 # seconds
    try:
        ser.open()
    except:
        ser.port = '/dev/ttyS1'
        ser.open()
    if ser.isOpen():
        return ser
    else:
        return None

def s12_listen(ser):
    """
    Listens for the answer of the S12 and returns the S12 state: 
       0: ready for macro 
       1: ready for S12 command
    """
    output_ended = False
    s12_state = None
    slix_alarms = []
    while not output_ended:
        for line in ser.readlines():
            print(line[:-1].decode("ascii"))
            if b">" in line:
                output_ended = True 
                s12_state = 0
            elif b"<" in line:
                output_ended = True 
                s12_state = 1
            elif b"SLIX" in line:
                slix_alarms.append(line[14:30])
    return (s12_state, slix_alarms)

if __name__ == "__main__":
    ser = connect()
    if not ser:
        print('Imposible establecer conexión.')
        quit()

    # Get the list files. They should be in the data/input directory
    print('Selecciona tu archivo')
    [print('\t', index + 1, ':', f) for index, f in enumerate(listdir('data/input/'))]
    f = input('\t Archivo')

    # Get the list of modules to check
    modules_to_check = []
    with open(f, 'r') as in_file:
        for l in in_file:
            if l.startswith("H'"):
                modules_to_check.append(l[2:6])

    # Query the S12
    print('\t========== Revisando las troncales ==========')
    ser.write('\x1b'.encode("ascii"))

    for module in modules_to_check:
        while s12_listen(ser)[0] == 0:
            ser.write('MM\r\n'.encode('ascii'))
        ser.write(("DISPLAY-TRUNK:NA1=H'" + module + ',TSLIST1=1&&5.').encode('ascii'))

