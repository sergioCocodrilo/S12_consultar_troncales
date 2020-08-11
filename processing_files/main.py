


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
    comment = ""
    while not output_ended:
        for line in ser.readlines():
            print(line[:-1].decode("ascii"))
            if b">" in line:
                output_ended = True 
                s12_state = 0
            elif b"<" in line:
                output_ended = True 
                s12_state = 1
            elif b"COMMENT" in line:
                comment = line[16:-2].decode("ascii")
    return (s12_state, comment)

if __name__ == "__main__":
    ser = connect()
    if not ser:
        print('Imposible establecer conexión.')
        quit()

    # Get the list files. They should be in the data/input directory
    files = listdir('data/input/')
    print('Selecciona tu archivo')
    [print('\t', index + 1, ':', f) for index, f in enumerate(files)]
    f = files[int(input('\t Archivo: ')) - 1]

    # Get the list of modules to check
    modules_to_check = []
    with open('data/input/' + f, 'r') as in_file:
        for l in in_file:
            if l.startswith("H'"):
                modules_to_check.append(l[2:6])

    # Query the S12
    print('\t========== Revisando las troncales ==========')
    ser.write('\x1b'.encode("ascii"))

    while s12_listen(ser)[0] == 0:
        ser.write('MM\r\n'.encode('ascii'))

    module_state = []
    for module in modules_to_check:
        ser.write(("DISPLAY-TRUNK:NA1=H'" + module + ',TSLIST1=1.\r\n').encode('ascii'))
        while True:
            state, comment = s12_listen(ser)
            if comment != "":
                module_state.append((module, comment))
            if state == 1:
                break
            else:
                ser.write('MM\r\n'.encode('ascii'))

    print('\t========== Resumen ==========')
    for pair in module_state:
        print(pair)

