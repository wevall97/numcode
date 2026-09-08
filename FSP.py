import time
import subprocess as su
import socket as sk
import threading as th
import json
import fireSett as fs
import smtplib
from email.message import EmailMessage
import os
import imaplib
import email as email1
import uuid
import random
import re
import pythoncom
import wmi
import psutil
from winotify import Notification
import winsound
from advanced_risk_engine import (
    AdvancedRiskEngine,
    get_process_role,
    start_baseline_updater
)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# check "block=1" اتاكد اناها شغاله حرفيا 
# check all code
# serish erorr: when i delete a rule without using the system  "aof.py" send to the server "delhac" but nothing alse hapen
# انقل كل شي جديد اضفته في نظام الفردي لي النظام الكامل
#COPY
##############################################################################
ta=r'''$rules = Get-NetFirewallRule
$ports = Get-NetFirewallPortFilter | Group-Object InstanceID -AsHashTable
$apps  = Get-NetFirewallApplicationFilter | Group-Object InstanceID -AsHashTable
$addrs = Get-NetFirewallAddressFilter | Group-Object InstanceID -AsHashTable

function Get-IPScope($ip) {
    if ($null -eq $ip -or $ip -eq "Any" -or $ip -eq "*") {
        return "Any"
    }
    if ($ip -match "127\.0\.0\.1" -or $ip -match "::1") {
        return "Localhost"
    }
    if ($ip -match "^192\.168\." -or
        $ip -match "^10\." -or
        $ip -match "^172\.(1[6-9]|2[0-9]|3[0-1])\.") {
        return "Local Network"
    }
    if ($ip -match "LocalSubnet") {
        return "Local Network"
    }
    if ($ip -match "DNS" -or $ip -match "DHCP" -or $ip -match "DefaultGateway") {
        return "Trusted IP"
    }
    return "Public IP"
}

($rules | ForEach-Object {
    $p  = $ports[$_.InstanceID]
    $a  = $apps[$_.InstanceID]
    $ad = $addrs[$_.InstanceID]

    $realPath = if ($a.Program) {
        [Environment]::ExpandEnvironmentVariables($a.Program)
    } else {
        $null
    }

    $scope = Get-IPScope $ad.RemoteAddress

    [PSCustomObject]@{
        DisplayName = $_.DisplayName
        Name        = $_.Name
        Direction   = $_.Direction.ToString()
        Action      = $_.Action.ToString()
        Profile     = $_.Profile.ToString()
        Enabled     = $_.Enabled.ToString()
        Protocol    = $p.Protocol
        LocalPort   = $p.LocalPort
        RemotePort  = $p.RemotePort
        Program     = $realPath
        IPScope     = $scope
    }
}) | ConvertTo-Json -Depth 3 | Out-File "C:\FS-File\firewall_light.json" -Encoding utf8
'''




ta1=r'''$rules = Get-NetFirewallRule
$ports = Get-NetFirewallPortFilter | Group-Object InstanceID -AsHashTable
$apps  = Get-NetFirewallApplicationFilter | Group-Object InstanceID -AsHashTable
$addrs = Get-NetFirewallAddressFilter | Group-Object InstanceID -AsHashTable

function Get-IPScope($ip) {
    if ($null -eq $ip -or $ip -eq "Any" -or $ip -eq "*") {
        return "Any"
    }
    if ($ip -match "127\.0\.0\.1" -or $ip -match "::1") {
        return "Localhost"
    }
    if ($ip -match "^192\.168\." -or
        $ip -match "^10\." -or
        $ip -match "^172\.(1[6-9]|2[0-9]|3[0-1])\.") {
        return "Local Network"
    }
    if ($ip -match "LocalSubnet") {
        return "Local Network"
    }
    if ($ip -match "DNS" -or $ip -match "DHCP" -or $ip -match "DefaultGateway") {
        return "Trusted IP"
    }
    return "Public IP"
}

($rules | ForEach-Object {
    $p  = $ports[$_.InstanceID]
    $a  = $apps[$_.InstanceID]
    $ad = $addrs[$_.InstanceID]

    $realPath = if ($a.Program) {
        [Environment]::ExpandEnvironmentVariables($a.Program)
    } else {
        $null
    }

    $scope = Get-IPScope $ad.RemoteAddress

    [PSCustomObject]@{
        DisplayName = $_.DisplayName
        Name        = $_.Name
        Direction   = $_.Direction.ToString()
        Action      = $_.Action.ToString()
        Profile     = $_.Profile.ToString()
        Enabled     = $_.Enabled.ToString()
        Protocol    = $p.Protocol
        LocalPort   = $p.LocalPort
        RemotePort  = $p.RemotePort
        Program     = $realPath
        IPScope     = $scope
    }
}) | ConvertTo-Json -Depth 3 | Out-File "C:\FS-File\firewallcopy.json" -Encoding utf8
'''
##############################################################################

def email_alr():
    toast = Notification(
    app_id="FS Notification",
    title="Offline Alert",
    msg="Sending email alert and doing your order are stop ,because you are offline right now\n Check your internet connction.")
    
    toast.show()
    for _ in range(2):
        winsound.Beep(2000, 300)  
        time.sleep(0.2)


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


def online_IP():
    global arl,drl,mrl
    while True:
        try:
            try:
                server=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
                server.connect(("1.1.1.1",80))
                ips=server.getsockname()[0]
                server.close()
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)

                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            settings["IP-U"] =ips
                            json.dump(settings,f,indent=4) 
                break
            except Exception:
                
                server=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
                server.connect(("8.8.8.8",443))
                ips=server.getsockname()[0]
                server.close()

                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)

                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            settings["IP-U"] =ips
                            json.dump(settings,f,indent=4) 
                break
        except Exception:
            time.sleep(5)
            continue

    reconn_server()
    time.sleep(1)
    ars(arl)
    drs(drl)
    mrs(mrl)




def reconn_server():
    global c
    MAX_RETRIES = 30   # حد أقصى للمحاولات
    RETRY_DELAY = 5    # ثوانٍ بين كل محاولة
    retry_count = 0


    while True:
        try:
            c = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            c.settimeout(10)  # ← timeout 10 ثوانٍ
            c.connect((ip, 9999))
            chck = c.recv(1024).decode('utf-8')
            if chck == '1':
                c.sendall("add".encode())
            break
        except Exception as e:
            retry_count += 1
            if retry_count >= MAX_RETRIES:
                exit(1)
            time.sleep(RETRY_DELAY)


def ars(a=list):
    l=len(a)
    if l !=0:
        l=l/16
        for _ in range(l):
            add_rule_logs(a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0))
            time.sleep(5)
    


def drs(a=list):
    l=len(a)
    if l !=0:
        l=l/8
        for _ in range(l):
            delete_rule_logs(a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0))
            time.sleep(5)


def mrs(a=list):
    l=len(a)
    if l !=0:
        l=l/10
        for _ in range(l):
            modefiy_rule_logs(a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0),a.pop(0))
            time.sleep(5)


#COPY
##############################################################################
def email_notif(PROGRAM_NAME,PROGRAM_PATH,RULE_ACTION,ACTION_TAKEN,email_rvs):
    
    notif_mas=f'''
Hello,

A suspicious firewall rule modification was detected on your device.

Program Name: {PROGRAM_NAME}
Program Path: {PROGRAM_PATH}
Detected Action: {RULE_ACTION}


Automatic Response Taken:
{ACTION_TAKEN}

If this activity is legitimate, please review the program and your firewall configuration.

Security System:
FS System
'''
    try:
        msg= EmailMessage()
        msg["Subject"]=f"Security Alert - ID({str(uuid.uuid4())[:8]})"
        msg["From"]="aofnotification@gmail.com"
        msg["To"]=email_rvs
        msg.set_content(notif_mas)
        email="aofnotification@gmail.com"
        password="oqgspkawnyeftyjw"
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(email,password)
            smtp.send_message(msg)  
    except Exception:
        email_alr()
        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
            data = json.load(f)

        if data["IP-U"]!="0":

            th.Thread(target=online_IP).start()

            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                data = json.load(f)
                data["IP-U"]="0"
                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                    json.dump(data,f,indent=4)

#EDIT
##############################################################################
arl=[]
drl=[]
mrl=[]
def add_rule_logs(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,T,white_list):
    try:
        # امشي اضيف باقي ملفات الcsv الموجوده في النسخه المنفصله

        # 
        c.sendall("hackAdd".encode())
        c.recv(1024).decode()
        c.sendall(pro_name.encode())
        c.recv(1024).decode()
        c.sendall(pro_path.encode())
        c.recv(1024).decode()
        c.sendall(ip_user.encode())
        c.recv(1024).decode()
        c.sendall(mac_user.encode())
        c.recv(1024).decode()
        c.sendall(DisplayName.encode())
        c.recv(1024).decode()
        c.sendall(Name.encode())
        c.recv(1024).decode()
        c.sendall(Direction.encode())
        c.recv(1024).decode()
        c.sendall(Action.encode())
        c.recv(1024).decode()
        c.sendall(Profile.encode())
        c.recv(1024).decode()
        c.sendall(Enabled.encode())
        c.recv(1024).decode()
        c.sendall(Protocol.encode())
        c.recv(1024).decode()
        c.sendall(LocalPort.encode())
        c.recv(1024).decode()
        c.sendall(RemotePort.encode())
        c.recv(1024).decode()
        c.sendall(Program.encode())
        c.recv(1024).decode()
        c.sendall(T.encode())
        c.recv(1024).decode()  
        c.sendall(white_list.encode())
        check1=c.recv(1024).decode()
        check1=check1.replace("1","")
        check1=check1.strip()
    except Exception:
        email_alr()
        arl.append(pro_name)
        arl.append(pro_path)
        arl.append(ip_user)
        arl.append(mac_user)
        arl.append(DisplayName)
        arl.append(Name)
        arl.append(Direction)
        arl.append(Action)
        arl.append(Profile)
        arl.append(Enabled)
        arl.append(Protocol)
        arl.append(LocalPort)
        arl.append(RemotePort)
        arl.append(Program)
        arl.append(T)
        arl.append(white_list)


        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
            data = json.load(f)

        if data["IP-U"]!="0":

            th.Thread(target=online_IP).start()

            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                data = json.load(f)
                data["IP-U"]="0"
                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                    json.dump(data,f,indent=4)

##############################################################################

