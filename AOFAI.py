import socket as sk
import json
import random
import smtplib
from email.message import EmailMessage
import time
import os
import subprocess as su
import uuid



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
            s='{"user-state": "USER","email": "","bossemail": "","IP-S": "","IP-U": "","MAC": "","advance-mode": "0","advance-password": "0","firstconn": "0","FWS": "","timerF": "","deleteR": "null","checkrulename": [],"ruleName": [],"Rolue": "null","constan": "no","timerR": [],"Enaply list": [],"Disaply list": []}'
            p=json.loads(s)
            with open(r"C:\FWSH-files\settings.json","w",encoding='utf-8')as f:
                json.dump(p,f,indent=4)
        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)         
            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    
                    if settings["email"]=="":
                        while True:
                            emai=input("Email Address: ")
                            if "@" in emai and ".com" in emai:
                                
                                emai=emai.strip()
                                settings["email"]=emai
                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                                    break
                            else:
                                print("Please enter a valid email address.")
                                continue
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
                # msg["Subject"]=f"Enter Password - ID({str(uuid.uuid4())[:8]})"
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
                        
                        with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                            settings["IP-S"] =ip
                            
                            settings["firstconn"] = "1"
                            json.dump(settings, f, indent=4)


                    check2=settings["firstconn"]
                    
                    
                    
                    if check2=="1":
                        try:
                            result = su.run('powershell -Command "Get-NetAdapter | Select-Object MacAddress"', shell=True,text=True,capture_output=True)
                            result=result.stdout
                            mac = [l.strip() for l in result.splitlines() if "-" in l] 
                            mac=mac[-1]  
                        except Exception:
                            mac="null"
                        check7=0
                        try:
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
                        except Exception:
                            check7=1

                        if check7==0:
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["IP-U"] =ips
                                settings["MAC"] =mac
                                with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                    json.dump(settings, f, indent=4)
                        ip=settings["IP-S"]
        


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
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["bossemail"]=bossemail 
                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            break
                    except Exception:
                        
                        continue
            
                        
                        
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    ips=settings["IP-U"]  
                    mac=settings["MAC"]  
                    email_rvs=settings["email"]
                    bossemail=settings["bossemail"]  
                    
                        
                
                                
                print("enter (help) for help")
                while True:
                    

                    masge=input("Enter your message: ")
                    masge=masge.lower()
                    masge=masge.strip()
                    
                    if masge=="help" or masge=="h":
                        help='''

    1. firewall state : to change firewall state (off / on).
    2. add new rule : to add one new rule for firewall.
    3. delete rule : to delete one rule from firewall.
    4. advance mode : it is a mode make you to add meny rules and make the rule conest or not. 

    '''
                        print(help)
                    if masge=="firewall state" or masge=="1":
                        print("if you wont to exit enter (exit)")
                        while True:
                            rolu=input("Enter firewall state (on to enable, off to disable): ")
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
                            c.sendall(mac.encode())
                            check1=c.recv(1024).decode()
                            check1=check1.replace("1","")
                            check1=check1.strip()
                            if check1=="firewall log.csv" or check1=="firewall log.csv1":
                                
                                msg= EmailMessage()
                                msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=check4
                                msg.set_content(f"someone reading the server's log file '{check1}'\ndo the porotocole ")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)
                        
                        if rolu!="exit":
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                data = json.load(f)
                                data["FWS"]=rolu
                                if rolu=="off":
                                    data["timerF"]=timer
                                
                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(data,f,indent=4)
                            print("Firewall state has been changed.")
                        
                        

                    elif masge=="add new rule" or masge=="2":
                        print("if you wont to exit enter (exit)")
                        while True:
                            rule=input("Enter the rule: ")
                            if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule:
                                print("try agean")
                                continue
                            if "-or" in rule.lower() or "if" in rule.lower() or "try" in rule.lower() or "catch" in rule.lower():
                                print("try agean")
                                continue
                            if "new-netfirewallrule" not in rule.lower()  or "-displayname" not in rule.lower():
                                print("try agean")
                                continue
                            else:
                                break
                        if rule!="exit":
                            rule=rule.strip()
                            rule=rule.replace("'",'"')
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
                            msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
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

