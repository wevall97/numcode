import time
import subprocess as su
import socket as sk
import threading as th
import json
import fireSett as fs
import asyncio as sa
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
import risk_score as rs


# check all code
# serish erorr: when i delete a rule without using the system the "aof.py" send to the server "delhac" but nothing alse hapen

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
        Direction   = [int]$_.Direction
        Action      = [int]$_.Action
        Profile     = [int]$_.Profile
        Enabled     = [int]$_.Enabled
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
        Direction   = [int]$_.Direction
        Action      = [int]$_.Action
        Profile     = [int]$_.Profile
        Enabled     = [int]$_.Enabled
        Protocol    = $p.Protocol
        LocalPort   = $p.LocalPort
        RemotePort  = $p.RemotePort
        Program     = $realPath
        IPScope     = $scope
    }
}) | ConvertTo-Json -Depth 3 | Out-File "C:\FS-File\firewallcopy.json" -Encoding utf8
'''

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



def add_rule_logs(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,T):
    
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
    check1=c.recv(1024).decode()
    check1=check1.replace("1","")
    check1=check1.strip()

def delete_rule_logs(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,T):
    
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
    check1=c.recv(1024).decode()
    check1=check1.replace("1","")
    check1=check1.strip()

def modefiy_rule_logs(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,ii,gema,T):

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
    check1=c.recv(1024).decode()
    check1=check1.replace("1","")
    check1=check1.strip()

go=1
pro=1
ere=0
block=1  
pas=0

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

with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:

    settings = json.load(f) 
    chck2=0

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
    

    FIREWALL_KEYWORDS = [
        'New-NetFirewallRule',
        'Set-NetFirewallRule',
        'Remove-NetFirewallRule',
        'Enable-NetFirewallRule',
        'Disable-NetFirewallRule'
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

                                if is_target_process(name) and is_firewall_related(cmd_line, name) and parent_name=="powershell.exe":
                                    block=0

                                elif is_target_process(name) and is_firewall_related(cmd_line, name) and parent_name=="hack tool.exe":
                                    print("jr")
                                    path = f'''(Get-AuthenticodeSignature "{parent_path}").Status'''
                                    chick_vil, error = poewrshell(path)
                                    print(chick_vil.strip())   
                                    print(parent_name)
                                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        parent_pid=str(parent_pid)
                                        s=parent_pid+"+"+parent_name+"$"+parent_path
                                        settings["path_proName_PID"]=s

                                        
                                        s=parent_name+parent_path
                                        settings["white list checker"]=s

                                        with open(r"C:\FS-File\settings.json", 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4)

                except Exception as e:
                    print("WMI error:", e)
                    time.sleep(1)

        finally:
            pythoncom.CoUninitialize()


    th.Thread(target=mal_dit).start()



    while True:
        # try:
            
            pathfile=os.path.exists(r"C:\FS-File\firewall_light.json")
            
            poewrshell(ta)            
            pathfile=os.path.exists(r"C:\FS-File\sent_ids.txt")
            if pathfile==False:
                with open(r"C:\FS-File\sent_ids.txt","w",encoding='utf-8')as f:
                    f.write("")

            #check firewall state    
            a,error=poewrshell('Get-NetFirewallProfile | Select-Object Enabled')
            # a=a.stdout  
            if "False" in a: 
                poewrshell(r"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")


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
                pas=1
            
            if pas==0:
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f) 
                    settings["IP-U"]=ips
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                    pas=1
            #conn with the praimry conn   
            while True:
                try:
                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f) 
                        ip=settings["IP-S"]
                    
                    c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                    c.connect((ip, 9999))
                    #vrefiy the server to end the loop
                    chck=c.recv(1024).decode('utf-8')
                    if chck=='1':
                        
                        c.sendall("add".encode())
                    break
                except Exception:
                    
                    continue
                    
                    
                        
            #return D:\FS-File\settings.json to the defult
            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f) 
                if settings["user-state"]=="USER":
                    bossemail=settings["bossemail"]
                if settings["FWS"]=="":
                    settings["FWS"]="null"
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["timerF"]=="":
                    settings["timerF"]="0"
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["Rolue"]!="null":
                    settings["Rolue"]="null"
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["FWS"]=="off" or settings["FWS"]=="on" or settings["FWS"]=="off-all":
                    settings["FWS"]="null"
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["timerF"]!="0":
                    settings["timerF"]="0"
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["timerR"]!=[]:
                    settings["timerR"]=[]
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["ruleName"]!=[]:
                    settings["ruleName"]=[]
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["checkrulename"]!=[]: 
                    for aa in settings["checkrulename"]:
                        poewrshell(f'Remove-NetFirewallRule -DisplayName "{aa}"')
                    settings["checkrulename"]=[]
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["constan"]!="no":
                    settings["constan"]="no"
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                
                if settings["deleteR"]!="null":
                    settings["deleteR"]="null"
                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                email_rvs=settings["email"]
                user_state=settings["user-state"]
                mac=settings["MAC"]

            ps_script = """
$log = New-Object System.Diagnostics.Eventing.Reader.EventLogWatcher('Microsoft-Windows-Windows Firewall With Advanced Security/Firewall')
Register-ObjectEvent $log EventRecordWritten -Action {
    $id = $Event.SourceEventArgs.EventRecord.Id
    [Console]::WriteLine("FW_EVENT:$id")
    [Console]::Out.Flush()
}
$log.Enabled = $true
while($true) { Start-Sleep -Milliseconds 100 }
"""

            pp = su.Popen(
                ["powershell", "-NoProfile", "-Command", ps_script],
                stdout=su.PIPE,
                stderr=su.PIPE,
                text=True,
                bufsize=1)
            

            def check_state(num,state):
                num=str(num)
                if state.lower()=="direction":
                    if num=="1":
                        return "Inbound"
                    elif num=="2":
                        return "Outbound"
                
                if state.lower()=="action":
                    if num=="2":
                        return "Allow"
                    elif num=="1":
                        return "Block"
                
                if state.lower()=="profile":
                    if num=="1":
                        return "Domain"
                    elif num=="2":
                        return "Private"
                    elif num=="4":
                        return "Public"
                    elif num=="3":
                        return "Domain + Private"
                    elif num=="5":
                        return "Domain + Public"
                    elif num=="6":
                        return "Private + Public"
                    elif num=="7":
                        return "Domain + Private + Public"
                    elif num=="0":
                        return "Any"
                    
                if state.lower()=="enabled":
                    if num=="1":
                        return "True"
                    else:
                        return "False"
                    
            

            def ckeck_email():
                
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    ips=settings["IP-U"]
                global status,from_,timer,mac,bossemail,ta,ta1,block,ere,pro,go,deleteR
                while True:
                    
                    IMAP_SERVER = "imap.gmail.com"
                    EMAIL_ACCOUNT = "aofnotification@gmail.com"
                    EMAIL_PASSWORD = "oqgspkawnyeftyjw"
                    with open(r"C:\FS-File\sent_ids.txt", "r", encoding='utf-8') as f:
                        sent_ids=f.read().strip()
                        
                    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
                    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
                    mail.select("inbox")


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
                                        
                                        with open(r"C:\FS-File\sent_ids.txt", "w",encoding='utf-8') as f:
                                            sent_id="".join(map(str,sent_ids))
                                            f.write(sent_id)
                                        with open(r"C:\FS-File\sent_ids.txt", "r",encoding='utf-8') as f:
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
                                                        with open(r"C:\FS-File\sent_ids.txt", "r",encoding='utf-8') as f:
                                                            sent_ids=f.read()
                                                            sent_ids=sent_ids.replace("#","")  
                                                            
                                                            
                                                        with open(r"C:\FS-File\sent_ids.txt", "w",encoding='utf-8') as f:
                                                            sent_id="".join(map(str,sent_ids))
                                                            f.write(sent_id)  
                                                    
                                                        
                                        with open(r"C:\FS-File\sent_ids.txt", "r",encoding='utf-8') as f:
                                            sent_ids=f.read()
                                            
                                            sent_ids=sent_ids.replace(l1,"")  
                                            
                                        with open(r"C:\FS-File\sent_ids.txt", "w",encoding='utf-8') as f:
                                            sent_id="".join(map(str,sent_ids))
                                            f.write(sent_id)     

                                        if firest=="approved" and l2=="%": 
                                            
                                            ran = random.randint(100000, 999999)
                                            ran=str(ran)
                                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                settings = json.load(f)
                                                settings["advance-password"]=ran
                                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                    json.dump(settings,f,indent=4)
                                            msg= EmailMessage()
                                            msg["Subject"]=f"Identity verification - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content(f"Your password: {ran}")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)   
                                            
                                        elif firest!="approved"  and l2=="%": 
                                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                settings = json.load(f)
                                                settings["advance-mode"]="0"
                                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                    json.dump(settings,f,indent=4)
                                            msg= EmailMessage()
                                            msg["Subject"]=f"Request rejection - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content(f"The official did not approve your request.")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)


                                        if firest=="approved" and l2=="&":
                                            
                                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                settings = json.load(f)
                                                if l.endswith("e"):
                                                    l=l[:-1]
                                                    settings["Enaply list"]=[l]
                                                    action="Enable"
                                                else:
                                                    l=l[:-1]
                                                    settings["Disaply list"]=[l]
                                                    action="Disable"
                                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                    json.dump(settings,f,indent=4)


                                            if l.endswith("m") or l.endswith("h"):
                                                z=l.index("^")
                                                bb=l[z:]
                                                aa=l.replace(bb,"")
                                                bb=bb.replace("^","")
                                                
                                            on="rua"
                                            c.sendall(on.encode())
                                            c.recv(1024).decode()
                                            c.sendall(aa.encode())
                                            c.recv(1024).decode()
                                            c.sendall(bb.encode())
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
                                            if check1=="action rule log.csv" or check1=="action rule log.csv1":
                                                
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
                                            msg= EmailMessage()
                                            msg["Subject"]=f"Request approval - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content("The base state was successfully changed.")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)


                                        elif firest!="approved"  and l2=="&":
                                            
                                            msg= EmailMessage()
                                            msg["Subject"]=f"Request rejection - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content("The official did not approve your request.")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)


                                        if firest=="approved" and l2=="|":
                                            
                                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                                settings = json.load(f)
                                                settings["deleteR"]=l
                                                
                                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                    json.dump(settings,f,indent=4)
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
                                            if check1=="delete rule log.csv" or check1=="delete rule log.csv1":
                                                
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
                                            msg= EmailMessage()
                                            msg["Subject"]=f"Request approva - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content("Rule delete successfully.")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)
                                        elif firest!="approved"  and l2=="|":
                                            
                                            msg= EmailMessage()
                                            msg["Subject"]=f"Request rejection - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content("The official did not approve your request.")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)
                                        


                                        if firest=="approved"  and l2=="#":
                                            
                                            l=l.replace("#","")
                                    

                                            with open(r"C:\FS-File\sent_ids.txt", "r",encoding='utf-8') as f:
                                                sent_ids=f.readlines()
                                                for line in sent_ids:
                                                    if line.startswith("~"):
                                                        l1=line
                                                        
                                                        timer=line[1:]
                                                        
                                                        
                                            with open(r"C:\FS-File\sent_ids.txt", "r",encoding='utf-8') as f:
                                                sent_ids=f.read()
                                                sent_ids=sent_ids.replace(l1,"")  
                                                
                                            with open(r"C:\FS-File\sent_ids.txt", "w",encoding='utf-8') as f:
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
                                            if check1=="add rule log.csv" or check1=="add rule log.csv1":
                                            
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
                                            msg= EmailMessage()
                                            msg["Subject"]=f"Request approval - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content("Rule ADD successfully.")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)



                                        elif firest!="approved" and l2=="#":
                                            with open(r"C:\FS-File\sent_ids.txt", "r",encoding='utf-8') as f:
                                                sent_ids=f.readlines()
                                                for line in sent_ids:
                                                    if line.startswith("~"):
                                                        l1=line   
                                            with open(r"C:\FS-File\sent_ids.txt", "r",encoding='utf-8') as f:
                                                sent_ids=f.read()
                                                sent_ids=sent_ids.replace(l1,"") 
                                                
                                            with open(r"C:\FS-File\sent_ids.txt", "w",encoding='utf-8') as f:
                                                sent_id="".join(map(str,sent_ids))
                                                f.write(sent_id) 

                                            msg= EmailMessage()
                                            msg["Subject"]=f"Request rejection - ID({str(uuid.uuid4())[:8]})"
                                            msg["From"]="aofnotification@gmail.com"
                                            msg["To"]=email_rvs
                                            msg.set_content("The official did not approve your request.")
                                            email="aofnotification@gmail.com"
                                            password="oqgspkawnyeftyjw"
                                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                                smtp.login(email,password)
                                                smtp.send_message(msg)


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



            def thp():
                rtime=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                global tr,ed,pp,output,error,ta,ta1,block,ere,pro,go,deleteR
                for linep in iter(pp.stdout.readline, ''):
                    linep = linep.strip()
                    
                    if linep:
                        print("in dady: ",tr)
                        if "FW_EVENT:" in linep and tr==0:
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                ips=settings["IP-U"]
                                mac=settings["MAC"]
                                user_email=settings["email"]

                            output, error =poewrshell(ta1)
                            op1=0
                            op=0
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
                            print("op:",op)
                            print("op1:",op1)
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
                                        else:
                                            whi_ls=False

                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4) 
                                
                                except Exception:
                                    ere=1
                                for i in firecopy:
                                    if i not in firelight:
                                        DisplayName=i["DisplayName"]
                                        Name=i["Name"]
                                        Direction=i["Direction"]
                                        Direction=check_state(Direction,"Direction")

                                        Action=i["Action"]
                                        Action=check_state(Action,"Action")

                                        Profile=i["Profile"]
                                        Profile=check_state(Profile,"Profile")

                                        Enabled=i["Enabled"]
                                        Enabled=check_state(Enabled,"Enabled")

                                        Protocol=i["Protocol"]
                                        LocalPort=i["LocalPort"]
                                        LocalPort=str(LocalPort)
                                        RemotePort=i["RemotePort"]
                                        Program=i["Program"]
                                        IPScope=i["IPScope"]
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
                                            if Program=="System":
                                                chick_vil="Valid"
                                                ricor=rs.risk_score_add_vrifiy(chick_vil.strip(),Action,Direction,Protocol,LocalPort,IPScope)

                                            elif Program!="Any":
                                                path = f'''(Get-AuthenticodeSignature "{Program}").Status'''
                                                chick_vil, error = poewrshell(path)
                                                if error:
                                                    chick_vil="UnknownError"
                                                if whi_ls==True:
                                                    chick_vil="Valid"
                                                ricor=rs.risk_score_add_vrifiy(chick_vil.strip(),Action,Direction,Protocol,LocalPort,IPScope)
                                            
                                            else:
                                                ricor=rs.risk_score_add_not_vrifiy(Action,Direction,Protocol,LocalPort,IPScope)
                                            if ricor <= 85 :
                                                # Allow + Log
                                                add_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,rtime)
                                                print("allow + log")
                                                pass
                                            
                                            elif ricor <= 120 or ricor <= 180 or ricor>181:
                                                # Block + Alert
                                                poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                                print("block + alert")
                                                
                                                if not_loop==0:
                                                    ms=f'''