#EDIT
##############################################################################
def delete_rule_logs(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,T,white_list):
    try:
        c.sendall("hackDel".encode())
        c.recv(1024).decode()
        c.sendall(pro_name.encode())
        c.recv(1024).decode()
        c.sendall(pro_path.encode())
        c.recv(1024).decode()
        c.sendall(T.encode())
        c.recv(1024).decode()
        c.sendall(ip_user.encode())
        c.recv(1024).decode()
        c.sendall(mac_user.encode())
        c.recv(1024).decode()
        c.sendall(DisplayName.encode())
        c.recv(1024).decode()
        c.sendall(Name.encode())
        c.recv(1024).decode()
        c.sendall(white_list.encode())
        check1=c.recv(1024).decode()
        check1=check1.replace("1","")
        check1=check1.strip()
    except Exception:
        email_alr()
        drl.append(pro_name)
        drl.append(pro_path)
        drl.append(ip_user)
        drl.append(mac_user)
        drl.append(DisplayName)
        drl.append(Name)
        drl.append(T)
        drl.append(white_list)

        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
            data = json.load(f)

        if data["IP-U"]!="0":

            th.Thread(target=online_IP).start()

            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                data = json.load(f)
                data["IP-U"]="0"
                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                    json.dump(data,f,indent=4)

#EDIT
##############################################################################
def modefiy_rule_logs(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,ii,gema,T,white_list ):
    
    try:
        c.sendall("hackMod".encode())
        c.recv(1024).decode()
        c.sendall(pro_name.encode())
        c.recv(1024).decode()
        c.sendall(pro_path.encode())
        c.recv(1024).decode()
        c.sendall(ip_user.encode())
        c.recv(1024).decode()
        c.sendall(mac_user.encode())
        c.recv(1024).decode()
        c.sendall(DisplayName.encode())
        c.recv(1024).decode()
        c.sendall(Name.encode())
        c.recv(1024).decode()
        c.sendall(ii.encode())
        c.recv(1024).decode()
        c.sendall(gema.encode())
        c.recv(1024).decode()
        c.sendall(T.encode())
        c.recv(1024).decode()
        c.sendall(white_list.encode())
        check1=c.recv(1024).decode()
        check1=check1.replace("1","")
        check1=check1.strip()
    except Exception:
        email_alr()
        mrl.append(pro_name)
        mrl.append(pro_path)
        mrl.append(ip_user)
        mrl.append(mac_user)
        mrl.append(DisplayName)
        mrl.append(Name)
        mrl.append(ii)
        mrl.append(gema)
        mrl.append(T)
        mrl.append(white_list)

        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
            data = json.load(f)

        if data["IP-U"]!="0":

            th.Thread(target=online_IP).start()

            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                data = json.load(f)
                data["IP-U"]="0"
                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                    json.dump(data,f,indent=4)




def black_list():
    # make csv file for it
    # try to get the programe name and path to put it here 
    global block1
    s_p=1
    bl=[]
    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        bl=list(settings["BL_Rule_Check"])
        f_priority=list(settings["first_priority"])
        s_priority=list(settings["second_priority"])
        emai=settings["email"]

        settings["BL_Rule_Check"]=""
        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
            json.dump(settings,f,indent=4)

    for i in range(bl):
        if bl[i] in f_priority:
            block1=1

            s_p=0
            if bl[1]!="":
                poewrshell(f'Remove-NetFirewallRule -Name "{bl[1]}"')
            else:
                poewrshell(f'Remove-NetFirewallRule -DisplayName "{bl[0]}"')

            poewrshell(ta)

            block1=0
            try:
                msg= EmailMessage()
                msg["Subject"]=f"Identity verification - ID({str(uuid.uuid4())[:8]})"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=emai
                msg.set_content(f"After checking the rule:\n\nDisplayName: {bl[0]}\nName: {bl[1]}\n\nThat has been add by the program:\n{bl[10]}\n\nWe found that the rule have items that not allowed to have, so it have been deleted.\n\n\nSecurity System:\nFS System")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
            except Exception:
                email_alr()
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    data = json.load(f)

                if data["IP-U"]!="0":

                    th.Thread(target=online_IP).start()

                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        data = json.load(f)
                        data["IP-U"]="0"
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(data,f,indent=4)

            ms = f'''
The rule that added by:
Program Path: {bl[10]}

Have been deleted because it have an allowed items 
'''
            toast = Notification(app_id="FS Notification",
                                title="Black List Item Alert", msg=ms)
            toast.show()
            for _ in range(2):
                winsound.Beep(2000, 300)
                time.sleep(0.2)

            break

    if s_p==1:
        if any(set(bl)==set(x) for x in s_priority):
            block1=1
            
            if bl[1]!="":
                poewrshell(f'Remove-NetFirewallRule -Name "{bl[1]}"')
            else:
                poewrshell(f'Remove-NetFirewallRule -DisplayName "{bl[0]}"')

            poewrshell(ta)

            block1=0
            try:
                msg= EmailMessage()
                msg["Subject"]=f"Identity verification - ID({str(uuid.uuid4())[:8]})"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=emai
                msg.set_content(f"After checking the rule:\n\nDisplayName: {bl[0]}\nName: {bl[1]}\n\nThat has been add by the program:\n{bl[10]}\n\nWe found that the rule have items that not allowed to have, so it have been deleted.\n\n\nSecurity System:\nFS System")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
            except Exception:
                email_alr()
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    data = json.load(f)

                if data["IP-U"]!="0":

                    th.Thread(target=online_IP).start()

                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        data = json.load(f)
                        data["IP-U"]="0"
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(data,f,indent=4)


            ms = f'''
The rule that added by:
Program Path: {bl[10]}

Have been deleted because it have an allowed items 
'''
            toast = Notification(app_id="FS Notification",
                                title="Black List Item Alert", msg=ms)
            toast.show()
            for _ in range(2):
                winsound.Beep(2000, 300)
                time.sleep(0.2)

##############################################################################

#CHECK
##############################################################################
go=1
pro=1
ere=0
block=1  
trw=1
##############################################################################

#COPY
##############################################################################
risk_engine = AdvancedRiskEngine()
start_baseline_updater(risk_engine)
##############################################################################


#COPY
##############################################################################
pathfile=os.path.exists(r"C:\FS-File\loop.txt")
if pathfile==False:
    with open(r"C:\FS-File\loop.txt","w",encoding='utf-8')as f:
        f.write("")
else:
    with open(r"C:\FS-File\loop.txt","w",encoding='utf-8')as f:
        f.write("")

pathfile=os.path.exists(r"C:\FS-File\loop-2.txt")
if pathfile==False:
    with open(r"C:\FS-File\loop-2.txt","w",encoding='utf-8')as f:
        f.write("")
else:
    with open(r"C:\FS-File\loop-2.txt","w",encoding='utf-8')as f:
        f.write("")

        
pathfile=os.path.exists(r"C:\FS-File\loop-3.txt")
if pathfile==False:
    with open(r"C:\FS-File\loop-3.txt","w",encoding='utf-8')as f:
        f.write("")
else:
    with open(r"C:\FS-File\loop-3.txt","w",encoding='utf-8')as f:
        f.write("")
##############################################################################

#COPY: TO MAKE THE FILE UNEDIT
##############################################################################
with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:

    settings = json.load(f)
 
    chck2=0
##############################################################################

#COPY: PUT IT IN THE TOP
##############################################################################
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
    
    poewrshell(ta)   
##############################################################################

#EDIT
##############################################################################
    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f) 

        if settings["user-state"]=="USER":
            bossemail=settings["bossemail"]
            settings["advance-mode"]="0"
            settings["advance-password"]="0"

        if settings["FWS"]=="":
            settings["FWS"]="null"
            
        if settings["timerF"]=="":
            settings["timerF"]="0"
            
        if settings["Rolue"]!="null":
            settings["Rolue"]="null"
            
        if settings["FWS"]=="off" or settings["FWS"]=="on" or settings["FWS"]=="off-all":
            settings["FWS"]="null"
            
        if settings["timerF"]!="0":
            settings["timerF"]="0"
            
        if settings["timerR"]!=[]:
            settings["timerR"]=[]
            
        if settings["ruleName"]!=[]:
            settings["ruleName"]=[] 
            
        if settings["checkrulename"]!=[]: 
            for aa in settings["checkrulename"]:
                reslt,error=poewrshell(f'Remove-NetFirewallRule -DisplayName "{aa}"')
                if error:
                    poewrshell(f'Remove-NetFirewallRule -Name "{aa}"')
            settings["checkrulename"]=[]
            
        if settings["constan"]!="no":
            settings["constan"]="no"
        
        if settings["deleteR"]!="null":
            settings["deleteR"]="null"

        if settings["modify_rule"]!="null":
            settings["modify_rule"]="null"
        
        if settings["path_proName_PID"]!="":
            settings["path_proName_PID"]=""

        if settings["white list checker"]!="":
            settings["white list checker"]=""
        
        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
            json.dump(settings,f,indent=4)
##############################################################################

#COPY: IF I CAN IMPROVE IT DO IT
##############################################################################
        email_rvs=settings["email"]
        user_state=settings["user-state"]
        mac=settings["MAC"]
        
    FIREWALL_KEYWORDS = [
        'New-NetFirewallRule',
        'Set-NetFirewallRule',
        'Remove-NetFirewallRule',
        'netsh advfirewall firewall add rule',
        'netsh advfirewall firewall set rule',
        'netsh advfirewall firewall delete rule'
    ]

    TARGET_PROCESSES = [
        'powershell.exe',
        'pwsh.exe',  
        'cmd.exe',
        'netsh.exe'
    ]

    def is_firewall_related(cmd_line, process_name):
        if not cmd_line or cmd_line == 'N/A':
            return False
        
        cmd_lower = cmd_line.lower()
        
        for keyword in FIREWALL_KEYWORDS:
            if keyword.lower() in cmd_lower:
                return True
        
        return False

    def is_target_process(process_name):
        
        if not process_name:
            return False
        
        process_lower = process_name.lower()
        
        for target in TARGET_PROCESSES:
            if target.lower() in process_lower:
                return True
        
        return False
    
##############################################################################

#COPY: EDIT
##############################################################################
    def mal_dit():
        global parent_name,chick_vil,ta,ta1,block,ere,pro,go,deleteR
        pythoncom.CoInitialize()   
        try:
            c = wmi.WMI()
            process_watcher = c.Win32_ProcessStartTrace.watch_for()
            
            while True:
                try:
                    event = process_watcher()
                    pid = event.ProcessID
                    name = event.ProcessName
                    
                    processes = c.Win32_Process(ProcessId=pid)
                    
                    if processes:
                        p = processes[0]
                        # exe_path = getattr(p, 'ExecutablePath', 'N/A')
                        cmd_line = getattr(p, 'CommandLine', 'N/A')
                        parent_pid = getattr(p, 'ParentProcessId', None)
                        
                        # parent_info = "N/A"
                        if parent_pid:
                            parent_processes = c.Win32_Process(ProcessId=parent_pid)
                            if parent_processes:
                                parent = parent_processes[0]
                                parent_path = getattr(parent, 'ExecutablePath', 'N/A')
                                parent_name = getattr(parent, 'Name', 'N/A')
                                # parent_cmd = getattr(parent, 'CommandLine', 'N/A')

                                TRUSTED_POWERSHELL_PATHS = [
                                    r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
                                    r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
                                    r"C:\Program Files\PowerShell\7\pwsh.exe"
                                ]

                                if is_target_process(name) and is_firewall_related(cmd_line, name) and parent_name == "powershell.exe":
                                    if parent_path in TRUSTED_POWERSHELL_PATHS:
                                        block = 0
                                    else:
                                        block = 1  # powershell من مسار غير موثوق = مشبوه

                                elif is_target_process(name) and is_firewall_related(cmd_line, name) and parent_name!="FSP.exe":
                                    path = f'''(Get-AuthenticodeSignature "{parent_path}").Status'''
                                    chick_vil, error = poewrshell(path)
                                    chick_vil=list(chick_vil)
                                    chick_vil=''.join(chick_vil)
                                    

                                    # ── جديد: احصل على صلاحيات العملية فوراً قبل أن تنتهي
                                    process_role = get_process_role(parent_pid)

                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        parent_pid=str(parent_pid)
                                        s=parent_pid+"+"+parent_name+"$"+parent_path
                                        settings["path_proName_PID"]=s
                                        s=parent_name+parent_path
                                        settings["white list checker"]=s
                                        # ── جديد: احفظ الصلاحيات في الإعدادات
                                        settings["user_role"]=process_role
                                        with open(r"C:\FS-File\settings.json", 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4)

                except Exception as e:
                    time.sleep(1)

        finally:
            pythoncom.CoUninitialize()


    th.Thread(target=mal_dit).start()
