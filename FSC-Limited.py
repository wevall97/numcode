import subprocess as su
import random
import os
import json
import smtplib
from email.message import EmailMessage
import uuid
import time
import socket as sk
import pandas as pd
import threading as th


#في الجزئيه حقت نقل مجلد ملفات csv خليه قبل عمليه الارسال يقوم بي نسخ المجلد و تغير اسمه حتى يشير الى جهاز معين
#do ping to check if the server working or not
#make a method that let me know if the user has been offline


# الانظمه الفضل لي ابنيها :
# black list
# check if the user is offline
# sending "Security_Events" to any server

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


def generate_password():
    password=random.randint(111111,999999)
    password=str(password)
    return password


def check_inputs(rule,num,ruletype=any):

    if num==1:
        forbidden = ['#','|','%','~',';','&','\\','@','$',')','(','`','\n','\r','\x00']
        for ch in forbidden:
            if ch in rule:
                return "Your rule should not contain special characters."
        
        dangerous_keywords = [
            "-or ", "if ", "try ", "catch ",
            "invoke-", "iex ", "iwr ",          # ← جديد
            "downloadstring", "webclient",        # ← جديد
            "start-process", "invoke-expression"  # ← جديد
        ]
        for kw in dangerous_keywords:
            if kw in rule.lower():
                return "The rule contains invalid elements."
        
        if "new-netfirewallrule"  in rule.lower():
            return "The rule contains invalid elements."
        
        if "-displayname"  in rule.lower():
            return "The rule contains invalid elements."
        else:
            return "1"
        


    if num==2:
        forbidden = ['#','|','%','~',';','&','\\','@','$',')','(','`','\n','\r','\x00']
        for ch in forbidden:
            if ch in rule:
                return "Your rule should not contain special characters."
        
        dangerous_keywords = [
            "-or ", "if ", "try ", "catch ",
            "invoke-", "iex ", "iwr ",          # ← جديد
            "downloadstring", "webclient",        # ← جديد
            "start-process", "invoke-expression"  # ← جديد
        ]
        for kw in dangerous_keywords:
            if kw in rule.lower():
                return "The rule contains invalid elements."
        
        if "new-netfirewallrule"  in rule.lower()  or "-displayname"  in rule.lower():
            return ("The rule contains strange elements. Rewrite it correctly.")
        
        chderu,error=poewrshell(f'Get-NetFirewallRule -{ruletype} "{rule}"')
        
        if error:
            return ("There is no rule by that name")
        
        else:
            return "1"


        

def check_timer():

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
    return timer


def on_off_line():
   
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

    return ips





             
print("checking system files...")


try:
           
    os.mkdir(r"C:\FS-File")
except Exception:
    pass

try:
           
    os.mkdir(r"C:\FS-File\Security_Events")
except Exception:
    pass

pathfile=os.path.exists(r"C:\FS-File\settings.json")

if pathfile==False:
    s='{"email": "","IP-U": "","MAC": "","IP-S": "null","FWS": "","timerF": "","deleteR": "null","Rolue": "null","checkrulename": [],"ruleName": [],"statee": "null","constan": "no","timerR": [],"path_proName_PID": "","white list": [],"white list checker": "","modify_rule": "null","user_role": "UNKNOWN","work_start": 8,"work_end": 18,"work_days": [0,1,2,3,4]}'
    p=json.loads(s)
    with open(r"C:\FS-File\settings.json","w",encoding='utf-8')as f:
        json.dump(p,f,indent=4)


time.sleep(1.5)
print("checking connction...\n")
time.sleep(1.5)

ips=on_off_line()

if ips=="null":
    print("You are offline, check your internet.")
    time.sleep(5)
    os._exit(0)

with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f)

    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
            settings["IP-U"] =ips
            json.dump(settings,f,indent=4) 


with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f)

    try:
        result, error = poewrshell("Get-NetAdapter | Select-Object MacAddress")
        result=list(result)
        result=''.join(result)
        mac = [lmac.strip() for lmac in result.splitlines() if "-" in lmac] # تعديل
        mac=mac[-1] 

    except Exception:
        mac="null"

    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
        settings["MAC"] =mac
        json.dump(settings,f,indent=4)

 

with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f)

    if settings["email"]=="":
        while True:
            emai=input("Enter your Email Address: ")
            if "@gmail.com" in emai :
                
                settings["email"]=emai.strip()
                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                    json.dump(settings,f,indent=4)
                    break
            else:
                print("Please enter a valid email address.")
                continue


with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f)
    check4=settings["email"]


