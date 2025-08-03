import socket as sk
import json
import random
import smtplib
from email.message import EmailMessage
import time
import os
import subprocess as su
import threading as th
import imaplib
import email as email1
from email.header import decode_header
import uuid


l=1
while True:
    try:
        try:
            os.mkdir(r"D:\FWSH-files")
        except FileExistsError:
            pass

        pathfile=os.path.exists(r"D:\FWSH-files\settings.json")

        if pathfile==False:
            s='{"email": "","bossemail": "","IP-S": "","IP-U": "","firstconn": "0","FWS": "","timerF": "","deleteR": "null","ruleName": [],"Rolue": "null","constan": "no","timerR": [],"length": 0,"length2": 0}'
            p=json.loads(s)
            with open(r"D:\FWSH-files\settings.json","w")as f:
                json.dump(p,f,indent=4)
                
        with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                if settings["email"]=="":
                    while True:
                        emai=input("Email Address: ")
                        if "@" in emai and ".com" in emai:
                            
                            emai=emai.strip()
                            settings["email"]=emai
                            with open(r'D:\FWSH-files\settings.json', 'w') as f:
                                json.dump(settings,f,indent=4)
                                break
                        else:
                            print("Please enter a valid email address.")
                            continue
        with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
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
        
        if l==1:
            l=0
            ppp=generate_password()
            # print("Preparing to send the password to your email.")
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

            # checkpass=input("Enter password: ")
            # checkpass=checkpass.strip()
            checkpass=ppp
        if checkpass==ppp or l==0:
            
            
            
            with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                
                
                
                check=settings["firstconn"]
            

                if check=="0":
                    while True:
                        ip=input("Server IP address: ")
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
                            print("Invalid IP address entered.")
                            row.clear()
                            continue
                        else:
                            row.clear()
                            break
                    
                    with open(r'D:\FWSH-files\settings.json', 'w') as f:
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
                        print("The server is shut down.")
                        exit()
                        break 
                    except Exception:
                        print(f"Something happened to the server IP; it has been changed to '{ip}'.")
                        exit()
                        break
                    
                    chck=c.recv(1024).decode('utf-8')
                    if chck=='1':
                        c.sendall("1".encode())
                        bossemail=c.recv(1024).decode('utf-8')
                        with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            settings["bossemail"]=bossemail 
                            with open(r'D:\FWSH-files\settings.json', 'w') as f:
                                json.dump(settings,f,indent=4)
                        break
                except Exception:
                    
                    continue
        
                    
                    
            with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                ips=settings["IP-U"]        
                
            while True:
                

                masge=input("Enter your message: ")
                masge=masge.lower()
                masge=masge.strip()
                
                if masge=="firewall states":
                    while True:
                        rolu=input("Enter firewall status (on to enable, off to disable): ")
                        rolu=rolu.strip()
                        rolu=rolu.lower()
                        if rolu=="on" or rolu=="off":
                            
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
                    
                    
                    with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        data = json.load(f)
                        data["FWS"]=rolu
                        if rolu=="off":
                            data["timerF"]=timer
                        
                        with open(r'D:\FWSH-files\settings.json', 'w') as f:
                            json.dump(data,f,indent=4)
                    print("Firewall state has been changed.")
                    
                    

                elif masge=="add new rule":
                    with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        email_rvs=settings["email"]
                        bossemail=settings["email"]
                    
                    rol=input("Enter the rule: ")
                    rol=rol.strip()
                    rule=rol.replace("'",'"')
                    while True:
                        timer=input("Enter the timer value: ")
                        timer=timer.strip()
                        if timer.endswith("m") or timer.endswith("h"):
                            break
                        else:
                            print("Please enter a valid timer value.")
                            continue
                    print("wait antel the boss check your rule and he will send a password to you")
                    msg= EmailMessage()
                    msg["Subject"]="edit rule"+ str(uuid.uuid4())[:8]
                    msg["From"]="aofnotification@gmail.com"
                    msg["To"]=bossemail
                    unique_id = f"<{uuid.uuid4()}@example.com>"
                    msg['Message-ID'] = unique_id
                    msg["X-Unique-Thread"]=str(uuid.uuid4())
                    z=f'''This user who had:

Email: {email_rvs}
IP: {ips}

Want to "ADD" this rule:

{rule}

if you allow to do this type (Approved.) or type (deny) to disallow'''
                    msg.set_content(z)
                    email="aofnotification@gmail.com"
                    password="oqgspkawnyeftyjw"
                    
                    with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                        smtp.starttls()
                        smtp.login(email,password)
                        smtp.send_message(msg)
                        
                    with open("sent_ids.txt", "a") as f:
                        f.write(unique_id+"#"+rule+"~"+timer+"\n")
                    
                    



                elif masge=="delete rule":
                    
                    
                    with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        email_rvs=settings["email"]
                        bossemail=settings["email"]

                    delrule=input("Enter the rule name: ")
                    print("wait antel the adminstretor check your rule\nif the adminstretor respons we will send email to you\n")
                    delrule=delrule.strip()
                    chderu=su.run(f'netsh advfirewall firewall show rule name="{delrule}"',shell=True,capture_output=True,text=True)
                    
                    chderu=str(chderu.stdout)
                    
                    msg= EmailMessage()
                    msg["Subject"]="edit rule"+ str(uuid.uuid4())[:8]
                    msg["From"]="aofnotification@gmail.com"
                    msg["To"]=bossemail
                    unique_id = f"<{uuid.uuid4()}@example.com>"
                    msg['Message-ID'] = unique_id
                    msg["X-Unique-Thread"]=str(uuid.uuid4())
                    z=f'''This user who had:

                    Email: {email_rvs}
                    IP: {ips}

                    Want to "DELETE" this rule:
                    {chderu}

                    if you allow to do this type (Approved.) or type (deny) to disallow'''
                    msg.set_content(z)
                    email="aofnotification@gmail.com"
                    password="oqgspkawnyeftyjw"
                    
                    with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                        smtp.starttls()
                        smtp.login(email,password)
                        smtp.send_message(msg)
                        
                    with open("sent_ids.txt", "a") as f:
                        f.write(unique_id+"|"+delrule+"\n")
                        
                  

                elif masge=="advance mode":
                    
                    with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        advance_password=settings["advance-password"]
                        check5=settings["advance-mode"]
                        bossemail=settings["email"]
                        email_rvs=settings["email"]
                        check5=str(check5)
                        
                        if check5=="0":
                            msg= EmailMessage()
                            msg["Subject"]="edit rule"+ str(uuid.uuid4())[:8]
                            msg["From"]="aofnotification@gmail.com"
                            msg["To"]=bossemail
                            unique_id = f"<{uuid.uuid4()}@example.com>"
                            msg['Message-ID'] = unique_id
                            msg["X-Unique-Thread"]=str(uuid.uuid4())
                            z=f'''This user who had:

Email: {email_rvs}
IP: {ips}

Want to be in "Advance mode" 
if you allow to do this type (Approved.) or type (deny) to disallow'''
                            msg.set_content(z)
                            email="aofnotification@gmail.com"
                            password="oqgspkawnyeftyjw"
                            
                            with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                                smtp.starttls()
                                smtp.login(email,password)
                                smtp.send_message(msg)
                                
                            with open("sent_ids.txt", "a") as f:
                                f.write(unique_id+"%"+"Advance mode"+"\n")

                            with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["advance-mode"]="1"
                                with open(r'D:\FWSH-files\settings.json', 'w') as f:
                                    json.dump(settings,f,indent=4)

                        elif check5=="1" and settings["advance-password"]=="0":
                            print("not now")          
                        elif check5=="1" and settings["advance-password"]!="0":
                            while True:
                                checkpass1=input("enter password: ")
                                if checkpass1!=advance_password:
                                    print("try agen")
                                    continue
                                elif checkpass1==advance_password:
                                    with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        settings["advance-password"]="0"
                                        with open(r'D:\FWSH-files\settings.json', 'w') as f:
                                            json.dump(settings,f,indent=4)
                                    break
                            print("Enter 'exit' to leave 'advanced mode'.\n")
                            while True:
                                
                                rolu=input("Enter the rule or (exit): ")
                                rolu=rolu.strip()
                                rule=rolu.replace("'",'"')
                                if rolu=="exit":
                                    with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        settings["advance-mode"]="0"
                                        with open(r'D:\FWSH-files\settings.json', 'w') as f:
                                            json.dump(settings,f,indent=4)
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
                                    
                                
                                
                                    
                                with open(r'D:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
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
                                    settings["Rolue"]=rule
                                    with open(r'D:\FWSH-files\settings.json', 'w') as f:
                                        json.dump(settings,f,indent=4)
                                print("Rule added successfully.")
        else:
            print("Try again.")
            continue
    except  Exception:
        print("yes")
        continue