##############################################################################

#COPY
##############################################################################
    while True:
        try:
            
##############################################################################
 
#COPY: IN TOP
# ##############################################################################           
                     
            pathfile=os.path.exists(r"C:\FS-File\email_ids.txt")
            if pathfile==False:
                with open(r"C:\FS-File\email_ids.txt","w",encoding='utf-8')as f:
                    f.write("")
##############################################################################

#COPY:IN TOP
# ##############################################################################   
            a,error=poewrshell('Get-NetFirewallProfile | Select-Object Enabled')
            a=list(a)
            a=''.join(a)

            # a=a.stdout  
            if "False" in a: 
                poewrshell(r"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")

##############################################################################

#COPY
##############################################################################
            try:
                result, error = poewrshell("Get-NetAdapter | Select-Object MacAddress")
                result = ''.join(list(result))
                mac_list = [lmac.strip() for lmac in result.splitlines() if "-" in lmac]
                mac = mac_list[-1] if mac_list else "null"
            except Exception:
                mac = "null"
                
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
##############################################################################

#DELETE
##############################################################################
            #conn with the praimry conn   
            MAX_RETRIES = 30   # حد أقصى للمحاولات
            RETRY_DELAY = 5    # ثوانٍ بين كل محاولة
            retry_count = 0


            while True:
                try:
                    c = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                    c.settimeout(10)  # ← timeout 10 ثوانٍ
                    c.connect((ip, 9999))
                    chck = c.recv(1024).decode('utf-8')
                    if chck == '1':
                        c.sendall("add".encode())
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count >= MAX_RETRIES:
                        exit(1)
                    time.sleep(RETRY_DELAY)
                    
##############################################################################    
                        
            #return D:\FS-File\settings.json to the defult
            
#COPY: IN TOP
##############################################################################
            ps_script = """
$TARGET_IDS = @(2002, 2004, 2005, 2006, 2097, 2099, 2052, 2082)

$watcher = New-Object System.Diagnostics.Eventing.Reader.EventLogWatcher(
    'Microsoft-Windows-Windows Firewall With Advanced Security/Firewall'
)

Register-ObjectEvent $watcher EventRecordWritten -Action {
    $ids = @(2002, 2004, 2005, 2006, 2097, 2099, 2052, 2082)
    $id = $Event.SourceEventArgs.EventRecord.Id
    if ($ids -contains $id) {
        [Console]::WriteLine($id)
        [Console]::Out.Flush()
    }
}

$watcher.Enabled = $true
while ($true) { Start-Sleep -Seconds 10 }
"""
##############################################################################

#COPY
##############################################################################

            pp = su.Popen(
                ["powershell", "-NoProfile", "-Command", ps_script],
                stdout=su.PIPE,
                stderr=su.PIPE,
                text=True,
                bufsize=1)
##############################################################################

            
#EDIT: CHECK IF I NEED SOMTHING
##############################################################################
            def ckeck_email():
                
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    ips=settings["IP-U"]
                global status,from_,timer,mac,bossemail,ta,ta1,block,ere,pro,go,deleteR
                while True:
                    IMAP_SERVER = "imap.gmail.com"
                    EMAIL_ACCOUNT = "aofnotification@gmail.com"
                    EMAIL_PASSWORD = "oqgspkawnyeftyjw"
                    with open(r"C:\FS-File\email_ids.txt", "r", encoding='utf-8') as f:
                        sent_ids=f.read().strip()
                        
                    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
                    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
                    mail.select("inbox")

                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        bossemail=settings["bossemail"] 
                    status, messages = mail.search(None, f'(FROM "{bossemail}")')  

                    for num in messages[0].split():
                        status, data = mail.fetch(num, '(RFC822)')
                        msg1 = email1.message_from_bytes(data[0][1])
                        in_reply_to = msg1.get("In-Reply-To")
                        
                        from_ = msg1.get("From")
                        
                        if in_reply_to and in_reply_to.strip() in sent_ids:
                            
                            if msg1.is_multipart():
                                for part in msg1.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        firest=body.strip().splitlines()[0]
                                        firest=str(firest.strip()).lower()
                                    
                                        sent_ids=sent_ids.replace(in_reply_to,"")
                                        
                                        with open(r"C:\FS-File\email_ids.txt", "w",encoding='utf-8') as f:
                                            sent_id="".join(map(str,sent_ids))
                                            f.write(sent_id)
                                        with open(r"C:\FS-File\email_ids.txt", "r",encoding='utf-8') as f:
                                            sent_ids=f.readlines()
                                            for line in sent_ids:
                                                if line.startswith("|") or line.startswith("#") or line.startswith("%") or line.startswith("&"):
                                                    l1=line
                                                    l2=line[:1]
                                                    l=line[1:]
                                                    if "~" in l:
                                                        chck1=l.index("~")
                                                        l=l[:chck1]
                                                        l1=l
                                                        with open(r"C:\FS-File\email_ids.txt", "r",encoding='utf-8') as f:
                                                            sent_ids=f.read()
                                                            sent_ids=sent_ids.replace("#","")  
                                                            
                                                            
                                                        with open(r"C:\FS-File\email_ids.txt", "w",encoding='utf-8') as f:
                                                            sent_id="".join(map(str,sent_ids))
                                                            f.write(sent_id)  
                                                    
                                                        
                                        with open(r"C:\FS-File\email_ids.txt", "r",encoding='utf-8') as f:
                                            sent_ids=f.read()
                                            
                                            sent_ids=sent_ids.replace(l1,"")  
                                            
                                        with open(r"C:\FS-File\email_ids.txt", "w",encoding='utf-8') as f:
                                            sent_id="".join(map(str,sent_ids))
                                            f.write(sent_id)     
###########################################################################
#delete                                 
                                        # ofl=="0"
                                        # if firest=="approved" and l2=="%": 
                                            
                                        #     ran = random.randint(100000, 999999)
                                        #     ran=str(ran)
                                        #     with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        #         settings = json.load(f)
                                        #         settings["advance-password"]=ran
                                        #         with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                        #             json.dump(settings,f,indent=4)
                                        #     msg= EmailMessage()
                                        #     msg["Subject"]=f"Identity verification - ID({str(uuid.uuid4())[:8]})"
                                        #     msg["From"]="aofnotification@gmail.com"
                                        #     msg["To"]=email_rvs
                                        #     msg.set_content(f"This is your password to verify your identity and connect to the server:\n{ran}\nIf you did not request this password, please check your account security immediately.\n\n\nSecurity System:\nFS System")
                                        #     email="aofnotification@gmail.com"
                                        #     password="oqgspkawnyeftyjw"
                                        #     with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                        #         smtp.login(email,password)
                                        #         smtp.send_message(msg)   
                                            
                                        # elif firest!="approved"  and l2=="%": 
                                        #     with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        #         settings = json.load(f)
                                        #         settings["advance-mode"]="0"
                                        #         with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                        #             json.dump(settings,f,indent=4)
                                        #     msg= EmailMessage()
                                        #     msg["Subject"]=f"Request rejection - ID({str(uuid.uuid4())[:8]})"
                                        #     msg["From"]="aofnotification@gmail.com"
                                        #     msg["To"]=email_rvs
                                        #     msg.set_content(f"The official did not approve your request.\nIf you have any questions, please contact support.\n\n\nSecurity System:\nFS System")
                                        #     email="aofnotification@gmail.com"
                                        #     password="oqgspkawnyeftyjw"
                                        #     with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                        #         smtp.login(email,password)
                                        #         smtp.send_message(msg)