There is a new firewall rule added by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block'''
                                                    toast = Notification(
                                                    app_id="FS Notification",
                                                    title="Add Firewall Rule Alert",
                                                    msg=ms)
                                                    
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)  
                                                        time.sleep(0.2)
                                                    
                                                    
                                                    email_notif("UNKNOWN","UNKNOWN","ADDING RULE","BLOCK",user_email) 

                                                with open(r"C:\FS-File\loop.txt", "+a",encoding='utf-8') as f:
                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                #not_loop=1
                                                add_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,rtime)

                                        
                                        if pro==1:
                                            path = f'''(Get-AuthenticodeSignature "{pro_path}").Status'''
                                            vrifiy1, error = poewrshell(path)
                                            if whi_ls==True:
                                                vrifiy1="Valid"
                                            ricor=rs.risk_score_add_vrifiy(vrifiy1.strip(),Action,Direction,Protocol,LocalPort,IPScope)
                                            
                                            if whi_ls:

                                                print("allow + log") 
                                                add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,rtime)


                                            elif ricor <= 85 :
                                                # Allow + Log
                                               
                                                add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,rtime)
                                                print("allow + log")
                                                pass
                                            
                                            elif ricor <= 120:
                                                # Block + Alert
                                                print("block + alert")
                                                ms=f'''