if you allow to do this type (Approved) or type (Deny) to disallow'''
                            msg.set_content(z)
                            email="aofnotification@gmail.com"
                            password="oqgspkawnyeftyjw"
                            
                            with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                                smtp.starttls()
                                smtp.login(email,password)
                                smtp.send_message(msg)
                            rule=f'powershell -Command {rule}'
                            with open(r"C:\FWSH-files\sent_ids.txt", "a",encoding='utf-8') as f:
                                f.write(unique_id+"#"+rule+"~"+timer+"\n")
                        
                        



                    elif masge=="delete rule" or masge=="3":
                        print("if you wont to exit enter (exit)")
                        
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            check6=settings["checkrulename"]
                            check6=list(check6)
                        while True:
                            delrule=input("Enter the rule name: ")
                            if delrule=="exit":
                                break
                            if "#" in delrule or "%" in delrule or "|" in delrule or "~" in delrule:
                                print("try agean")
                                continue
                            if delrule in check6:
                                print("try agean")
                                continue
                            else:
                                break
                        if delrule!="exit":
                            
                            print("wait antel the adminstretor check your rule\nif the adminstretor respons we will send email to you\n")
                            delrule=delrule.strip()
                            chderu=su.run(f'powershell -Command Get-NetFirewallRule -DisplayName "{delrule}"',shell=True,capture_output=True,text=True)
                            
                            chderu=str(chderu.stdout)
                            
                            msg= EmailMessage()
                            msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
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

if you allow to do this type (Approved) or type (Deny) to disallow'''
                            msg.set_content(z)
                            email="aofnotification@gmail.com"
                            password="oqgspkawnyeftyjw"
                            
                            with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                                smtp.starttls()
                                smtp.login(email,password)
                                smtp.send_message(msg)
                                
                            with open(r"C:\FWSH-files\sent_ids.txt", "a",encoding='utf-8') as f:
                                f.write(unique_id+"|"+delrule+"\n")
                            
                    

                    elif masge=="advance mode" or masge=="4":
                        
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            advance_password=settings["advance-password"]
                            check5=settings["advance-mode"]
                            check5=str(check5)
                            
                            if check5=="0":
                                msg= EmailMessage()
                                msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=bossemail
                                unique_id = f"<{uuid.uuid4()}@example.com>"
                                msg['Message-ID'] = unique_id
                                msg["X-Unique-Thread"]=str(uuid.uuid4())
                                z=f'''This user who had:

Email: {email_rvs}
IP: {ips}

Want to be in "Advance mode" 
if you allow to do this type (Approved) or type (Deny) to disallow'''
                                msg.set_content(z)
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                
                                with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                                    smtp.starttls()
                                    smtp.login(email,password)
                                    smtp.send_message(msg)
                                    
                                with open(r"C:\FWSH-files\sent_ids.txt", "a",encoding='utf-8') as f:
                                    f.write(unique_id+"%"+"Advance mode"+"\n")

                                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    settings["advance-mode"]="1"
                                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                        json.dump(settings,f,indent=4)

                            elif check5=="1" and settings["advance-password"]=="0":
                                print("not now")          
                            elif check5=="1" and settings["advance-password"]!="0":
                                print("if you wont to exit enter (exit)")
                                while True:
                                    checkpass1=input("enter password: ")
                                    if checkpass1=="exit":
                                        break
                                    if checkpass1!=advance_password:
                                        print("try agen")
                                        continue
                                    elif checkpass1==advance_password:
                                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                            settings = json.load(f)
                                            settings["advance-password"]="0"
                                            with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)
                                        break
                                if checkpass1!="exit":
                                    while True:
                                        
                                        while True:
                                            rolu=input("Enter the rule or (exit): ")
                                            rolu=rolu.strip()
                                            rule=rolu.replace("'",'"')
                                            if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule:
                                                print("try agean")
                                                continue
                                            if "-or" in rule.lower() or "if" in rule.lower() or "try" in rule.lower() or "catch" in rule.lower():
                                                print("try agean")
                                                continue
                                            if "new-netfirewallrule" not in rule.lower()  or "-displayname" not in rule.lower():
                                                print("try agean")
                                                continue
                                            if rule=="exit":
                                                break
                                            else:
                                                break
                                        if rule=="exit":
                                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                                settings = json.load(f)
                                                settings["advance-mode"]="0"
                                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
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
                                        c.recv(1024).decode()
                                        c.sendall(mac.encode())
                                        check1=c.recv(1024).decode()
                                        check1=check1.replace("1","")
                                        check1=check1.strip()
                                        if check1=="add rule log.csv" or check1=="add rule log.csv1":
                                            
                                            msg= EmailMessage()
                                            msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=check4
                                            msg.set_content(f"someone reading the server's log file '{check1}'\ndo the porotocole ")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)
                        


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
                                            
                                        
                                        
                                        rule=f'powershell -Command {rule}'   
                                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                            settings = json.load(f)
                                            settings["constan"]=constan
                                            if constan=="no":
                                                
                                                
                                                s=settings["checkrulename"]
                                                s=list(s)
                                                s.append(rulename)
                                                settings["checkrulename"]=s 

                                                s=settings["ruleName"]
                                                s=list(s)
                                                s.append(rulename)
                                                settings["ruleName"]=s
                                            
                                                s=settings["timerR"]
                                                s=list(s)
                                                s.append(timer)
                                                settings["timerR"]=s
                                            settings["Rolue"]=rule
                                            with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)
                                        print("Rule added successfully.")




                    elif masge=="rule action" or masge=="5":
                        print("if you wont to exit enter (exit)")
                        
                        
                        while True:
                            ruleac=input("Enter the rule name: ")
                            ruleac=ruleac.strip()
                            
                            if "#" in ruleac or "|" in ruleac or "%" in ruleac or "~" in ruleac or ";" in ruleac or "&" in ruleac or "\\" in ruleac:
                                print("try agean")
                                continue
                            if "-or" in ruleac.lower() or "if" in ruleac.lower() or "try" in ruleac.lower() or "catch" in ruleac.lower():
                                print("try agean")
                                continue
                            if "new-netfirewallrule" in ruleac.lower()  or "-displayname"  in ruleac.lower():
                                print("try agean")
                                continue
                            else:
                                break


                        while True:
                            action=input("Enter Rule Action (Enably , Disaply): ").lower().strip()
                            if action=="enably" or action=="disaply":
                                break
                            else:
                                print("try agean")
                                continue

                        if action=="enably":
                            action1="e"
                        else:
                            action1="d"

                        while True:
                            timer=input("Enter the timer value: ")
                            timer=timer.strip()
                            timer=timer.lower()
                            if timer.endswith("h") or timer.endswith("m"):
                                break
                            else:
                                print("Try again.")
                                continue
                        if ruleac!="exit":
                            
                            print("prepar to sending email to the adminstretor \n")
                            
                            chderu=su.run(f'powershell -Command Get-NetFirewallRule -DisplayName "{ruleac}"',shell=True,capture_output=True,text=True)
                            
                            chderu=str(chderu.stdout)
                            
                            msg= EmailMessage()
                            msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                            msg["From"]="aofnotification@gmail.com"
                            msg["To"]=bossemail
                            unique_id = f"<{uuid.uuid4()}@example.com>"
                            msg['Message-ID'] = unique_id
                            msg["X-Unique-Thread"]=str(uuid.uuid4())
                            z=f'''This user who had:

Email: {email_rvs}
IP: {ips}

Want to "{action}" this rule:
{chderu}

if you allow to do this type (Approved) or type (Deny) to disallow'''
                            msg.set_content(z)
                            email="aofnotification@gmail.com"
                            password="oqgspkawnyeftyjw"
                            
                            with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                                smtp.starttls()
                                smtp.login(email,password)
                                smtp.send_message(msg)
                            ruleac=ruleac + "^" + timer + action1
                            with open(r"C:\FWSH-files\sent_ids.txt", "a",encoding='utf-8') as f:
                                f.write(unique_id+"&"+ruleac+"\n")
                            print("wait until the adminstretor check your email\nif the adminstretor respons we will send email to you\n")
            else:
                print("Try again.")
                continue
    except  Exception:
        print("there are error")
        continue
    