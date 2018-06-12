from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time


def isOnline():
    print('is on-line')

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


MQTT_ENDPOINT='a21gw47iweqs9h.iot.eu-central-1.amazonaws.com'
MQTT_CLIENTID='Raspberry-111'

myMQTTClient = AWSIoTMQTTClient(MQTT_CLIENTID) 
myMQTTClient.configureEndpoint(MQTT_ENDPOINT, 8833) 
myMQTTClient.configureCredentials("/home/pi/Projects/DAB/root.CA", "/home/pi/Projects/DAB/27bf00e25e-private.pem.key", "/home/pi/Projects/DAB/27bf00e25e-certificate.pem.crt")

myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(10)
#myMQTTClient.mqttCommandTimeout_ms = 10000;
#myMQTTClient.tlsHandshakeTimeout_ms = 10000;


print('Connect')
myMQTTClient.onOnline=isOnline
myMQTTClient.connect(keepAliveIntervalSecond=60)

print('Publish')
myMQTTClient.publish("thing/FlightInfoBerry", "myPayload", 0)

print('Subscribe')
myMQTTClient.subscribe("thing/FlightInfoBerry", 1, customCallback)
time.sleep(4)
myMQTTClient.unsubscribe("thing/FlightInfoBerry")

print('Disconnect')
myMQTTClient.disconnect()