There is a new firewall rule added by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block
'''
                                                if go==1:
                                                    if not_loop==0:
                                                        toast = Notification(
                                                        app_id="FS Notification",
                                                        title="Add Firewall Rule Alert",
                                                        
                                                        msg=ms)
                                                        
                                                        toast.show()
                                                        for _ in range(2):
                                                            winsound.Beep(2000, 300)  
                                                            time.sleep(0.2)
                                                        #not_loop=1
                                                        email_notif(pro_name,pro_path,"ADDING RULE","BLOCK",user_email) 

                                                # if not_loop==0:    
                                                with open(r"C:\FS-File\loop.txt", "+a",encoding='utf-8') as f:
                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                # not_loop=1
                                                if go==2:
                                                    # if not_loop==0:
                                                        pid=int(pid)
                                                        process = psutil.Process(pid)
                                                        parent_name = process.name()
                                                        parent_path = process.exe()
                                                        if parent_path==pro_path and parent_name==pro_name:
                                                            process = psutil.Process(pid)
                                                            process.kill()
                                                       # not_loop=1
                                                        ms=f'''
There is a new firewall rule added by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program
'''
                                                        toast = Notification(
                                                        app_id="FS Notification",
                                                        title="Add Firewall Rule Alert",
                                                        msg=ms)
                                                        
                                                        toast.show()
                                                        for _ in range(2):
                                                            winsound.Beep(2000, 300)  
                                                            time.sleep(0.2)
                                                        email_notif(pro_name,pro_path,"ADDING RULE","KILL PROGRAM + BLOCK",user_email) 

                                                    # Kill Process
                                                    # delete the rule from the file
                                                go=1
                                                poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                                add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,rtime)



                                            elif ricor <= 180 or ricor>181:
                                                #Block + Kill Process + Alert
                                                # if not_loop==0:
                                                    pid=int(pid)
                                                    process = psutil.Process(pid)
                                                    parent_name = process.name()
                                                    parent_path = process.exe()
                                                    if parent_path==pro_path and parent_name==pro_name:
                                                        process = psutil.Process(pid)
                                                        process.kill()
                                                    # not_loop=1
                                                    poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                                    print("block + alert + kill process")
                                                    ms=f'''
There is a new firewall rule added by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program
'''
                                                    toast = Notification(
                                                    app_id="FS Notification",
                                                    title="Add Firewall Rule Alert",
                                                    msg=ms)
                                                    
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)  
                                                        time.sleep(0.2)
                                                    email_notif(pro_name,pro_path,"ADDING RULE","KILL PROGRAM + BLOCK") 

                                                    add_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,str(time.strftime('%Y-%m-%d %H:%M:%S')))

                                                
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
                                        else:
                                            whi_ls=False
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4) 
                                
                                except Exception:
                                    ere=1
                                for i in firelight:
                                    
                                    if i not in firecopy:
                                        print("in loop")
                                        DisplayName=i["DisplayName"]
                                        Name=i["Name"]
                                        Direction=i["Direction"]
                                        Direction=check_state(Direction,"Direction")

                                        Action=i["Action"]
                                        Action=check_state(Action,"Action")

                                        Profile=i["Profile"]
                                        Profile=check_state(Profile,"Profile")

                                        Enabled=i["Enabled"]
                                        Enabled=check_state(Enabled,"Enabled")

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
                                            print(10)
                                            pro=0
                                            chi,error=poewrshell(rf'Test-Path "{Program}"')
                                            ricor=rs.risk_score_delete_not_vrifiy(DisplayName+" "+Name,Program,Action,Direction,Protocol,LocalPort,IPScope,chi.strip())
                                            if ricor=="Block":
                                                if not_loop==0:
                                                    ms=f'''
