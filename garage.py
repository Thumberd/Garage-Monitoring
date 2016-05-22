import requests
from chipGPIO import *
import time
import json
import PiCom

Fjson = open("data.json", "r")
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
        print(str(PEUval) + " / " + str(Xval))
        if PEUval == 1:
                print("Garage 208 ouvert")
                if(not PEUisUp):
                        PEUtimeUp = time.time()
                        PEUisUp = True
                print(time.time() - PEUtimeUp)
                if time.time() - PEUtimeUp >= 300 and PEUnotified == False:
                        sendSMS("Garage 208 ouvert depuis plus de 5min. Normal ?")
                        PEUnotified = True
        elif PEUval == 0:
                PEUnotified = False
                PEUtimeUp = 0
                PEUisUp = False

        if Xval == 1:
                print("Garage Xsara ouvert")
                if(not XisUp):
                        XtimeUp = time.time()
                        XisUp = True
                print(time.time() - XtimeUp)
                if time.time() - XtimeUp >= 300 and Xnotified == False:
                        sendSMS("Garage Xsara ouvert depuis plus de 5min. Normal ?")
                        Xnotified = True
        elif Xval == 0:
                Xnotified = False
                XtimeUp = 0
                XisUp = False

        time.sleep(1)



