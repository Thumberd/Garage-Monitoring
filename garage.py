import requests
from chipGPIO import *
import time

PEU = 2
X = 0

pinMode(PEU, "INPUT")
PEUtimeUp = 0
PEUisUp = False
PEUnotified = False

pinMode(X, "INPUT")
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
                if time.time() - PEUtimeUp >= 600 and PEUnotified == False:
                        r = requests.get("https://smsapi.free-mobile.fr/sendmsg?user=10908880&pass=9o83gNpCCAMjjs&msg=Garage%20208%20ouvert%20depuis%20plus%20de%2010min.%20Normal%20?")
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
                if time.time() - XtimeUp >= 600 and Xnotified == False:
                        r = requests.get("https://smsapi.free-mobile.fr/sendmsg?user=10908880&pass=9o83gNpCCAMjjs&msg=Garage%20Xsara%20ouvert%20depuis%20plus%20de%2010min.%20Normal%20?")
                        Xnotified = True
        elif Xval == 0:
                Xnotified = False
                XtimeUp = 0
                XisUp = False

        time.sleep(1)