There is a new firewall rule deleted by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block
'''###########################################################
                                                    toast = Notification(
                                                    app_id="FS Notification",
                                                    title="Delete Firewall Rule Alert",
                                                    msg=ms)
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)  
                                                        time.sleep(0.2)
                                                    email_notif("UNKNOWN","UNKNOWN","DELETEING RULE","BLOCK",user_email) 

                                                        
                                                with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                                
                                             
                                        
                                                addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                                poewrshell(addrule)
                                                print("block + alert")
                                                delete_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rtime)

                                            
                                            elif ricor <= 85 :
                                                # Allow + Log
                                                print("allow + log")
                                                delete_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rtime)
                                            elif ricor <= 120 or ricor <= 180 or ricor>181:
                                                # Block + Alert
                                                print("block + alert")
                                                if not_loop==0:
                                                    ms=f'''
There is a new firewall rule deleted by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block
'''###########################################################
                                                    toast = Notification(
                                                    app_id="FS Notification",
                                                    title="Delete Firewall Rule Alert",
                                                    msg=ms)
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)  
                                                        time.sleep(0.2)
                                                    email_notif("UNKNOWN","UNKNOWN","DELETEING RULE","BLOCK",user_email) 

                                                        
                                                with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                                addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                                poewrshell(addrule)
                                                delete_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rtime)


                                            



                                        if pro==1:
                                            path = f'''(Get-AuthenticodeSignature "{pro_path}").Status'''
                                            vrifiy1, error = poewrshell(path)

                                            if whi_ls==True:
                                                vrifiy1="Valid"
                                            tre=rf'(Get-AuthenticodeSignature "{pro_path}").SignerCertificate.GetNameInfo("SimpleName",$false)'
                                            compony_name,error=poewrshell(tre)
                                            if compony_name=="":
                                                compony_name="unknwon"
                                            if Program!="System":
                                                chi,error=poewrshell(rf'Test-Path "{Program}"')


                                            if (compony_name=="Microsoft Windows" and Program =="System") or (compony_name=="Microsoft Windows" and "WINDOWS\system" in Program):
                                                #Log
                                                print(11)
                                                delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime)
                                            elif (compony_name!="Microsoft Windows" and Program =="System") or (compony_name!="Microsoft Windows" and "WINDOWS\system" in Program):
                                                # Block + Alert + log
                                                print("resit + alert")
                                                print(12)
                                                if go==1:
                                                    if not_loop==0:
                                                        ms=f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block
'''
                                                        toast = Notification(
                                                        app_id="FS Notification",
                                                        title="Delete Firewall Rule Alert",
                                                        msg=ms)
                                                        toast.show()
                                                        for _ in range(2):
                                                            winsound.Beep(2000, 300)  
                                                            time.sleep(0.2)
                                                        email_notif(pro_name,pro_path,"DELETEING RULE","BLOCK",user_email) 
                                                with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                if go==2:
                                                        ms=f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program
'''
                                                        pid=int(pid)
                                                        process = psutil.Process(pid)
                                                        parent_name = process.name()
                                                        parent_path = process.exe()
                                                        if parent_path==pro_path and parent_name==pro_name:
                                                            process = psutil.Process(pid)
                                                            process.kill()
                                                        toast = Notification(
                                                        app_id="FS Notification",
                                                        title="Delete Firewall Rule Alert",
                                                        msg=ms)
                                                        
                                                        toast.show()
                                                        for _ in range(2):
                                                            winsound.Beep(2000, 300)  
                                                            time.sleep(0.2)
                                                        email_notif(pro_name,pro_path,"DELETEING RULE","KILL PROGRAM + BLOCK",user_email) 

                                                    # Kill Process
                                                    # delete the rule from the file
                                                go=1
                                                addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                                poewrshell(addrule)
                                                delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime)

                                            

                                            else:
                                                print(13)
                                                security_vendors = ["Microsoft","Microsoft Corporation","Windows Defender","Microsoft Defender","Symantec","Symantec Corporation","Norton","NortonLifeLock","Gen Digital","Broadcom","Broadcom Inc","McAfee","McAfee LLC","McAfee Corp","Trellix","FireEye","FireEye Inc","Kaspersky","Kaspersky Lab","Kaspersky Labs","Kaspersky Lab ZAO","ESET","ESET spol","ESET, spol. s r.o.","Avast","Avast Software","AVG","AVG Technologies","Avira","Avira GmbH","Bitdefender","Bitdefender SRL","Sophos","Sophos Ltd","Sophos Group","Trend Micro","Trend Micro Inc","Malwarebytes","Malwarebytes Inc","Panda","Panda Security","F-Secure","F-Secure Corporation","WithSecure","G Data","G Data Software","Comodo","Comodo Security","Xcitium","ZoneAlarm","Check Point","Check Point Software","Webroot","Webroot Inc","Fortinet","Fortinet Inc","CrowdStrike","CrowdStrike Inc","CrowdStrike Holdings","SentinelOne","SentinelOne Inc","Carbon Black","CarbonBlack","VMware Carbon Black","Cisco","Cisco Systems","Elastic","Elastic NV","Cybereason","Cybereason Inc","SecureWorks","Secureworks Inc","Quick Heal","QuickHeal","Seqrite","K7 Computing","K7 Security","TotalAV","Protected.net"]
                                                for vendor in security_vendors:
                                                    if compony_name.lower()==vendor.lower():
                                                        compony=True
                                                        break
                                                    else:
                                                        compony=False
                                                        break

                                                if whi_ls:

                                                    print("allow + log") 
                                                    delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime)

                                                elif compony_name.lower()in Program.lower():
                                                    #log
                                                    delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime)
                                                    print(14)
                                                    # pass
                                                
                                                


                                                elif vrifiy1!="Valid":
                                                    print("resit + alert")
                                                    print(15)
                                                    if go==1:
                                                        if not_loop==0:
                                                            ms=f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block
'''
                                                            toast = Notification(
                                                            app_id="FS Notification",
                                                            title="Delete Firewall Rule Alert",
                                                            msg=ms)
                                                            toast.show()
                                                            for _ in range(2):
                                                                winsound.Beep(2000, 300)  
                                                                time.sleep(0.2)
                                                            email_notif(pro_name,pro_path,"DELETEING RULE","BLOCK",user_email) 

                                                    with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                                        f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                    if go==2:
                                                            ms=f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program
