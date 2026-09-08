import time
import subprocess as su
import threading as th
import json
import smtplib
from email.message import EmailMessage
import os
import uuid
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
import socket as sk
import fireSett as fs
import pandas as pd
import struct
import shutil
import asyncio



F_L=r'''$rules = Get-NetFirewallRule
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




F_C=r'''$rules = Get-NetFirewallRule
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

block1=0
block2=1
block3=1
block4=0
block5=1  
block6=1
block7=1

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
        pass


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


def Add_rule_log(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,rule,white_list,black_l):
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
            "Black_list":["Black_list"],# انقل ده لي النسخه المكتمله
            "TIME":["TIME"]
        }

        d=pd.DataFrame(datafrme)
        d.to_csv(r"C:\FS-File\Security_Events\Add_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


    datafrme={
            "IP":[ip_user],
            "MAC":[mac_user],
            "Program_Name":[pro_name],
            "Program_Path":[pro_path],
            "DisplayName":[DisplayName],
            "Name":[Name],
            "RULE":[rule],
            "TIMER":["NULL"],
            "Permanent":["NO"],# get for it a new name
            "White_list":[white_list],
            "Black_list":[black_l],
            "TIME":[str(time.strftime('%Y-%m-%d %H:%M:%S'))]
        }

    d=pd.DataFrame(datafrme)
    try:
        d.to_csv(r"C:\FS-File\Security_Events\Add_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    except Exception:
        pass


def Delete_rule_log(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,white_list):
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
            "IP":[ip_user],
            "MAC":[mac_user],
            "Program_Name":[pro_name],
            "Program_Path":[pro_path],
            "white list":[white_list],
            "DisplayName":[DisplayName],
            "Name":[Name],
            "TIME":[str(time.strftime('%Y-%m-%d %H:%M:%S'))]
        }

    d=pd.DataFrame(datafrme)
    try:
        d.to_csv(r"C:\FS-File\Security_Events\Delete_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    except Exception:
        pass



def State_rule_log(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,ii,gema,white_list):
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
            "IP":[ip_user],
            "MAC":[mac_user],
            "Program_Name":[pro_name],
            "Program_Path":[pro_path],
            "white list":[white_list],
            "DisplayName":[DisplayName],
            "Name":[Name],
            "Component":[ii],
            "NewValue":[gema],
            "TIME":[str(time.strftime('%Y-%m-%d %H:%M:%S'))]
        }

    d=pd.DataFrame(datafrme)
    try:
        d.to_csv(r"C:\FS-File\Security_Events\State_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    except Exception:
        pass



def Add_Rule_Tamper(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,Direction,Action,Profile,Enabled,Protocol,LocalPort,RemotePort,Program,T,white_list):
    try:
        s=pd.read_csv(r"C:\FS-File\Security_Events\Add_Rule_Tamper.csv") 
    except Exception:
        print("error: Add_Rule_Tamper()1")
        datafrme={
            "IP":["IP"],
            "MAC":["MAC"],
            "Program_Name":["Program_Name"],
            "Program_Path":["Program_Path"],
            "white list":["white list"],
            "DisplayName":["DisplayName"],
            "Name":["Name"],
            "Direction":["Direction"],
            "Action":["Action"],
            "Profile":["Profile"],
            "Enabled":["Enabled"],
            "Protocol":["Protocol"],
            "LocalPort":["LocalPort"],
            "RemotePort":["RemotePort"],
            "Program":["Program"],
            "TIME":["TIME"]
        }

        s=pd.DataFrame(datafrme)
        s.to_csv(r"C:\FS-File\Security_Events\Add_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    datafrme={
            "IP":[ip_user],
            "MAC":[mac_user],
            "Program_Name":[pro_name],
            "Program_Path":[pro_path],
            "white list":[white_list],
            "DisplayName":[DisplayName],
            "Name":[Name],
            "Direction":[Direction],
            "Action":[Action],
            "Profile":[Profile],
            "Enabled":[Enabled],
            "Protocol":[Protocol],
            "LocalPort":[LocalPort],
            "RemotePort":[RemotePort],
            "Program":[Program],
            "TIME":[T]
        }

    d=pd.DataFrame(datafrme)
    try:
        d.to_csv(r"C:\FS-File\Security_Events\Add_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    except Exception:
        print("error: Add_Rule_Tamper()2")
        pass



def Delete_Rule_Tamper(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,T,white_list):
    try:
        s=pd.read_csv(r"C:\FS-File\Security_Events\Delete_Rule_Tamper.csv") 
    except Exception:
        print("error: Delete_Rule_Tamper()1")
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

        s=pd.DataFrame(datafrme)
        s.to_csv(r"C:\FS-File\Security_Events\Delete_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    datafrme={
            "IP":[ip_user],
            "MAC":[mac_user],
            "Program_Name":[pro_name],
            "Program_Path":[pro_path],
            "white list":[white_list],
            "DisplayName":[DisplayName],
            "Name":[Name],
            "TIME":[T]
        }

    d=pd.DataFrame(datafrme)
    try:
        d.to_csv(r"C:\FS-File\Security_Events\Delete_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    except Exception:
        print("error: Delete_Rule_Tamper()2")
        pass


def Modified_Rule_Tamper(pro_name,pro_path,ip_user,mac_user,DisplayName,Name,ii,gema,T,white_list ):
    
    try:
        s=pd.read_csv(r"C:\FS-File\Security_Events\Modified_Rule_Tamper.csv") 
    except Exception:
        print("error: Modified_Rule_Tamper()1")
        datafrme={
            "IP":["IP"],
            "MAC":["MAC"],
            "Program_Name":["Program_Name"],
            "Program_Path":["Program_Path"],
            "white list":["white list"],
            "DisplayName":["DisplayName"],
            "Name":["Name"],
            "Modified item":["Modified item"],
            "New value":["New value"],
            "TIME":["TIME"]
        }

        s=pd.DataFrame(datafrme)
        s.to_csv(r"C:\FS-File\Security_Events\Modified_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    datafrme={
            "IP":[ip_user],
            "MAC":[mac_user],
            "Program_Name":[pro_name],
            "Program_Path":[pro_path],
            "white list":[white_list],
            "DisplayName":[DisplayName],
            "Name":[Name],
            "Modified item":[ii],
            "New value":[gema],
            "TIME":[T]
        }

    d=pd.DataFrame(datafrme)
    try:
        d.to_csv(r"C:\FS-File\Security_Events\Modified_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
    except Exception:
        print("error: Modified_Rule_Tamper()2")
        pass



def fssl():
    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        ip_s=settings["IP-S"]
        n_m=settings["MAC"]
        emai=settings["email"]
        settings["IP-S"]="null"
        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
            json.dump(settings,f,indent=4)

        

        TEMP_NAME = f"{n_m} (FSSL)"

        async def send_folder(folder_path: str, host: str = '127.0.0.1', port: int = 9992):
            folder_path   = os.path.abspath(folder_path)
            src_dir       = os.path.dirname(folder_path)
            temp_dir      = os.path.join(src_dir, TEMP_NAME)
            temp_zip_base = os.path.join(src_dir, TEMP_NAME)
            temp_zip      = temp_zip_base + '.zip'

            # ── Step 1: Copy folder with temp name ───────────────────────────────────
            shutil.copytree(folder_path, temp_dir)
            print(f"[*] Folder copied  → {temp_dir}")

            try:
                # ── Step 2: Compress temp folder → ZIP ───────────────────────────────
                shutil.make_archive(temp_zip_base, 'zip', src_dir, TEMP_NAME)
                print(f"[*] Archive created → {temp_zip}")

            finally:
                # ── Step 3: Delete temp folder (zip is enough now) ───────────────────
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    print(f"[*] Temp folder deleted → {temp_dir}")

            # ── Step 4: Send ZIP ──────────────────────────────────────────────────────
            try:
                reader, writer = await asyncio.open_connection(host, port)

                try:
                    ready = await reader.read(1)
                    if ready != b'1':
                        raise ConnectionError(f"Unexpected server signal: {ready!r}")

                    filename   = TEMP_NAME + '.zip'
                    name_bytes = filename.encode('utf-8')
                    file_size  = os.path.getsize(temp_zip)

                    writer.write(struct.pack('>I', len(name_bytes)))
                    writer.write(name_bytes)
                    writer.write(struct.pack('>Q', file_size))
                    await writer.drain()

                    with open(temp_zip, 'rb') as f:
                        while chunk := f.read(65536):
                            writer.write(chunk)
                            await writer.drain()

                    resp = await reader.read(3)
                    if resp == b'OK':
                        print(f"[+] Folder sent successfully ({file_size:,} bytes)")
                    else:
                        print(f"[-] Server error: {resp!r}")

                finally:
                    writer.close()
                    await writer.wait_closed()

            finally:
                # ── Step 5: Delete ZIP ────────────────────────────────────────────────
                if os.path.exists(temp_zip):
                    os.remove(temp_zip)
                    print(f"[*] Temp ZIP deleted → {temp_zip}")


            msg= EmailMessage()
            msg["Subject"]=f"Identity verification - ID({str(uuid.uuid4())[:8]})"
            msg["From"]="aofnotification@gmail.com"
            msg["To"]=emai
            msg.set_content(f"Your folder has send sussfully.\n\n\nSecurity System:\nFS System")
            email="aofnotification@gmail.com"
            password="oqgspkawnyeftyjw"
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(email,password)
                smtp.send_message(msg)

        asyncio.run(send_folder(r"C:\FS-File\Security_Events", host=ip_s))




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

            poewrshell(F_L)

            block1=0

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

            poewrshell(F_L)

            block1=0

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

    

def do_ruls():
    global block7,block1,F_L,F_C,block5,block4,block3,block2,deleteR
    if fws=="off" and block7==1:
        block7=0
        block1=1
        fs.fireOff(fws,timer)
        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            settings["FWS"]="null"
            settings["timerF"]="0"
            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                json.dump(settings,f,indent=4)
        block7=1
        time.sleep(0.1)
        block1=0



def add__rule():
    # make a prameter for timerr and rulename
    global rulename,timerr,block1,F_L,F_C,block5,block4,block3,block2,deleteR
    
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
    block1=1
    poewrshell(f'Remove-NetFirewallRule -DisplayName "{rulename}"')

    
    poewrshell(F_L)
    with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        v=settings["checkrulename"]
        v=list(v)        
        v.remove(rulename)
        settings["checkrulename"]=v
        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
            json.dump(settings,f,indent=4)
    time.sleep(0.1)   
    block1=0 



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



with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f) 

    if settings["IP-S"]!="null":
        settings["IP-S"]="null"
        
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



pathfile=os.path.exists(r"C:\FS-File\email_ids.txt")
if pathfile==False:
    with open(r"C:\FS-File\email_ids.txt","w",encoding='utf-8')as f:
        f.write("")



with open(r"C:\FS-File\loop.txt","w",encoding='utf-8')as f:
    f.write("")



with open(r"C:\FS-File\loop-2.txt","w",encoding='utf-8')as f:
    f.write("")

        

with open(r"C:\FS-File\loop-3.txt","w",encoding='utf-8')as f:
    f.write("")



try:
    result, error = poewrshell("Get-NetAdapter | Select-Object MacAddress")
    result = ''.join(list(result))
    mac_list = [lmac.strip() for lmac in result.splitlines() if "-" in lmac]
    mac = mac_list[-1] if mac_list else "null"
except Exception:
    print("error: mac")
    mac = "null"
    
try:
    try:
        server=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
        server.connect(("1.1.1.1",80))
        ips=server.getsockname()[0]
        server.close()
    except Exception:
        print("error: ip1")
        
        server=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
        server.connect(("8.8.8.8",443))
        ips=server.getsockname()[0]
        server.close()
except Exception:
    print("error: ip2")
    ips="null"
    
with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f)
    settings["IP-U"] =ips
    settings["MAC"] =mac
    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
        json.dump(settings, f, indent=4)




a,error=poewrshell('Get-NetFirewallProfile | Select-Object Enabled')
a=list(a)
a=''.join(a)

# a=a.stdout  
if "false" in a.lower(): 
    poewrshell(r"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")


poewrshell(F_L)


#find a way to rexequded if it close
#############################
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

pp = su.Popen(
    ["powershell", "-NoProfile", "-Command", ps_script],
    stdout=su.PIPE,
    stderr=su.PIPE,
    text=True,
    bufsize=1)

#############################


def mal_dit():
    global parent_name,chick_vil,F_L,F_C,block5,block4,block3,block2,deleteR
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

                            #check this code
                            #######################
                            if is_target_process(name) and is_firewall_related(cmd_line, name) and parent_name == "powershell.exe":
                                if parent_path in TRUSTED_POWERSHELL_PATHS:
                                    block5 = 0
                                else:
                                    block5 = 1  # powershell من مسار غير موثوق = مشبوه
                            #######################

                            #make a thread to speed the detaction
                            #######################
                            elif is_target_process(name) and is_firewall_related(cmd_line, name) and parent_name!="python.exe":
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

                            #######################

                            
            except Exception as e:
                print("error: mal_dit()")
                time.sleep(1)

    finally:
        pythoncom.CoUninitialize()


th.Thread(target=mal_dit).start()



risk_engine = AdvancedRiskEngine()
start_baseline_updater(risk_engine)






def thp():
    try:
       
        global block1,pp,output,error,F_L,F_C,block5,block4,block3,block2,deleteR,block6
        
        for linep in iter(pp.stdout.readline, ''):
            linep = linep.strip()

             # استدعاء المعلومات المهمه مره واحده فقط
            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                ips=settings["IP-U"]
                mac=settings["MAC"]
                user_email=settings["email"]
                fws=settings["FWS"]
    
            # استدعاء اوقات ساعات العمل
            with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                _s = json.load(f)
                _work_start = _s.get("work_start", 8)
                _work_end   = _s.get("work_end",   18)
                _work_days  = _s.get("work_days",  [0,1,2,3,4])
                
            
            if linep:
                rtime=str(time.strftime('%Y-%m-%d %H:%M:%S'))

                if "2082" in linep and block1==0:
                    

                    if fws=="null":
                        a=poewrshell('Get-NetFirewallProfile | Select-Object Enabled')
                        a=list(a)
                        a=''.join(a)
                        # rembmber to add notifcations of email popup notfiy
                        if "False" in a:
                            poewrshell('Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True')
                            ms = f'''
There is a new firewall rule added by:
Program Name: UNKNOWN
Program Path: UNKNOWN
Action: Block 
                '''
                            toast = Notification(app_id="FS Notification",
                                                title="Add Firewall Rule Alert", msg=ms)
                            toast.show()
                            for _ in range(2):
                                winsound.Beep(2000, 300)
                                time.sleep(0.2)
                            try:
                                s=pd.read_csv(r"C:\FS-File\Security_Events\Firewall_Tamper.csv") 
                            except Exception:
                                datafrme={
                                    "IP":["IP"],
                                    "MAC":["MAC"],
                                    "STATE":["STATE"],
                                    "TIME":["TIME"]
                                }

                                s=pd.DataFrame(datafrme)
                                s.to_csv(r"C:\FS-File\Security_Events\Firewall_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                            datafrme={
                                    "IP":[ips],
                                    "MAC":[mac],
                                    "STATE":["off"],
                                    "TIME":[rtime]
                                }

                            d=pd.DataFrame(datafrme)
                            try:
                                d.to_csv(r"C:\FS-File\Security_Events\Firewall_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                            except Exception:
                                pass
                            
                            

                if ("2004" in linep or "2005" in linep or "2006" in linep or "2097" in linep or "2099" in linep or "2052" in linep)and (block1==0):
                    op1=0
                    op=0
                    if block6==1:
                        output, error =poewrshell(F_C)
                        
                    
                    
                        while True:
                            try:
                                with open(r"C:\FS-File\firewallcopy.json", "r", encoding="utf-8-sig") as fc:
                                    firecopy = json.load(fc)
                                    break
                            except Exception:
                                print("error: thp=1")
                                continue

                        with open(r"C:\FS-File\firewall_light.json", "r", encoding="utf-8-sig") as f:
                            firelight = json.load(f)
                        

                        for i in firelight:
                            if i not in firecopy:
                                op=1

                        for i in firecopy:
                            if i not in firelight:
                                op1=1
                    # اتاكد هل كده بتمنع مني اني انشء او افوت احداث مهمه
                    
                    if (op==0 and op1==0) and (block6==1):
                        def end():
                            global block6
                            block6=0
                            time.sleep(3)
                            block6=1
                        th.Thread(target=end).start()

                    
                    if op==0 and op1==1:
                        not_loop=0
                        if block5==0:
                            toast = Notification(
                            app_id="Security Tool",
                            title="Firewall Alert",
                            msg="Unknown program tried to modify firewall rules.")
                            
                            toast.show()
                            for _ in range(2):
                                winsound.Beep(2000, 300)  
                                time.sleep(0.2)
                            block5=1

                        #   ["path_proName_PID"] بتفاعل لو ما كان في اي قيمه في 
                        try:
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                
                                ppp=settings["path_proName_PID"]
                                if ppp=="":
                                    block4=1
                                # فصلتهم عشان لو ما لقيت مسار البرنامج
                                # اما التحت لو لقيت اسم البرنامج
                                else:
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
                                        # اتاكد هل كل الاماكن الفيها البرنامج مضمون هل الكود بيتجدد
                                         # انا حاسي انو ما اخير اختها هنا عشان اقدر اشوف خطوره القاعده
                                    else:
                                        whi_ls=False

                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                        json.dump(settings,f,indent=4) 
                        
                        except Exception:
                            print("error: thp=2")
                            block4=1


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

                                # انقل ده و عناصره لي النسخه المكتمله
                                rule=["New-NetFirewallRule"]
                                rule.append(f" -DisplayName {DisplayName}")
                                rule.append(f" -Name {Name}")
                                rule.append(f" -Action {Action}")
                                rule.append(f" -Direction {Direction}")
                                rule.append(f" -Enabled {Enabled}")
                                rule.append(f" -Profile {Profile}")
                                rule.append(f" -Protocol {Protocol}")
                                rule.append(f" -LocalPort {LocalPort}")
                                rule.append(f" -Remoteport {RemotePort}")
                                rule.append(f' -Program "{Program}"')
                                rule=''.join(rule)

                                # if not_loop==0:

                                try:
                                    with open(r"C:\FS-File\loop.txt", "r",encoding='utf-8') as f:
                                        loop=f.readlines()
                                        l=0
                                        for line in loop:
                                            if pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                                l+=1
                                                block2=0
                                                not_loop=1
                                            if l==2:
                                                block2=2
                                                break
                                except Exception:
                                    pass    


                                if block4==1:
                                    block3=0
                                    # ── اقرأ صلاحيات العملية من الإعدادات
                                    with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                        _s = json.load(f)
                                        _role = _s.get("user_role", "UNKNOWN")

                                    if Program=="System" or "WINDOWS\\system" in Program:
                                        chick_vil="Valid"

                                    elif Program!="":# انا اضفت دي عشان مرات بيكون البرنامج مافي
                                        chick_vil="UnknownError" # -غيرها لي -غير معروف 

                                    elif Program!="Any":
                                        path = f'''(Get-AuthenticodeSignature "{Program}").Status'''
                                        chick_vil, error = poewrshell(path)
                                        # عشان امنع لو البرنامج ما كان موجود
                                        if error:
                                            chick_vil="UnknownError"

                                        else:
                                            chick_vil=list(chick_vil)
                                            chick_vil=''.join(chick_vil)


                                    else: #check
                                       
                                        chick_vil="Any"

                                    # ── النظام المتقدم بدل rs.risk_score_add_*
                                    result = risk_engine.calculate(
                                        operation    = "ADD",
                                        mac          = mac,
                                        signature    = chick_vil.strip() if chick_vil!="Any" else "NotSigned",# ابحث عن معنى السطر ده
                                        action       = Action,
                                        direction    = Direction,
                                        protocol     = Protocol,
                                        port         = LocalPort,
                                        ip_scope     = IPScope,
                                        user_role    = _role,
                                        timestamp    = time.time(),
                                        program_path = "UNKNOWN", # اضافه جديده
                                        work_start   = _work_start,   # ← جديد
                                        work_end     = _work_end,     # ← جديد
                                        work_days    = _work_days     # ← جديد
                                    )
                                    ricor      = result["score"]
                                    risk_level = result["risk_level"]
                                    patterns   = result["triggered_patterns"]

                                    # if whi_ls:
                                    #     Add_Rule_Tamper("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,
                                    #                 Direction,Action,Profile,Enabled,Protocol,
                                    #                 LocalPort,RemotePort,Program,rtime,"NO")  
                                    #     poewrshell(F_L)


                                    # اضيف جزء جديد يعبر عن حاله خطوره القاعده بالشكل البيخرجه النظام
                                    if risk_level == "LOW":#     جديد      
                                        Add_rule_log("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rule,"NO","NO")
                                        poewrshell(F_L)
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                            settings = json.load(f)
                                            settings["BL_Rule_Check"]=bl
                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4) 

                                        th.Thread(target=black_list).start()
                                    # لي شنو انا خليت ميديم يقدر يضيف قاعده
                                    # شيل الجزء الخاص يانشاء ملف ملف الفيروول لاني ما عارف اسم و مسار البرنامج الحصل على ميديم
                                    elif risk_level == "MEDIUM":# جديد
                                        Add_rule_log("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rule,"NO","NO")
                                        poewrshell(F_L)
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                            settings = json.load(f)
                                            settings["BL_Rule_Check"]=bl
                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4) 

                                        th.Thread(target=black_list).start()

                                    elif risk_level in ("HIGH", "CRITICAL"):
                                        # ابحث هل ممكن قاعده عادي ما يكون عندها name
                                        poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                        # if not_loop==0:
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
                                        Add_Rule_Tamper("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,
                                                    Direction,Action,Profile,Enabled,Protocol,
                                                    LocalPort,RemotePort,Program,rtime,"NO")
                                

                                
                                if block3==1:
                                    path = f'''(Get-AuthenticodeSignature "{pro_path}").Status'''
                                    vrifiy1, error = poewrshell(path)
                                    # عشان امنع لو البرنامج ما كان موجود
                                    if error:
                                        vrifiy1="UnknownError"

                                    else:
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
                                        Add_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,rule,"YES","NO")
                                        poewrshell(F_L)

                                    elif risk_level == "LOW":
                                        Add_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,rule,"NO","NO")  
                                        poewrshell(F_L)
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                            settings = json.load(f)
                                            settings["BL_Rule_Check"]=bl
                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4) 

                                        th.Thread(target=black_list).start()

                                    elif risk_level == "MEDIUM":
                                        Add_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,rule,"NO","NO")  
                                        poewrshell(F_L)
                                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                            settings = json.load(f)
                                            settings["BL_Rule_Check"]=bl
                                            with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                                json.dump(settings,f,indent=4) 

                                        th.Thread(target=black_list).start()



                                    elif risk_level == "HIGH":
                                        

                                        pat_str = ", ".join(patterns) if patterns else "HIGH RISK"
                                        if block2==1 and not_loop==0:
                                            poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
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

                                        # اضيفها لي الباقين
                                        if block2==2:

                                            pat_str = ", ".join(patterns) if patterns else "HIGH RISK"
                                            try:
                                                _pid = int(pid)
                                                _proc = psutil.Process(_pid)
                                                if _proc.exe()==pro_path and _proc.name()==pro_name:
                                                    _proc.kill()
                                            except Exception:
                                                print("error: thp=3")
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
                                            
                                        block2=1
                                        
                                        Add_Rule_Tamper(pro_name,pro_path,ips,mac,DisplayName,Name,
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
                                            print("error: thp=3")
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
                                        Add_Rule_Tamper(pro_name,pro_path,ips,mac,DisplayName,Name,
                                                    Direction,Action,Profile,Enabled,Protocol,
                                                    LocalPort,RemotePort,Program,rtime,"NO")

                                        
                                block3=1    
                            
                            

                    if op==1 and op1==0:
                        not_loop=0
                        if block5==0:
                            toast = Notification(
                            app_id="Security Tool",
                            title="Firewall Alert",
                            msg="Unknown program tried to modify firewall rules.")
                            
                            toast.show()
                            for _ in range(2):
                                winsound.Beep(2000, 300)  
                                time.sleep(0.2)
                            block5=1

                        try:
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                
                                ppp=settings["path_proName_PID"]
                                if ppp=="":
                                    block4=1

                                else:
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
                            print("error: thp=4")
                            block4=1


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

                                try:

                                    with open(r"C:\FS-File\loop-2.txt", "r",encoding='utf-8') as f:
                                        loop=f.readlines()
                                        l=0
                                        for line in loop:
                                            if pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                                l+=1
                                                block2=0
                                                not_loop=1
                                            if l==2:
                                                block2=2
                                                break

                                except Exception:
                                    pass


                                if block4==1:
                                    block3=0
                                    # ── اقرأ الصلاحيات
                                    with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                        _s = json.load(f)
                                        _role = _s.get("user_role", "UNKNOWN")

                                  
                                    # ── signature للبرنامج المرتبط بالقاعدة المحذوفة
                                    if Program == "System" or "WINDOWS\\system" in Program:
                                        _sig = "Valid"

                                    elif Program == "":
                                        _sig = "UnknownError"

                                    elif Program != "Any": 
                                        _sig_raw, error = poewrshell(f'(Get-AuthenticodeSignature "{Program}").Status')

                                        if error:
                                            _sig = "UnknownError"

                                        else:    
                                            _sig = ''.join(list(_sig_raw)).strip()
                                    else:#check
                                        _sig = "Any"

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
                                        Delete_rule_log("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,"NO")
                                        poewrshell(F_L)

                                    elif risk_level == "MEDIUM":
                                        Delete_rule_log("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,"NO")
                                        poewrshell(F_L)

                                    elif risk_level in ("HIGH", "CRITICAL"):

                                            addrule = (f'New-NetFirewallRule -DisplayName "{DisplayName}"'
                                            f' -Name "{Name}" -Direction {Direction}'
                                            f' -Action {Action} -Profile {Profile}'
                                            f' -Enabled {Enabled} -Protocol {Protocol}'
                                            f' -LocalPort {LocalPort} -RemotePort {RemotePort}'
                                            f' -Program "{Program}"')
                                            poewrshell(addrule)

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

                                        
                                            Delete_Rule_Tamper("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,rtime,"NO")



                                if block3==1:
                                    # ── التوقيع
                                    # vrifiy1= .....
                                    path = f'(Get-AuthenticodeSignature "{pro_path}").Status'
                                    vrifiy1, error = poewrshell(path)
                                    if error:
                                        vrifiy1 = "UnknownError"

                                    else:    
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
                                        Delete_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,"YES")
                                        poewrshell(F_L)

                                    elif risk_level == "LOW":
                                        Delete_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,"NO")
                                        poewrshell(F_L)

                                    elif risk_level == "MEDIUM":
                                        Delete_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,"NO")
                                        poewrshell(F_L)

                                    elif risk_level == "HIGH":
                                        pat_str = ", ".join(patterns) if patterns else "HIGH RISK"
                                        if block2 == 1 and not_loop == 0:
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

                                        if block2 == 2:
                                            try:
                                                _pid = int(pid)
                                                _proc = psutil.Process(_pid)
                                                if _proc.exe() == pro_path and _proc.name() == pro_name:
                                                    _proc.kill()
                                            except Exception:
                                                print("error: thp=5")
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

                                        block2 = 1
                                        addrule = (f'New-NetFirewallRule -DisplayName "{DisplayName}"'
                                                    f' -Name "{Name}" -Direction {Direction}'
                                                    f' -Action {Action} -Profile {Profile}'
                                                    f' -Enabled {Enabled} -Protocol {Protocol}'
                                                    f' -LocalPort {LocalPort} -RemotePort {RemotePort}'
                                                    f' -Program "{Program}"')
                                        poewrshell(addrule)
                                        Delete_Rule_Tamper(pro_name,pro_path,ips,mac,DisplayName,Name,rtime,"NO")

                                    elif risk_level == "CRITICAL":
                                        pat_str = ", ".join(patterns) if patterns else "CRITICAL"
                                        try:
                                            _pid = int(pid)
                                            _proc = psutil.Process(_pid)
                                            if _proc.exe() == pro_path and _proc.name() == pro_name:
                                                _proc.kill()
                                        except Exception:
                                            print("error: thp=6")
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
                                        Delete_Rule_Tamper(pro_name,pro_path,ips,mac,DisplayName,Name,rtime,"NO")

                                    block3 = 1     

                                
                    # with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                    #     settings = json.load(f)
                    #     eds=settings["edit_wait"]
                    # if eds == "0":
                    if block1==0:
                        if op==1 and op1==1:

                            if block5==0:
                                toast = Notification(
                                app_id="Security Tool",
                                title="Firewall Alert",
                                msg="Unknown program tried to modify firewall rules.")
                                
                                toast.show()
                                for _ in range(2):
                                    winsound.Beep(2000, 300)  
                                    time.sleep(0.2)
                                block5=1


                            not_loop=0
                            try:
                                                
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    
                                    ppp=settings["path_proName_PID"]
                                    if ppp=="":
                                        block4=1

                                    else:
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
                                print("error: thp=7")
                                block4=1


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

                                            try:

                                                with open(r"C:\FS-File\loop-3.txt", "r",encoding='utf-8') as f:
                                                    loop=f.readlines()
                                                    l=0
                                                    for line in loop:
                                                        if pro_name+pro_path+Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                                            l+=1
                                                            block2=0
                                                            not_loop=1
                                                        if l==2:
                                                            block2=2
                                                            break

                                            except Exception:
                                                pass


                                            if block4==1:
                                                block3=0

                                                # ── اقرأ الصلاحيات
                                                with open(r'C:\FS-File\settings.json', 'r', encoding='utf-8') as f:
                                                    _s = json.load(f)
                                                    _role = _s.get("user_role", "UNKNOWN")

                                                # ── حدد signature بناءً على البرنامج المرتبط بالقاعدة
                                                if Program == "System" or "WINDOWS\\system" in Program:
                                                    _sig = "Valid"

                                                elif Program == "":
                                                    _sig = "UnknownError"

                                                elif Program != "Any":
                                                    _sig_raw, error = poewrshell(
                                                        f'(Get-AuthenticodeSignature "{Program}").Status'
                                                    )

                                                    if error:
                                                        _sig = "UnknownError"
                                                    else:
                                                        _sig = ''.join(list(_sig_raw)).strip()

                                                    
                                                else:#check
                                                    _sig = "Any"

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
                                                    poewrshell(F_L)
                                                    w = _revert_modify()
                                                    State_rule_log("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,ii,w,"NO")

                                                elif risk_level == "MEDIUM":
                                                    poewrshell(F_L)
                                                    w = _revert_modify()
                                                    State_rule_log("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,ii,w,"NO")

                                                elif risk_level in ("HIGH", "CRITICAL"):
                                                    # if not_loop == 0:
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
                                                    Modified_Rule_Tamper("UNKNOWN","UNKNOWN",ips,mac,DisplayName,Name,ii,w,rtime,"NO")


                                            if block3==1:
                                                path = f'(Get-AuthenticodeSignature "{pro_path}").Status'
                                                vrifiy1, error = poewrshell(path)

                                                if error: 
                                                    vrifiy1 = "UnknownError"

                                                else:
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
                                                    State_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,"YES")
                                                    poewrshell(F_L)

                                                elif risk_level == "LOW":
                                                    w = i[ii] if ii in i else ""
                                                    State_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,"NO")
                                                    poewrshell(F_L)

                                                elif risk_level == "MEDIUM":
                                                    w = i[ii] if ii in i else ""
                                                    State_rule_log(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,"NO")
                                                    poewrshell(F_L)

                                                elif risk_level == "HIGH":
                                                    pat_str = ", ".join(patterns) if patterns else "HIGH RISK"
                                                    if block2 == 1 and not_loop == 0:
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

                                                    if block2 == 2:
                                                        try:
                                                            _pid = int(pid)
                                                            _proc = psutil.Process(_pid)
                                                            if _proc.exe() == pro_path and _proc.name() == pro_name:
                                                                _proc.kill()
                                                        except Exception:
                                                            print("error: thp=8")
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

                                                    block2 = 1
                                                    w = _revert_modify_pro()
                                                    Modified_Rule_Tamper(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime,"NO")

                                                elif risk_level == "CRITICAL":
                                                    pat_str = ", ".join(patterns) if patterns else "CRITICAL"
                                                    try:
                                                        _pid = int(pid)
                                                        _proc = psutil.Process(_pid)
                                                        if _proc.exe() == pro_path and _proc.name() == pro_name:
                                                            _proc.kill()
                                                    except Exception:
                                                        print("error: thp=9")
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
                                                    Modified_Rule_Tamper(pro_name,pro_path,ips,mac,DisplayName,Name,ii,w,rtime,"NO")

                                                block3 = 1
    except Exception:
        print("error: thp()")
        block1=0
        block2=1
        block3=1
        block4=0
        block5=1  
        block6=1
        th.Thread(target=thp).start()

th.Thread(target=thp).start()

print("yes")
with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:

    settings = json.load(f)
    while True:
        try:


            class Handler(FileSystemEventHandler):
                def on_modified(self, event):
                    global fws,ip,timer,rule,rulename,timerr,ips,constan,deleteR,modify_rule,mac,block1,F_L,F_C,block5,block4,block3,block2,block7,ll,email_rvs,ips,ips,constan,rule,modify_rule,mac,block1,F_L,F_C,block5,block4,block3,block2,deleteR,bossemail,user_email

                    if r"C:\FS-File\settings.json" in event.src_path:
                        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)

         

                            ip=settings["IP-S"]


                            if ip !="null":
                                th.Thread(target=fssl).start()


                            user_email=settings["email"]
                            email_rvs=user_email
                            
                            ips=settings["IP-U"]
                            
                            fws=settings["FWS"]
                            
                            deleteR=settings["deleteR"]

                          
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
                        
                        
                        #check order from user
                        if fws=="off" and block7==1:
                            #run close firewall function
                            th.Thread(target=do_ruls).start()
                        elif fws=="on":
                            #open firewall
                            block1=1
                            poewrshell(r"Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["FWS"]="null"
                                settings["timerF"]="0"
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            block7=1
                            time.sleep(0.1)
                            block1=0
                        
                        #delete rule from the firewall
                        if deleteR!="null":
                            block1=1
                            z=deleteR.index("wevall")
                            z=z+6
                            ruletype=deleteR[z:]
                            deleteR=deleteR.replace(deleteR[z:],"")
                            deleteR=deleteR.replace("wevall","")
                            
                            poewrshell(f'Remove-NetFirewallRule -{ruletype} "{deleteR}"')
                            
                            poewrshell(F_L)
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["deleteR"]="null"
                                
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            time.sleep(0.1)
                            block1=0


                        #add rule to the firewall 
                        if rule!="null":
                            
                            if constan=="yes":
                                block1=1
                                poewrshell(rule)

                                poewrshell(F_L)
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    settings["Rolue"]="null"
                                    settings["constan"]="no"
                                    
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                                time.sleep(0.1)
                                block1=0

                            elif constan=="no":
                                block1=1
                                poewrshell(rule)
                                
                                poewrshell(F_L)
                                
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                        settings = json.load(f)
                                        settings["Rolue"]="null"
                                        settings["constan"]="no"
                                        
                                        with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                            json.dump(settings,f,indent=4)

                                        time.sleep(0.1)
                                        block1=0
                                #run add rules function
                                th.Thread(target=add__rule).start()


                        if modify_rule !="null" :
                            block1=1
                            poewrshell(modify_rule)
                            poewrshell(F_L)
                            
                            with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["modify_rule"]="null"
                                with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            block1=0
                
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
            print("error: on_modified()")
            block1=0
            continue