import socket as sk
import json
import EncDec as ed
import random
import smtplib
from email.message import EmailMessage
import time
import os
# remamber to add "length=settings["length"]" in 'settings.json'
# added new shaep to the last lines

# edit the path
try:
    os.mkdir(r"D:\AOF-files")
except FileExistsError:
    pass

pathfile=os.path.exists(r"D:\AOF-files\settings.json")

if pathfile==False:
    s='{"email": "","IP-S": "","IP-U": "","firstconn": "0","FWS": "","timerF": "","ruleName": [],"Rolue": "null","timerR": [],"length": 0,"length2": 0}'# i need to check the index in "ruleName" and "timerR"
    p=json.loads(s)
    with open(r"D:\AOF-files\settings.json","w")as f:
        json.dump(p,f,indent=4)
        
with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        if settings["email"]=="":
            while True:
                emai=input("enter your email: ")
                if "@" in emai and ".com" in emai:
                    
                    emai=emai.strip()
                    settings["email"]=emai
                    with open(r'D:\AOF-files\settings.json', 'w') as f:
                        json.dump(settings,f,indent=4)
                        break
                else:
                    print("enter a valid email")
                    continue
with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f)
    check4=settings["email"]
    

def generate_password():
    
    row1 = []
    for _ in range(6):
        ran = random.randint(0, 9)
        ran = str(ran)
        row1.append(ran)
    password = ''.join(map(str,row1))
    row1.clear()
    return password
  

ppp=generate_password()
# print("prepar to send the password to your email")
# msg= EmailMessage()
# msg["Subject"]="Enter password"
# msg["From"]="aofnotification@gmail.com"
# msg["To"]=check4
# msg.set_content(f"your password is: {ppp}")
# email="aofnotification@gmail.com"
# password="oqgspkawnyeftyjw"
# with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
#     smtp.login(email,password)
#     smtp.send_message(msg)
checkpass=ppp
# checkpass=input("enter password: ")
# checkpass=checkpass.strip()