'''
                                                            pid=int(pid)
                                                            process = psutil.Process(pid)
                                                            parent_name = process.name()
                                                            parent_path = process.exe()
                                                            if parent_path==pro_path and parent_name==pro_name:
                                                                process = psutil.Process(pid)
                                                                process.kill()
                                                            toast = Notification(
                                                            app_id="FS Notification",
                                                            title="Delete Firewall Rule Alert",
                                                            msg=ms)
                                                            
                                                            toast.show()
                                                            for _ in range(2):
                                                                winsound.Beep(2000, 300)  
                                                                time.sleep(0.2)
                                                            email_notif(pro_name,pro_path,"DELETEING RULE","KILL PROGRAM + BLOCK",user_email) 

                                                        # Kill Process
                                                        # delete the rule from the file
                                                    go=1
                                                    addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                                    poewrshell(addrule)
                                                    delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime)
                                                    
                                                
                                                
                                                elif vrifiy1=="Valid" and chi=="False":
                                                    #log
                                                    delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime)
                                                    print(16)
                                                    pass

                                                elif vrifiy1=="Valid" and chi=="True" and compony==True:
                                                    #log
                                                    delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime)
                                                    print(17)
                                                    pass
                                            
                                                elif vrifiy1=="Valid" and chi=="True" and compony_name==False:
                                                    print("resit + alert")
                                                    print(18)
                                                    if go==1:
                                                        if not_loop==0:
                                                            ms=f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block
'''
                                                            toast = Notification(
                                                            app_id="FS Notification",
                                                            title="Delete Firewall Rule Alert",
                                                            msg=ms)
                                                            
                                                            toast.show()
                                                            for _ in range(2):
                                                                winsound.Beep(2000, 300)  
                                                                time.sleep(0.2)
                                                            email_notif(pro_name,pro_path,"DELETEING RULE","BLOCK",user_email) 

                                                    
                                                    with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                                        f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                    if go==2:
                                                            ms=f'''
There is a new firewall rule deleted by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program
'''
                                                            pid=int(pid)
                                                            process = psutil.Process(pid)
                                                            parent_name = process.name()
                                                            parent_path = process.exe()
                                                            if parent_path==pro_path and parent_name==pro_name:
                                                                process = psutil.Process(pid)
                                                                process.kill()
                                                            toast = Notification(
                                                            app_id="FS Notification",
                                                            title="Delete Firewall Rule Alert",
                                                            msg=ms)
                                                            
                                                            toast.show()
                                                            for _ in range(2):
                                                                winsound.Beep(2000, 300)  
                                                                time.sleep(0.2)
                                                            email_notif(pro_name,pro_path,"DELETEING RULE","KILL PROGRAM + BLOCK",user_email) 

                                                        # Kill Process
                                                        # delete the rule from the file
                                                    go=1
                                                    addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                                    poewrshell(addrule)
                                                    delete_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,rtime)
                                        pro=1       

                                        
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                eds=settings["edit_wait"]
                            if eds == "0":
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
                                            Direction1=check_state(Direction1,"Direction")

                                            Action1=iz["Action"]
                                            Action1=check_state(Action1,"Action")

                                            Profile1=iz["Profile"]
                                            Profile1=check_state(Profile1,"Profile")

                                            Enabled1=iz["Enabled"]
                                            Enabled1=check_state(Enabled1,"Enabled")

                                            Protocol1=iz["Protocol"]
                                            LocalPort1=iz["LocalPort"]
                                            LocalPort1=str(LocalPort1)
                                            RemotePort1=iz["RemotePort"]
                                            IPScope1=iz["IPScope"]

                                    for i in firelight:
                                        if i not in firecopy:

                                
                                            Direction=i["Direction"]
                                            Direction=check_state(Direction,"Direction")

                                            Action=i["Action"]
                                            Action=check_state(Action,"Action")

                                            Profile=i["Profile"]
                                            Profile=check_state(Profile,"Profile")

                                            Enabled=i["Enabled"]
                                            Enabled=check_state(Enabled,"Enabled")

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
                                                        if Program=="System" or "WINDOWS\system" in Program or Program!=Program1:
                                                            print("resit + alert")
                                                            if not_loop==0:
                                                                ms=f'''
There is a new firewall rule modified by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block
'''
                                                                toast = Notification(
                                                                app_id="FS Notification",
                                                                title="Modify Firewall Rule Alert",
                                                                msg=ms)
                                                                toast.show()
                                                                for _ in range(2):
                                                                    winsound.Beep(2000, 300)  
                                                                    time.sleep(0.2)
                                                                email_notif("UNKNOWN","UNKNOWN","MODIFING RULE","BLOCK",user_email)
                                                                    
                                                            with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                                f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                                        
                                                                # not_loop=1
                                                            
                                                            if ii.lower() in ["direction","action","profile","enabled","displayName"]:
                                                                if ii.lower() in ["direction","action","profile","enabled"]:
                                                                    w=check_state(i[ii],ii)
                                                                    poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} {w}\n')
                                                                    
                                                                else:
                                                                    poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} "{i[ii]}"\n')
                                                                    w=i[ii]
                                                                    
                                                            elif ii.lower() in ["protocol","localPort","remotePort"]:
                                                                poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallPortFilter | Set-NetFirewallPortFilter -{ii} {i[ii]}\n')
                                                                w=i[ii]
                                                            elif ii.lower() == "program":
                                                                poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallApplicationFilter | Set-NetFirewallApplicationFilter -Program "{i[ii]}"\n')
                                                                w=i[ii]
                                                            modefiy_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,ii,w,rtime)



                                                        else:    
                                                            ricor=rs.risk_score_modify_not_vrifiy(Action,Direction,Protocol,LocalPort,IPScope,Action1,Direction1,Protocol1,LocalPort1,IPScope1)
                                                            if ricor <= 85 :
                                                                # Allow + Log
                                                                print("allow + log")
                                                                pass
                                                            
                                                            elif ricor <= 120 or ricor <= 180 or ricor>181:
                                                                # Block + Alert
                                                                print("block + alert")
                                                                
                                                                if not_loop==0:
                                                                    ms=f'''
There is a new firewall rule modified by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block
'''
                                                                    toast = Notification(
                                                                    app_id="FS Notification",
                                                                    title="Modify Firewall Rule Alert",
                                                                    msg=ms)
                                                                    
                                                                    toast.show()
                                                                    for _ in range(2):
                                                                        winsound.Beep(2000, 300)  
                                                                        time.sleep(0.2)
                                                                    
                                                                    email_notif("UNKNOWN","UNKNOWN","MODIFING RULE","BLOCK",user_email)    
                                                                with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                                            
                                                                    # not_loop=1
                                                                if ii.lower() in ["direction","action","profile","enabled","displayName"]:
                                                                    if ii.lower() in ["direction","action","profile","enabled"]:
                                                                        w=check_state(i[ii],ii)
                                                                        poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} {w}\n')
                                                                        
                                                                    else:
                                                                        poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} "{i[ii]}"\n')
                                                                        w=i[ii]
                                                                elif ii.lower() in ["protocol","localPort","remotePort"]:
                                                                    poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallPortFilter | Set-NetFirewallPortFilter -{ii} {i[ii]}\n')
                                                                    w=i[ii]
                                                                elif ii.lower() == "program":
                                                                    poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallApplicationFilter | Set-NetFirewallApplicationFilter -Program "{i[ii]}"\n')
                                                                    w=i[ii]
                                                            modefiy_rule_logs("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,ii,w,rtime)

                                                    if pro==1:
                                                        print(1)
                                                        path = f'''(Get-AuthenticodeSignature "{pro_path}").Status'''
                                                        vrifiy1, error = poewrshell(path)

                                                        if whi_ls==True:
                                                            vrifiy1="Valid"
                                                        
                                                        tre=rf'(Get-AuthenticodeSignature "{pro_path}").SignerCertificate.GetNameInfo("SimpleName",$false)'
                                                        compony_name,error=poewrshell(tre)
                                                        if compony_name=="":
                                                            compony_name="unknwon"

                                                        security_vendors = ["Microsoft","Microsoft Corporation","Windows Defender","Microsoft Defender","Symantec","Symantec Corporation","Norton","NortonLifeLock","Gen Digital","Broadcom","Broadcom Inc","McAfee","McAfee LLC","McAfee Corp","Trellix","FireEye","FireEye Inc","Kaspersky","Kaspersky Lab","Kaspersky Labs","Kaspersky Lab ZAO","ESET","ESET spol","ESET, spol. s r.o.","Avast","Avast Software","AVG","AVG Technologies","Avira","Avira GmbH","Bitdefender","Bitdefender SRL","Sophos","Sophos Ltd","Sophos Group","Trend Micro","Trend Micro Inc","Malwarebytes","Malwarebytes Inc","Panda","Panda Security","F-Secure","F-Secure Corporation","WithSecure","G Data","G Data Software","Comodo","Comodo Security","Xcitium","ZoneAlarm","Check Point","Check Point Software","Webroot","Webroot Inc","Fortinet","Fortinet Inc","CrowdStrike","CrowdStrike Inc","CrowdStrike Holdings","SentinelOne","SentinelOne Inc","Carbon Black","CarbonBlack","VMware Carbon Black","Cisco","Cisco Systems","Elastic","Elastic NV","Cybereason","Cybereason Inc","SecureWorks","Secureworks Inc","Quick Heal","QuickHeal","Seqrite","K7 Computing","K7 Security","TotalAV","Protected.net"]
                                                        for vendor in security_vendors:
                                                            if compony_name.lower()==vendor.lower():
                                                                compony=True
                                                                break
                                                            else:
                                                                compony=False
                                                                break

                                                        if (compony_name=="Microsoft Windows" and Program =="System") or (compony_name=="Microsoft Windows" and "WINDOWS\system" in Program) or (compony==True and Program =="System") or (compony==True and "WINDOWS\system" in Program):
                                                            #Log
                                                            if ii.lower() in ["direction","action","profile","enabled"]:
                                                                w=check_state(i[ii],ii)
                                                            else:
                                                                w=i[ii]
                                                            modefiy_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime)
                                                        elif (compony_name!="Microsoft Windows" and Program =="System") or (compony_name!="Microsoft Windows" and "WINDOWS\system" in Program) or (compony==False and Program =="System") or (compony==False and "WINDOWS\system" in Program):
                                                            # Block + Alert + log
                                                            print("resit + alert")
                                                            
                                                            if go==1:
                                                                if not_loop==0:
                                                                    ms=f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block