####################################################################################

                                        if firest=="approved" and l2=="&":
                                            
                                            rowo=[]
                                            rowo1=[]
                                            for y in l:
                                                if y=="*":
                                                    break
                                                rowo.append(y)
                                            rowo=''.join(rowo)
                                            l=l[len(rowo)+1:]

                                            for y in l:
                                                if y=="^":
                                                    break
                                                rowo1.append(y)
                                            rowo1=''.join(rowo1)
                                            l=l[len(rowo1)+1:]

                                            z=l.index("wevall")
                                            z+=6
                                            component=l[:z]
                                            component=component.replace("wevall","")
                                            newvalue=l[z:]

                                            
                                            # rulem 
                                            check1="tt"
                                            try: 
                                                on="rua"
                                                c.sendall(on.encode())
                                                c.recv(1024).decode()
                                                c.sendall(rowo1.encode())
                                                c.recv(1024).decode()
                                                c.sendall(component.encode())
                                                c.recv(1024).decode()
                                                c.sendall(newvalue.encode())
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
                                            except Exception:
                                                ofl=on_off_line()

                                            if check1=="action rule log.csv" or check1=="action rule log.csv1":
                                                try:
                                                    msg= EmailMessage()
                                                    msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                                    msg["From"]="aofnotification@gmail.com"
                                                    msg["To"]=email_rvs
                                                    msg.set_content(f"Someone is reading the 'State_rule.csv' file.\n you should check the server's status to see if it has been compromised or not.")
                                                    email="aofnotification@gmail.com"
                                                    password="oqgspkawnyeftyjw"
                                                    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                        smtp.login(email,password)
                                                        smtp.send_message(msg)
                                                except Exception:
                                                    email_alr()
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                            
                                                    if data["IP-U"]!="0":
                            
                                                        th.Thread(target=online_IP).start()
                            
                                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                            data = json.load(f)
                                                            data["IP-U"]="0"
                                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                                json.dump(data,f,indent=4)

                                            try:         
                                                msg= EmailMessage()
                                                msg["Subject"]=f"Request approval - ID({str(uuid.uuid4())[:8]})"
                                                msg["From"]="aofnotification@gmail.com"
                                                msg["To"]=email_rvs
                                                msg.set_content("The base state was successfully changed.\n\n\nSecurity System:\nFS System")
                                                email="aofnotification@gmail.com"
                                                password="oqgspkawnyeftyjw"
                                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                    smtp.login(email,password)
                                                    smtp.send_message(msg)
                                            except Exception:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)

                                            if ofl !="null":
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    settings = json.load(f)
                                                    settings["modify_rule"]=rowo
                                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                        json.dump(settings,f,indent=4)
                                            else:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)

                                                    
                                        elif firest!="approved"  and l2=="&":
                                            try:
                                                msg= EmailMessage()
                                                msg["Subject"]=f"Request rejection - ID({str(uuid.uuid4())[:8]})"
                                                msg["From"]="aofnotification@gmail.com"
                                                msg["To"]=email_rvs
                                                msg.set_content("The official did not approve your request.\nIf you have any questions, please contact support.\n\n\nSecurity System:\nFS System")
                                                email="aofnotification@gmail.com"
                                                password="oqgspkawnyeftyjw"
                                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                    smtp.login(email,password)
                                                    smtp.send_message(msg)
                                            except Exception:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)

                                        if firest=="approved" and l2=="|":

                                            z=l.index("wevall")
                                            z=z+6
                                            l=l.replace(l[z:],"")
                                            l=l.replace("wevall","")
                                            #ruled
                                            check1="tt"
                                            try:
                                                on="del"
                                                c.sendall(on.encode())
                                                c.recv(1024).decode()
                                                c.sendall(l.encode())
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
                                            except Exception:
                                                ofl=on_off_line()
                                            if check1=="delete rule log.csv" or check1=="delete rule log.csv1":
                                                try:
                                                    msg= EmailMessage()
                                                    msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                                    msg["From"]="aofnotification@gmail.com"
                                                    msg["To"]=email_rvs
                                                    msg.set_content(f"Someone is reading the 'Delete_rule.csv' file.\n you should check the server's status to see if it has been compromised or not.")
                                                    email="aofnotification@gmail.com"
                                                    password="oqgspkawnyeftyjw"
                                                    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                        smtp.login(email,password)
                                                        smtp.send_message(msg)
                                                except Exception:
                                                    email_alr()
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                            
                                                    if data["IP-U"]!="0":
                            
                                                        th.Thread(target=online_IP).start()
                            
                                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                            data = json.load(f)
                                                            data["IP-U"]="0"
                                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                                json.dump(data,f,indent=4)

                                            try:        
                                                msg= EmailMessage()
                                                msg["Subject"]=f"Request approva - ID({str(uuid.uuid4())[:8]})"
                                                msg["From"]="aofnotification@gmail.com"
                                                msg["To"]=email_rvs
                                                msg.set_content("The rule was successfully deleted.\n\n\nSecurity System:\nFS System")
                                                email="aofnotification@gmail.com"
                                                password="oqgspkawnyeftyjw"
                                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                    smtp.login(email,password)
                                                    smtp.send_message(msg)
                                            except Exception:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)


                                            if ofl !="null":

                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    settings = json.load(f)
                                                    settings["deleteR"]=l
                                                    
                                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                        json.dump(settings,f,indent=4)
                                            else:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)

                                        elif firest!="approved"  and l2=="|":
                                            try:
                                                msg= EmailMessage()
                                                msg["Subject"]=f"Request rejection - ID({str(uuid.uuid4())[:8]})"
                                                msg["From"]="aofnotification@gmail.com"
                                                msg["To"]=email_rvs
                                                msg.set_content("The official did not approve your request.\nIf you have any questions, please contact support.\n\n\nSecurity System:\nFS System")
                                                email="aofnotification@gmail.com"
                                                password="oqgspkawnyeftyjw"
                                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                    smtp.login(email,password)
                                                    smtp.send_message(msg)
                                            except Exception:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)


                                        if firest=="approved"  and l2=="#":
                                            
                                            l=l.replace("#","")
                                    

                                            with open(r"C:\FS-File\email_ids.txt", "r",encoding='utf-8') as f:
                                                sent_ids=f.readlines()
                                                for line in sent_ids:
                                                    if line.startswith("~"):
                                                        l1=line
                                                        
                                                        timer=line[1:]
                                                        
                                                        
                                            with open(r"C:\FS-File\email_ids.txt", "r",encoding='utf-8') as f:
                                                sent_ids=f.read()
                                                sent_ids=sent_ids.replace(l1,"")  
                                                
                                            with open(r"C:\FS-File\email_ids.txt", "w",encoding='utf-8') as f:
                                                sent_id="".join(map(str,sent_ids))
                                                f.write(sent_id) 
                                            
                                            row1=[]
                                            row = re.split(" ",l)
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
                                            if rulename.startswith(("'",'"')) and rulename.endswith(("'",'"')):
                                                rulename=rulename[1:-1]
                                            # rulea
                                            check1="tt"
                                            try:
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
                                                c.sendall(l.encode())
                                                c.recv(1024).decode()
                                                c.sendall("no".encode())
                                                c.recv(1024).decode()
                                                c.sendall(mac.encode())
                                                check1=c.recv(1024).decode()
                                                check1=check1.replace("1","")
                                                check1=check1.strip()
                                            except Exception:
                                                ofl=on_off_line()

                                            if check1=="add rule log.csv" or check1=="add rule log.csv1":
                                                try:
                                                    msg= EmailMessage()
                                                    msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                                    msg["From"]="aofnotification@gmail.com"
                                                    msg["To"]=email_rvs
                                                    msg.set_content(f"Someone is reading the 'Add_rule_log.csv' file.\n you should check the server's status to see if it has been compromised or not.")
                                                    email="aofnotification@gmail.com"
                                                    password="oqgspkawnyeftyjw"
                                                    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                        smtp.login(email,password)
                                                        smtp.send_message(msg)
                                                except Exception:
                                                    email_alr()
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                            
                                                    if data["IP-U"]!="0":
                            
                                                        th.Thread(target=online_IP).start()
                            
                                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                            data = json.load(f)
                                                            data["IP-U"]="0"
                                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                                json.dump(data,f,indent=4)

                                            if ofl !="null":
                                                
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
                                                    
                                                
                                            
                                                    
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    settings = json.load(f)
                                                    
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
                                                    settings["Rolue"]=l
                                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                        json.dump(settings,f,indent=4)
                                            else:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)

                                            try:
                                                msg= EmailMessage()
                                                msg["Subject"]=f"Request approval - ID({str(uuid.uuid4())[:8]})"
                                                msg["From"]="aofnotification@gmail.com"
                                                msg["To"]=email_rvs
                                                msg.set_content("The rule was successfully added.\n\n\nSecurity System:\nFS System")
                                                email="aofnotification@gmail.com"
                                                password="oqgspkawnyeftyjw"
                                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                    smtp.login(email,password)
                                                    smtp.send_message(msg)
                                            except Exception:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)


                                        elif firest!="approved" and l2=="#":
                                            with open(r"C:\FS-File\email_ids.txt", "r",encoding='utf-8') as f:
                                                sent_ids=f.readlines()
                                                for line in sent_ids:
                                                    if line.startswith("~"):
                                                        l1=line   
                                            with open(r"C:\FS-File\email_ids.txt", "r",encoding='utf-8') as f:
                                                sent_ids=f.read()
                                                sent_ids=sent_ids.replace(l1,"") 
                                                
                                            with open(r"C:\FS-File\email_ids.txt", "w",encoding='utf-8') as f:
                                                sent_id="".join(map(str,sent_ids))
                                                f.write(sent_id) 
                                            try:
                                                msg= EmailMessage()
                                                msg["Subject"]=f"Request rejection - ID({str(uuid.uuid4())[:8]})"
                                                msg["From"]="aofnotification@gmail.com"
                                                msg["To"]=email_rvs
                                                msg.set_content("The official did not approve your request.\nIf you have any questions, please contact support.\n\n\nSecurity System:\nFS System")
                                                email="aofnotification@gmail.com"
                                                password="oqgspkawnyeftyjw"
                                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                    smtp.login(email,password)
                                                    smtp.send_message(msg)
                                            except Exception:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                        
                                                if data["IP-U"]!="0":
                        
                                                    th.Thread(target=online_IP).start()
                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)

                                        mail.store(num,"+FLAGS","\\Deleted")
                                        mail.expunge()
                    mail.logout()
                    time.sleep(5)




            if user_state=="USER" and chck2==0:
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    if settings["advance-mode"]!="0":
                        settings["advance-mode"]="0"
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(settings,f,indent=4)
                th.Thread(target=ckeck_email).start()
                chck2=1
##############################################################################

