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
                            emai=input("Enter your Email Address: ")
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
                
                ppp=generate_password()
                # print("Preparing to send the password to your email.")
                # msg= EmailMessage()
                # msg["Subject"]=f"Identity verification - ID({str(uuid.uuid4())[:8]})"
                # msg["From"]="aofnotification@gmail.com"
                # msg["To"]=check4
                # msg.set_content(f"Your password: {ppp}")
                # email="aofnotification@gmail.com"
                # password="oqgspkawnyeftyjw"
                # with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                #     smtp.login(email,password)
                #     smtp.send_message(msg)

                # checkpass=input("Enter the password: ")
                # checkpass=checkpass.strip()
                checkpass=ppp  
            if checkpass==ppp or l==0:
                
                
                
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    
                    
                    
                    check=settings["firstconn"]
                

                    if check=="0":
                        while True:
                            ip=input("Enter Server IP address: ")
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
        
                if l==1:
                    print("Connecting to the server....")
                    l=0
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

1. Firewall Mode : To change firewall state (off / on).
2. Add New Rule : Add a temporary rule to the firewall.
3. Delete Rule : To delete rule from the firewall.
4. Advance Mode : It is a mode that allows you to add more than one rule to the firewall while specifying their persistence status.
5. Rule State : To disable or enable a specific rule.

'''
                        print(help)
                    if masge=="firewall state" or masge=="1":
                        print("If you want to exit enter (exit)")
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
                                

                            
                                

                            
                        
                        c.sendall(rolu.encode())
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
                        print("If you want to exit enter (exit)")
                        while True:
                            rule=input("Enter the rule: ")
                            if rule=="exit":
                                break
                            if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule:
                                print("Your rule should not contain any of these symbols (# | % ~ ; & \\).")
                                continue
                            if "-or" in rule.lower() or "if" in rule.lower() or "try" in rule.lower() or "catch" in rule.lower():
                                print("The rule contains strange elements. Rewrite it correctly.")
                                continue
                            if "new-netfirewallrule" not in rule.lower()  or "-displayname" not in rule.lower():
                                print("Enter a rule in PowerShell format")
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
                            print("Preparing to send the Email to the official.")
                            msg= EmailMessage()
                            msg["Subject"]=f"Add request - ID({str(uuid.uuid4())[:8]})"
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

if you allow to do this, type (Approved) or type (Deny) to not allowed'''
                            msg.set_content(z)
                            email="aofnotification@gmail.com"
                            password="oqgspkawnyeftyjw"
                            
                            with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                                smtp.starttls()
                                smtp.login(email,password)
                                smtp.send_message(msg)
                           # rule=f'powershell -Command {rule}'
                            with open(r"C:\FWSH-files\sent_ids.txt", "a",encoding='utf-8') as f:
                                f.write(unique_id+"#"+rule+"~"+timer+"\n")
                            print("Wait until the official approves your request.\nYou will receive an email containing the activation code.")
                        



                    elif masge=="delete rule" or masge=="3":
                        print("If you want to exit enter (exit)")
                        
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            check6=settings["checkrulename"]
                            check6=list(check6)
                        while True:
                            delrule=input("Enter the rule name: ")
                            if delrule=="exit":
                                break
                            if "#" in delrule or "%" in delrule or "|" in delrule or "~" in delrule or ";" in delrule or "&" in delrule or "\\" in delrule:
                                print("Your rule should not contain any of these symbols (# | % ~ ; & \\).")
                                continue
                            if delrule in check6:
                                print("The rule can only be deleted when its validity period expires.")
                                continue
                            else:
                                break
                        if delrule!="exit":
                            print("Preparing to send the Email to the official.")
                            
                            delrule=delrule.strip()
                            chderu=su.run(f'powershell -Command Get-NetFirewallRule -DisplayName "{delrule}"',shell=True,capture_output=True,text=True)
                            
                            chderu=str(chderu.stdout)
                            
                            msg= EmailMessage()
                            msg["Subject"]=f"Delete request - ID({str(uuid.uuid4())[:8]})"
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