'''
                                                                    toast = Notification(
                                                                    app_id="FS Notification",
                                                                    title="Modify Firewall Rule Alert",
                                                                    msg=ms)
                                                                    not_loop=1
                                                                    toast.show()
                                                                    for _ in range(2):
                                                                        winsound.Beep(2000, 300)  
                                                                        time.sleep(0.2)
                                                                    email_notif(pro_name,pro_path,"MODIFING RULE","BLOCK",user_email)
                                                                    
                                                            # if not_loop==0:
                                                                
                                                            with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                                f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                            # not_loop=1
                                                            if go==2:
                                                                    ms=f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program
'''
                                                                # if not_loop==0:
                                                                    pid=int(pid)
                                                                    process = psutil.Process(pid)
                                                                    parent_name = process.name()
                                                                    parent_path = process.exe()
                                                                    if parent_path==pro_path and parent_name==pro_name:
                                                                        process = psutil.Process(pid)
                                                                        process.kill()
                                                                    # not_loop=1
                                                                    toast = Notification(
                                                                    app_id="FS Notification",
                                                                    title="Modify Firewall Rule Alert",
                                                                    msg=ms)
                                                                    
                                                                    toast.show()
                                                                    for _ in range(2):
                                                                        winsound.Beep(2000, 300)  
                                                                        time.sleep(0.2)
                                                                    email_notif(pro_name,pro_path,"MODIFING RULE","KILL PROGRAM + BLOCK",user_email)
                                                                # Kill Process
                                                                # delete the rule from the file
                                                            go=1
                                                            if ii.lower() in ["direction","action","profile","enabled","displayName"]:
                                                                if ii.lower() in ["direction","action","profile","enabled"]:
                                                                    w=check_state(i[ii],ii)
                                                                    poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} {w}\n')
                                                                    
                                                                else:
                                                                    poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} "{i[ii]}"\n')
                                                                    w=i[ii]
                                                            elif ii.lower() in ["protocol","localPort","remotePort"]:
                                                                poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallPortFilter | Set-NetFirewallPortFilter -{ii} {i[ii]}\n')
                                                                w=i[ii]
                                                            elif ii.lower() == "program":
                                                                poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallApplicationFilter | Set-NetFirewallApplicationFilter -Program "{i[ii]}"\n')
                                                                w=i[ii]
                                                            modefiy_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime)

                                                        else:
                                                            print(2)
                                                            
                                                            if whi_ls:

                                                                print("allow + log") 

                                                            elif compony_name.lower() in Program.lower():
                                                                #log
                                                                print(3)
                                                                pass
                                                            

                                                            elif vrifiy1!="Valid":
                                                                print(4)
                                                                print("resit + alert")
                                                        
                                                                if go==1:
                                                                    if not_loop==0:
                                                                        ms=f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block