if checkpass==ppp:
    
    
    
    with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        
        
        
        check=settings["firstconn"]
      

        if check=="0":
            while True:
                ip=input("Enter IP server: ")
                ip=ip.strip()
                s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
                s.connect(("1.1.1.1",80))
                ips=s.getsockname()[0]
                s.close()
                row=[]
                for i in ip:
                    if i==".":
                        row.append(i)
                if len(row)!=3:
                    print("Invalid IP address")
                    row.clear()
                    continue
                else:
                    row.clear()
                    break
            
            with open(r'D:\AOF-files\settings.json', 'w') as f:
                settings["IP-S"] =ip
                settings["IP-U"] =ips
                settings["firstconn"] = "1"
                json.dump(settings, f, indent=4)


        check2=settings["firstconn"]
        
        
        
        if check2=="1":
            check3=settings["IP-S"]
            
        
            ip = check3
            
            
        
    
    
    
    while True:
        try:
            c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            try:
                c.connect((ip, 9999))
            except ConnectionRefusedError:
                print("the server is shot downe")
                exit()
                break 
            except Exception:
                print(f"somethig hapned to the ip server it is change to '{ip}'")
                exit()
                break
            
            chck=c.recv(1024).decode('utf-8')
            if chck=='1':
                c.sendall("1".encode())
                break
        except Exception:
            
            continue
  
            
            
    with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        ips=settings["IP-U"]        
        
    while True:
        

        masge=input("enter masge: ")
       
        masge=masge.strip()
        #edit firewall states
        if masge=="firewall states":
            while True:
                rolu=input("enter firewall states: ")
                rolu=rolu.strip()
                if rolu=="on" or rolu=="off":
                    
                    break
                else:
                    print("enter 'on' or 'off'")
                    continue
            if rolu=="off":
                while True:
                    timer=input("enter timer: ")
                    timer=timer.strip()
                    if timer.endswith("m") or timer.endswith("h") or timer.endswith("s"):
                        break
                    else:
                        print("enter a valid timer")
                        continue
                timerlog=timer
                if timer.endswith("m"):
                    lens=len(timer)
                    timer=timer[:lens-1]
                    timer=int(timer)
                    timer*=60
                    timer=str(timer)
                    


                elif timer.endswith("h"):
                    lens=len(timer)
                    timer=timer[:lens-1]
                    timer=int(timer)
                    timer*=3600
                    timer=str(timer)
                    

                elif timer.endswith("s"):
                    lens=len(timer)
                    timer=timer[:lens-1]
                    

                
                off="off"
                c.sendall(off.encode())
                c.recv(1024).decode()
                c.sendall(timerlog.encode())
                c.recv(1024).decode()
                c.sendall(str(time.strftime('%Y-%m-%d %H:%M:%S')).encode())
                c.recv(1024).decode()
                ips=str(ips)
                c.sendall(ip.encode())
            
            
            with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                data = json.load(f)
                data["FWS"]=rolu
                if rolu=="off":
                    data["timerF"]=timer
                
                with open(r'D:\AOF-files\settings.json', 'w') as f:
                    json.dump(data,f,indent=4)
            print("firewall states change")
            
            

        elif masge=="add new rule":
            
            c.sendall(masge.encode())
            rol=input("enter rule: ")
            rol=rol.strip()
            rule=rol.replace("'",'"')
            c.sendall(rule.encode())
            while True:
                timer=input("enter timer: ")
                timer=timer.strip()
                if timer.endswith("m") or timer.endswith("h") or timer.endswith("s"):
                    break
                else:
                    print("enter a valid timer")
                    continue
            ips=str(ips)
            c.sendall(ip.encode())
            print("wait antel the boss check your rule and he will send a password to you")
            checkpass1=c.recv(1024).decode()
            
            while True:
                entpass=input("enter password: ")
                entpass=entpass.strip()
                if entpass!=checkpass1:
                    print("try agen")
                    continue
                if entpass==checkpass1:
                    break
                
            row=[]
            row1=[]


            for i in rule:
                row1.append(i)
                if i =="'" or i=='"':
                    break
            d=''.join(row1)
            e=rule.removeprefix(d)
            for i in e:
                if i =="'" or i=='"':
                    break
                row.append(i)
            rulename=''.join(row)
            print(rulename)
            row.clear()
            row1.clear()
            on="on"
            c.sendall(on.encode())
            c.recv(1024).decode()
            c.sendall(rulename.encode())
            c.recv(1024).decode()
            timerlog=timer
            c.sendall(timerlog.encode())
            c.recv(1024).decode()
            c.sendall(str(time.strftime('%Y-%m-%d %H:%M:%S')).encode())
            c.recv(1024).decode()
            ips=str(ips)
            c.sendall(ip.encode())
            c.recv(1024).decode()
            c.sendall(rule.encode())
            if timer.endswith("m"):
                lens=len(timer)
                timer=timer[:lens-1]
                timer=int(timer)
                timer*=60
                timer=str(timer)
                


            elif timer.endswith("h"):
                lens=len(timer)
                timer=timer[:lens-1]
                timer=int(timer)
                timer*=3600
                timer=str(timer)
                
            
            elif timer.endswith("s"):
                lens=len(timer)
                timer=timer[:lens-1]
                
            with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                length=settings["length"]
                length+=1
                settings["length"]=length
                s=settings["ruleName"]
                s=list(s)
                s.append(rulename)
                settings["ruleName"]=s 
                s=settings["timerR"]
                s=list(s)
                s.append(timer)
                settings["timerR"]=s
                settings["Rolue"]=rule
                with open(r'D:\AOF-files\settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)


        elif masge=="advance mode":
            c.sendall(masge.encode())
            checkpass1=c.recv(1024).decode()
            ips=str(ips)
            c.sendall(ip.encode())
            while True:
                entpass=input("enter password: ")
                entpass=entpass.strip()
                if entpass!=checkpass1:
                    print("try agen")
                    continue
                if entpass==checkpass1:
                    break
            print("enter 'exit' to exit form 'advance mode'\n")
            while True:
                
                rolu=input("enter rule: ")
                rolu=rolu.strip()
                rule=rolu.replace("'",'"')
                if rolu=="exit":
                    break
                while True:
                    timer=input("enter timer: ")
                    timer=timer.strip()
                    if timer.endswith("m") or timer.endswith("h") or timer.endswith("s"):
                        break
                    else:
                        print("enter a valid timer")
                        continue
                row=[]
                row1=[]


                for i in rule:
                    row1.append(i)
                    if i =="'" or i=='"':
                        break
                d=''.join(row1)
                e=rule.removeprefix(d)
                for i in e:
                    if i =="'" or i=='"':
                        break
                    row.append(i)
                rulename=''.join(row)
                row.clear()
                row1.clear()
                on="on"
                c.sendall(on.encode())
                c.recv(1024).decode()
                c.sendall(rulename.encode())
                c.recv(1024).decode()
                timerlog=timer
                c.sendall(timerlog.encode())
                c.recv(1024).decode()
                c.sendall(str(time.strftime('%Y-%m-%d %H:%M:%S')).encode())
                c.recv(1024).decode()
                ips=str(ips)
                c.sendall(ip.encode())
                c.recv(1024).decode()
                c.sendall(rule.encode())
                if timer.endswith("m"):
                    lens=len(timer)
                    timer=timer[:lens-1]
                    timer=int(timer)
                    timer*=60
                    timer=str(timer)
                    


                elif timer.endswith("h"):
                    lens=len(timer)
                    timer=timer[:lens-1]
                    timer=int(timer)
                    timer*=3600
                    timer=str(timer)
                    
                
                elif timer.endswith("s"):
                    lens=len(timer)
                    timer=timer[:lens-1]
                    
                with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    length=settings["length"]
                    length+=1
                    settings["length"]=length
                    s=settings["ruleName"]
                    s=list(s)
                    s.append(rulename)
                    settings["ruleName"]=s
                    s=settings["timerR"]
                    s=list(s)
                    s.append(timer)
                    settings["timerR"]=s
                    settings["Rolue"]=rule
                    with open(r'D:\AOF-files\settings.json', 'w') as f:
                        json.dump(settings,f,indent=4)
else:
    print("try agen")
    time.sleep(1)
    exit()