import serial
import requests
import time

class ModemCommunication:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def send_command(self, command):
        self.ser.write((command + '\r\n').encode())
        time.sleep(1)  # Bekleme süresi, ihtiyaca göre ayarlanabilir

    def read_response(self):
        response = self.ser.read_all().decode('utf-8')
        return response

    def close_connection(self):
        self.ser.close()

    def send_get_request(self, url):
        response = requests.get(url)
        return response.text

    def send_post_request(self, url, data=None):
        response = requests.post(url, data=data)
        return response.text


modem = ModemCommunication('/dev/ttyUSB3', baudrate=115200)

try:
    # sending at command
    modem.send_command('AT')

   # Reading response from modem
    response = modem.read_response()
    print(f'Modemden gelen cevap: {response}')

    # Sending HTTP GET request
    get_response = modem.send_get_request('https://webhook.site/a0559e00-7985-4099-b8f5-d5161b4b771f')
    print(f'GET isteği cevabı: {get_response}')

   # Sending HTTP POST request
    post_response = modem.send_post_request('https://webhook.site/a0559e00-7985-4099-b8f5-d5161b4b771f', data={'key': 'value'})
    print(f'POST isteği cevabı: {post_response}')

finally:
    
    modem.close_connection()