'''
                                                                        toast = Notification(
                                                                        app_id="FS Notification",
                                                                        title="Modify Firewall Rule Alert",
                                                                        msg=ms)
                                                                        # not_loop=1
                                                                        toast.show()
                                                                        for _ in range(2):
                                                                            winsound.Beep(2000, 300)  
                                                                            time.sleep(0.2)
                                                                        email_notif(pro_name,pro_path,"MODIFING RULE","BLOCK",user_email)
                                                                
                                                                # if not_loop==0:   
                                                                with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                                # not_loop=1
                                                                if go==2:
                                                                        ms=f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program
'''
                                                                    # if not_loop==0:
                                                                        pid=int(pid)
                                                                        process = psutil.Process(pid)
                                                                        parent_name = process.name()
                                                                        parent_path = process.exe()
                                                                        if parent_path==pro_path and parent_name==pro_name:
                                                                            process = psutil.Process(pid)
                                                                            process.kill()
                                                                        # not_loop=1
                                                                        toast = Notification(
                                                                        app_id="FS Notification",
                                                                        title="Modify Firewall Rule Alert",
                                                                        msg=ms)
                                                                        
                                                                        toast.show()
                                                                        for _ in range(2):
                                                                            winsound.Beep(2000, 300)  
                                                                            time.sleep(0.2)
                                                                        email_notif(pro_name,pro_path,"MODIFING RULE","KILL PROGRAM + BLOCK",user_email)
                                                                    # Kill Process
                                                                    # delete the rule from the file
                                                                go=1
                                                                if ii.lower() in ["direction","action","profile","enabled","displayName"]:
                                                                    if ii.lower() in ["direction","action","profile","enabled"]:
                                                                        w=check_state(i[ii],ii)
                                                                        poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} {w}\n')
                                                                        
                                                                    else:
                                                                        poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} "{i[ii]}"\n')
                                                                        
                                                                elif ii.lower() in ["protocol","localPort","remotePort"]:
                                                                    poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallPortFilter | Set-NetFirewallPortFilter -{ii} {i[ii]}\n')
                                                                    
                                                                elif ii.lower() == "program":
                                                                    poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallApplicationFilter | Set-NetFirewallApplicationFilter -Program "{i[ii]}"\n')

                                                            
                                                            
                                                            elif vrifiy1=="Valid" and compony==True:
                                                                #log
                                                                print(5)
                                                                pass
                                                            
                                                            elif (vrifiy1=="Valid" and compony==False) and (Action=="Block" or Direction=="Inbound" or Enabled=="True" or Enabled=="False" or Direction=="Outbound" or Action=="Allow" or Program1!=Program):
                                                                # check the program if it is the same 
                                                                #log
                                                                print(6)
                                                                print("resit + alert")
                                                        
                                                                if go==1:
                                                                    if not_loop==0:
                                                                        ms=f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block
'''
                                                                        toast = Notification(
                                                                        app_id="FS Notification",
                                                                        title="Modify Firewall Rule Alert",
                                                                        msg=ms)
                                                                        # not_loop=1
                                                                        toast.show()
                                                                        for _ in range(2):
                                                                            winsound.Beep(2000, 300)  
                                                                            time.sleep(0.2)
                                                                        email_notif(pro_name,pro_path,"MODIFING RULE","BLOCK",user_email)
                                                                
                                                                # if not_loop==0:   
                                                                with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                                    f.write(pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction+"\n")
                                                                    # not_loop=1
                                                                if go==2:
                                                                        ms=f'''
