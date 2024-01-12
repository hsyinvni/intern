import json
from ModemLib import ModemLib

class MQTTExample:
    def __init__(self):
        # Bağlantı için modem nesnesini oluştur
        self.modem = ModemLib()

    def send_mqtt_message(self, topic, message):
        # MQTT mesajını gönder
        payload = json.dumps({'message': message})
        
        # HiveMQ cluster bilgileri
        mqtt_broker = "132fbec9d6b44eb7846955e824e934d2.s1.eu.hivemq.cloud"
        mqtt_port = 8883
        mqtt_username = "hivemq.webclient.1705069172207"
        mqtt_password = "vxw&,610I.GTtBeWm%4K"
        
        # MQTT bağlantı komutları
        self.modem.send_at_command('AT+QMTOPEN=0,"{}","{}",{}'.format(mqtt_broker, mqtt_port, 1), 1)
        self.modem.send_at_command('AT+QMTCONN=0,"{}","{}","{}"'.format('ClientID', mqtt_username, mqtt_password), 1)
        self.modem.send_at_command('AT+QMTSUB=0,1,"{}"'.format(topic), 1)
        self.modem.send_at_command('AT+QMTPUB=0,0,0,0,"{}","{}"'.format(topic, len(payload)), 1)
        self.modem.send_at_command(payload, 1)
        self.modem.send_at_command('AT+QMTCLOSE=0', 1)

    def receive_mqtt_message(self, topic):
        # Belirli bir MQTT topic'e subscribe ol
        self.modem.send_at_command('AT+QMTOPEN=0,"{}","{}",{}'.format("132fbec9d6b44eb7846955e824e934d2.s1.eu.hivemq.cloud", 8883, 1), 1)
        self.modem.send_at_command('AT+QMTCONN=0,"{}","{}","{}"'.format('ClientID', 'hivemq.webclient.1705069172207', 'vxw&,610I.GTtBeWm%4K'), 1)
        self.modem.send_at_command('AT+QMTSUB=0,1,"{}"'.format(topic), 1)
        
        # Mesajın gelmesini bekleyerek oku
        response = self.modem.send_at_command('AT+QMTPUB=0,1,1,0', 1)
        
        # Bağlantıyı kapat
        self.modem.send_at_command('AT+QMTCLOSE=0', 1)
        
        return response

if __name__ == "__main__":
    # Örnek kullanım
    mqtt_example = MQTTExample()
    
    # MQTT mesajı gönder
    mqtt_example.send_mqtt_message("deneme", "Hello from ModemLib!")

    # MQTT mesajını oku
    received_message = mqtt_example.receive_mqtt_message("deneme")
    print("Received MQTT Message:", received_message)

    # Modem bağlantısını kapat
    mqtt_example.modem.close_connection()