#EDIT: REMOVE EVERY THING I DONT NEED
##############################################################################
            def thp():
                rtime=str(time.strftime('%Y-%m-%d %H:%M:%S'))#put the time in it real place
                global tr,pp,output,error,ta,ta1,block,ere,pro,go,deleteR,fws,user_email
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    ips=settings["IP-U"]
                    mac=settings["MAC"]
                    user_email=settings["email"]
                    fws=settings["FWS"]


                with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                    _s = json.load(f)
                    _work_start = _s.get("work_start", 8)
                    _work_end   = _s.get("work_end",   18)
                    _work_days  = _s.get("work_days",  [0,1,2,3,4])


                for linep in iter(pp.stdout.readline, ''):
                    linep = linep.strip()
                    
                    if linep:
                        if "2082" in linep and tr==0:
                            

                            if fws=="null":
                                a=poewrshell('Get-NetFirewallProfile | Select-Object Enabled')
                                a=list(a)
                                a=''.join(a)
                                if "False" in a and fws=="null" :
                                    poewrshell('Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True')
                                    #send to server to add to the csv file
                                    check1="tt"
                                    try:
                                        c.sendall("hackOff".encode())
                                        c.recv(1024).decode()
                                        ips=str(ips)
                                        c.sendall(ips.encode())
                                        c.recv(1024).decode()
                                        c.sendall(mac.encode())
                                        check1=c.recv(1024).decode()
                                        check1=check1.replace("1","")
                                        check1=check1.strip()
                                    except Exception:
                                        email_alr()
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                            data = json.load(f)
                
                                        if data["IP-U"]!="0":
                
                                            th.Thread(target=online_IP).start()
                
                                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                data = json.load(f)
                                                data["IP-U"]="0"
                                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                    json.dump(data,f,indent=4)

                                    time.sleep(0.1)

                                    
                                    if check1=="issue FWS.csv" or check1=="issue FWS.csv1":
                                        try:
                                            msg= EmailMessage()
                                            msg["Subject"]=f"FOR TEST - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content(f"Someone is reading the 'FirewallTamper.csv' file.\n you should check the server's status to see if it has been compromised or not.")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)
                                        except Exception :
                                            email_alr()
                                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                data = json.load(f)
                    
                                            if data["IP-U"]!="0":
                    
                                                th.Thread(target=online_IP).start()
                    
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                                                    data["IP-U"]="0"
                                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                        json.dump(data,f,indent=4)

                                    #send email to the user
                                    try:
                                        msg= EmailMessage()
                                        msg["Subject"]=f"Detect stop attempt - ID({str(uuid.uuid4())[:8]})"
                                        msg["From"]="aofnotification@gmail.com"
                                        msg["To"]=email_rvs
                                        msg.set_content(f"An attempt was made to disable the firewall on your device, but it was blocked by FS System.\nIf you did not make this change, please check your device's security immediately.\n\n\nSecurity System:\nFS System")
                                        email="aofnotification@gmail.com"
                                        password="oqgspkawnyeftyjw"
                                        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                            smtp.login(email,password)
                                            smtp.send_message(msg)
                                    except Exception:
                                        email_alr()
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                            data = json.load(f)
                
                                        if data["IP-U"]!="0":
                
                                            th.Thread(target=online_IP).start()
                
                                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                data = json.load(f)
                                                data["IP-U"]="0"
                                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                    json.dump(data,f,indent=4)


                        if ("2004" in linep or "2005" in linep or "2006" in linep or "2097" in linep or "2099" in linep or "2052" in linep)and (tr==0):
                            op1=0
                            op=0
                            if trw==1:
                                output, error =poewrshell(ta1)
                                
                            
                            
                                while True:
                                    try:
                                        with open(r"C:\FS-File\firewallcopy.json", "r", encoding="utf-8-sig") as fc:
                                            firecopy = json.load(fc)
                                            break
                                    except Exception:
                                        continue

                                with open(r"C:\FS-File\firewall_light.json", "r", encoding="utf-8-sig") as f:
                                    firelight = json.load(f)
                                

                                for i in firelight:
                                    if i not in firecopy:
                                        op=1

                                for i in firecopy:
                                    if i not in firelight:
                                        op1=1

                            if (op==0 and op1==0) and (trw==1):
                                def end():
                                    global trw
                                    trw=0
                                    time.sleep(3)
                                    trw=1
                                th.Thread(target=end).start()

                            
                            if op==0 and op1==1:
                                not_loop=0
                                if block==0:
                                    toast = Notification(
                                    app_id="Security Tool",
                                    title="Firewall Alert",
                                    msg="Unknown program tried to modify firewall rules.")
                                    
                                    toast.show()
                                    for _ in range(2):
                                        winsound.Beep(2000, 300)  
                                        time.sleep(0.2)
                                    block=1


                                try:
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        
                                        ppp=settings["path_proName_PID"]
                                        if ppp=="":
                                            ere=1
                                        ppp1=ppp
                                        ppp=""
                                        settings["path_proName_PID"]=ppp
                                        row=[]
                                        for ppnp in ppp1:
                                            if ppnp=="+":
                                                pid=''.join(row)
                                                row.clear()
                                                continue
                                            if ppnp=="$":
                                                pro_name=''.join(row)
                                                row.clear()
                                                continue
                                            row.append(ppnp)
                                        pro_path=''.join(row)
                                        

                                        whitelist=settings["white list checker"]
                                        whi_ls=whitelist
                                        whitelist=""
                                        settings["white list checker"]=whitelist

                                        if whi_ls in settings["white list"]:
                                            whi_ls=True
                                            poewrshell(ta)
                                        else:
                                            whi_ls=False

                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4) 
                                
                                except Exception:
                                    ere=1
                                for i in firecopy:
                                    if i not in firelight:
                                        bl=[]
                                        DisplayName=i["DisplayName"]
                                        bl.append(DisplayName)
                                        Name=i["Name"]
                                        bl.append(Name)
                                        Direction=i["Direction"]
                                        bl.append(Direction)
                                        Action=i["Action"]
                                        bl.append(Action)
                                        Profile=i["Profile"]
                                        bl.append(Profile)
                                        Enabled=i["Enabled"]
                                        bl.append(Enabled)
                                        Protocol=i["Protocol"]
                                        bl.append(Protocol)
                                        LocalPort=i["LocalPort"]
                                        bl.append(LocalPort)
                                        LocalPort=str(LocalPort)
                                        RemotePort=i["RemotePort"]# ليه انا ماخليت الريموت بورت زي لوكل بورت         هل انا اصلا ما بعمل تحقق منه في نظام التحققمن القاعده
                                        bl.append(RemotePort)
                                        Program=i["Program"]
                                        bl.append(Program)
                                        IPScope=i["IPScope"]
                                        bl.append(IPScope)

                                        
                                        # if not_loop==0:
                                        with open(r"C:\FS-File\loop.txt", "r",encoding='utf-8') as f:
                                            loop=f.readlines()
                                            l=0
                                            for line in loop:
                                                if pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                                    l+=1
                                                    go=0
                                                    not_loop=1
                                                if l==2:
                                                    go=2
                                                    break
                                            

                                        if ere==1:
                                            pro=0
                                            # ── اقرأ صلاحيات العملية من الإعدادات
                                            with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                                _s = json.load(f)
                                                _role = _s.get("user_role", "UNKNOWN")
                                            if Program=="System":
                                                chick_vil="Valid"
                                            elif Program!="Any":
                                                path = f'''(Get-AuthenticodeSignature "{Program}").Status'''
                                                chick_vil, error = poewrshell(path)
                                                chick_vil=list(chick_vil)
                                                chick_vil=''.join(chick_vil)
                                                if error:
                                                    chick_vil="UnknownError"
                                                if whi_ls==True:
                                                    chick_vil="Valid"
                                            else:
                                                chick_vil="Any"
                                            # ── النظام المتقدم بدل rs.risk_score_add_*
                                            result = risk_engine.calculate(
                                                operation    = "ADD",
                                                mac          = mac,
                                                signature    = chick_vil.strip() if chick_vil!="Any" else "NotSigned",
                                                action       = Action,
                                                direction    = Direction,
                                                protocol     = Protocol,
                                                port         = LocalPort,
                                                ip_scope     = IPScope,
                                                user_role    = _role,
                                                timestamp    = time.time(),
                                                program_path = "UNKNOWN",
                                                work_start   = _work_start,   # ← جديد
                                                work_end     = _work_end,     # ← جديد
                                                work_days    = _work_days     # ← جديد
                                            )
                                            ricor      = result["score"]
                                            risk_level = result["risk_level"]
                                            patterns   = result["triggered_patterns"]

                                            if risk_level == "LOW":
                                                add_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,
                                                            Direction,Action,Profile,Enabled,Protocol,
                                                            LocalPort,RemotePort,Program,rtime,"NO")
                                                poewrshell(ta)

                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    settings = json.load(f)
                                                    settings["BL_Rule_Check"]=bl
                                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                        json.dump(settings,f,indent=4) 
        
                                                th.Thread(target=black_list).start()



                                            elif risk_level == "MEDIUM":
                                                add_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,
                                                            Direction,Action,Profile,Enabled,Protocol,
                                                            LocalPort,RemotePort,Program,rtime,"NO")
                                                poewrshell(ta)

                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    settings = json.load(f)
                                                    settings["BL_Rule_Check"]=bl
                                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                        json.dump(settings,f,indent=4) 
        
                                                th.Thread(target=black_list).start()
                                                

                                            elif risk_level in ("HIGH", "CRITICAL"):
                                                poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                                if not_loop==0:
                                                    pat_str = ", ".join(patterns) if patterns else "HIGH RISK"
                                                    ms = f'''
There is a new firewall rule added by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block [{pat_str}]
                                        '''
                                                    toast = Notification(app_id="FS Notification",
                                                                        title="Add Firewall Rule Alert", msg=ms)
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)
                                                        time.sleep(0.2)
                                                    email_notif("UNKNOWN","UNKNOWN",
                                                                f"ADDING RULE [{pat_str}]","BLOCK",user_email)
                                                add_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,
                                                            Direction,Action,Profile,Enabled,Protocol,
                                                            LocalPort,RemotePort,Program,rtime,"NO")
                                        

                                        
                                        if pro==1:
                                            path = f'''(Get-AuthenticodeSignature "{pro_path}").Status'''
                                            vrifiy1, error = poewrshell(path)
                                            vrifiy1=list(vrifiy1)
                                            vrifiy1=''.join(vrifiy1)

                                            if whi_ls==True:
                                                vrifiy1="Valid"
                                        # ── اقرأ الصلاحيات
                                            with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                                _s = json.load(f)
                                                _role = _s.get("user_role", "UNKNOWN")

                                            # ── النظام المتقدم
                                            result = risk_engine.calculate(
                                                operation    = "ADD",
                                                mac          = mac,
                                                signature    = vrifiy1.strip(),
                                                action       = Action,
                                                direction    = Direction,
                                                protocol     = Protocol,
                                                port         = LocalPort,
                                                ip_scope     = IPScope,
                                                user_role    = _role,
                                                timestamp    = time.time(),
                                                program_path = pro_path,
                                                work_start   = _work_start,   # ← جديد
                                                work_end     = _work_end,     # ← جديد
                                                work_days    = _work_days     # ← جديد
                                            )
                                            ricor      = result["score"]
                                            risk_level = result["risk_level"]
                                            patterns   = result["triggered_patterns"] 


                                            if whi_ls:
                                                add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,rtime,"YES")
 
                                            elif risk_level == "LOW":
                                                add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,
                                                            Direction,Action,Profile,Enabled,Protocol,
                                                            LocalPort,RemotePort,Program,rtime,"NO")
                                                poewrshell(ta)

                                            elif risk_level == "MEDIUM":
                                                add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,
                                                            Direction,Action,Profile,Enabled,Protocol,
                                                            LocalPort,RemotePort,Program,rtime,"NO")
                                                poewrshell(ta)

                                            elif risk_level == "HIGH":
                                                pat_str = ", ".join(patterns) if patterns else "HIGH RISK"
                                                if go==1 and not_loop==0:
                                                    ms = f'''
There is a new firewall rule added by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block [{pat_str}]
                                        '''
                                                    toast = Notification(app_id="FS Notification",
                                                                        title="Add Firewall Rule Alert", msg=ms)
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)
                                                        time.sleep(0.2)
                                                    email_notif(pro_name,pro_path,
                                                                f"ADDING RULE [{pat_str}]","BLOCK",user_email)
                                                with open(r"C:\FS-File\loop.txt", "+a", encoding='utf-8') as f:
                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                go=1
                                                poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                                add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,
                                                            Direction,Action,Profile,Enabled,Protocol,
                                                            LocalPort,RemotePort,Program,rtime,"NO")

                                            elif risk_level == "CRITICAL":
                                                pat_str = ", ".join(patterns) if patterns else "CRITICAL"
                                                try:
                                                    _pid = int(pid)
                                                    _proc = psutil.Process(_pid)
                                                    if _proc.exe()==pro_path and _proc.name()==pro_name:
                                                        _proc.kill()
                                                except Exception:
                                                    pass
                                                poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                                ms = f'''
There is a new firewall rule added by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program [{pat_str}]
                                        '''
                                                toast = Notification(app_id="FS Notification",
                                                                    title="Add Firewall Rule Alert", msg=ms)
                                                toast.show()
                                                for _ in range(2):
                                                    winsound.Beep(2000, 300)
                                                    time.sleep(0.2)
                                                email_notif(pro_name,pro_path,
                                                            f"ADDING RULE [{pat_str}]","KILL PROGRAM + BLOCK",user_email)
                                                add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,
                                                            Direction,Action,Profile,Enabled,Protocol,
                                                            LocalPort,RemotePort,Program,rtime,"NO")

                                                
                                        pro=1    
                                    
                                    

                            if op==1 and op1==0:
                                not_loop=0
                                if block==0:
                                    toast = Notification(
                                    app_id="Security Tool",
                                    title="Firewall Alert",
                                    msg="Unknown program tried to modify firewall rules.")
                                    
                                    toast.show()
                                    for _ in range(2):
                                        winsound.Beep(2000, 300)  
                                        time.sleep(0.2)
                                    block=1

                                try:
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        
                                        ppp=settings["path_proName_PID"]
                                        if ppp=="":
                                            ere=1
                                        ppp1=ppp
                                        ppp=""
                                        settings["path_proName_PID"]=ppp
                                        row=[]
                                        for ppnp in ppp1:
                                            if ppnp=="+":
                                                pid=''.join(row)
                                                row.clear()
                                                continue
                                            if ppnp=="$":
                                                pro_name=''.join(row)
                                                row.clear()
                                                continue
                                            row.append(ppnp)
                                        pro_path=''.join(row)

                                        whitelist=settings["white list checker"]
                                        whi_ls=whitelist
                                        whitelist=""
                                        settings["white list checker"]=whitelist

                                        if whi_ls in settings["white list"]:
                                            whi_ls=True
                                            poewrshell(ta)
                                        else:
                                            whi_ls=False
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4) 
                                
                                except Exception:
                                    ere=1
                                for i in firelight:
                                    
                                    if i not in firecopy:
                                        DisplayName=i["DisplayName"]
                                        Name=i["Name"]
                                        Direction=i["Direction"]

                                        Action=i["Action"]

                                        Profile=i["Profile"]

                                        Enabled=i["Enabled"]

                                        Protocol=i["Protocol"]
                                        LocalPort=i["LocalPort"]
                                        LocalPort=str(LocalPort)
                                        RemotePort=i["RemotePort"]
                                        Program=i["Program"]
                                        IPScope=i["IPScope"]
                                        # if not_loop==0:
                                        with open(r"C:\FS-File\loop-2.txt", "r",encoding='utf-8') as f:
                                            loop=f.readlines()
                                            l=0
                                            for line in loop:
                                                if pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                                    l+=1
                                                    go=0
                                                    not_loop=1
                                                if l==2:
                                                    go=2
                                                    break

                                        if ere==1:
                                            pro=0

                                            # ── اقرأ الصلاحيات
                                            with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                                _s = json.load(f)
                                                _role = _s.get("user_role", "UNKNOWN")

                                            # ── تحقق هل البرنامج المحذوفة قاعدته موجود على القرص
                                            chi, error = poewrshell(rf'Test-Path "{Program}"')
                                            chi = ''.join(list(chi)).strip()

                                            # ── signature للبرنامج المرتبط بالقاعدة المحذوفة
                                            if Program == "System" or "WINDOWS\\system" in Program:
                                                _sig = "Valid"
                                            elif Program != "Any" and chi == "True":
                                                _sig_raw, _ = poewrshell(
                                                    f'(Get-AuthenticodeSignature "{Program}").Status'
                                                )
                                                _sig = ''.join(list(_sig_raw)).strip()
                                                if not _sig:
                                                    _sig = "UnknownError"
                                            else:
                                                _sig = "NotSigned"

                                            result = risk_engine.calculate(
                                                operation    = "DELETE",
                                                mac          = mac,
                                                signature    = _sig,
                                                action       = Action,
                                                direction    = Direction,
                                                protocol     = Protocol,
                                                port         = LocalPort,
                                                ip_scope     = IPScope,
                                                user_role    = _role,
                                                timestamp    = time.time(),
                                                program_path = "UNKNOWN",
                                                work_start   = _work_start,   # ← جديد
                                                work_end     = _work_end,     # ← جديد
                                                work_days    = _work_days     # ← جديد
                                            )
                                            ricor      = result["score"]
                                            risk_level = result["risk_level"]
                                            patterns   = result["triggered_patterns"]

                                            if risk_level == "LOW":
                                                delete_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rtime,"NO")
                                                poewrshell(ta)

                                            elif risk_level == "MEDIUM":
                                                delete_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rtime,"NO")
                                                poewrshell(ta)

                                            elif risk_level in ("HIGH", "CRITICAL"):
                                                if not_loop == 0:
                                                    pat_str = ", ".join(patterns) if patterns else risk_level
                                                    ms = f'''
There is a new firewall rule deleted by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block [{pat_str}]
                                        '''
                                                    toast = Notification(
                                                        app_id="FS Notification",
                                                        title="Delete Firewall Rule Alert",
                                                        msg=ms)
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)
                                                        time.sleep(0.2)
                                                    email_notif("UNKNOWN","UNKNOWN",
                                                                f"DELETING RULE [{pat_str}]","BLOCK",user_email)

                                                addrule = (f'New-NetFirewallRule -DisplayName "{DisplayName}"'
                                                        f' -Name "{Name}" -Direction {Direction}'
                                                        f' -Action {Action} -Profile {Profile}'
                                                        f' -Enabled {Enabled} -Protocol {Protocol}'
                                                        f' -LocalPort {LocalPort} -RemotePort {RemotePort}'
                                                        f' -Program "{Program}"')
                                                poewrshell(addrule)
                                                delete_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rtime,"NO")



                                        if pro==1:
                                            # ── التوقيع
                                            path = f'(Get-AuthenticodeSignature "{pro_path}").Status'
                                            vrifiy1, error = poewrshell(path)
                                            vrifiy1 = ''.join(list(vrifiy1))
                                            if whi_ls == True:
                                                vrifiy1 = "Valid"

                                            # ── اقرأ الصلاحيات
                                            with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                                _s = json.load(f)
                                                _role = _s.get("user_role", "UNKNOWN")

                                            result = risk_engine.calculate(
                                                operation    = "DELETE",
                                                mac          = mac,
                                                signature    = vrifiy1.strip(),
                                                action       = Action,
                                                direction    = Direction,
                                                protocol     = Protocol,
                                                port         = LocalPort,
                                                ip_scope     = IPScope,
                                                user_role    = _role,
                                                timestamp    = time.time(),
                                                program_path = pro_path,
                                                work_start   = _work_start,   # ← جديد
                                                work_end     = _work_end,     # ← جديد
                                                work_days    = _work_days     # ← جديد
                                            )
                                            ricor      = result["score"]
                                            risk_level = result["risk_level"]
                                            patterns   = result["triggered_patterns"]

                                            if whi_ls:
                                                delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime,"YES")

                                            elif risk_level == "LOW":
                                                delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime,"NO")
                                                poewrshell(ta)

                                            elif risk_level == "MEDIUM":
                                                delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime,"NO")
                                                poewrshell(ta)

                                            elif risk_level == "HIGH":
                                                pat_str = ", ".join(patterns) if patterns else "HIGH RISK"
                                                if go == 1 and not_loop == 0:
                                                    ms = f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block [{pat_str}]
                                            '''
                                                    toast = Notification(
                                                        app_id="FS Notification",
                                                        title="Delete Firewall Rule Alert",
                                                        msg=ms)
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)
                                                        time.sleep(0.2)
                                                    email_notif(pro_name,pro_path,
                                                                f"DELETING RULE [{pat_str}]","BLOCK",user_email)

                                                with open(r"C:\FS-File\loop-2.txt", "+a", encoding='utf-8') as f:
                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                                if go == 2:
                                                    try:
                                                        _pid = int(pid)
                                                        _proc = psutil.Process(_pid)
                                                        if _proc.exe() == pro_path and _proc.name() == pro_name:
                                                            _proc.kill()
                                                    except Exception:
                                                        pass
                                                    ms = f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program [{pat_str}]
                                            '''
                                                    toast = Notification(
                                                        app_id="FS Notification",
                                                        title="Delete Firewall Rule Alert",
                                                        msg=ms)
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)
                                                        time.sleep(0.2)
                                                    email_notif(pro_name,pro_path,
                                                                f"DELETING RULE [{pat_str}]","KILL PROGRAM + BLOCK",user_email)

                                                go = 1
                                                addrule = (f'New-NetFirewallRule -DisplayName "{DisplayName}"'
                                                            f' -Name "{Name}" -Direction {Direction}'
                                                            f' -Action {Action} -Profile {Profile}'
                                                            f' -Enabled {Enabled} -Protocol {Protocol}'
                                                            f' -LocalPort {LocalPort} -RemotePort {RemotePort}'
                                                            f' -Program "{Program}"')
                                                poewrshell(addrule)
                                                delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime,"NO")

                                            elif risk_level == "CRITICAL":
                                                pat_str = ", ".join(patterns) if patterns else "CRITICAL"
                                                try:
                                                    _pid = int(pid)
                                                    _proc = psutil.Process(_pid)
                                                    if _proc.exe() == pro_path and _proc.name() == pro_name:
                                                        _proc.kill()
                                                except Exception:
                                                    pass
                                                ms = f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program [{pat_str}]
                                            '''
                                                toast = Notification(
                                                    app_id="FS Notification",
                                                    title="Delete Firewall Rule Alert",
                                                    msg=ms)
                                                toast.show()
                                                for _ in range(2):
                                                    winsound.Beep(2000, 300)
                                                    time.sleep(0.2)
                                                email_notif(pro_name,pro_path,
                                                            f"DELETING RULE [{pat_str}]","KILL PROGRAM + BLOCK",user_email)
                                                addrule = (f'New-NetFirewallRule -DisplayName "{DisplayName}"'
                                                            f' -Name "{Name}" -Direction {Direction}'
                                                            f' -Action {Action} -Profile {Profile}'
                                                            f' -Enabled {Enabled} -Protocol {Protocol}'
                                                            f' -LocalPort {LocalPort} -RemotePort {RemotePort}'
                                                            f' -Program "{Program}"')
                                                poewrshell(addrule)
                                                delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime,"NO")

                                            pro = 1     

                                        
                            # with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                            #     settings = json.load(f)
                            #     eds=settings["edit_wait"]
                            # if eds == "0":
                            if tr==0:
                                if op==1 and op1==1:

                                    if block==0:
                                        toast = Notification(
                                        app_id="Security Tool",
                                        title="Firewall Alert",
                                        msg="Unknown program tried to modify firewall rules.")
                                        
                                        toast.show()
                                        for _ in range(2):
                                            winsound.Beep(2000, 300)  
                                            time.sleep(0.2)
                                        block=1


                                    not_loop=0
                                    try:
                                                        
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                            settings = json.load(f)
                                            
                                            ppp=settings["path_proName_PID"]
                                            if ppp=="":
                                                ere=1
                                            ppp1=ppp
                                            ppp=""
                                            settings["path_proName_PID"]=ppp
                                            row=[]
                                            for ppnp in ppp1:
                                                if ppnp=="+":
                                                    pid=''.join(row)
                                                    row.clear()
                                                    continue
                                                if ppnp=="$":
                                                    pro_name=''.join(row)
                                                    row.clear()
                                                    continue
                                                row.append(ppnp)
                                            pro_path=''.join(row)

                                            whitelist=settings["white list checker"]
                                            whi_ls=whitelist
                                            whitelist=""
                                            settings["white list checker"]=whitelist

                                            if whi_ls in settings["white list"]:
                                                whi_ls=True
                                                poewrshell(ta)
                                            else:
                                                whi_ls=False
                                    
                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4) 
                                
                                    except Exception:
                                        ere=1
                                    for iz in firecopy:
                                        if iz not in firelight:
                                            Program1=iz["Program"]
                                            Direction1=iz["Direction"]

                                            Action1=iz["Action"]

                                            Profile1=iz["Profile"]

                                            Enabled1=iz["Enabled"]

                                            Protocol1=iz["Protocol"]
                                            LocalPort1=iz["LocalPort"]
                                            LocalPort1=str(LocalPort1)
                                            RemotePort1=iz["RemotePort"]
                                            IPScope1=iz["IPScope"]

                                    for i in firelight:
                                        if i not in firecopy:

                                
                                            Direction=i["Direction"]

                                            Action=i["Action"]

                                            Profile=i["Profile"]

                                            Enabled=i["Enabled"]

                                            Protocol=i["Protocol"]
                                            LocalPort=i["LocalPort"]
                                            LocalPort=str(LocalPort)
                                            RemotePort=i["RemotePort"]
                                            Program=i["Program"]
                                            IPScope=i["IPScope"]

                                            dat=firelight.index(i)
                                            for ii in i:
                                                if i[ii] != firecopy[dat][ii]:
                                                    Name=i["Name"]
                                                    DisplayName=i["DisplayName"]

                                                    # if not_loop==0:
                                                    with open(r"C:\FS-File\loop-3.txt", "r",encoding='utf-8') as f:
                                                        loop=f.readlines()
                                                        l=0
                                                        for line in loop:
                                                            if pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                                                l+=1
                                                                go=0
                                                                not_loop=1
                                                            if l==2:
                                                                go=2
                                                                break

                                                    if ere==1:
                                                        pro=0

                                                        # ── اقرأ الصلاحيات
                                                        with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                                            _s = json.load(f)
                                                            _role = _s.get("user_role", "UNKNOWN")

                                                        # ── حدد signature بناءً على البرنامج المرتبط بالقاعدة
                                                        if Program == "System" or "WINDOWS\\system" in Program:
                                                            _sig = "Valid"
                                                        elif Program != "Any":
                                                            _sig_raw, _ = poewrshell(
                                                                f'(Get-AuthenticodeSignature "{Program}").Status'
                                                            )
                                                            _sig = ''.join(list(_sig_raw)).strip()
                                                            if not _sig:
                                                                _sig = "UnknownError"
                                                        else:
                                                            _sig = "NotSigned"

                                                        # ── إذا البرنامج تغيّر (Program!=Program1) = خطر إضافي
                                                        # نُضيف 20 نقطة عن طريق تغيير operation إلى MODIFY_PROG
                                                        # لكن نبقى على MODIFY لأن النظام لا يعرف MODIFY_PROG
                                                        # الحل: نمرر signature كـ NotSigned إذا Program!=Program1
                                                        if Program != Program1:
                                                            _sig = "NotSigned"

                                                        result = risk_engine.calculate(
                                                            operation    = "MODIFY",
                                                            mac          = mac,
                                                            signature    = _sig,
                                                            action       = Action,
                                                            direction    = Direction,
                                                            protocol     = Protocol,
                                                            port         = LocalPort,
                                                            ip_scope     = IPScope,
                                                            user_role    = _role,
                                                            timestamp    = time.time(),
                                                            program_path = "UNKNOWN",
                                                            work_start   = _work_start,   # ← جديد
                                                            work_end     = _work_end,     # ← جديد
                                                            work_days    = _work_days     # ← جديد
                                                        )
                                                        ricor      = result["score"]
                                                        risk_level = result["risk_level"]
                                                        patterns   = result["triggered_patterns"]

                                                        # دالة مساعدة محلية لإعادة القاعدة لحالتها الأصلية
                                                        def _revert_modify():
                                                            if ii.lower() in ["direction","action","profile","enabled"]:
                                                                w = i[ii]
                                                                poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} {w}\n')
                                                            elif ii.lower() == "displayname":
                                                                w = i[ii]
                                                                poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} "{w}"\n')
                                                            elif ii.lower() in ["protocol","localport","remoteport"]:
                                                                w = i[ii]
                                                                poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallPortFilter | Set-NetFirewallPortFilter -{ii} {w}\n')
                                                            elif ii.lower() == "program":
                                                                w = i[ii]
                                                                poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallApplicationFilter | Set-NetFirewallApplicationFilter -Program "{w}"\n')
                                                            else:
                                                                w = i[ii]
                                                            return w

                                                        if risk_level == "LOW":
                                                            poewrshell(ta)

                                                        elif risk_level == "MEDIUM":
                                                            poewrshell(ta)

                                                        elif risk_level in ("HIGH", "CRITICAL"):
                                                            if not_loop == 0:
                                                                pat_str = ", ".join(patterns) if patterns else risk_level
                                                                ms = f'''
