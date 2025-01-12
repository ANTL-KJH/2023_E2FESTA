"""
* Project : 2023CDP main information class
* Program Purpose and Features :
* - information class
* Author : JH KIM
* First Write Date : 2023.07.17
* ==========================================================================
* Program history
* ==========================================================================
* Author    		Date		    Version		History
* JH KIM            2023.07.17		v1.00		First Write
* MG KIM            2023.08.22		v1.10		Change Details
* JH KIM            2023.10.27      v1.11       Add VibActionFlag/setButton func Modified 
"""
import threading
from naviUtils.constant import *

# button state has four different state
# buttonState | -1   |  Default
# buttonState |  1   |  Infra Search Call
# buttonState |  2   |  Okay Call or Stop(No) Call
# buttonState |  3   |  Text Recognition Call
# buttonState |  4   |  Snap Shot(Hand Cam) Call

class Information:
    def __init__(self):
        self.__buttonState = -1  # Default Button State : -1
        self.cs = threading.Lock()
        self.__systemState = 0
        self.now_system = []  # 실행중인 시스템 목록
        self.now_thread = []  # 실행중인 스레드 목록
        self.terminate_flag = False
        self.ip = SERVER_IP
        self.port = SERVER_PORT
        self.udp_port = UDP_PORT
        self.bluetooth_flag=False
        self.capture_data=""
        self.__chk_flag_receive_data=0
        self.vibActionFlag = True   # 진동모듈(vib) 동작 플래그, True이면 동작, Flase이면 미동작


    def show_info(self):
        self.info_list=[self.getButtonState(),self.get_now_system(),
                       self.get_now_thread(),self.getSystemState(),
                       self.get_terminate_flag()]
        return self.info_list

    def getButtonState(self):  # Button state accessor
        return self.__buttonState
    
    def get_now_system(self):
        return self.now_system

    def get_now_thread(self):
        return self.now_thread

    def setButtonState(self, state):  # Button state mutator
        self.cs.acquire()
        print("SYSTEM ALARM::Button State Changed({} -> {})".format(self.getButtonState(), state))
        if self.__buttonState == -2 and state == -2:
            self.changeVibrationFlag()
            self.__buttonState = -1
        else:
            self.__buttonState = state
        self.cs.release()
        return

    # Get System state
    def getSystemState(self):  # System state accessor
        return self.__systemState

    # Set System state
    def setSystemState(self, newSysState):  # System state mutator
        print("SYSTEM ALARM::System State Changed({} -> {})".format(self.getSystemState(), newSysState))
        self.__systemState = newSysState
        return
    
    # Add System in system list
    def add_system(self, system_purpose):
        print(f"SYSTEM ALARM::{system_purpose} appended in SYSTEM list")
        self.now_system.append(system_purpose)
        return

    # remove system list
    def remove_system(self, system_purpose):
        print(f"SYSTEM ALARM::{system_purpose} system removed from list")
        if system_purpose in self.now_system:
            self.now_system.remove(system_purpose)
        else:
            #print("Information System Error")
            assert("ERROR TYPE : SYSTEM irregular terminate occur")
        return


    # Add Thread in thread list
    def add_thread(self, thread_purpose):
        print(f"SYSTEM ALARM::{thread_purpose} appended in THREAD list")
        self.now_thread.append(thread_purpose)
        return
    
    # Therminate Thread list
    def terminate_thread(self, thread_purpose):
        print(f"SYSTEM ALARM::{thread_purpose} thread terminated")
        if thread_purpose in self.now_thread:
            self.now_thread.remove(thread_purpose)
        else:
            #print("Information System Error")
            assert("ERROR TYPE : Thread Could not Found")
        return


    # terminate flag accesser
    def get_terminate_flag(self):
        return self.terminate_flag
    
    # try system terminate
    def terminate_all(self):
        self.terminate_flag = True
        return

    def get_IP(self):
        return self.ip
        
    def get_PORT(self):
        return self.port

    def get_udp_PORT(self):
        return self.udp_port

    def set_capture_data(self,data):
        self.capture_data=data

    def return_capture_data(self):
        return (self.capture_data)
    
    def return_capture_end_flag(self):
        return self.__chk_flag_receive_data
    
    
    def set_return_capture_end_flag(self,data):
        self.__chk_flag_receive_data=data

    
    def set_bluetooth_flag(self,fl):
       self.bluetooth_flag=fl
    def get_bluetooth_flag(self):
        return self.bluetooth_flag

    def changeVibrationFlag(self):
        if self.vibActionFlag == True:
            self.vibActionFlag = False
            print("SYSTEM ALARM::Turn Off the Vibration Module")
        else:
            self.vibActionFlag = True
            print("SYSTEM ALARM::Turn On the Vibration Module")

    def getVibrationFlag(self):
        return self.vibActionFlag