if you allow to do this type (Approved) or type (Deny) to not allowed'''
                            msg.set_content(z)
                            email="aofnotification@gmail.com"
                            password="oqgspkawnyeftyjw"
                            
                            with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                                smtp.starttls()
                                smtp.login(email,password)
                                smtp.send_message(msg)
                                
                            with open(r"C:\FWSH-files\sent_ids.txt", "a",encoding='utf-8') as f:
                                f.write(unique_id+"|"+delrule+"\n")
                            print("Wait until the official approves your request.\nYou will receive an email.\n")
                    

                    elif masge=="advance mode" or masge=="4":
                        
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            advance_password=settings["advance-password"]
                            check5=settings["advance-mode"]
                            check5=str(check5)
                            
                            if check5=="0":
                                print("Preparing to send the Email to the official.")
                                msg= EmailMessage()
                                msg["Subject"]=f"Advance Mode - ID({str(uuid.uuid4())[:8]})"
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
                                print("Your request has not yet been approved by the official.")          
                            elif check5=="1" and settings["advance-password"]!="0":
                                print("If you want to exit enter (exit)")
                                while True:
                                    checkpass1=input("Enter the password: ")
                                    if checkpass1=="exit":
                                        break
                                    if checkpass1!=advance_password:
                                        print("Rewrite the correct code")
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
                                            if rule=="exit":
                                                break
                                            if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule:
                                                print("Your rule should not contain any of these symbols (# | % ~ ; & \\).")
                                                continue
                                            if "-or" in rule.lower() or "if" in rule.lower() or "try" in rule.lower() or "catch" in rule.lower():
                                                print("The rule contains strange elements. Rewrite it correctly.")
                                                continue
                                            if "new-netfirewallrule" not in rule.lower()  or "-displayname" not in rule.lower():
                                                print("Enter a rule in PowerShell format")
                                                continue
                                            
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
                                            constan=input("Enter a constant for the rule's status ('yes' for a permanent rule, 'no' for a temporary rule): ")
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
                                                    print("Please enter a valid timer value.")
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
                                        on="addrule"
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
                        print("If you want to exit enter (exit)")
                        
                        
                        while True:
                            ruleac=input("Enter the rule name: ")
                            ruleac=ruleac.strip()
                            
                            if "#" in ruleac or "|" in ruleac or "%" in ruleac or "~" in ruleac or ";" in ruleac or "&" in ruleac or "\\" in ruleac:
                                print("Your rule should not contain any of these symbols (# | % ~ ; & \\).")
                                continue
                            if "-or" in ruleac.lower() or "if" in ruleac.lower() or "try" in ruleac.lower() or "catch" in ruleac.lower():
                                print("The rule contains strange elements. Rewrite it correctly.")
                                continue
                            if "new-netfirewallrule" in ruleac.lower()  or "-displayname"  in ruleac.lower():
                                print("The rule contains strange elements. Rewrite it correctly.")
                                continue
                            else:
                                break


                        while True:
                            action=input("Enter Rule Action (Enable , Disable): ").lower().strip()
                            if action=="enable" or action=="disable":
                                pass
                            else:
                                print("Enter (enable/disable)")
                                continue
                            chderu=su.run(f'powershell -Command Get-NetFirewallRule -DisplayName "{ruleac}"',shell=True,capture_output=True,text=True)
                            chderu=str(chderu.stdout)
                            if "Enabled                       : True" in chderu and action=="enable":
                                print("This rule is irlady enabled")
                                continue
                            if "Enabled                       : False" in chderu and action=="disable":
                                print("This rule is irlady disabled")
                                continue
                            else:
                                break
                        if action=="enable":
                            action="Enable"
                            action1="e"
                        else:
                            action="Disable"
                            action1="d"

                        while True:
                            timer=input("Enter the timer value: ")
                            timer=timer.strip()
                            timer=timer.lower()
                            if timer.endswith("h") or timer.endswith("m"):
                                break
                            else:
                                print("Please enter a valid timer value.")
                                continue
                        if ruleac!="exit":
                            
                            print("Preparing to send the Email to the official.")
                            
                            chderu=su.run(f'powershell -Command Get-NetFirewallRule -DisplayName "{ruleac}"',shell=True,capture_output=True,text=True)
                            
                            chderu=str(chderu.stdout)
                            
                            msg= EmailMessage()
                            msg["Subject"]=f"Rule State - ID({str(uuid.uuid4())[:8]})"
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

if you allow to do this type (Approved) or type (Deny) to not allowed'''
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
                            print("Wait until the official approves your request.\nYou will receive an email.\n")
            else:
                print("Rewrite the correct code")
                continue
    except  Exception:
        print("there are error")
        continue
    