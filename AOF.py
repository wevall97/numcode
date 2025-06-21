import time
import subprocess as su
import socket as sk
import threading as th
import json
'''1.6 V'''
RemoteManagement=''
UnicastResponseToMulticast=''
Rolue=''
timmer=''
with open(r'D:\projackt\tools\settings.json', 'r') as file:
    add=json.load()
    RemoteManagement=RemoteManagement[""]
    UnicastResponseToMulticast=UnicastResponseToMulticast[""]
    Rolue=Rolue[""][0]
    timmer=timmer[''][0]
def connction():
    global ordr
    while True:
        try:
            c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            c.connect(('192.168.1.13', 9999))
            check=c.recv(1024).decode('utf-8')
            if check=='1':
                break
        except Exception:
            continue
    while True:
        ordr=c.recv(1094).decode('utf-8')
        c.sendall(''.encode('utf-8'))
th.Thread(target=connction).start()

while True:
    
        
    s=su.run('netsh advfirewall show allprofiles', shell=True, capture_output=True, text=True)
    f=s.stdout
    if 'RemoteManagement                      Enable' in f:
        pass
    if 'UnicastResponseToMulticast            Disable' in f:
        pass
    if 'State                                 OFF' in f or len(f) != 2094 :
        
        su.run('netsh advfirewall set allprofiles state on', shell=True)
        with open(r'C:\Users\ibrah\logfirewall\firewall state.txt', '+a') as file:
            file.write(f'Firewall was off at {time.strftime('%Y-%m-%d %H:%M:%S')} \n')
    
    time.sleep(timmer)  
    