ppp=generate_password()
# print("Preparing to send the password to your email.")
# msg= EmailMessage()
# msg["Subject"]=f"Identity verification - ID({str(uuid.uuid4())[:8]})"
# msg["From"]="aofnotification@gmail.com"
# msg["To"]=check4
# msg.set_content(f"This is your password to verify your identity and connect to the server:\n{ppp}\n\nIf you did not request this password, please check your account security immediately.\n\n\nSecurity System:\nFS System")
# email="aofnotification@gmail.com"
# password="oqgspkawnyeftyjw"
# with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
#     smtp.login(email,password)
#     smtp.send_message(msg)


lock=0
def locker():
    global lock
    time.sleep(180)
    if lock==0:
        print("\n***********************************")
        print("the program will close in 5 second")
        print("***********************************\n")
        time.sleep(5)
        os._exit(0)

th.Thread(target=locker).start()



checkpass=ppp
attmet=0
while True:
    # checkpass=input("Enter the password: ")
    # checkpass=checkpass.strip()
    if checkpass==ppp:
        break
    if attmet==3:
        print("try agen letar")
        time.sleep(5)
        os._exit(0)
    if checkpass!=ppp:
        attmet+=1
        print("\nRewrite the correct code")
        print(f"You have left {4-attmet} atmtted\n")
        continue
    

lock=1

