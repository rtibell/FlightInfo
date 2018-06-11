from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

MQTT_ENDPOINT='a21gw47iweqs9h.iot.eu-central-1.amazonaws.com'
MQTT_CLIENTID='Raspberry-111'
myMQTTClient = AWSIoTMQTTClient(MQTT_CLIENTID, useWebsocket=True)
myMQTTClient.configureEndpoint(MQTT_ENDPOINT, 443) #443
myMQTTClient.configureCredentials("/home/pi/Projects/DAB/root.CA")

myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

print('Connect')
myMQTTClient.connect()
print('Publish')
myMQTTClient.publish("thing/FlightInfoBerry", "myPayload", 0)

print('Subscribe')
myMQTTClient.subscribe("thing/FlightInfoBerry", 1, customCallback)
myMQTTClient.unsubscribe("thing/FlightInfoBerry")

print('Disconnect')
myMQTTClient.disconnect()