There is a new firewall rule modified by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block [{pat_str}]
                                                    '''
                                                                toast = Notification(
                                                                    app_id="FS Notification",
                                                                    title="Modify Firewall Rule Alert",
                                                                    msg=ms)
                                                                toast.show()
                                                                for _ in range(2):
                                                                    winsound.Beep(2000, 300)
                                                                    time.sleep(0.2)
                                                                email_notif("UNKNOWN","UNKNOWN",
                                                                            f"MODIFYING RULE [{pat_str}]","BLOCK",user_email)

                                                            w = _revert_modify()
                                                            modefiy_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,ii,w,rtime,"NO")


                                                    if pro==1:
                                                        path = f'(Get-AuthenticodeSignature "{pro_path}").Status'
                                                        vrifiy1, error = poewrshell(path)
                                                        vrifiy1 = ''.join(list(vrifiy1))
                                                        if whi_ls == True:
                                                            vrifiy1 = "Valid"

                                                        # ── اقرأ الصلاحيات
                                                        with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                                            _s = json.load(f)
                                                            _role = _s.get("user_role", "UNKNOWN")

                                                        result = risk_engine.calculate(
                                                            operation    = "MODIFY",
                                                            mac          = mac,
                                                            signature    = vrifiy1.strip(),
                                                            action       = Action,
                                                            direction    = Direction,
                                                            protocol     = Protocol,
                                                            port         = LocalPort,
                                                            ip_scope     = IPScope,
                                                            user_role    = _role,
                                                            timestamp    = time.time(),
                                                            program_path = pro_path,
                                                            work_start   = _work_start,   # ← جديد
                                                            work_end     = _work_end,     # ← جديد
                                                            work_days    = _work_days     # ← جديد
                                                        )
                                                        ricor      = result["score"]
                                                        risk_level = result["risk_level"]
                                                        patterns   = result["triggered_patterns"]

                                                        # دالة مساعدة محلية لإعادة القاعدة لحالتها الأصلية
                                                        def _revert_modify_pro():
                                                            if ii.lower() in ["direction","action","profile","enabled"]:
                                                                w = i[ii]
                                                                poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} {w}\n')
                                                            elif ii.lower() == "displayname":
                                                                w = i[ii]
                                                                poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} "{w}"\n')
                                                            elif ii.lower() in ["protocol","localport","remoteport"]:
                                                                w = i[ii]
                                                                poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallPortFilter | Set-NetFirewallPortFilter -{ii} {w}\n')
                                                            elif ii.lower() == "program":
                                                                w = i[ii]
                                                                poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallApplicationFilter | Set-NetFirewallApplicationFilter -Program "{w}"\n')
                                                            else:
                                                                w = i[ii]
                                                            return w

                                                        if whi_ls:
                                                            w = i[ii] if ii in i else ""
                                                            modefiy_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime,"YES")

                                                        elif risk_level == "LOW":
                                                            w = i[ii] if ii in i else ""
                                                            modefiy_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime,"NO")
                                                            poewrshell(ta)

                                                        elif risk_level == "MEDIUM":
                                                            w = i[ii] if ii in i else ""
                                                            modefiy_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime,"NO")
                                                            poewrshell(ta)

                                                        elif risk_level == "HIGH":
                                                            pat_str = ", ".join(patterns) if patterns else "HIGH RISK"
                                                            if go == 1 and not_loop == 0:
                                                                ms = f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block [{pat_str}]
                                                    '''
                                                                toast = Notification(
                                                                    app_id="FS Notification",
                                                                    title="Modify Firewall Rule Alert",
                                                                    msg=ms)
                                                                toast.show()
                                                                for _ in range(2):
                                                                    winsound.Beep(2000, 300)
                                                                    time.sleep(0.2)
                                                                email_notif(pro_name,pro_path,
                                                                            f"MODIFYING RULE [{pat_str}]","BLOCK",user_email)

                                                            with open(r"C:\FS-File\loop-3.txt", "+a", encoding='utf-8') as f:
                                                                f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                                            if go == 2:
                                                                try:
                                                                    _pid = int(pid)
                                                                    _proc = psutil.Process(_pid)
                                                                    if _proc.exe() == pro_path and _proc.name() == pro_name:
                                                                        _proc.kill()
                                                                except Exception:
                                                                    pass
                                                                ms = f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program [{pat_str}]
                                                    '''
                                                                toast = Notification(
                                                                    app_id="FS Notification",
                                                                    title="Modify Firewall Rule Alert",
                                                                    msg=ms)
                                                                toast.show()
                                                                for _ in range(2):
                                                                    winsound.Beep(2000, 300)
                                                                    time.sleep(0.2)
                                                                email_notif(pro_name,pro_path,
                                                                            f"MODIFYING RULE [{pat_str}]","KILL PROGRAM + BLOCK",user_email)

                                                            go = 1
                                                            w = _revert_modify_pro()
                                                            modefiy_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime,"NO")

                                                        elif risk_level == "CRITICAL":
                                                            pat_str = ", ".join(patterns) if patterns else "CRITICAL"
                                                            try:
                                                                _pid = int(pid)
                                                                _proc = psutil.Process(_pid)
                                                                if _proc.exe() == pro_path and _proc.name() == pro_name:
                                                                    _proc.kill()
                                                            except Exception:
                                                                pass
                                                            ms = f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program [{pat_str}]
                                                    '''
                                                            toast = Notification(
                                                                app_id="FS Notification",
                                                                title="Modify Firewall Rule Alert",
                                                                msg=ms)
                                                            toast.show()
                                                            for _ in range(2):
                                                                winsound.Beep(2000, 300)
                                                                time.sleep(0.2)
                                                            email_notif(pro_name,pro_path,
                                                                        f"MODIFYING RULE [{pat_str}]","KILL PROGRAM + BLOCK",user_email)
                                                            w = _revert_modify_pro()
                                                            modefiy_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime,"NO")

                                                        pro = 1


            th.Thread(target=thp).start()

