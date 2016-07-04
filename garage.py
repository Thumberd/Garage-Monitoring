import logging
 
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
 
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('/home/chip/Garage/garage.log', 'a', 1000000, 1)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 

steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)

import requests
from chipGPIO import *
import time
import json
import PiCom

Fjson = open("/home/chip/Garage/data.json", "r")
data = Fjson.read()
Fjson.close()

def saveData(jsonT):
    global jsonData
    Fjson = open("data.json", "w")
    Fjson.write(jsonT)
    Fjson.close()
    jsonData = json.loads(jsonT)

jsonData = json.loads(data)

PEU = jsonData['garage'][0]['gpio']
X = jsonData['garage'][1]['gpio']

def updateFree():
    if(PiCom.testConnection()):
        users = PiCom.getApifree()
        jsonData['apiFree'] = users
        saveData(json.dumps(jsonData))

def sendSMS(msg):
    updateFree()
    for user in jsonData['apiFree']:
        r = requests.get("https://smsapi.free-mobile.fr/sendmsg?user=" + str(user['user']) + "&pass=" + str(user['key']) + "&msg=" + str(msg))

def informRPI(id, state):
	payload={'state': state}
	r = requests.post("http://192.168.0.17/api/v1/garage/" + str(id), data=payload)

pinMode(PEU, INPUT)
PEUtimeUp = 0
PEUisUp = False
PEUnotified = False

pinMode(X, INPUT)
XtimeUp = 0
XisUp = False
Xnotified = False

while True:
        PEUval = digitalRead(PEU)
        Xval = digitalRead(X)
        logger.info(str(PEUval) + " / " + str(Xval))
        if PEUval == 1:
                logger.info("Garage 208 ouvert")
                if(not PEUisUp):
			PiCom.updateGarageState(jsonData['garage'][0]['id'], 1)
                        PEUtimeUp = time.time()
                        PEUisUp = True
                print(time.time() - PEUtimeUp)
                if time.time() - PEUtimeUp >= 300 and PEUnotified == False:
                        sendSMS("Garage 208 ouvert depuis plus de 5min. Normal ?")
                        PEUnotified = True
        elif PEUval == 0:
		if PEUisUp == True:
			PiCom.updateGarageState(jsonData['garage'][0]['id'], 0)
                PEUnotified = False
                PEUtimeUp = 0
                PEUisUp = False

        if Xval == 1:
                logger.info("Garage Xsara ouvert")
                if(not XisUp):
			PiCom.updateGarageState(jsonData['garage'][1]['id'], 1)
                        XtimeUp = time.time()
                        XisUp = True
                print(time.time() - XtimeUp)
                if time.time() - XtimeUp >= 300 and Xnotified == False:
                        sendSMS("Garage Xsara ouvert depuis plus de 5min. Normal ?")
                        Xnotified = True
        elif Xval == 0:
		if XisUp:
			PiCom.updateGarageState(jsonData['garage'][1]['id'], 0)
                Xnotified = False
                XtimeUp = 0
                XisUp = False

        time.sleep(1)