while True:
    try:

        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f) 

             

            print("enter (help) for help")

            masge=input("Enter your message: ").strip().lower()
            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                ips=settings["IP-U"]  
                mac=settings["MAC"] 


            if masge=="help" or masge=="h":
                help='''

1. Firewall Mode : To change firewall state (off / on).
2. Add New Rule  : Add a temporary rule to the firewall.
3. Delete Rule   : To delete rule from the firewall.
4. Rule State    : To disable or enable a specific rule.
5. White list    : To manage the white list.
6. Settings      : To change your settings.
7. CSV           : To send all the csv files from your pc to the server you choose.
'''
                print(help)
            


            if masge=="firewall mode" or masge=="1":
                print("If you want to exit enter (exit)")
                while True:
                    state=input("Enter firewall state (on to enable, off to disable): ").lower().strip()
                    
                    if state in ["on","off","exit"]:
                        
                        break
                    else:
                        print("Enter 'on' or 'off'")
                        continue
                if state=="off":
                    timer=check_timer()
                    timer_log=timer
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
                    
                
                if state!="exit":
                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        data = json.load(f)
                        data["FWS"]=state
                        if state=="off":
                            data["timerF"]=timer
                        
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(data,f,indent=4)
                    

                    try:
                        s=pd.read_csv(r"C:\FS-File\Security_Events\Firewall_log.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "FWS":["FWS"],
                            "TIMER":["TIMER"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-File\Security_Events\Firewall_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "FWS":[state],
                            "TIMER":[timer_log],
                            "TIME":[str(time.strftime('%Y-%m-%d %H:%M:%S'))]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-File\Security_Events\Firewall_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        print("ali")

                    print("Firewall state has been changed.")

            

            elif masge=="add new rule" or masge=="2":
                
                rule=["New-NetFirewallRule"]
                medn=0
                ex=0
                constan="no"
                DisplayName=''
                Name=''
                Action=''
                Direction=''
                Enabled=''
                LocalPort='0'
                Protocol=''
                Remoteport='0'
                Profile=''
                Program=''

                while True:

                    DisplayName=input("Enter DisplayName or (exit): ").strip()
                    if DisplayName=="exit":
                        ex=1
                        break
                    if not DisplayName:
                        break
                    res=check_inputs(DisplayName,1)
                    if res=="1":
                        rule.append(f" -DisplayName {DisplayName}")
                        medn=1
                        break
                    print(res)
                    continue
                
                if ex==0:
                    while True:

                        Name=input("Enter Name or (exit): ").strip()
                        if Name=="exit":
                            ex=1
                            break
                        if not Name:
                            break
                        res=check_inputs(Name,1)
                        if res=="1":
                            rule.append(f" -Name {Name}")
                            medn=2+medn
                            break
                        print(res)
                        continue
                #check if it works
                if medn==0 and ex==0:
                    print("You must enter 'Name' or 'DisplayName'")

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
                            print("Enter a valid option.")
                            continue


                    while True:

                        ruty1=input(f"Enter {ruty}: ").strip()
                        if not ruty1:
                            continue
                        res=check_inputs(ruty1,1)
                        if res=="1":
                            medn=4
                            break
                        print(res)
                        continue
                

                if ex==0:
                    while True:
                        Action=input("Enter Action or (exit): ").strip()
                        if Action=="exit":
                            ex=1
                            break
                        if not Action:
                            break
                        if Action.lower() not in ["allow","block"]:
                            print("Enter a valid action (allow/block).")
                            continue
                        else:
                            rule.append(f" -Action {Action}")
                            break


                if ex==0:
                    while True:
                        Direction=input("Enter Direction or (exit): ").strip()
                        if Direction=="exit":
                            ex=1
                            break
                        if not Direction:
                            break
                        if Direction.lower() not in ["inbound","outbound"]:
                            print("Enter a valid direction (inbound/outbound).")
                            continue
                        else:
                            rule.append(f" -Direction {Direction}")
                            break


                if ex==0:
                    while True:
                        Enabled=input("Enter Enabled or (exit): ").strip()
                        if Enabled=="exit":
                            ex=1
                            break
                        if not Enabled:
                            break
                        if Enabled.lower() not in ["true","false"]:
                            print("Enter a valid enabled value (true/false).")
                            continue
                        else:
                            rule.append(f" -Enabled {Enabled}")
                            break

                if ex==0:
                    #check this in futuer
                    while True:
                        Profile=input("Enter Profile or (exit): ").strip()
                        if Profile=="exit":
                            ex=1
                            break
                        if not Profile:
                            break
                        if Profile.lower() not in ["domain","private","public"]:
                            print("Enter a valid profile (domain/private/public).")
                            continue
                        else:
                            rule.append(f" -Profile {Profile}")
                            break

                if ex==0:
                    #put the auther Protocols
                    while True:
                        Protocol=input("Enter Protocol or (exit): ").strip()
                        if Protocol=="exit":
                            ex=1
                            break
                        if not Protocol:
                            break
                        if Protocol.lower() not in ["tcp","udp","icmp"]:
                            print("Enter a valid protocol (tcp/udp/icmp).")
                            continue
                        else:
                            rule.append(f" -Protocol {Protocol}")
                            break


                if ex==0:
                    while True:
                        LocalPort=input("Enter LocalPort or (exit): ").strip()
                        if LocalPort=="exit":
                            ex=1
                            break
                        if not LocalPort:
                            break
                        if not LocalPort.isdigit() or int(LocalPort)<1 or int(LocalPort)>65535:
                            print("Enter a valid port number (1-65535).")
                            continue
                        else:
                            rule.append(f" -LocalPort {LocalPort}")
                            break


                if ex==0:
                    while True:
                        Remoteport=input("Enter Remoteport or (exit): ").strip()
                        if Remoteport=="exit":
                            ex=1
                            break
                        if not Remoteport:
                            break
                        if not Remoteport.isdigit() or int(Remoteport)<1 or int(Remoteport)>65535:
                            print("Enter a valid port number (1-65535).")
                            continue
                        else:
                            rule.append(f" -Remoteport {Remoteport}")
                            break


                if ex==0:
                    while True:
                        Program=input("Enter Program or (exit): ").strip()
                        if Program=="exit":
                            ex=1
                            break
                        if not Program:
                            break
                        Program=Program.replace('"','')
                        if not Program.endswith(".exe"):
                            print("Enter a valid program path (should end with .exe).")
                            continue
                        if '"' in Program or "'" in Program:
                            print("Enter a valid program path (without ' or '').")
                            continue
                        else:
                            rule.append(f' -Program "{Program}"')
                            break
                

                if ex==0:
                    rule=''.join(rule)
                    while True:
                        tim_pre=input("Do you want the rule to be permanent (y/n): ").lower().strip()
                        if tim_pre in ["n","no"]:
                            #check if i need to make it like a real timer or just left it like that
                            timer=check_timer()
                            timer_log=timer

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

                            if medn==1:
                                rulename=DisplayName
                            elif  medn==2:
                                rulename=Name
                            elif  medn==3:
                                rulename=DisplayName
                            elif  medn==4:
                                rulename=ruty

                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                data = json.load(f)
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
                            break

                        elif tim_pre in ["y","yes"]:

                            if medn==1:
                                rulename=DisplayName
                            elif  medn==2:
                                rulename=Name
                            elif  medn==3:
                                rulename=DisplayName
                            elif  medn==4:
                                rulename=ruty

                            constan="yes"
                            timer_log="null"
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["constan"]="yes"
                                settings["Rolue"]=rule
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            break

                        else:
                            print("You must enter (yse/no)")
                            continue
                        
                    if medn==1:
                        rulename_log="null"
                    elif  medn==2:
                        rulename_log=Name
                        rulename="null"
                    elif  medn==3:
                        rulename_log=Name
                    elif  medn==4:
                        if ruty=="Name":
                            rulename_log=ruty
                            rulename="null"
                        else:
                            rulename_log="null"

                    try:
                        s=pd.read_csv(r"C:\FS-File\Security_Events\Add_rule_log.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Program_Name":["Program_Name"],
                            "Program_Path":["Program_Path"],
                            "DisplayName":["DisplayName"],
                            "Name":["Name"],
                            "RULE":["RULE"],
                            "TIMER":["TIMER"],
                            "Permanent":["Permanent"],
                            "White_list":["White_list"],
                            "TIME":["TIME"]
                        }

                        d=pd.DataFrame(datafrme)
                        d.to_csv(r"C:\FS-File\Security_Events\Add_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Program_Name":["FS System"],
                            "Program_Path":["FS System"],
                            "DisplayName":[rulename],
                            "Name":[rulename_log],
                            "RULE":[rule],
                            "TIMER":[timer_log],
                            "Permanent":[constan],# get for it a new name
                            "White_list":["NO"],
                            "TIME":[str(time.strftime('%Y-%m-%d %H:%M:%S'))]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-File\Security_Events\Add_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        print("ali")
                    print("Your rule had been add")

                


            elif masge=="delete rule" or masge=="3":
                print("If you want to exit enter (exit)")
                        
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    exs_rule=settings["checkrulename"]
                    exs_rule=list(exs_rule)

                while True:
                    ds_n=input("Do you want to enter the rule 'DisplayName' or 'Name': ")
                    ds_n=ds_n.strip().lower()
                    if ds_n=="exit":
                        break
                    if ds_n in ["name","n"]:
                        ds_n="Name"
                        break
                    elif ds_n in ["displayname","d"]:
                        ds_n="DisplayName"
                        break
                    else:
                        print("Enter 'DisplayName' or 'Name'")
                        continue

                delrule="exit"
                if ds_n!="exit":
                    while True:
                        delrule=input(f"Enter the rule {ds_n} or (exit): ")
                        delrule=delrule.strip()
                        if delrule=="exit":
                            break
                        if delrule in exs_rule:
                            print("The rule can only be deleted when its validity period expires.")
                            continue
                        
                        print("The rule is being checking...")
                        
                        time.sleep(1)
                        ree=check_inputs(delrule,2,ds_n)
                        if ree=="1":
                            break
                        print(ree)
                    
                    if delrule!="exit":
                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            settings["deleteR"]=delrule
                            
                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4)
                        
                        if ds_n=="DisplayName":
                            name_log="null"
                        else:
                            name_log=ds_n
                            ds_n="null"

                        try:
                            s=pd.read_csv(r"C:\FS-File\Security_Events\Delete_rule_log.csv") 
                        except Exception:
                            datafrme={
                                "IP":["IP"],
                                "MAC":["MAC"],
                                "Program_Name":["Program_Name"],
                                "Program_Path":["Program_Path"],
                                "white list":["white list"],
                                "DisplayName":["DisplayName"],
                                "Name":["Name"],
                                "TIME":["TIME"]
                            }

                            d=pd.DataFrame(datafrme)
                            d.to_csv(r"C:\FS-File\Security_Events\Delete_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 


                        datafrme={
                                "IP":[ips],
                                "MAC":[mac],
                                "Program_Name":["FS System"],
                                "Program_Path":["FS System"],
                                "white list":["NO"],
                                "DisplayName":[ds_n],
                                "Name":[name_log],
                                "TIME":[str(time.strftime('%Y-%m-%d %H:%M:%S'))]
                            }

                        d=pd.DataFrame(datafrme)
                        try:
                            d.to_csv(r"C:\FS-File\Security_Events\Delete_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                        except Exception:
                            print("ali")
                        print(f"'{delrule}' has been deleted")
                




            elif masge=="rule state" or masge=="4":
                
                rulerow=[]
                theend=0
                print("if you want to exit enter (exit)")
                while True:
                    dn_n=input("Do you want to enter the rule 'DisplayName' or 'Name': ")
                    dn_n=dn_n.strip().lower()
                    if dn_n=="exit":
                        break
                    if dn_n in ["name","n"]:
                        dn_n="Name"
                        break
                    elif dn_n in ["displayname","d"]:
                        dn_n="DisplayName"
                        break
                    else:
                        print("Enter a valid option.")
                        continue

                delrule="exit"
                if dn_n!="exit":

                    while True:
                        delrule=input(f"Enter the rule {dn_n} or (exit): ")
                        delrule=delrule.strip()
                        if delrule=="exit":
                            break
                        print("The rule is being checking...")
                        time.sleep(1)
                        ree=check_inputs(delrule,2,dn_n)
                        if ree=="1":
                            break
                        print(ree)

                if delrule!="exit":

                    chderu,error=poewrshell(f'$rule = Get-NetFirewallRule -{dn_n} "{delrule}"; $port = Get-NetFirewallPortFilter -AssociatedNetFirewallRule $rule; $app = Get-NetFirewallApplicationFilter -AssociatedNetFirewallRule $rule; [PSCustomObject]@{{ DisplayName=$rule.DisplayName; Name=$rule.Name; Direction=$rule.Direction; Action=$rule.Action; Profile=$rule.Profile; Enabled=$rule.Enabled; Protocol=$port.Protocol; LocalPort=$port.LocalPort; RemotePort=$port.RemotePort; Program=$app.Program }}')      
                    chderu1=list(chderu)
                    chderu2=list(chderu.replace('\n','').replace(' ',''))
                    chderu1=''.join(chderu1)
                    chderu2=''.join(chderu2)
                    print(chderu1)
                    print("component   :value\n")

                if delrule!="exit":

                    while True: 
                        while True:   
                            component=input("Enter the component you want to change (Action, Direction, Enabled,...) or (exit): ").strip()
                            if component.lower()=="exit":
                                break

                            
                            if component.lower() in ["displayname","name","action","direction","enabled","localport","protocol","remoteport","profile","program"]:
                                break
                            else:
                                print("Enter a valid component.")
                                continue

                        if component.lower()=="exit":
                            delrule="exit"
                            break
                        
                        while True:
                            newvalue=input(f"Enter the new value of '{component}' or (exit): ").strip()

                            if newvalue=="exit":
                                break

                            if f"{component.lower()}:{newvalue.lower()}" in chderu2.lower():
                                print(f"'{component}' already has this value")
                                
                                continue

                            if component.lower()=="action":
                                if newvalue.lower() not in ["allow","block"]:
                                    print("Enter a valid action (allow/block).")
                                    
                                    continue

                            if component.lower()=="direction":
                                if newvalue.lower() not in ["inbound","outbound"]:
                                    print("Enter a valid direction (inbound/outbound).")
                                    continue

                            if component.lower()=="enabled":
                                if newvalue.lower() not in ["true","false"]:
                                    print("Enter a valid enabled value (true/false).")
                                    continue

                            if component.lower()=="profile":
                                if newvalue.lower() not in ["domain","private","public"]:
                                    print("Enter a valid profile (domain/private/public).")
                                    continue

                            if component.lower()=="protocol":
                                if newvalue.lower() not in ["tcp","udp","icmp"]:
                                    print("Enter a valid protocol (tcp/udp/icmp).")
                                    continue

                            if component.lower()=="localport" or component.lower()=="remoteport":
                                if not newvalue.isdigit() or int(newvalue)<1 or int(newvalue)>65535:
                                    print("Enter a valid port number (1-65535).")
                                    continue

                            if component.lower()=="program":
                                newvalue=newvalue.replace('"','')
                                if not newvalue.endswith(".exe"):
                                    print("Enter a valid program path (should end with .exe).")
                                    continue

                            if component.lower()=="displayname" or component.lower()=="name":
                                if "#" in newvalue or "|" in newvalue or "%" in newvalue or "~" in newvalue or ";" in newvalue or "&" in newvalue or "\\" in newvalue or "@" in newvalue or "$" in newvalue or ")" in newvalue or "(" in newvalue:
                                    print("Your rule should not contain any of these symbols (# | % ~ ; & \\ @ $ ( ) )")
                                    continue

                                if "-or " in newvalue.lower() or "if " in newvalue.lower() or "try " in newvalue.lower() or "catch " in newvalue.lower():
                                    print("The rule contains strange elements. Rewrite it correctly.")
                                    continue

                                if "new-netfirewallrule"  in newvalue.lower()  or "-displayname"  in newvalue.lower():
                                    print("The rule contains strange elements. Rewrite it correctly.")
                                    continue

                            if component.lower() in ["direction","action","profile","enabled"]:
                                rulerow.append(f'Set-NetFirewallRule -{dn_n} "{delrule}" -{component} {newvalue} ')

                            if component.lower() in ["protocol","localport","remoteport"]:
                                rulerow.append(f'Get-NetFirewallRule -{dn_n} "{delrule}" | Get-NetFirewallPortFilter | Set-NetFirewallPortFilter -{component} {newvalue} ')

                            if component.lower()=="program":
                                rulerow.append(f'Get-NetFirewallRule -{dn_n} "{delrule}" | Get-NetFirewallApplicationFilter | Set-NetFirewallApplicationFilter -{component} "{newvalue}" ')

                            
                            break

                        break
                    
                    if newvalue.lower()=="exit":
                        delrule="exit"
                        break

                if delrule!="exit":
                    
                    rulerow=''.join(rulerow)
                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        settings["modify_rule"]=rulerow
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(settings,f,indent=4)
                    
                    if dn_n=="DisplayName":
                        name_log="null"
                    else:
                        name_log=dn_n
                        dn_n="null"

                    try:
                        s=pd.read_csv(r"C:\FS-File\Security_Events\State_rule_log.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Program_Name":["Program_Name"],
                            "Program_Path":["Program_Path"],
                            "white list":["white list"],
                            "DisplayName":["DisplayName"],
                            "Name":["Name"],
                            "component":["Component"],
                            "newvalue":["NewValue"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-File\Security_Events\State_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Program_Name":["FS System"],
                            "Program_Path":["FS System"],
                            "white list":["NO"],
                            "DisplayName":[dn_n],
                            "Name":[name_log],
                            "Component":[component],
                            "NewValue":[newvalue],
                            "TIME":[str(time.strftime('%Y-%m-%d %H:%M:%S'))]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-File\Security_Events\State_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        print("ali")
                        
                    print("Your rule has been modify")
                    


                    
            elif masge=="black list" or masge=="5":

                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    f_priority=settings["first_priority"]
                    f_priority=list(f_priority)
                    s_priority=settings["second_priority"]
                    s_priority=list(s_priority)

                while True:
                    e_d=input("1. If you want to add items to the black list\n2. If you want to delete items from the black list.\n\n>").strip()

                    if e_d not in ["1","2"]:
                        print("Enter number (1 or 2).")
                        continue


                    elif e_d=="1":
                        while True:
                            rule=[]
                            ex=0
                            DisplayName=''
                            Name=''
                            Action=''
                            Direction=''
                            Enabled=''
                            LocalPort='0'
                            Protocol=''
                            Remoteport='0'
                            Profile=''
                            Program=''
                            while True:
                                aolwea=input("Do you want to enter items with first or second priority (f/s): ").strip()
                                if aolwea not in ["first","f","second","s"]:
                                    print("You need to enter (f or s)")
                                    continue

                                DisplayName=input("Enter DisplayName or (exit): ").strip()

                                if (DisplayName in f_priority) and aolwea in ["first","f"]:
                                    print("This item is alridy exist")
                                    continue

                                if DisplayName=="exit":
                                    ex=1
                                    break
                                if not DisplayName:
                                    break
                                res=check_inputs(DisplayName,1)
                                if res=="1":
                                    rule.append(DisplayName)
                                    break
                                print(res)
                                continue

                            if ex==0:
                                while True:

                                    Name=input("Enter Name or (exit): ").strip()
                                    if (Name in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if Name=="exit":
                                        ex=1
                                        break
                                    if not Name:
                                        break
                                    res=check_inputs(Name,1)
                                    if res=="1":
                                        rule.append(Name)
                                        break
                                    print(res)
                                    continue
                            #check if it works

                            if ex==0:
                                while True:
                                    Action=input("Enter Action or (exit): ").strip()
                                    if (Action in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if Action=="exit":
                                        ex=1
                                        break
                                    if not Action:
                                        break
                                    if Action.lower() not in ["allow","block"]:
                                        print("Enter a valid action (allow/block).")
                                        continue
                                    else:
                                        rule.append(Action)
                                        break


                            if ex==0:
                                while True:
                                    Direction=input("Enter Direction or (exit): ").strip()
                                    if (Direction in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if Direction=="exit":
                                        ex=1
                                        break
                                    if not Direction:
                                        break
                                    if Direction.lower() not in ["inbound","outbound"]:
                                        print("Enter a valid direction (inbound/outbound).")
                                        continue
                                    else:
                                        rule.append(Direction)
                                        break


                            if ex==0:
                                while True:
                                    Enabled=input("Enter Enabled or (exit): ").strip()
                                    if (Enabled in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if Enabled=="exit":
                                        ex=1
                                        break
                                    if not Enabled:
                                        break
                                    if Enabled.lower() not in ["true","false"]:
                                        print("Enter a valid enabled value (true/false).")
                                        continue
                                    else:
                                        rule.append(Enabled)
                                        break

                            if ex==0:
                                #check this in futuer
                                while True:
                                    Profile=input("Enter Profile or (exit): ").strip()
                                    if (Profile in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if Profile=="exit":
                                        ex=1
                                        break
                                    if not Profile:
                                        break
                                    if Profile.lower() not in ["domain","private","public"]:
                                        print("Enter a valid profile (domain/private/public).")
                                        continue
                                    else:
                                        rule.append(Profile)
                                        break

                            if ex==0:
                                #put the auther Protocols
                                while True:
                                    Protocol=input("Enter Protocol or (exit): ").strip()
                                    if (Protocol in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if Protocol=="exit":
                                        ex=1
                                        break
                                    if not Protocol:
                                        break
                                    if Protocol.lower() not in ["tcp","udp","icmp"]:
                                        print("Enter a valid protocol (tcp/udp/icmp).")
                                        continue
                                    else:
                                        rule.append(Protocol)
                                        break


                            if ex==0:
                                while True:
                                    LocalPort=input("Enter LocalPort or (exit): ").strip()
                                    if (LocalPort in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if LocalPort=="exit":
                                        ex=1
                                        break
                                    if not LocalPort:
                                        break
                                    if not LocalPort.isdigit() or int(LocalPort)<1 or int(LocalPort)>65535:
                                        print("Enter a valid port number (1-65535).")
                                        continue
                                    else:
                                        rule.append(LocalPort)
                                        break


                            if ex==0:
                                while True:
                                    Remoteport=input("Enter Remoteport or (exit): ").strip()
                                    if (Remoteport in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if Remoteport=="exit":
                                        ex=1
                                        break
                                    if not Remoteport:
                                        break
                                    if not Remoteport.isdigit() or int(Remoteport)<1 or int(Remoteport)>65535:
                                        print("Enter a valid port number (1-65535).")
                                        continue
                                    else:
                                        rule.append(Remoteport)
                                        break


                            if ex==0:
                                while True:
                                    Program=input("Enter Program or (exit): ").strip()
                                    if (Program in f_priority) and aolwea in ["first","f"]:
                                            print("This item is alridy exist")
                                            continue
                                    if Program=="exit":
                                        ex=1
                                        break
                                    if not Program:
                                        break
                                    Program=Program.replace('"','')
                                    if not Program.endswith(".exe"):
                                        print("Enter a valid program path (should end with .exe).")
                                        continue
                                    if '"' in Program or "'" in Program:
                                        print("Enter a valid program path (without ' or \").")
                                        continue
                                    else:
                                        rule.append(Program)
                                        break


                            if ex==0:
                                if len(rule)==1 and aolwea in ["second","s"]:
                                    print("You must enter more than one item")
                                    continue

                                if len(rule)==0:
                                    print("You must enter an item")
                                    continue
                                
                                if any(set(rule)==set(x) for x in s_priority) and aolwea in ["second","s"]:
                                    print("Those itmes are alridy exist")
                                    continue
                                else:
                                    break
                            else:
                                break



                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            f_priority=settings["first_priority"]
                            f_priority=list(f_priority)
                            s_priority=settings["second_priority"]
                            s_priority=list(s_priority)

                            if aolwea in ["second","s"]:
                                s_priority.append(rule)

                            else:
                                for i in range(len(rule)):
                                    f_priority.append(rule[i])

                            settings["first_priority"]=f_priority
                            settings["second_priority"]=s_priority

                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)


                    elif e_d=="2":
                        while True:
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                f_priority=settings["first_priority"]
                                f_priority=list(f_priority)
                                s_priority=settings["second_priority"]
                                s_priority=list(s_priority)

                            d_item=input("1. First priority\n2. Second priority")

                            if d_item not in ["1","First priority","2","Second priority"]:
                                print("You must enter one of these choses.")
                                continue

                            elif d_item in ["1","First priority"]:
                                while True:
                                    print(f"First priority items:  {f_priority}\n\n")
                                    dfp=input("Enter one item to delete or exit: ").strip()

                                    if dfp=="exit":
                                        break
                                    try:
                                        f_priority.remove(dfp)
                                        print(f"Item '{dfp}' delete succfuly.")
                                        settings["first_priority"]=f_priority
                            
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)

                                    except Exception:
                                        print(f"Item '{dfp}' dose not exist.")



                            elif d_item in ["2","Second priority"]:
                                while True:
                                    print("Second priority items:\n")
                                    m=0
                                    for i in s_priority:
                                        m+=1
                                        print(f"{m}: {i}")

                                    dfp=input("\n\nEnter the number of the list of items to delete or exit: ").strip()

                                    if dfp=="exit":
                                        break

                                    if not dfp.startswith(["0","1","2","3","4","5","6","7","8","9"]):
                                        print("Enter a number or exit.")
                                        continue
                                    
                                    dfp=int(dfp)
                                    if dfp<=m and dfp>0:
                                        s_priority.pop(dfp-1)
                                        print(f"List number {dfp} delete succfuly.")

                                        settings["second_priority"]=s_priority
                            
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4)
                                    else:
                                        print(f"List number {dfp} dose not exist")



            elif masge=="white list" or masge=="6":
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
                                    print("It is already in the white list.")
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
                                    print("It is not in the white list") 
                                    continue
                                s.remove(programe+propath)
                                data["white list"]=s
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(data,f,indent=4)
                        print(f"{programe} has been removed from the white list")
                    else:
                        print("You must enter 'add' or 'delete'")
                        continue
            




            elif masge=="settings" or masge=="7":
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)

                    print("Your Email: "+settings["email"]+"\n")
                    days_map = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
                    current_days = settings.get("work_days", [0,1,2,3,4])
                    current_days_str = ", ".join([days_map[d] for d in current_days])

                    print(f"Work Hours: {settings.get('work_start',8)}:00 → {settings.get('work_end',18)}:00")
                    print(f"Work Days : {current_days_str}\n")
                    print("\nOptions: 'email' | 'workhours' | 'workdays' | '' | exit.")

                    while True:
                        newstt = input("Enter your options: ").strip().lower()
                        if newstt.lower()=="exit":
                            break
                        elif newstt.lower()=="email":
                            while True:
                                emai=input("Enter your new Email Address: ")
                                if "@gmail.com" in emai :
                                    emai=emai.strip()
                                    settings["email"]=emai
                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                        json.dump(settings,f,indent=4)
                                        break
                                else:
                                    print("Please enter a valid email address.")
                                    continue
                            print("Email updated successfully.")
                            

                        elif newstt == "workhours":
                            while True:
                                try:
                                    ws = input("Enter work start hour (0-23): ").strip()
                                    we = input("Enter work end hour (0-23): ").strip()
                                    ws, we = int(ws), int(we)
                                    if not (0 <= ws <= 23 and 0 <= we <= 23):
                                        print("Hours must be between 0 and 23.")
                                        continue
                                    if ws >= we:
                                        print("Start hour must be less than end hour.")
                                        continue
                                    break
                                except ValueError:
                                    print("Enter a valid number.")
                                    continue

                            with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                settings = json.load(f)
                            settings["work_start"] = ws
                            settings["work_end"]   = we
                            with open(r'C:\FS-File\settings.json', 'w', encoding='utf-8') as f:
                                json.dump(settings, f, indent=4)
                            print(f"Work hours updated: {ws}:00 → {we}:00")



                        elif newstt == "workdays":
                            print("Days: 0=Mon  1=Tue  2=Wed  3=Thu  4=Fri  5=Sat  6=Sun")
                            print("Example: to set Mon-Thu enter:  0 1 2 3\n")
                            while True:
                                try:
                                    raw = input("Enter work days (space-separated): ").strip()
                                    days = [int(d) for d in raw.split()]
                                    if not days:
                                        print("Enter at least one day.")
                                        continue
                                    if any(d < 0 or d > 6 for d in days):
                                        print("Days must be between 0 and 6.")
                                        continue
                                    # إزالة التكرار مع الحفاظ على الترتيب
                                    days = sorted(list(set(days)))
                                    break
                                except ValueError:
                                    print("Enter numbers only.")
                                    continue

                            days_map = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",
                                        4:"Fri",5:"Sat",6:"Sun"}
                            days_str = ", ".join([days_map[d] for d in days])

                            with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                settings = json.load(f)
                            settings["work_days"] = days
                            with open(r'C:\FS-File\settings.json', 'w', encoding='utf-8') as f:
                                json.dump(settings, f, indent=4)
                            print(f"Work days updated: {days_str}")

                        else:
                            print("Enter a valid option.")
                            continue
            


            elif masge=="csv" or masge=="8":
                while True:
                    ip_s=input("Enter Server IP address: ")
                    ip_s=ip_s.strip()
                    
                    row=[]
                    chnum=["1","2","3","4","5","6","7","8","9","0","."] 
                    for cnum in ip_s:
                        if cnum not in chnum:
                            cnum="block"
                            break
                    if cnum=="block":
                        print("Invalid IP address entered.")
                        continue

                    if ip_s.endswith(".") or ip_s.startswith("."):
                        print("Invalid IP address entered.")
                        continue
                    
                    if "." not in ip_s:
                        print("Invalid IP address entered.")
                        continue

                    for i in ip_s:
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
                    settings["IP-S"] =ip_s
                    
                    json.dump(settings, f, indent=4)

                print("preparing to send the CSV file to the server...")
                print("You will receive an email when the file is sent successfully.\n")

    except  Exception:
        continue
        