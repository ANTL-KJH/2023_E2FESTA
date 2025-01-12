"""
* Project : 2023CDP Eddystone Broadcasting Subway ver
* Program Purpose and Features :
* - send broadcasting message
* Author : JH KIM, JH SUN
* First Write Date : 2023.07.04
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH KIM            2023.07.04      v1.00       First Write
* JH KIM            2023.07.07      v1.01       Broadcasting duration changed
"""
import os
import time

class trafficSignal:
    def __init__(self):
        self.initializeBeacon()
        os.system("sudo hciconfig hci0 up")
        os.system("sudo hciconfig hci0 leadv 3")
        self.signal = "U"
        self.leftTime = 6
        self.leftTimeSec = 59
        
    def setSignal(self, newSig):
        self.signal = newSig
        
    def getSignal(self):
        return self.signal
    
    def afterOneSec(self):
        time.sleep(1)
        if self.leftTimeSec > 0:
            self.leftTimeSec -= 1
        else:
            self.afterOneMin()
    
    def afterOneMin(self):
        if self.leftTime > 0:
            self.leftTime -= 1
        else:
            self.changeTurn()
        self.leftTimeSec = 59
            
    def trafficBroadcasting(self):
        defaultStr = "sudo hcitool -i hci0 cmd 0x08 0x0008 17 02 01 06 03 03 aa fe 0f 16 aa fe 10 00 "
        SUB = "53 55 42 "
        if self.getSignal() == "U":
            signalStr = "55 "
        else:
            signalStr = "44 "

        Ten = str(self.leftTime // 10 + 30)
        One = str(self.leftTime % 10 + 30)
        sendStr = defaultStr + SUB + "30 30 31 "+ signalStr + Ten + " " + One
        os.system(sendStr)
        self.afterOneSec()
        

    def changeTurn(self):
        if self.getSignal() == "U":
            self.setSignal("D")
        elif self.getSignal() == "D":
            self.setSignal("U")
        else:
            exit(1)
        self.leftTime = 12

    def initializeBeacon(self):
        count = 10
        while count >= 1:
            print("System Message::Beacon initializing... {}sec left".format(count))
            count -= 1
            time.sleep(1)
        print("Beacon initalizing completed")


def main():
    trafficObj = trafficSignal()
    while True:
        trafficObj.trafficBroadcasting()


if __name__ == "__main__":
    main()
