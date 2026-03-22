import socket as sk
import json
import random
import smtplib
from email.message import EmailMessage
import time
import os
import subprocess as su
import uuid
import re

# chick the name of the commend "rule state"
# check all code
print("checking system files...")

def poewrshell(ordar):
    p = su.Popen(
        ["powershell.exe", "-Command", ordar],  
        stdin=su.PIPE,
        stdout=su.PIPE,
        stderr=su.PIPE,
        text=True
    )
    
    output, error = p.communicate()
    return output, error


l=1
while True:
    try:
        try:
           
            os.mkdir(r"C:\FS-File")
        except Exception:
           pass

        pathfile=os.path.exists(r"C:\FS-File\settings.json")

        if pathfile==False:
            s='{"user-state": "ADMEN","email": "","IP-S": "","IP-U": "","MAC": "","firstconn": "0","FWS": "","timerF": "","deleteR": "null","checkrulename": [],"ruleName": [],"Rolue": "null","constan": "no","timerR": [],"Enaply list": [],"Disaply list": [],"edit_wait": "0","path_proName_PID": "","white list": [],"white list checker": ""}'
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
                            if "@gmail.com" in emai :
                                
                                emai=emai.strip()
                                settings["email"]=emai
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                                    break
                            else:
                                print("Please enter a valid email address.")
                                continue
            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
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
            if l==0 or checkpass==ppp:
                
                
                
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    
                    
                    
                    check=settings["firstconn"]
                

                    if check=="0":
                        while True:
                            ip=input("Enter Server IP address: ")
                            ip=ip.strip()
                            
                            row=[]
                            chnum=["1","2","3","4","5","6","7","8","9","0","."] 
                            for cnum in ip:
                                if cnum not in chnum:
                                    cnum="block"
                                    break
                            if cnum=="block":
                                print("Invalid IP address entered.")
                                continue

                            if ip.endswith(".") or ip.startswith("."):
                                print("Invalid IP address entered.")
                                continue
                            
                            if "." not in ip:
                                print("Invalid IP address entered.")
                                continue

                            for i in ip:
                                row.append(i)
                                if i==".":
                                    lenrow=len(row)
                                    if lenrow==4:
                                        jl=''.join(row)
                                        jl=jl[:-1]
                                        jl=int(jl)
                                        if jl>255:
                                            lenrow="block"
                                            break
                                        else:
                                            row.clear()  
                                    elif lenrow>4:
                                        row.clear()
                                        lenrow="block"
                                        break
                                    else:
                                        row.clear()
                                
                            if lenrow=="block":
                                print("Invalid IP address entered.")
                                continue
                            else:
                                break
                        
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            settings["IP-S"] =ip
                            
                            settings["firstconn"] = "1"
                            json.dump(settings, f, indent=4)
                        

                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        check2=settings["firstconn"]
                    
                    
                    
                    if check2=="1":
                        try:
                            result = poewrshell("Get-NetAdapter | Select-Object MacAddress")
                            result=list(result)
                            result=''.join(result)
                            mac = [lmac.strip() for lmac in result.splitlines() if "-" in lmac] # تعديل
                            mac=mac[-1]  
                        except Exception:
                            mac="null"
                            
                        ip=settings["IP-S"]
                        try:
                            try:
                                server=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
                                server.connect(("1.1.1.1",80))
                                ips=server.getsockname()[0]
                                server.close()
                            except Exception:
                                
                                server=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
                                server.connect(("8.8.8.8",443))
                                ips=server.getsockname()[0]
                                server.close()
                        except Exception:
                            ips="null"
                            
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
                            c.sendall("1".encode())
                            bossemail=c.recv(1024).decode('utf-8')
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["bossemail"]=bossemail 
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            break
                    except Exception:
                        
                        continue
            
                        
                      
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    ips=settings["IP-U"]  
                    mac=settings["MAC"]  
                    email_rvs=settings["email"]
                    bossemail=settings["bossemail"]  
                    
                        
                def check_inputs(rule,num,ruletype=any):

                    if num==1:
                        if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule or "@" in rule or "$" in rule or ")" in rule or "(" in rule:
                            return ("Your rule should not contain any of these symbols (# | % ~ ; & \\ @ $ ( ) )")
                        
                        if "-or " in rule.lower() or "if " in rule.lower() or "try " in rule.lower() or "catch " in rule.lower():#تعديل
                            return ("The rule contains strange elements. Rewrite it correctly.")
                        
                        if "new-netfirewallrule" not in rule.lower():
                            return ("Enter a rule in PowerShell format")
                        
                        else:
                            return "1"
                        


                    if num==2:
                        if "#" in rule or "%" in rule or "|" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule or "@" in rule or "$" in rule or ")" in rule or "(" in rule:
                            return ("Your rule should not contain any of these symbols (# | % ~ ; & \\ @ $ ( ) )")
                        
                        if "-or " in rule.lower() or "if " in rule.lower() or "try " in rule.lower() or "catch " in rule.lower():
                            return ("The rule contains strange elements. Rewrite it correctly.")
                        
                        if "new-netfirewallrule"  in rule.lower()  or "-displayname"  in rule.lower():
                            return ("The rule contains strange elements. Rewrite it correctly.")
                        
                        chderu,error=poewrshell(f'Get-NetFirewallRule -{ruletype} "{rule}"')
                        
                        if error:
                            return ("There is no rule by that name")
                        
                        else:
                            return "1"



                    if num==3:
                        if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule or "@" in rule or "$" in rule or ")" in rule or "(" in rule:
                            return ("Your rule should not contain any of these symbols (# | % ~ ; & \\ @ $ ( ) )")
                        
                        if "-or " in rule.lower() or "if " in rule.lower() or "try " in rule.lower() or "catch " in rule.lower():
                            return ("The rule contains strange elements. Rewrite it correctly.")
                        
                        if "new-netfirewallrule"  in rule.lower()  or "-displayname"  in rule.lower():
                            return ("The rule contains strange elements. Rewrite it correctly.")
                        
                        chderu,error=poewrshell(f'Get-NetFirewallRule -{ruletype} "{rule}"')
                        
                        if error:
                            return("There is no rule by that name")
                        else:
                            return "1"
                       



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
6. White list : To manage the white list.
'''
                        print(help)
                    if masge=="white list" or masge=="6":
                        m='''
