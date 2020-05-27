import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests

url = "https://www.fast2sms.com/dev/bulk"



#Provide your IBM Watson Device Credentials
organization = "pwyh4c"
deviceType = "greenhouse"
deviceId = "572604"
authMethod = "token"
authToken = "12345678"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        hum=random.randint(10, 40)
        #print(hum)
        temp =random.randint(30, 80)
        sm=random.randint(10, 40)
        #Send Temperature & Humidity & Soil Moisture to IBM Watson
        data = { 'Temperature' : temp, 'Humidity': hum,'Soil_Moisture':sm }
        if (hum<15 or temp>50 or sm<15):
            r=requests.get("https://www.fast2sms.com/dev/bulk?authorization=YpMetB4F7XQnE0iDghZRkHJvCTofAOs5Gc1PI8uqlSdU6Nmar2neW1wki4dZBAOPUv37NXrKGf205Jaq&sender_id=FSTSMS&message=Alert%crossed%threshold%value&language=english&route=p&numbers=9553401679")
            print(r.status_code)
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum,"Soil Moisture = %s"%sm, "to IBM Watson")

        success = deviceCli.publishEvent("Weather", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
