import schedule
import time
import datetime
import os
import json
from sense_hat import SenseHat
from time import sleep
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient




def reportAmbient(self, params, packet):	
	reporting();


def reporting():
	print("%s\n\nTempurature: %s\nHumidity: %s\nPressure: %s\n"%(datetime.datetime.now(),sense.temperature,sense.humidity,sense.pressure))
	message = {"deviceId": "SOon", "timeStamp": str(datetime.datetime.now()),"Tempurature": str(sense.temperature),"Humidity": str(sense.humidity)}
	jsonData = json.dumps(message)
	myMQTTClient.publish("iot/storeAmbientLog",jsonData, 0)


sense = SenseHat() 

print("Initiated, Standing by")

myMQTTClient = AWSIoTMQTTClient("ambientTracker")
 
myMQTTClient.configureEndpoint("a3p30umu4xlo8l-ats.iot.us-east-1.amazonaws.com", 8883)
 
certRootPath = '/home/pi/Documents/iot/'
myMQTTClient.configureCredentials("{}root-ca.pem".format(certRootPath), "{}cloud.pem.key".format(certRootPath), "{}cloud.pem.crt".format(certRootPath))
 
myMQTTClient.configureOfflinePublishQueueing(-1) 
myMQTTClient.configureDrainingFrequency(2) 
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

myMQTTClient.connect()
myMQTTClient.subscribe("iot/forceToLog", 1, reportAmbient)
schedule.every(120).minutes.do(reporting)

while True:
		schedule.run_pending()
		time.sleep(5)


