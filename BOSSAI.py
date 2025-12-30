import socket as sk
import json
import random
import time
import os
import subprocess as su
import uuid
from email.message import EmailMessage
import smtplib

# chick the name of the commend "rule state"

# check all code

l=1
while True:
    try:
        try:
            
            os.mkdir(r"C:\FS-File")
        except Exception:
            pass

        pathfile=os.path.exists(r"C:\FS-File\settings.json")

        if pathfile==False:
            s='{"user-state": "ADMEN","email": "","IP-S": "","IP-U": "","MAC": "","firstconn": "0","FWS": "","timerF": "","deleteR": "null","checkrulename": [],"ruleName": [],"Rolue": "null","constan": "no","timerR": [],"Enaply list": [],"Disaply list": []}'
            p=json.loads(s)
            with open(r"C:\FS-File\settings.json","w",encoding='utf-8')as f:
                json.dump(p,f,indent=4)
        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f) 
            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    
                    if settings["email"]=="":
                        while True:
                            emai=input("Enter your Email Address: ")
                            if "@" in emai and ".com" in emai:
                                
                                emai=emai.strip()
                                settings["email"]=emai
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                                    break
                            else:
                                print("Please enter a valid email address.")
                                continue
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(settings,f,indent=4)
            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                check4=settings["email"]
            

            def generate_password():
                password=random.randint(111111,999999)
                password=str(password)
                return password
            
            if l==1:
                
                ppp=generate_password()
                print("Preparing to send the password to your email.")
                msg= EmailMessage()
                msg["Subject"]=f"Identity verification - ID({str(uuid.uuid4())[:8]})"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=check4
                msg.set_content(f"Your password: {ppp}")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
                checkpass=input("Enter the password: ")
                checkpass=checkpass.strip()
                
            if checkpass==ppp or l==0:
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
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
                        
                        
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
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
                            
                        ip=settings["IP-S"]
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
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["IP-U"] =ips
                                settings["MAC"] =mac
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings, f, indent=4)
                    

                if l==1:
                    print("Connecting to the server....")
                    time.sleep(1)
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
                            
                            check4=str(check4)
                            
                            c.sendall(check4.encode())
                            break
                    except Exception:
                        
                        continue
                
                
                        
                def check_inputs(rule,num):

                    if num==1:
                        if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule or "@" in rule or "$" in rule or ")" in rule or "(" in rule:
                            return ("Your rule should not contain any of these symbols (# | % ~ ; & \\ @ $ ( ) ).")
                        
                        if "-or" in rule.lower() or "if" in rule.lower() or "try" in rule.lower() or "catch" in rule.lower():
                            return ("The rule contains strange elements. Rewrite it correctly.")
                        
                        if "new-netfirewallrule" not in rule.lower()  or "-displayname" not in rule.lower():
                            return ("Enter a rule in PowerShell format")
                        
                        else:
                            return "1"
                        


                    if num==2:
                        if "#" in rule or "%" in rule or "|" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule or "@" in rule or "$" in rule or ")" in rule or "(" in rule:
                            return ("Your rule should not contain any of these symbols (# | % ~ ; & \\ @ $ ( ) ).")
                        
                        chderu=su.run(f'powershell -Command Get-NetFirewallRule -DisplayName "{rule}"',shell=True,capture_output=True,text=True)
                        chderu=str(chderu.stdout).strip()
                        if "" in chderu and "DisplayName" not in chderu:
                            return ("There is no rule by that name")
                        
                        else:
                            return "1"



                    if num==3:
                        if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule or "@" in rule or "$" in rule or ")" in rule or "(" in rule:
                            return ("Your rule should not contain any of these symbols (# | % ~ ; & \\ @ $ ( ) ).")
                        
                        if "-or" in rule.lower() or "if" in rule.lower() or "try" in rule.lower() or "catch" in rule.lower():
                            return ("The rule contains strange elements. Rewrite it correctly.")
                        
                        if "new-netfirewallrule"  in rule.lower()  or "-displayname"  in rule.lower():
                            return ("The rule contains strange elements. Rewrite it correctly.")
                        
                        chderu=su.run(f'powershell -Command Get-NetFirewallRule -DisplayName "{rule}"',shell=True,capture_output=True,text=True)
                        chderu=str(chderu.stdout).strip()
                        if "" in chderu and "DisplayName" not in chderu:
                            return("There is no rule by that name")
                        else:
                            return "1"
                        
                    
                

                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    ips=settings["IP-U"] 
                    mac=settings["MAC"] 
                print("enter (help) for help")
                while True:
                    
                    masge=input("Enter your message: ")
                    masge=masge.strip()
                    masge=masge.lower()
                    
                    if masge=="help" or masge=="h":
                        help='''
                        
1. Firewall Mode : To change firewall state (off / on).
2. Add New Rule : Add a temporary rule to the firewall.
3. Delete Rule : To delete rule from the firewall.
4. Advance Mode : It is a mode that allows you to add more than one rule to the firewall while specifying their persistence status.
5. Firewall State Off All : To disable the firewall for all connected devices.
6. Firewall State On All : To enable the firewall for all connected devices.
7. Rule State : To disable or enable a specific rule.

'''
                        print(help)
                    if masge=="Firewall Mode" or masge=="1":
                        print("If you want to exit enter (exit)\n")
                        while True:
                            rolu=input("Enter firewall statu (on to enable, off to disable): ")
                            rolu=rolu.strip()
                            rolu=rolu.lower()
                            if rolu=="on" or rolu=="off" or rolu=="exit":
                                
                                break
                            else:
                                print("There is an error. Enter 'on' or 'off'")
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
                                

                            
                                

                            
                        if rolu!="exit":    
                            c.sendall(rolu.encode())
                            c.recv(1024).decode()
                            if rolu=="on":
                               timerlog="null" 
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
                                msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=check4
                                msg.set_content(f"Someone is reading the 'Firewall_log.csv' file.\n you should check the server's status to see if it has been compromised or not.")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)
                            
                        if rolu !="exit":
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                data = json.load(f)
                                data["FWS"]=rolu
                                if rolu=="off":
                                    data["timerF"]=timer
                                
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(data,f,indent=4)
                            print("Firewall state has been changed.")



                    elif masge=="add new rule" or masge=="2":
                        
                        while True:
                            rolu=input("Enter the rule or (exit): ")
                            rolu=rolu.strip()
                            rule=rolu.replace("'",'"')
                            if rule=="exit":
                                break
                            re=check_inputs(rule,1)
                            if re=="1" :
                                break
                            print(re)
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
                            c.sendall(mac.encode())
                            check1=c.recv(1024).decode()
                            check1=check1.replace("1","")
                            check1=check1.strip()
                            if check1=="add rule log.csv" or check1=="add rule log.csv1":
                                
                                msg= EmailMessage()
                                msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=check4
                                msg.set_content(f"Someone is reading the 'Add_rule_log.csv' file.\n you should check the server's status to see if it has been compromised or not.")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)
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
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
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
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            print("Rule added successfully.")



                    elif masge=="delete rule" or masge=="3":
                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            check6=settings["checkrulename"]
                            check6=list(check6)
                        
                        print("if you want to exit enter (exit)")
                        
                        
                        while True:
                            delrule=input("Enter the rule name: ")
                            delrule=delrule.strip()
                            if delrule=="exit":
                                break

                            
                            if delrule in check6:
                                print("The rule can only be deleted when its validity period expires.")
                                continue
                            print("The rule is being checking...")
                            time.sleep(1)
                            re=check_inputs(delrule,2)
                            if re=="1":
                                break
                            print(re)
                            
                            
                            
                            
                        if delrule!="exit":
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["deleteR"]=delrule
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
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
                            c.sendall(mac.encode())
                            check1=c.recv(1024).decode()
                            check1=check1.replace("1","")
                            check1=check1.strip()
                            if check1=="delete rule log.csv" or check1=="delete rule log.csv1":
                                
                                msg= EmailMessage()
                                msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=check4
                                msg.set_content(f"Someone is reading the 'Delete_rule.csv' file.\n you should check the server's status to see if it has been compromised or not.")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)
                            print(f"The Rule '{delrule}' deleted successfully.")
                        
                        

                    elif masge=="advance mode" or masge=="4":
                        
                        print("if you want to exit enter (exit)")
                        
                        
                        while True:
                            
                            
                            while True:
                                rolu=input("Enter the rule: ")
                                rolu=rolu.strip()
                                rule=rolu.replace("'",'"')
                                if rule=="exit":
                                    break
                                re=check_inputs(rule,1)
                                if re=="1" :
                                    break
                                print(re)
                            if rule=="exit":
                                break
                            while True:
                                constan=input("Enter a constant for the rule's status ('yes' for a permanent rule, 'no' for a temporary rule): ")
                                constan=constan.strip()
                                constan=constan.lower()
                                if constan=="yes" or constan=="no":
                                    break
                                else:
                                    print("Enter 'yes' or 'no'")
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
                                msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=check4
                                msg.set_content(f"Someone is reading the 'Add_rule_log.csv' file.\n you should check the server's status to see if it has been compromised or not.")
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
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["constan"]=constan
                                if constan=="no":
                                    

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
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            print("Rule added successfully.")



                    
                    elif masge=="firewall state off all" or masge=="5":
                        
                        c.sendall("firewall state off all".encode())
                        c.recv(1024).decode()
                        c.sendall("gg".encode())
                        print("The firewall will be turned off after 10 seconds.")
                        break  
                    elif masge=="firewall state on all" or masge=="6":

                        c.sendall("firewall state on all".encode())
                        c.recv(1024).decode()
                        c.sendall("gg".encode())
                        print("The firewall will restart after 10 seconds.")
                        break

                
                    

                    elif masge=="rule state" or masge=="7":
                        print("If you want to exit enter (exit)")
                        
                        
                        while True:
                            ruleac=input("Enter the rule name: ")
                            ruleac=ruleac.strip()
                            if ruleac=="exit":
                                break
                            
                            print("The rule is being checking...")
                            time.sleep(1)
                            re=check_inputs(ruleac,3)
                            if re=="1":
                                break
                            print(re)

                        if ruleac!="exit":
                            while True:
                                action=input("Enter Rule Action (Enable , Disable): ").lower().strip()
                                if action=="enable" or action=="disable" or action=="exit":
                                    pass
                                else:
                                    print("Enter (enable/disable)")
                                    continue
                                if action=="exit":
                                    break
                                

                                print("The rule is being checking...")
                                time.sleep(1)
                                chderu=su.run(f'powershell -Command Get-NetFirewallRule -DisplayName "{ruleac}"',shell=True,capture_output=True,text=True)
                                chderu=str(chderu.stdout).strip()
                                if "Enabled                       : True" in chderu and action=="enable":
                                    print ("This rule is currently enabled")
                                    
                                if "Enabled                       : False" in chderu and action=="disable":
                                    print ("This rule is currently disabled")
                                    
                                else:
                                    break  
                                
                            if action!="exit":

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
                        if ruleac!="exit" and action!="exit":
                            
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                if action=="enably":
                                    settings["Enaply list"]=[ruleac + "^" + timer]
                                else:
                                    settings["Disaply list"]=[ruleac + "^" + timer]
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)

                            on="rua"
                            c.sendall(on.encode())
                            c.recv(1024).decode()
                            c.sendall(ruleac.encode())
                            c.recv(1024).decode()
                            c.sendall(timer.encode())
                            c.recv(1024).decode()
                            c.sendall(action.encode())
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
                            if check1=="acction rule log.csv" or check1=="action rule log.csv1":
                                
                                msg= EmailMessage()
                                msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=check4
                                msg.set_content(f"Someone is reading the 'State_rule.csv' file.\n you should check the server's status to see if it has been compromised or not.")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)
                            
                            print(f"The Rule state of : '{ruleac}' change successfully.")
                
            else:
                print("Rewrite the correct code")
                continue
                
    except  Exception:
        
        continue