#thread_bl.py
"""
* Project : 2023CDP Eddystone Receiver
* Program Purpose and Features :
* - receive broadcasting message and processing
* Author : JH KIM, JH SUN
* First Write Date : 2023.06.30
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* JH SUN			2023.06.30      v1.00	    First Write
* JH KIM            2023.06.30      v1.01       scan func write
* JH SUN            2023.07.02      V1.02       우선순위 큐 사용하여 다수의 eddystone이 들어왔을때 RSSI 가 가장 높은 비콘만 받아온다.             우선순위 큐의 사이즈 개선/시작할때 오류 발생(1회) 
* JH SUN            2023.07.02      V1.02       우선순위큐에서 데이터 추출후 원소 초기화 작업                                                    시작할때 오류 발생(1회) 
* JH SUN            2023 07.02      V1.10       멀티 스레드를 통해 scan과 출력을 각각의 스레드로 관리한다.                                       시작할때 오류 발생(1회)
* JH SUN            2023 07.02      V1.11       dead_lock 발생 해결 priorty_queue에서는 que.notempty()가아닌 not que.empty()사용   멀티스레드 정상 작동                                                      시작할때 오류 발생(1회)
* JH SUN            2023 07.03      V1.20       ReceiveSignal 클래스 생성       
* JH SUN            2023 07.4       V1.21       flag 에 따른 각각 함수 생성                                                                  
"""
from bluepy.btle import Scanner, DefaultDelegate
from queue import PriorityQueue
import threading
import time
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        self.__scan_data__ = {}
        if (DefaultDelegate != None):
            DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        raw = dev.getScanData()
        mac = dev.addr.upper()
        rssi = dev.rssi
        data = {}
        data['raw'] = raw
        data['mac'] = mac
        data['rssi'] = rssi
        self.__scan_data__ = data

    def getScanData(self):
        return self.__scan_data__





class ReceiveSignal:
    def __init__(self,scanner,duration):
        self.scanner=scanner  #scanner
        self.duration=duration  #scan duration
        self.lock=threading.Lock()
        self.que=PriorityQueue()
        self.data=''




    def scanData(self):   #scan thread func
        while True:
            devices = self.scanner.scan(self.duration)
            print("scan end",end="\n ")
            print("=============================")
            for dev in devices:
                for (adtype, desc, value) in dev.getScanData():
                    if  "aafe" in value:
                        rssi_power=abs(dev.rssi)   #if big rssi then less recive power
                        beaconData = value[8:]  #erase flag
                        print(rssi_power,beaconData)
                        self.lock.acquire()
                        self.que.put((rssi_power,beaconData))
                        self.lock.release()
            time.sleep(1)


    def print_scan_data(self):    #print thread func
        while True:

            self.lock.acquire()
            if self.que.empty():
                self.lock.release()
                time.sleep(2)
            else:

                rssi_beacon,data=self.que.get()
                self.data=data
                flag=self.Check_flag()   #chk flag

                if flag=="Traffic":
                    print("dfdf")
                    self.Traffic_sign()
                elif flag=="Subway":
                    self.Subway_sign()
                    
                
                self.Erase_que()  #erase que 
                self.lock.release() #mutex unlock
                time.sleep(1)

    def Check_flag(self):
        if self.data in "545246":   #traffic sign
            print("지하철")
            return "Traffic"
        elif self.data in "535542":  #SUB subway
            return "Subway"

    def Traffic_sign(self):
        trafiic_number,color,Ten,One=self.data[6:12],self.data[12:14],self.data[14:16],self.data[16:18]  #tuple형태로 data 꺼내오기
        if color=="47": 
            color="green"
        elif color=="52":
            color="red"
        print("This is Traffic  traffic_number is : " , trafiic_number,"color : ",color,"left time is ",int(Ten)-30,int(One)-30)


    def Subway_sign(self):
        subway_number,way,Ten,One=self.data[6:12],self.data[12:14],self.data[14:16],self.data[16:18]
        if way=="55":
            way="상행선"
        elif way=="44":
            way="하행선"
        print("This is Subway subway_number is : ",subway_number,"Way is ",way,"left time is ",int(Ten)-30,int(One)-30,"min")



    def Erase_que(self):    #priortyqueue use not que.empty()  erase all value 
        while not self.que.empty():
            self.que.get()



def main():
    duration =3 
    scan_delegate = ScanDelegate()
    scanner = Scanner().withDelegate(scan_delegate)
    receive_signal=ReceiveSignal(scanner,duration)


    scan_thread=threading.Thread(target=receive_signal.scanData)
    print_thread=threading.Thread(target=receive_signal.print_scan_data)

    scan_thread.start()
    print_thread.start()

    scan_thread.join()
    print_thread.join()

if __name__ == "__main__":
    main()

