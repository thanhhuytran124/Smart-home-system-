from umqtt.simple import MQTTClient
import network
import time

class MQTT:
    def __init__(self):
        self.client = None
        self.cb = None

    def connect_ww_or_tt(self, server, port, user, pwd, client_id):
        if user == "" and pwd == "":
            self.client = MQTTClient(client_id, server, port)
        else:
            self.client = MQTTClient(client_id, server, port, user, pwd)
            
        self.client.set_callback(self.on_receive)
        self.client.connect()
        
    def publish(self, topic, message):
        if self.client:
            self.client.publish(topic, str(message))

    def on_receive(self, topic, msg):
        if self.cb:
            self.cb(topic.decode('utf-8').split('/')[-1], msg.decode('utf-8'))

    def on_receive_message(self, topic, callback):
        self.cb = callback
        self.client.subscribe(topic)

    def check_msg(self):
        if self.client:
            self.client.check_msg()

mqtt = MQTT()
