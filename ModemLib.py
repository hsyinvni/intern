import serial
import serial.tools.list_ports
import time

class ModemLib:
    def __init__(self, port=None, baudrate=115200, timeout=1, parity=serial.PARITY_NONE):
        # Initialize the modem connection
        self.port = port or self.find_modem_port()
        if not self.port:
            raise Exception("GSM modem port not found.")
        self.serial_connection = serial.Serial(port=self.port, baudrate=baudrate, timeout=timeout, parity=parity)

    @staticmethod
    def find_modem_port():
        # Find the port of the connected GSM modem by checking available ports
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "VID:PID=2C7C:0125" in port.hwid.upper():
                return port.device
        return None

    def send_at_command(self, command, delay_flag):
        # Send an AT command and receive the response
        self.serial_connection.write((command + '\r\n').encode())
    
        if delay_flag in [0, 2]:
            time.sleep(1)
        elif delay_flag == 1:
            time.sleep(2)

        response = self.serial_connection.read(self.serial_connection.in_waiting).decode()
        if delay_flag == 2:
            time.sleep(1)
        return response
        
    def close_connection(self):
        # Close the modem connection
        self.serial_connection.close()

    def perform_http_request(self, url, method='GET', data=None):
        # Send necessary AT commands for making an HTTP request and receive the response
        self.send_at_command('AT+QHTTPCFG="contextid",1', 0)
        self.send_at_command(f'AT+QHTTPURL={len(url)},80', 0)
        self.send_at_command(url, 0)

        if method == 'GET':
            response = self.send_at_command('AT+QHTTPGET=80', 2)
        else:
            self.send_at_command(f'AT+QHTTPPOST={len(data)},80,80', 0)
            response = self.send_at_command(data, 0)

        response += self.send_at_command('AT+QHTTPREAD=80', 1)
        return self.filter_http_response(response)
        
    def filter_http_response(self, raw_response):
        # Process the modem response and extract the desired parts
        lines = raw_response.replace('\r', '').split('\n')
        filtered_response = {'response': [], 'status': 0}
        search_terms = ('+QHTTPGET', '+QHTTPPOST', '+QHTTPREAD', 'Request successful', 'OK', 'CONNECT')

        for line in lines:
            line = line.strip()
            if line.startswith(search_terms):
                filtered_response['response'].append(line)

        return filtered_response
