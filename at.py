import serial
import time

class ModemCommunication:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def send_command(self, command):
        self.ser.write((command + '\r\n').encode())
        time.sleep(1) 

    def read_response(self):
        response = self.ser.read_all().decode('utf-8')
        return response

    def close_connection(self):
        self.ser.close()


modem = ModemCommunication('/dev/ttyUSB3', baudrate=115200)

try:
    
    modem.send_command('AT')

    
    response = modem.read_response()
    print(f'Modemden gelen cevap: {response}')

    

finally:
    
    modem.close_connection()