##############################################################################

#COPY: CHECK IF I NEEDED
##############################################################################
            lkl = 1
            tr  = 0
##############################################################################

#DELETE
##############################################################################
            def clos_fw():
                global tr, ta, ta1, block, ere, pro, go, deleteR
                
                while True:  # ← loop لإعادة الاتصال إذا انقطع
                    try:
                        cc = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                        cc.connect((ip, 9991))
                        cc.sendall("client".encode())
                        
                        while True:
                            try:
                                order = cc.recv(1024).decode('utf-8')
                                cc.sendall("1".encode())
                                close = cc.recv(1024).decode('utf-8')
                                cc.sendall("1".encode())
                                tr = 1
                                if order == "4":
                                    
                                    with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                        settings = json.load(f)
                                        settings["FWS"]    = "off-all"
                                        settings["timerF"] = "0"
                                    with open(r'C:\FS-File\settings.json', 'w', encoding='utf-8') as f:
                                        json.dump(settings, f, indent=4)
                                    poewrshell("Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False")

                                elif order == "5":
                                    
                                    with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                        settings = json.load(f)
                                        settings["FWS"]    = "null"
                                        settings["timerF"] = "0"
                                    with open(r'C:\FS-File\settings.json', 'w', encoding='utf-8') as f:
                                        json.dump(settings, f, indent=4)
                                    poewrshell("Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")

                                    
                                elif order == "6":
                                    
                                    with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                        settings = json.load(f)
                                        if settings["user-state"]=="USER":
                                            settings["bossemail"] = close
                                            with open(r'C:\FS-File\settings.json', 'w', encoding='utf-8') as f:
                                                json.dump(settings, f, indent=4)

                                elif order == "1":
                                    #check the rule in the (FSA) to make it allwas end in the displayname or name with ((contrlize-FS))
                                    # maybe the adminstrator send a rule with a name (not displayname) 
                                    #check if i have two rules with the same name but defrent elemintes
                                    # stop the user or the admin if they want to add arule the name or displayname end with ((contrlize-FS))
                                    poewrshell(close)
                                    poewrshell(ta)


                                elif order == "2":
                                    
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        v=settings["checkrulename"]
     
                                    z=close.index("wevall")
                                    z=z+6
                                    ruletype=close[z:]
                                    close=close.replace(close[z:],"")
                                    close=close.replace("wevall","")

                                    if close not in v:
                                        vrifiy1, error =poewrshell(f'Remove-NetFirewallRule -{ruletype} "{close}"')
                                        if not error:
                                            poewrshell(ta)


                                elif order == "3":
                                    vrifiy1, error =poewrshell(close)
                                    if not error:
                                        poewrshell(ta)


                                elif order == "7":
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        f_priority=settings["first_priority"]
                                        f_priority=list(f_priority)
                                        f_priority.remove(close)
                                        settings["first_priority"]=f_priority
                            
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)


                                elif order == "8":
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        s_priority=settings["second_priority"]
                                        s_priority=list(s_priority)
                                        s_priority.pop(int(close)-1)
                                        settings["second_priority"]=s_priority
                            
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)


                                elif order == "9":
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        s_priority=settings["second_priority"]
                                        s_priority=list(s_priority)
                                        s_priority.append(list(close))
                                        settings["second_priority"]=s_priority
                            
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)


                                elif order == "0":
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        f_priority=settings["first_priority"]
                                        f_priority=list(f_priority)
                                        for i in range(list(close)):
                                            f_priority.append(i)
                                        settings["first_priority"]=f_priority
                            
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4)


                                elif order == "#":
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        settings["IP-S"]=close

                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4)

                                        if settings["user-state"]=="USER":

                                            toast = Notification(
                                            app_id="FS Notification",
                                            title="Restart PC",
                                            msg="The adminstoretor has change the IP-Server, you need to restart your PC.")
                                            
                                            toast.show()
                                            for _ in range(2):
                                                winsound.Beep(2000, 300)  
                                                time.sleep(0.2)


                                            notif_mas='''
    Hello,

    The adminstoretor has change the IP-Server, you need to restart your PC.  

    Security System:
    FS System

    '''

                                            try:
                                                msg= EmailMessage()
                                                msg["Subject"]=f"Security Alert - ID({str(uuid.uuid4())[:8]})"
                                                msg["From"]="aofnotification@gmail.com"
                                                msg["To"]=email_rvs
                                                msg.set_content(notif_mas)
                                                email="aofnotification@gmail.com"
                                                password="oqgspkawnyeftyjw"
                                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                    smtp.login(email,password)
                                                    smtp.send_message(msg)  
                                            except Exception:
                                                email_alr()
                                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                    data = json.load(f)
                                        
                                                if data["IP-U"]!="0":
                                        
                                                    th.Thread(target=online_IP).start()
                                        
                                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                        data = json.load(f)
                                                        data["IP-U"]="0"
                                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                            json.dump(data,f,indent=4)
                            
                                        else:

                                            toast = Notification(
                                            app_id="FS Notification",
                                            title="Restart PC",
                                            msg="You can now restart your PC.")
                                            
                                            toast.show()
                                            for _ in range(2):
                                                winsound.Beep(2000, 300)  
                                                time.sleep(0.2)        


                                time.sleep(1)
                                tr = 0

                            except Exception as e:
                                tr = 0
                                
                                break  # ← اخرج من الحلقة الداخلية لإعادة الاتصال

                    except Exception as e:
                        #tr = 0  if anything happend just let it work
                        time.sleep(5)  # ← انتظر قبل إعادة المحاولة

            # شغّله مرة واحدة عند البدء مباشرة
            th.Thread(target=clos_fw, daemon=True).start()