You can add programs to the white list to prevent them from being blocked by the System.
To add a program to the white list, enter 'add' and then provide the program name and its path.
To delete a program from the white list, enter 'delete' and then provide the program name and its path.
To exit the white list management, enter 'exit'.
'''
                        print(m+"\n")
                        time.sleep(2)
                        while True:
                            mack=input("Enter 'add' or 'delete' or 'exit': ").lower()
                            if mack.strip()=="exit":
                                break
                            elif mack.strip()=="add":

                                programe=input("Enter the program name: ").strip()
                                propath=input("Enter the program path: ").strip()
                                
                                propath=propath.replace("'","")
                                propath=propath.replace('"',"")
                                if not programe.endswith(".exe"):
                                    programe=programe+".exe"
                                

                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        data = json.load(f)
                                        s=data["white list"]
                                        s=list(s)
                                        if programe+propath in s:
                                            print("it is in the white list aerldy")
                                            continue
                                        
                                        s.append(programe+propath)
                                        data["white list"]=s
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(data,f,indent=4)
                                print(f"{programe} has been added to the white list")
                            elif mack=="delete":
                                programe=input("Enter the program name: ").strip()
                                propath=input("Enter the program path: ").strip()

                                propath=propath.replace("'","")
                                propath=propath.replace('"',"")
                                if not programe.endswith(".exe"):
                                    programe=programe+".exe"
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        data = json.load(f)
                                        s=data["white list"]
                                        s=list(s)
                                        if programe+propath not in s:
                                            print("it is not in the white list") 
                                            continue
                                        s.remove(programe+propath)
                                        data["white list"]=s
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(data,f,indent=4)
                                print(f"{programe} has been removed from the white list")
                            else:
                                print("you must enter 'add' or 'delete'")
                                continue
                                


                    if masge=="firewall mode" or masge=="1":
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
                                co=0 
                                timer=input("Enter the timer value: ")
                                timer=timer.strip().lower() 

                                if not (timer.endswith("m") or  timer.endswith("h")):
                                    print("Please enter a valid timer value.")
                                    continue

                                smol=["1","2","3","4","5","6","7","8","9","0","m","h"]
                                for smolrimer in timer:
                                    if smolrimer not in smol:
                                        print("Please enter a valid timer value.")
                                        co=1
                                        break

                                if co==1:
                                    continue

                                morh=[]
                                for smolrimer in timer:
                                    morh.append(smolrimer)
                                    if smolrimer =="h" or smolrimer =="m":
                                        break
                                timer=''.join(morh)

                                if timer.endswith("m") or timer.endswith("h"):
                                    break

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
                                

                            
                                

                            
                        if rolu != "exit":
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
                        
                        if rolu!="exit":
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                data = json.load(f)
                                data["FWS"]=rolu
                                if rolu=="off":
                                    data["timerF"]=timer
                                
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(data,f,indent=4)
                            print("Firewall state has been changed.")
                        
                        

                    elif masge=="add new rule" or masge=="2":
                        print("If you want to exit enter (exit)")
                        while True:
                            rule=input("Enter the rule: ")
                            rule=rule.strip()
                            
                            if rule=="exit":
                                break

                            if "'" in rule:
                                print("ok")
                                continue

                            ree=check_inputs(rule,1)
                            if ree=="1" :
                                break
                            print(ree)

                        if rule!="exit":
                            
                            while True:
                                co=0 
                                timer=input("Enter the timer value: ")
                                timer=timer.strip().lower() # تعديل

                                if not (timer.endswith("m") or  timer.endswith("h")):#تعديل
                                    print("Please enter a valid timer value.")
                                    continue

                                smol=["1","2","3","4","5","6","7","8","9","0","m","h"]
                                for smolrimer in timer:
                                    if smolrimer not in smol:
                                        print("Please enter a valid timer value.") #تعديل 
                                        co=1
                                        break

                                if co==1:
                                    continue

                                morh=[]
                                for smolrimer in timer:
                                    morh.append(smolrimer)
                                    if smolrimer =="h" or smolrimer =="m":#تعديل
                                        break
                                timer=''.join(morh)

                                if timer.endswith("m") or timer.endswith("h"):
                                    break

                            print("Preparing to send the Email to the official....")
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
                            with open(r"C:\FS-File\sent_ids.txt", "+a",encoding='utf-8') as f:#if i get problem delete '+' from the "a"
                                f.write(unique_id+"#"+rule+"~"+timer+"\n")
                            print("Wait until the official approves your request.\nYou will receive an email containing the activation code.")
                        



                    elif masge=="delete rule" or masge=="3":
                        print("If you want to exit enter (exit)")
                        
                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            check6=settings["checkrulename"]
                            check6=list(check6)

                        while True:
                            ruty=input("Do you want to enter the rule 'DisplayName' or 'Name': ")
                            ruty=ruty.strip().lower()
                            if ruty=="exit":
                                break
                            if ruty in ["name","n"]:
                                ruty="Name"
                                break
                            elif ruty in ["displayname","d"]:
                                ruty="DisplayName"
                                break
                            else:
                                print("ok")
                                continue

                        while True:
                            delrule=input(f"Enter the rule {ruty} or (exit): ")
                            delrule=delrule.strip()
                            if delrule=="exit":
                                break
                            if delrule in check6:
                                print("The rule can only be deleted when its validity period expires.")
                                continue
                            
                            print("The rule is being checking...")
                            
                            time.sleep(1)
                            ree=check_inputs(delrule,2,ruty)
                            if ree=="1":
                                chderu=poewrshell(f'Get-NetFirewallRule -{ruty} "{delrule}"')
                                chderu=list(chderu)
                                chderu=''.join(chderu)
                                break
                            print(ree)
                        ####################################     
                        if delrule!="exit":
                            print("Preparing to send the Email to the official....")
                            
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
                                
                            with open(r"C:\FS-File\sent_ids.txt", "+a",encoding='utf-8') as f:
                                f.write(unique_id+"|"+delrule+"wevall"+ruty+"\n")# check it when you check "AOF.py"
                            print("Wait until the official approves your request.\nYou will receive an email.\n")
                    

                    elif masge=="advance mode" or masge=="4":
                        
                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            advance_password=settings["advance-password"]
                            check5=settings["advance-mode"]
                            check5=str(check5)
                            
                            if check5=="0":
                                print("Preparing to send the Email to the official....")
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
                                    
                                with open(r"C:\FS-File\sent_ids.txt", "+a",encoding='utf-8') as f:
                                    f.write(unique_id+"%"+"Advance mode"+"\n")

                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    settings["advance-mode"]="1"
                                    with open(r'C:\FS-File\settings.json', 'w') as f:
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
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                            settings = json.load(f)
                                            settings["advance-password"]="0"
                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)
                                        break

                                if checkpass1!="exit":
                                    while True:
                                        
                                        while True:
                                            rolu=input("Enter the rule or (exit): ")
                                            rule=rolu.strip()
                                           
                                            
                                            if rule=="exit":
                                                break
                                            ree=check_inputs(rule,1)
                                            if ree=="1" :
                                                break
                                            print(ree)
                                        if rule=="exit":
                                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                settings = json.load(f)
                                                settings["advance-mode"]="0"
                                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                    json.dump(settings,f,indent=4)
                                            break
                                        while True:
                                            constan=input("Enter a constant for the rule's status ('yes' for a permanent rule, 'no' for a temporary rule): ")
                                            constan=constan.strip()
                                            constan=constan.lower()
                                            if constan in ["yes","no","y","n"]:#تعديل
                                                break
                                            else:
                                                print("Enter 'yes' or 'no'")
                                                continue

                                        if constan=="no":
                                            while True:
                                                co=0 
                                                timer=input("Enter the timer value: ")
                                                timer=timer.strip().lower() # تعديل

                                                if not (timer.endswith("m") or  timer.endswith("h")):#تعديل
                                                    print("Please enter a valid timer value.")
                                                    continue

                                                smol=["1","2","3","4","5","6","7","8","9","0","m","h"]
                                                for smolrimer in timer:
                                                    if smolrimer not in smol:
                                                        print("Please enter a valid timer value.") #تعديل 
                                                        co=1
                                                        break

                                                if co==1:
                                                    continue

                                                morh=[]
                                                for smolrimer in timer:
                                                    morh.append(smolrimer)
                                                    if smolrimer =="h" or smolrimer =="m":#تعديل
                                                        break
                                                timer=''.join(morh)

                                                if timer.endswith("m") or timer.endswith("h"):
                                                    break

####################################################################################################################

                                        row1=[]
                                        row = re.split(" ",rule)
                                        for i in row:
                                            if i.lower() =="-displayname":
                                                e=int(row.index(i))+1
                                                rulename=row[e]
                                                if rulename=="":
                                                    while True:
                                                        e=e+1
                                                        rulename=row[e]
                                                        if rulename!="":
                                                            break
                                                if rulename.startswith(("'",'"')) and rulename.endswith(("'",'"')) and len(rulename)!=1:
                                                    row1.clear()
                                                    break
                                                if rulename.startswith('"'):
                                                        stri='"'
                                                else:
                                                    stri="'"
                                                while True:
                                                    row1.append(rulename)
                                                    row1.append(" ")
                                                    e=e+1
                                                    rulename=row[e]
                                                    if rulename.endswith(stri):
                                                        row1.append(rulename)
                                                        rulename=''.join(row1)
                                                        row1.clear()
                                                        row.clear()
                                                        break
                                                break
#####################################################################################################################

                                        c.sendall("addrule".encode())
                                        c.recv(1024).decode()
                                        c.sendall(rulename.encode())
                                        c.recv(1024).decode()
                                        if constan=="no":
                                            c.sendall(timer.encode())
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
                                            
                                        
                                        
                                        #rule=f'powershell -Command {rule}'   
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
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
                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)
                                        print("Rule added successfully.")




                    elif masge=="rule state" or masge=="5":
                        print("If you want to exit enter (exit)")
                        
                        while True:
                            ruty=input("Do you want to enter the rule 'DisplayName' or 'Name': ")
                            ruty=ruty.strip().lower()
                            if ruty=="exit":
                                break
                            if ruty in ["name","n"]:
                                ruty="Name"
                                break
                            elif ruty in ["displayname","d"]:
                                ruty="DisplayName"
                                break
                            else:
                                print("ok")
                                continue

                        while True:
                            ruleac=input(f"Enter the rule`s {ruty}: ")
                            ruleac=ruleac.strip()
                            if ruleac=="exit":
                                break
                            # chderu=poewrshell(f'Get-NetFirewallRule -DisplayName "{ruleac}"')
                            # chderu=str(chderu.stdout).strip()
                            
                            print("The rule is being checking...")
                            time.sleep(1)
                            ree=check_inputs(ruleac,3,ruty)
                            if ree=="1":
                                break
                            print(ree)
                        action="exit"
                        if ruleac!="exit":
                            while True:
                                action=input("Enter Rule Enable (True , False): ").lower().strip()
                                if action=="true" or action=="false" or action=="exit":
                                    pass
                                else:
                                    print("Enter (true/false)")
                                    continue
                                if action=="exit":
                                    break
                                

                                print("The rule is being checking...")
                                time.sleep(1)
                                chderu=poewrshell(f'Get-NetFirewallRule -{ruty} "{ruleac}"')
                                chderu=list(chderu)
                                chderu=''.join(chderu)
                                if "Enabled                       : True" in chderu and action=="true":
                                    print ("This rule is currently enabled (true)")
                                    
                                elif "Enabled                       : False" in chderu and action=="false":
                                    print ("This rule is currently disabled (false)")
                                    
                                else:
                                    break  
                                
                            if action!="exit":

                                if action=="true":
                                    action="Enable"
                                    action1="e"
                                else:
                                    action="Disable"
                                    action1="d"

                                while True:
                                    co=0 
                                    timer=input("Enter the timer value: ")
                                    timer=timer.strip().lower() # تعديل

                                    if not (timer.endswith("m") or  timer.endswith("h")):#تعديل
                                        print("Please enter a valid timer value.")
                                        continue

                                    smol=["1","2","3","4","5","6","7","8","9","0","m","h"]
                                    for smolrimer in timer:
                                        if smolrimer not in smol:
                                            print("Please enter a valid timer value.") #تعديل 
                                            co=1
                                            break

                                    if co==1:
                                        continue

                                    morh=[]
                                    for smolrimer in timer:
                                        morh.append(smolrimer)
                                        if smolrimer =="h" or smolrimer =="m":#تعديل
                                            break
                                    timer=''.join(morh)

                                    if timer.endswith("m") or timer.endswith("h"):
                                        break

                        if ruleac!="exit" and action!="exit":
                            
                            print("Preparing to send the Email to the official....")
                            
                            # chderu=poewrshell(f'Get-NetFirewallRule -{ruty} "{ruleac}"')
                            
                            # chderu=list(chderu)
                            # chderu=''.join(chderu)
                            
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
                            with open(r"C:\FS-File\sent_ids.txt", "a",encoding='utf-8') as f:
                                f.write(unique_id+"&"+ruleac+"wevall"+ruty+"\n")
                            print("Wait until the official approves your request.\nYou will receive an email.\n")
            else:
                print("Rewrite the correct code")
                continue
    except  Exception:
        print("error")
        continue
    #812