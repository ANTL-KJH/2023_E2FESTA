
#url 을 전송하는 방법

import requests

def send():
    url = 'http://43.201.213.223:8080/rcv?id=ID&id=SUB&id=1'
    response = requests.get(url)
    
send()