##############################################################################

#COPY
# ##############################################################################       
            #function to close the firewall
            def do_ruls():
                global lkl,tr,ta,ta1,block,ere,pro,go,deleteR
                if fws=="off" and lkl==1:
                    lkl=0
                    tr=1
                    fs.fireOff(fws,timer)
                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        settings["FWS"]="null"
                        settings["timerF"]="0"
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(settings,f,indent=4)
                    lkl=1
                    time.sleep(0.1)
                    tr=0
##############################################################################

#COPY
##############################################################################
            #function to add rules to the firewall
            def add__rule():
                global rulename,timerr,tr,ta,ta1,block,ere,pro,go,deleteR
                
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    a=settings["ruleName"]
                    w=settings["timerR"]
                    a=list(a)
                    w=list(w)
                    a.pop(0)
                    w.pop(0)
                    settings["ruleName"]=a
                    settings["timerR"]=w
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4) 
                
                time.sleep(timerr)
                tr=1
                poewrshell(f'Remove-NetFirewallRule -DisplayName "{rulename}"')
    
               
                poewrshell(ta)
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    v=settings["checkrulename"]
                    v=list(v)        
                    v.remove(rulename)
                    settings["checkrulename"]=v
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                time.sleep(0.1)   
                tr=0 
##############################################################################   

#COPY: CHECK IF I NEED
##############################################################################
            class Handler(FileSystemEventHandler):
                def on_modified(self, event):
                    global fws,ip,timer,rule,rulename,timerr,ips,constan,deleteR,modify_rule,mac,tr,ta,ta1,block,ere,pro,go,lkl,ll,email_rvs,ips,ips,constan,rule,modify_rule,mac,tr,ta,ta1,block,ere,pro,go,deleteR,bossemail,user_email

                    if r"C:\FS-File\settings.json" in event.src_path:
                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)

                            if settings["user-state"]=="USER":
                                bossemail=settings["bossemail"]

                            ip=settings["IP-S"]
                            
                            user_email=settings["email"]
                            email_rvs=user_email
                            
                            ips=settings["IP-U"]
                            
                            # rowFWS=["on","off","null"]
                            fws=settings["FWS"]
                            
                            deleteR=settings["deleteR"]

                            # if check4 in rowFWS:
                            #     fws= check4
                                    
                                

                            check5=settings["timerF"]
                            
                            timer=int(check5)      


                            constan=settings["constan"]

                            lens=settings["ruleName"]
                            lens=len(lens)
                            rule=settings["Rolue"]
                            if lens!=0 and constan=="no":
                                
                                rulename=settings["ruleName"][0]
                                timerr=settings["timerR"][0]
                                timerr=int(timerr)

                            modify_rule=settings["modify_rule"]
                        # if ll==1:
                        #     #run the seconed conn function
                        #     th.Thread(target=clos_fw).start()
                        #run the check D:\FS-File\settings.json function
                        
                        #check order from user
                        if fws=="off" and lkl==1:
                            #run close firewall function
                            th.Thread(target=do_ruls).start()
                        elif fws=="on":
                            #open firewall
                            tr=1
                            poewrshell(r"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["FWS"]="null"
                                settings["timerF"]="0"
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            lkl=1
                            time.sleep(0.1)
                            tr=0
                        
                        #delete rule from the firewall
                        if deleteR!="null":
                            tr=1
                            z=deleteR.index("wevall")
                            z=z+6
                            ruletype=deleteR[z:]
                            deleteR=deleteR.replace(deleteR[z:],"")
                            deleteR=deleteR.replace("wevall","")
                            
                            poewrshell(f'Remove-NetFirewallRule -{ruletype} "{deleteR}"')
                            
                            poewrshell(ta)
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["deleteR"]="null"
                                time.sleep(0.1)
                                tr=0
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            


                        #add rule to the firewall 
                        if rule!="null":
                            
                            if constan=="yes":
                                tr=1
                                poewrshell(rule)

                                poewrshell(ta)
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    settings["Rolue"]="null"
                                    settings["constan"]="no"
                                    time.sleep(0.1)
                                    tr=0
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                                
                            elif constan=="no":
                                tr=1
                                poewrshell(rule)
                                
                                poewrshell(ta)
                                
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        settings["Rolue"]="null"
                                        settings["constan"]="no"
                                        time.sleep(0.1)
                                        tr=0
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4)
                                        
                                #run add rules function
                                th.Thread(target=add__rule).start()


                        if modify_rule !="null" :
                            tr=1
                            poewrshell(modify_rule)
                            poewrshell(ta)
                            tr=0
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["modify_rule"]="null"
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)

                
            observer = Observer()
            observer.schedule(Handler(), path=r"C:\FS-File", recursive=False)
            observer.start()

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()

            observer.join()     
                    
        except Exception:
            tr=0
            continue
##############################################################################