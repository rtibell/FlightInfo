from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from FlightInfo import FlightInfo
import socket
import logging
import time
import argparse
import json

INET_ADDRESS="localhost"
INET_SOCKET=30003

AWS_HOST="a21gw47iweqs9h.iot.eu-central-1.amazonaws.com"
ROOT_CA="/home/pi/Projects/DAB/root.CA"
CERT="/home/pi/Projects/DAB/27bf00e25e-certificate.pem.crt"
KEY="/home/pi/Projects/DAB/27bf00e25e-private.pem.key"
SUBJECT="thing/FlightInfoBerry"
MODE="publish"
ClientId = "ABC123DEF987"

class MQTTClient:

    def __init__(self):
        self.dict = {}
        self.initLogging()
        self.initMQTT()
        self.initRadio()


    def onConnect(self):
        print("On Connect")

    # Custom MQTT message callback
    def customCallback(self, client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")


    def initRadio(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((INET_ADDRESS,INET_SOCKET))


    # Configure logging
    def initLogging(self):
        self.logger = logging.getLogger("AWSIoTPythonSDK.core")
        self.logger.setLevel(logging.DEBUG)
        self.streamHandler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.streamHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.streamHandler)


    # Init AWSIoTMQTTClient
    # AWSIoTMQTTClient connection configuration
    def initMQTT(self):
        self.myAWSIoTMQTTClient = None
        self.myAWSIoTMQTTClient = AWSIoTMQTTClient(ClientId)
        self.myAWSIoTMQTTClient.configureEndpoint(AWS_HOST, 8883)
        self.myAWSIoTMQTTClient.configureCredentials(ROOT_CA, KEY, CERT)
        self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        # Connect and subscribe to AWS IoT
        self.myAWSIoTMQTTClient.onOnline=self.onConnect
        print("***** Connect *****")
        self.myAWSIoTMQTTClient.connect()
        if MODE == 'both' or MODE == 'subscribe':
            self.myAWSIoTMQTTClient.subscribe(SUBJECT, 1, customCallback)
            time.sleep(2)

    def rdData(self):
        data = self.sock.recv(1024)
        obj = None
        if len(data) == 0:
            return None
        lst = data.decode("utf-8").rstrip().split(',')
        ky = lst[4]
        if ky in self.dict.keys():
            obj = self.dict[ky]
            obj.addMessage(lst)
        else:
            obj = FlightInfo(lst)
            self.dict[ky] = obj
        return obj


    # Publish to the same topic in a loop forever
    def publish(self, message):
        if MODE == 'both' or MODE == 'publish':
            messageJson = json.dumps(message)
            self.myAWSIoTMQTTClient.publish(SUBJECT, messageJson, 1)
            if MODE == 'publish':
                print('Published topic %s: %s\n' % (SUBJECT, messageJson))
            time.sleep(1)

    def start(self):
        self.loop()
        #message = {}
        #message['serialNumber'] = "ABCDEFG67890"
        #message['clickType'] = "DOUBLE"
        #message['batteryVoltage'] = "3000 mV"
        #self.publish(message)
      
 
    def loop(self): 
        while True:
            obj = self.rdData()
            if obj is None:
                break
            if obj.isRecordChanged():
                self.publish(obj.toDict())
                #print(obj.toString())
        self.sock.close()
        print('Final')
        print('=====')
        for k in self.dict.keys():
            print(self.dict[k].toString())
        print('Done!')


def main():
    mqtt = MQTTClient()
    mqtt.start()
    

if __name__ == "__main__":
    main()

