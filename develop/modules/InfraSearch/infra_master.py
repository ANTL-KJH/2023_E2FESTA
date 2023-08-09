# infra_master.py
"""
* Project : 2023CDP Eddystone Receiver
* Program Purpose and Features :
* - infrastructure explore master class
* Author : JH KIM, JH SUN, MG KIM
* First Write Date : 2023.07.11
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History                                                                                 code to fix
* MG KIM			2023.07.11      v0.10	    make from /juwhan_test/split_class.py
* JH SUN            2023.07.18      v1.00       write beacon master
* JH KIM            2023.07.20      v1.01       set_txt, read_tts merged
* JH KIM            2023.08.09      v1.10       source code optimization
"""
import time

from modules.InfraSearch.processing import ProcessingData
from modules.InfraSearch.scannrecive import ScanDelegate, ReceiveSignal
from bluepy.btle import Scanner
from modules.InfraSearch.utils import *
from modules.InfraSearch.constant import *
import requests


class beacon_master:
    def __init__(self, Speaker, mainInfo) -> None:
        self.receive = ReceiveSignal(scanner, duration)
        self.process = 0
        self.information = {}
        self.key = ""
        self.flag = ""
        self.data = ""
        self.speaker = Speaker
        self.mainInfo = mainInfo

    def scan_result_gtts(self):
        self.data = "주변에 "
        for i in self.information.keys():
            if i == Traffic:                    # 신호등
                self.data += (trf_gtts + ", ")
            elif i == Subway:                   # 지하철
                self.data += (sub_gtts + ", ")
        self.data = self.data[:-2]
        self.data += "이 있습니다. 원하시는 정보에 예 버튼을 눌러주세요"
        exitCode = self.start_gtts()
        return exitCode

    def scan_beacon(self):
        self.information = self.receive.scanData()  # scan을 한뒤 이러한 데이터가 있음을 알려주고 data를 전달받는다.
        if not self.information:                    # scan된 data가 없는 경우
            self.data = "주변에 스캔된 비콘이 없습니다."
            self.start_gtts()
            return False
        else:
            exitCode = self.scan_result_gtts()
            if exitCode == -1:      # Infrasearch exit button input
                return -1

            for dict_key in self.information.keys():
                if dict_key == Subway:
                    self.data = "지하철"
                elif dict_key == Traffic:
                    self.data = "신호등"

                exitCode = self.start_gtts()
                if exitCode == -1:  # Infrasearch exit button input
                    return exitCode
                sTime = time.time()
                while True:
                    eTime = time.time()
                    if eTime - sTime > 2:
                        break
                    if self.mainInfo.getButtonState() == 2 or exitCode == 2:
                        self.mainInfo.setButtonState(-1)
                        self.flag = dict_key
                        return True
            self.data = "버튼이 입력되지 않았습니다."
            self.start_gtts()
            return False

    def start_gtts(self):
        exitCode = self.speaker.tts_read(self.data)
        self.data = ""  # data reset
        return exitCode

    def connect_data_base(self):
        url = 'http://43.201.213.223:8080/rcv?id=ID&id=' + self.flag + '&id=' + self.key  # server로 전달할 id이다.
        response = requests.get(url)
        self.data = response.text + self.data

    def process_beacon(self):  # processes하는 부분이다.
        self.process = ProcessingData(self.information, self.flag)  # ProcessingData클래스에 인자전달과 생성을 해준다
        self.process.process_beacon_data()
        # self.connect_data_base()                                  # data_base에 연결하는 경우 주석 해제
        self.data, self.flag, self.key = self.process.return_gtts_mssage()  # prcessing된 message return

    def runScanBeacon(self):
        state = self.scan_beacon()          # beacon scan
        if (state == True):                 # 주변에 scan된 비콘이있을때
            self.process_beacon()           # beacon data processing
            self.start_gtts()               # speaker output
        return