There is a new firewall rule modified by:
Program Name: {pro_name}
Program Path: {pro_path}
Action: Block + Kill Program
'''
                                                                    # if not_loop==0:
                                                                        pid=int(pid)
                                                                        process = psutil.Process(pid)
                                                                        parent_name = process.name()
                                                                        parent_path = process.exe()
                                                                        if parent_path==pro_path and parent_name==pro_name:
                                                                            process = psutil.Process(pid)
                                                                            process.kill()
                                                                        # not_loop=1
                                                                        toast = Notification(
                                                                        app_id="FS Notification",
                                                                        title="Modify Firewall Rule Alert",
                                                                        msg=ms)
                                                                        
                                                                        toast.show()
                                                                        for _ in range(2):
                                                                            winsound.Beep(2000, 300)  
                                                                            time.sleep(0.2)
                                                                            
                                                                        email_notif(pro_name,pro_path,"MODIFING RULE","KILL PROGRAM + BLOCK",user_email)
                                                                    # Kill Process
                                                                    # delete the rule from the file
                                                                go=1
                                                                if ii.lower() in ["direction","action","profile","enabled","displayName"]:
                                                                    if ii.lower() in ["direction","action","profile","enabled"]:
                                                                        w=check_state(i[ii],ii)
                                                                        poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} {w}\n')
                                                                        
                                                                    else:
                                                                        poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} "{i[ii]}"\n')
                                                                        w=i[ii]
                                                                elif ii.lower() in ["protocol","localPort","remotePort"]:
                                                                    poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallPortFilter | Set-NetFirewallPortFilter -{ii} {i[ii]}\n')
                                                                    w=i[ii]
                                                                elif ii.lower() == "program":
                                                                    poewrshell(f'Get-NetFirewallRule -Name "{Name}" | Get-NetFirewallApplicationFilter | Set-NetFirewallApplicationFilter -Program "{i[ii]}"\n')
                                                                    w=i[ii]
                                                            modefiy_rule_logs(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime)


                                                    pro=1 


            th.Thread(target=thp).start()
            #keys to contrule
            l=1
            ll=1
            ed=0
            tr=0
            #function to conn to the seconed conn in the server
            def clos_fw():
                
                global ll,tr,ta,ta1,block,ere,pro,go,deleteR
                ll=0
                c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
                c.connect((ip, 9991))
                c.sendall("client".encode())
                while True:
                    try:
                        
                        #the orders that admenstretor want to run
                        close=c.recv(1024).decode('utf-8')
                        tr=1
                        if close=="off":
                            poewrshell(r"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False")
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["FWS"]="off-all"
                                settings["timerF"]="0"
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                        elif close=="on":
                            poewrshell(r"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["FWS"]="null"
                                settings["timerF"]="0"
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                        time.sleep(0.1)
                        tr=0
                    except Exception:
                        
                        continue



            #function to check the D:\FS-File\settings.json evry 10s
            async def check_files():
                global fws,ip,timer,rule,rulename,timerr,ips,constan,deleteR,enaply,disaply,mac,tr,ta,ta1,block,ere,pro,go
                
                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    

                    check=settings["IP-S"]
                    
                    ip = check
                        
                    ips=settings["IP-U"]

                    rowFWS=["on","off","null"]
                    check4=settings["FWS"]
                    
                    deleteR=settings["deleteR"]

                    if check4 in rowFWS:
                        fws= check4
                            
                        

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



                    enaply=settings["Enaply list"]
                    disaply=settings["Disaply list"]
                    
                        
                    
                    
                        

                    

                        
            #function to close the firewall
            def do_ruls():
                global l,tr,ta,ta1,block,ere,pro,go,deleteR
                if fws=="off" and l==1:
                    l=0
                    tr=1
                    fs.fireOff(fws,timer)
                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        settings["FWS"]="null"
                        settings["timerF"]="0"
                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(settings,f,indent=4)
                    l=1
                    time.sleep(0.1)
                    tr=0
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
                    

            while True:
                
                # #the main function that contrule in evry things
                async def main():
                    # pass
                    global l,ll,email_rvs,ips,email_rvs,ips,constan,rule,disaply,enaply,mac,ed,tr,ta,ta1,block,ere,pro,go,deleteR
                    
                    if ll==1:
                        #run the seconed conn function
                        th.Thread(target=clos_fw).start()
                    #run the check D:\FS-File\settings.json function
                    sa.gather(check_files())
                    
                    
                    await sa.sleep(0)
                    #check order from user
                    if fws=="off" and l==1:
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
                        l=1
                        time.sleep(0.1)
                        tr=0
                    #check if the firewall state is off without the user send any ordurs
                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        check=settings["FWS"]
                    if check=="null":
                        a=poewrshell(r'"Get-NetFirewallProfile | Select-Object Enabled"')
                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                firews=settings["FWS"]
                                firews=str(firews)
                        #run the belwo code if firewall is off without the user send any ordurs to return firewall on   
                        if "False" in a and firews=="null" :
                            tr=1
                            poewrshell(r'Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True')
                            #send to server to add to the csv file
                            c.sendall("hackOff".encode())
                            c.recv(1024).decode()
                            ips=str(ips)
                            c.sendall(ips.encode())
                            c.recv(1024).decode()
                            c.sendall(mac.encode())
                            check1=c.recv(1024).decode()
                            check1=check1.replace("1","")
                            check1=check1.strip()
                            time.sleep(0.1)
                            tr=0
                            if check1=="issue FWS.csv" or check1=="issue FWS.csv1":
                                
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
                            #send email to the user
                            msg= EmailMessage()
                            msg["Subject"]=f"Detect stop attempt - ID({str(uuid.uuid4())[:8]})"
                            msg["From"]="aofnotification@gmail.com"
                            msg["To"]=email_rvs
                            msg.set_content(f"your firewall state has been off,we rutern it to be open.\nTurn off the network to check if your device has been hacked or not")
                            email="aofnotification@gmail.com"
                            password="oqgspkawnyeftyjw"
                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                smtp.login(email,password)
                                smtp.send_message(msg)


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


                    if enaply !=[] :
                        ed=1
                        def enaply_action():
                            global enaply,ed,ta,ta1,block,ere,pro,go,deleteR
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                enaply=list(enaply)
                                enaply1=enaply.pop(0)
                                settings["Enaply list"]=enaply
                                settings["edit_wait"]="1"
                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4) 

                            action="e"
                            z=enaply1.index("wevall")
                            z=z+6
                            ruletype=enaply1[z:]
                            enaply1=enaply1.replace(enaply1[z:],"")
                            enaply1=enaply1.replace("wevall","")

                            if enaply1.endswith("m") or enaply1.endswith("h"):
                                z=enaply1.index("^")
                                bb=enaply1[z:]
                                aa=enaply1.replace(bb,"")
                                bb=bb.replace("^","")
                                if bb.endswith("m"):
                                    lens=len(bb)
                                    bb=bb[:lens-1]
                                    bb=int(bb)
                                    bb*=60
                                    bb=str(bb)
                                    


                                elif bb.endswith("h"):
                                    lens=len(bb)
                                    bb=bb[:lens-1]
                                    bb=int(bb)
                                    bb*=3600
                                    bb=str(bb)
                                

                            fs.action_rule(bb,aa,action,ruletype)
                            ed=1
                            time.sleep(0.1)
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                if settings["edit_wait"]=="1":
                                    settings["edit_wait"]="0"
                                    with open(r"C:\FS-File\settings.json", 'w',encoding='utf-8') as f:
                                        json.dump(settings,f,indent=4)
                        th.Thread(target=enaply_action).start()
                    


                    if disaply !=[] :
                        ed=1
                        def disaply_action():
                            global disaply,ed,ta,ta1,block,ere,pro,go,deleteR
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                disaply=list(disaply)
                                disaply1=disaply.pop(0)
                                settings["Disaply list"]=disaply
                                settings["edit_wait"]="1"
                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4) 
                            action="d"
                            z=disaply1.index("wevall")
                            z=z+6
                            ruletype=disaply1[z:]
                            disaply1=disaply1.replace(disaply1[z:],"")
                            disaply1=disaply1.replace("wevall","")

                            if disaply1.endswith("m") or disaply1.endswith("h"):
                                z=disaply1.index("^")
                                bb=disaply1[z:]
                                aa=disaply1.replace(bb,"")
                                bb=bb.replace("^","")
                                if bb.endswith("m"):
                                    lens=len(bb)
                                    bb=bb[:lens-1]
                                    bb=int(bb)
                                    bb*=60
                                    bb=str(bb)
                                    


                                elif bb.endswith("h"):
                                    lens=len(bb)
                                    bb=bb[:lens-1]
                                    bb=int(bb)
                                    bb*=3600
                                    bb=str(bb)
                                

                            fs.action_rule(bb,aa,action,ruletype)
                            ed=1
                            time.sleep(0.1)
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                if settings["edit_wait"]=="1":
                                    settings["edit_wait"]="0"
                                    with open(r"C:\FS-File\settings.json", 'w',encoding='utf-8') as f:
                                        json.dump(settings,f,indent=4)
                        th.Thread(target=disaply_action).start()

                #run the main function
                sa.run(main())
                
                #return to do this loop evry 10s
                print(1)
                time.sleep(5)
                if ed==1:
                    poewrshell(ta)
                    time.sleep(0.1)
                    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        if settings["edit_wait"]=="1":
                            settings["edit_wait"]="0"
                            with open(r"C:\FS-File\settings.json", 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4)
                    ed=0
                    
        # except Exception:
        #     print("error")
        #     continue