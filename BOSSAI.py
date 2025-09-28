import socket as sk
import json
import uuid
import random
import smtplib
from email.message import EmailMessage
import time
import os
import subprocess as su



# check all code

l=1
while True:
    try:
        try:
            
            os.mkdir(r"C:\FWSH-files")
        except Exception:
            pass

        pathfile=os.path.exists(r"C:\FWSH-files\settings.json")

        if pathfile==False:
            s='{"user-state": "ADMEN","email": "","IP-S": "","IP-U": "","firstconn": "0","FWS": "","timerF": "","deleteR": "null","checkrulename": [],"ruleName": [],"Rolue": "null","constan": "no","timerR": [],"length": 0,"length2": 0}'
            p=json.loads(s)
            with open(r"C:\FWSH-files\settings.json","w")as f:
                json.dump(p,f,indent=4)

        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                
                if settings["email"]=="":
                    while True:
                        emai=input("Email Address: ")
                        if "@" in emai and ".com" in emai:
                            
                            emai=emai.strip()
                            settings["email"]=emai
                            with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                json.dump(settings,f,indent=4)
                                break
                        else:
                            print("Please enter a valid email address.")
                            continue
                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                        json.dump(settings,f,indent=4)
        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            check4=settings["email"]
        

        def generate_password():
            password=random.randint(111111,999999)
            password=str(password)
            return password
        
        if l==1:
            l=0
            ppp=generate_password()
            # print("Preparing to send the password to your email.")
            # msg= EmailMessage()
            # msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
            # msg["From"]="aofnotification@gmail.com"
            # msg["To"]=check4
            # msg.set_content(f"your password is: {ppp}")
            # email="aofnotification@gmail.com"
            # password="oqgspkawnyeftyjw"
            # with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            #     smtp.login(email,password)
            #     smtp.send_message(msg)
            # checkpass=input("Enter password: ")
            # checkpass=checkpass.strip()
            checkpass=ppp
        if checkpass==ppp or l==0:
            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                
                
                
                check=settings["firstconn"]


                if check=="0":
            
                    while True:
                        ip=input("Server IP address: ")
                        ip=ip.strip()
                        
                        row=[]
                        for i in ip:
                            if i==".":
                                row.append(i)
                        if len(row)!=3:
                            print("Invalid IP address entered.")
                            row.clear()
                            continue
                        else:
                            row.clear()
                            break
                    
                    
                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                        settings["IP-S"] =ip
                        settings["firstconn"] = "1"
                        json.dump(settings, f, indent=4)


                check2=settings["firstconn"]
                
                
                
                if check2=="1":
                    ip=settings["IP-S"]
                    try:
                        s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
                        s.connect(("1.1.1.1",80))
                        ips=s.getsockname()[0]
                        s.close()
                    except Exception:
                        s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
                        s.connect(("8.8.8.8",443))
                        ips=s.getsockname()[0]
                        s.close()

                    with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        settings["IP-U"] =ips
                        with open(r'C:\FWSH-files\settings.json', 'w') as f:
                            json.dump(settings, f, indent=4)
                

            

            while True:
                try:
                    c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                    try:
                        c.connect((ip, 9999))
                    except ConnectionRefusedError:
                        print("The server is shut down.")
                        exit()
                        break 
                    except Exception:
                        print(f"Something happened to the server IP; it has been changed to '{ip}'.")
                        exit()
                        break
                    
                    chck=c.recv(1024).decode('utf-8')
                    if chck=='1':
                        
                        check4=str(check4)
                        
                        c.sendall(check4.encode())
                        break
                except Exception:
                    
                    continue
            
            
                    
                    
            def get_wifi_mac():
                result = su.check_output("netsh wlan show interfaces", shell=True, text=True)

                for line in result.splitlines():
                    if "Physical address" in line:
                        mac = line.split(":", 1)[1].strip()  
                        return mac 


            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                ips=settings["IP-U"] 
            while True:
                
                masge=input("Enter your message: ")
                masge=masge.strip()
                masge=masge.lower()
                
                if masge=="help" or masge=="h":
                    help='''
                    
1. firewall state : to change firewall state (off / on).
2. add new rule : to add one new rule for firewall.
3. delete rule : to delete rule from firewall.
4. advance mode : it is a mode make you to add miny rules and make the rule conest or not. 
5. firewall state off all : to disable all the concting user's firewall.
6. firewall state on all : to enable all the concting user's firewall.

'''
                print(help)
                if masge=="firewall states" or masge=="1":
                    print("if you wont to exit enter (exit)")
                    while True:
                        rolu=input("Enter firewall status (on to enable, off to disable): ")
                        rolu=rolu.strip()
                        rolu=rolu.lower()
                        if rolu=="on" or rolu=="off" or rolu=="exit":
                            
                            break
                        else:
                            print("Enter 'on' or 'off'")
                            continue
                    if rolu=="off":
                        while True:
                            timer=input("Enter the timer value: ")
                            timer=timer.strip()
                            timer=timer.lower()
                            if timer.endswith("m") or timer.endswith("h"):
                                break
                            else:
                                print("Please enter a valid timer value.")
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
                            

                        
                            

                        
                        off="off"
                        c.sendall(off.encode())
                        c.recv(1024).decode()
                        c.sendall(timerlog.encode())
                        c.recv(1024).decode()
                        c.sendall(str(time.strftime('%Y-%m-%d %H:%M:%S')).encode())
                        c.recv(1024).decode()
                        ips=str(ips)
                        c.sendall(ips.encode())
                        c.recv(1024).decode()
                        c.sendall(get_wifi_mac().encode())
                        
                    if rolu !="exit":
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            data = json.load(f)
                            data["FWS"]=rolu
                            if rolu=="off":
                                data["timerF"]=timer
                            
                            with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                json.dump(data,f,indent=4)
                        print("Firewall state has been changed.")



                elif masge=="add new rule" or masge=="2":
                    
                    while True:
                        rolu=input("Enter the rule or (exit): ")
                        rolu=rolu.strip()
                        rule=rolu.replace("'",'"')
                        if "#" in rule or "|" in rule or "%" in rule or "~" in rule:
                            print("try agean")
                            continue
                        else:
                            break
                    if rule!="exit":
                        while True:
                            timer=input("Enter the timer value: ")
                            timer=timer.strip()
                            timer=timer.lower()
                            if timer.endswith("m") or timer.endswith("h"):
                                break
                            else:
                                print("Please enter a valid timer value.")
                                continue
                        ppp=generate_password()
                        print("Preparing to send the password to your email.")
                        msg= EmailMessage()
                        msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                        msg["From"]="aofnotification@gmail.com"
                        msg["To"]=check4
                        msg.set_content(f"your password is: {ppp}")
                        email="aofnotification@gmail.com"
                        password="oqgspkawnyeftyjw"
                        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                            smtp.login(email,password)
                            smtp.send_message(msg)
                        while True:
                            entpass=input("Enter password: ")
                            entpass=entpass.strip()
                            if entpass==ppp:
                                break
                            else:
                                print("Try again.")
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
                        c.sendall(ips.encode())
                        c.recv(1024).decode()
                        c.sendall(rule.encode())
                        c.recv(1024).decode()
                        c.sendall("no".encode())
                        c.recv(1024).decode()
                        c.sendall(get_wifi_mac().encode())
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
                            
                    
                            
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
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
                            s=settings["checkrulename"]
                            s=list(s)
                            s.append(rulename)
                            settings["checkrulename"]=s
                            settings["Rolue"]=rule
                            with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                json.dump(settings,f,indent=4)
                        print("Rule added successfully.")



                elif masge=="delete rule" or masge=="3":
                    with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        check6=settings["checkrulename"]
                        check6=list(check6)
                    ppp=generate_password()
                    print("Preparing to send the password to your email.")
                    msg= EmailMessage()
                    msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                    msg["From"]="aofnotification@gmail.com"
                    msg["To"]=check4
                    msg.set_content(f"your password is: {ppp}")
                    email="aofnotification@gmail.com"
                    password="oqgspkawnyeftyjw"
                    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                        smtp.login(email,password)
                        smtp.send_message(msg)
                    print("if you wont to exit enter (exit)")
                    while True:
                        
                        entpass=input("Enter password: ")
                        entpass=entpass.strip()
                        if entpass==ppp or entpass=="exit":
                            break
                        else:
                            print("Try again.")
                            continue
                    if entpass!="exit":
                        while True:
                            delrule=input("Enter the rule name: ")
                            delrule=delrule.strip()
                            if "#" in delrule or "|" in delrule or "%" in delrule or "~" in delrule:
                                print("try agean")
                                continue
                            if delrule in check6:
                                print("try agean")
                                continue
                            
                            else:
                                break
                        if delrule!="exit":
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["deleteR"]=delrule
                                with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                    json.dump(settings,f,indent=4)

                            on="del"
                            c.sendall(on.encode())
                            c.recv(1024).decode()
                            c.sendall(delrule.encode())
                            c.recv(1024).decode()
                            c.sendall(str(time.strftime('%Y-%m-%d %H:%M:%S')).encode())
                            c.recv(1024).decode()
                            ips=str(ips)
                            c.sendall(ips.encode())
                            c.recv(1024).decode()
                            c.sendall(get_wifi_mac().encode())
                            print(f"Rule '{delrule}' deleted successfully.")
                    
                    

                elif masge=="advance mode" or masge=="4":
                    ppp=generate_password()
                    print("Preparing to send the password to your email.")
                    msg= EmailMessage()
                    msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                    msg["From"]="aofnotification@gmail.com"
                    msg["To"]=check4
                    msg.set_content(f"your password is: {ppp}")
                    email="aofnotification@gmail.com"
                    password="oqgspkawnyeftyjw"
                    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                        smtp.login(email,password)
                        smtp.send_message(msg)
                    print("if you wont to exit enter (exit)")
                    while True:
                        
                        entpass=input("Enter password: ")
                        entpass=entpass.strip()
                        if entpass==ppp or entpass=="exit":
                            break
                        else:
                            print("Try again.")
                            continue
                      
                    while True:
                        
                        
                        while True:
                            rolu=input("Enter the rule: ")
                            rolu=rolu.strip()
                            rule=rolu.replace("'",'"')
                            if "#" in rule or "|" in rule or "%" in rule or "~" in rule:
                                print("try agean")
                                continue
                            else:
                                break
                        if rule=="exit":
                            break
                        while True:
                            constan=input("Enter state constant (yes for permanent rule, no for temporary): ")
                            constan=constan.strip()
                            constan=constan.lower()
                            if constan=="yes" or constan=="no":
                                break
                            else:
                                print("enter 'yes' or 'no'")
                                continue
                        constan=constan.strip()
                        if constan=="no":
                            while True:
                                timer=input("Enter the timer value: ")
                                timer=timer.strip()
                                timer=timer.lower()
                                if timer.endswith("h") or timer.endswith("m"):
                                    break
                                else:
                                    print("Try again.")
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
                        if constan=="no":
                            timerlog=timer
                            c.sendall(timerlog.encode())
                        elif constan=="yes":
                            c.sendall("null".encode())
                        c.recv(1024).decode()
                        c.sendall(str(time.strftime('%Y-%m-%d %H:%M:%S')).encode())
                        c.recv(1024).decode()
                        ips=str(ips)
                        c.sendall(ips.encode())
                        c.recv(1024).decode()
                        c.sendall(rule.encode())
                        c.recv(1024).decode()
                        c.sendall(constan.encode())
                        c.recv(1024).decode()
                        c.sendall(get_wifi_mac().encode())
                        
                        if constan=="no":
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
                                
                            
                            
                            
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            settings["constan"]=constan
                            if constan=="no":
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

                                s=settings["checkrulename"]
                                s=list(s)
                                s.append(rulename)
                                settings["checkrulename"]=s
                            settings["Rolue"]=rule
                            with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                json.dump(settings,f,indent=4)
                        print("Rule added successfully.")



                
                elif masge=="firewall states off all" or masge=="5":
                    
                    ppp=generate_password()
                    print("Preparing to send the password to your email.")
                    msg= EmailMessage()
                    msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                    msg["From"]="aofnotification@gmail.com"
                    msg["To"]=check4
                    msg.set_content(f"your password is: {ppp}")
                    email="aofnotification@gmail.com"
                    password="oqgspkawnyeftyjw"
                    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                        smtp.login(email,password)
                        smtp.send_message(msg)
                    print("if you wont to exit enter (exit)")
                    while True:
                        entpass=input("Enter password: ")
                        entpass=entpass.strip()
                        if entpass==ppp or entpass=="exit" :
                            break
                        else:
                            print("Try again.")
                            continue
                    if entpass!="exit":
                        c.sendall(masge.encode())
                        c.recv(1024).decode()
                        c.sendall("gg".encode())
                        print("The firewall will be off in '10' seconds.")
                        break
                elif masge=="firewall states on all" or masge=="6":
                    c.sendall(masge.encode())
                    c.recv(1024).decode()
                    c.sendall("gg".encode())
                    print("The firewall will be on in '10' seconds.")
                    break
        else:
            print("Try again.")
            continue
            
    except  Exception:
        continue