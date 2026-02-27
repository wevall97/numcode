import subprocess as su
import json
import risk_score as rs
import wmi
import threading as th
import time
import pythoncom
from winotify import Notification
import winsound
import time
import os
import psutil
go=1
pro=1
ere=0
block=1

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
    global parent_name,chick_vil,block
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

                            elif is_target_process(name) and is_firewall_related(cmd_line, name) and parent_name=="ruleChecker.exe":
                                print("jr")
                                path = f'''(Get-AuthenticodeSignature "{parent_path}").Status'''
                                chick_vil, error = poewrshell(path)
                                print(chick_vil.strip())   
                                print(parent_name)
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    

                                    s=settings["path_proName_PID"]
                                    s=list(s)
                                    parent_pid=str(parent_pid)
                                    s.append(parent_pid+"+"+parent_name+"$"+parent_path)
                                    settings["path_proName_PID"]=s

                                    s=settings["white list checker"]
                                    s=list(s)
                                    s.append(parent_name+parent_path)
                                    settings["white list checker"]=s

                                    with open(r"C:\FS-File\settings.json", 'w',encoding='utf-8') as f:
                                        json.dump(settings,f,indent=4)

            except Exception as e:
                print("WMI error:", e)
                time.sleep(1)

    finally:
        pythoncom.CoUninitialize()

        


th.Thread(target=mal_dit).start()




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
poewrshell(ta)              

print(1)
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

for linep in iter(pp.stdout.readline, ''):
    linep = linep.strip()
    
    if linep:
        if "FW_EVENT:" in linep:

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
}) | ConvertTo-Json -Depth 3 | Out-File "C:\FS-File\firewallcopy.json" -Encoding utf8
'''
            poewrshell(ta)            
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
                
                print("gg")
                for i in firelight:
                    if i not in firecopy:
                        op=1

                for i in firecopy:
                    if i not in firelight:
                        op1=1


                if op==0 and op1==1:

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

                    for i in firecopy:
                        if i not in firelight:
                            DisplayName=i["DisplayName"]
                            
                            Direction=i["Direction"]
                            Direction=check_state(Direction,"Direction")

                            Action=i["Action"]
                            Action=check_state(Action,"Action")

                            Profile=i["Profile"]
                            Profile=check_state(Profile,"Profile")

                            Protocol=i["Protocol"]

                            LocalPort=i["LocalPort"]
                            LocalPort=str(LocalPort)

                            Program=i["Program"]
                            IPScope=i["IPScope"]
                            with open(r"C:\FS-File\loop.txt", "r",encoding='utf-8') as f:
                                loop=f.readlines()
                                l=0
                                for line in loop:
                                    if Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                        l+=1
                                        go=0
                                    if l==2:
                                        go=2
                                        break

                            try:
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    
                                    ppp=settings["path_proName_PID"]
                                    ppp=list(ppp)
                                    ppp1=ppp.pop(0)
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
                                    whitelist=list(whitelist)
                                    whi_ls=whitelist.pop(0)
                                    settings["white list checker"]=whitelist

                                    if whi_ls in settings["white list"]:
                                        whi_ls=True
                                    else:
                                        whi_ls=False

                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                        json.dump(settings,f,indent=4) 
                            
                            except Exception:
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
                                    print("allow + log")
                                    pass
                                
                                elif ricor <= 120 or ricor <= 180 or ricor>181:
                                    # Block + Alert
                                    poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                    print("block + alert")
                                    
                                    
                                    toast = Notification(
                                    app_id="Security Tool",
                                    title="Firewall Alert",
                                    msg="Unknown program tried to modify firewall rules.")
                                    
                                    toast.show()
                                    for _ in range(2):
                                        winsound.Beep(2000, 300)  
                                        time.sleep(0.2)
                                    
                                        
                                    with open(r"C:\FS-File\loop.txt", "+a",encoding='utf-8') as f:
                                        f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                               
                            if pro==1:
                                path = f'''(Get-AuthenticodeSignature "{pro_path}").Status'''
                                vrifiy1, error = poewrshell(path)
                                if whi_ls==True:
                                    vrifiy1="Valid"
                                ricor=rs.risk_score_add_vrifiy(vrifiy1.strip(),Action,Direction,Protocol,LocalPort,IPScope)
                                

                                if ricor <= 85 :
                                    # Allow + Log
                                    print("allow + log")
                                    pass
                                
                                elif ricor <= 120:
                                    # Block + Alert
                                    print("block + alert")
                                    
                                    if go==1:
                                        toast = Notification(
                                        app_id="Security Tool",
                                        title="Firewall Alert",
                                        msg="Unknown program tried to modify firewall rules.")
                                        
                                        toast.show()
                                        for _ in range(2):
                                            winsound.Beep(2000, 300)  
                                            time.sleep(0.2)
                                    
                                        
                                    with open(r"C:\FS-File\loop.txt", "+a",encoding='utf-8') as f:
                                        f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                    if go==2:
                                      
                                        pid=int(pid)
                                        process = psutil.Process(pid)
                                        parent_name = process.name()
                                        parent_path = process.exe()
                                        if parent_path==pro_path and parent_name==pro_name:
                                            process = psutil.Process(pid)
                                            process.kill()
                                        
                                        toast = Notification(
                                        app_id="Security Tool",
                                        title="Firewall Alert",
                                        msg="Unknown program tried to modify firewall rules.")
                                        
                                        toast.show()
                                        for _ in range(2):
                                            winsound.Beep(2000, 300)  
                                            time.sleep(0.2)
                                        # Kill Process
                                        # delete the rule from the file
                                    go=1
                                    poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')


                                elif ricor <= 180 or ricor>181:
                                    #Block + Kill Process + Alert
                                    
                                    pid=int(pid)
                                    process = psutil.Process(pid)
                                    parent_name = process.name()
                                    parent_path = process.exe()
                                    if parent_path==pro_path and parent_name==pro_name:
                                        process = psutil.Process(pid)
                                        process.kill()

                                    poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                                    print("block + alert + kill process")
                                    toast = Notification(
                                    app_id="Security Tool",
                                    title="Firewall Alert",
                                    msg="Unknown program tried to modify firewall rules.")
                                    
                                    toast.show()
                                    for _ in range(2):
                                        winsound.Beep(2000, 300)  
                                        time.sleep(0.2)


                                    
                            pro=1    
                        
                        

                if op==1 and op1==0:

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
                            with open(r"C:\FS-File\loop-2.txt", "r",encoding='utf-8') as f:
                                loop=f.readlines()
                                l=0
                                for line in loop:
                                    if Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                        l+=1
                                        go=0
                                    if l==2:
                                        go=2
                                        break

                            try:
                                with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    
                                    ppp=settings["path_proName_PID"]
                                    ppp=list(ppp)
                                    ppp1=ppp.pop(0)
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
                                    whitelist=list(whitelist)
                                    whi_ls=whitelist.pop(0)
                                    settings["white list checker"]=whitelist

                                    if whi_ls in settings["white list"]:
                                        whi_ls=True
                                    else:
                                        whi_ls=False
                                    with open(r'C:\FS-File\settings.json', 'w',encoding='utf-8') as f:
                                        json.dump(settings,f,indent=4) 
                            
                            except Exception:
                                print(10)
                                pro=0
                                chi,error=poewrshell(rf'Test-Path "{Program}"')
                                ricor=rs.risk_score_delete_not_vrifiy(DisplayName+" "+Name,Program,Action,Direction,Protocol,LocalPort,IPScope,chi.strip())
                                if ricor=="Block":
                                  

                                    addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                    poewrshell(addrule)
                                    print("block + alert + kill process")
                                    toast = Notification(
                                    app_id="Security Tool",
                                    title="Firewall Alert",
                                    msg="Unknown program tried to modify firewall rules.")
                                    
                                    toast.show()
                                    for _ in range(2):
                                        winsound.Beep(2000, 300)  
                                        time.sleep(0.2)


                                  
                                elif ricor <= 85 :
                                    # Allow + Log
                                    print("allow + log")
                                    pass
                                elif ricor <= 120 or ricor <= 180 or ricor>181:
                                    # Block + Alert
                                    print("block + alert")
                                    
                                    
                                    toast = Notification(
                                    app_id="Security Tool",
                                    title="Firewall Alert",
                                    msg="Unknown program tried to modify firewall rules.")
                                    
                                    toast.show()
                                    for _ in range(2):
                                        winsound.Beep(2000, 300)  
                                        time.sleep(0.2)
                                    
                                        
                                    with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                        f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                    addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                    poewrshell(addrule)


                                



                            if pro==1:
                                path = f'''(Get-AuthenticodeSignature "{pro_path}").Status'''
                                vrifiy1, error = poewrshell(path)

                                if whi_ls==True:
                                    vrifiy1="Valid"
                                tr=rf'(Get-AuthenticodeSignature "{pro_path}").SignerCertificate.GetNameInfo("SimpleName",$false)'
                                compony_name,error=poewrshell(tr)
                                if compony_name=="":
                                    compony_name="unknwon"
                                if Program!="System":
                                    chi,error=poewrshell(rf'Test-Path "{Program}"')


                                if (compony_name=="Microsoft Windows" and Program =="System") or (compony_name=="Microsoft Windows" and "WINDOWS\system" in Program):
                                    #Log
                                    print(11)
                                    pass
                                elif (compony_name!="Microsoft Windows" and Program =="System") or (compony_name!="Microsoft Windows" and "WINDOWS\system" in Program):
                                    # Block + Alert + log
                                    print("resit + alert")
                                    print(12)
                                    if go==1:
                                        toast = Notification(
                                        app_id="Security Tool",
                                        title="Firewall Alert",
                                        msg="Unknown program tried to modify firewall rules.")
                                        
                                        toast.show()
                                        for _ in range(2):
                                            winsound.Beep(2000, 300)  
                                            time.sleep(0.2)
                                    
                                        
                                    with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                        f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                    if go==2:
                                       
                                        pid=int(pid)
                                        process = psutil.Process(pid)
                                        parent_name = process.name()
                                        parent_path = process.exe()
                                        if parent_path==pro_path and parent_name==pro_name:
                                            process = psutil.Process(pid)
                                            process.kill()
                                        
                                        toast = Notification(
                                        app_id="Security Tool",
                                        title="Firewall Alert",
                                        msg="Unknown program tried to modify firewall rules.")
                                        
                                        toast.show()
                                        for _ in range(2):
                                            winsound.Beep(2000, 300)  
                                            time.sleep(0.2)
                                        # Kill Process
                                        # delete the rule from the file
                                    go=1
                                    addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                    poewrshell(addrule)

                                

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

                                    if compony_name.lower()in Program.lower():
                                        #log
                                        print(compony_name)
                                        print(14)
                                        # pass
                                    
                                    


                                    elif vrifiy1!="Valid":
                                        
                                        print("resit + alert")
                                        print(15)
                                        if go==1:
                                            toast = Notification(
                                            app_id="Security Tool",
                                            title="Firewall Alert",
                                            msg="Unknown program tried to modify firewall rules.")
                                            
                                            toast.show()
                                            for _ in range(2):
                                                winsound.Beep(2000, 300)  
                                                time.sleep(0.2)
                                        
                                            
                                        with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                            f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                        if go==2:
                                            
                                            pid=int(pid)
                                            process = psutil.Process(pid)
                                            parent_name = process.name()
                                            parent_path = process.exe()
                                            if parent_path==pro_path and parent_name==pro_name:
                                                process = psutil.Process(pid)
                                                process.kill()
                                            
                                            toast = Notification(
                                            app_id="Security Tool",
                                            title="Firewall Alert",
                                            msg="Unknown program tried to modify firewall rules.")
                                            
                                            toast.show()
                                            for _ in range(2):
                                                winsound.Beep(2000, 300)  
                                                time.sleep(0.2)
                                            # Kill Process
                                            # delete the rule from the file
                                        go=1
                                        addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                        poewrshell(addrule)
                                        
                                    
                                    
                                    elif vrifiy1=="Valid" and chi=="False":
                                        #log
                                        print(16)
                                        pass

                                    elif vrifiy1=="Valid" and chi=="True" and compony==True:
                                        #log
                                        print(17)
                                        pass
                                
                                    elif vrifiy1=="Valid" and chi=="True" and compony_name==False:
                                        print("resit + alert")
                                        print(18)
                                
                                        if go==1:
                                            toast = Notification(
                                            app_id="Security Tool",
                                            title="Firewall Alert",
                                            msg="Unknown program tried to modify firewall rules.")
                                            
                                            toast.show()
                                            for _ in range(2):
                                                winsound.Beep(2000, 300)  
                                                time.sleep(0.2)
                                        
                                            
                                        with open(r"C:\FS-File\loop-2.txt", "+a",encoding='utf-8') as f:
                                            f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                        if go==2:
                                            
                                            pid=int(pid)
                                            process = psutil.Process(pid)
                                            parent_name = process.name()
                                            parent_path = process.exe()
                                            if parent_path==pro_path and parent_name==pro_name:
                                                process = psutil.Process(pid)
                                                process.kill()
                                            
                                            toast = Notification(
                                            app_id="Security Tool",
                                            title="Firewall Alert",
                                            msg="Unknown program tried to modify firewall rules.")
                                            
                                            toast.show()
                                            for _ in range(2):
                                                winsound.Beep(2000, 300)  
                                                time.sleep(0.2)
                                            # Kill Process
                                            # delete the rule from the file
                                        go=1
                                        addrule=f'New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                                        poewrshell(addrule)
                            pro=1       

                            
                
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
                            ppp=list(ppp)
                            ppp1=ppp.pop(0)
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
                            whitelist=list(whitelist)
                            whi_ls=whitelist.pop(0)
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

                                    if not_loop==0:
                                        with open(r"C:\FS-File\loop-3.txt", "r",encoding='utf-8') as f:
                                            loop=f.readlines()
                                            l=0
                                            for line in loop:
                                                if Program+LocalPort+Protocol+Profile+Action+Direction==line.strip():
                                                    l+=1
                                                    go=0
                                                if l==2:
                                                    go=2
                                                    break

                                    if ere==1:
                                        pro=0
                                        if Program=="System" or "WINDOWS\system" in Program or Program!=Program1:
                                            print("resit + alert")
                                            
                                            if not_loop==0:
                                                toast = Notification(
                                                app_id="Security Tool",
                                                title="Firewall Alert",
                                                msg="Unknown program tried to modify firewall rules.")
                                                
                                                toast.show()
                                                for _ in range(2):
                                                    winsound.Beep(2000, 300)  
                                                    time.sleep(0.2)
                                                
                                                    
                                                with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                    f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                           
                                            not_loop=1
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
                                                    toast = Notification(
                                                    app_id="Security Tool",
                                                    title="Firewall Alert",
                                                    msg="Unknown program tried to modify firewall rules.")
                                                    
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)  
                                                        time.sleep(0.2)
                                                    
                                                        
                                                    with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                        f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                              
                                                not_loop=1
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


                                    if pro==1:
                                        print(1)
                                        path = f'''(Get-AuthenticodeSignature "{pro_path}").Status'''
                                        vrifiy1, error = poewrshell(path)

                                        if whi_ls==True:
                                            vrifiy1="Valid"
                                        
                                        tr=rf'(Get-AuthenticodeSignature "{pro_path}").SignerCertificate.GetNameInfo("SimpleName",$false)'
                                        compony_name,error=poewrshell(tr)
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
                                            pass
                                        elif (compony_name!="Microsoft Windows" and Program =="System") or (compony_name!="Microsoft Windows" and "WINDOWS\system" in Program) or (compony==False and Program =="System") or (compony==False and "WINDOWS\system" in Program):
                                            # Block + Alert + log
                                            print("resit + alert")
                                            
                                            if go==1:
                                                if not_loop==0:
                                                    toast = Notification(
                                                    app_id="Security Tool",
                                                    title="Firewall Alert",
                                                    msg="Unknown program tried to modify firewall rules.")
                                                    
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)  
                                                        time.sleep(0.2)
                                            if not_loop==0:
                                                
                                                with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                    f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                            if go==2:
                                                
                                                if not_loop==0:
                                                    pid=int(pid)
                                                    process = psutil.Process(pid)
                                                    parent_name = process.name()
                                                    parent_path = process.exe()
                                                    if parent_path==pro_path and parent_name==pro_name:
                                                        process = psutil.Process(pid)
                                                        process.kill()
                                                    
                                                    toast = Notification(
                                                    app_id="Security Tool",
                                                    title="Firewall Alert",
                                                    msg="Unknown program tried to modify firewall rules.")
                                                    
                                                    toast.show()
                                                    for _ in range(2):
                                                        winsound.Beep(2000, 300)  
                                                        time.sleep(0.2)
                                                # Kill Process
                                                # delete the rule from the file
                                            go=1
                                            not_loop=1
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

                                        

                                        else:
                                            print(2)
                                            

                                            if compony_name.lower() in Program.lower():
                                                #log
                                                print(3)
                                                pass
                                            

                                            elif vrifiy1!="Valid":
                                                print(4)
                                                print("resit + alert")
                                        
                                                if go==1:
                                                    if not_loop==0:
                                                        toast = Notification(
                                                        app_id="Security Tool",
                                                        title="Firewall Alert",
                                                        msg="Unknown program tried to modify firewall rules.")
                                                        
                                                        toast.show()
                                                        for _ in range(2):
                                                            winsound.Beep(2000, 300)  
                                                            time.sleep(0.2)
                                                
                                                if not_loop==0:   
                                                    with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                        f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                                if go==2:
                                                    
                                                    if not_loop==0:
                                                        pid=int(pid)
                                                        process = psutil.Process(pid)
                                                        parent_name = process.name()
                                                        parent_path = process.exe()
                                                        if parent_path==pro_path and parent_name==pro_name:
                                                            process = psutil.Process(pid)
                                                            process.kill()
                                                        
                                                        toast = Notification(
                                                        app_id="Security Tool",
                                                        title="Firewall Alert",
                                                        msg="Unknown program tried to modify firewall rules.")
                                                        
                                                        toast.show()
                                                        for _ in range(2):
                                                            winsound.Beep(2000, 300)  
                                                            time.sleep(0.2)
                                                    # Kill Process
                                                    # delete the rule from the file
                                                go=1
                                                not_loop=1
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
                                                        toast = Notification(
                                                        app_id="Security Tool",
                                                        title="Firewall Alert",
                                                        msg="Unknown program tried to modify firewall rules.")
                                                        
                                                        toast.show()
                                                        for _ in range(2):
                                                            winsound.Beep(2000, 300)  
                                                            time.sleep(0.2)
                                                
                                                if not_loop==0:   
                                                    with open(r"C:\FS-File\loop-3.txt", "+a",encoding='utf-8') as f:
                                                        f.write(Program+LocalPort+Protocol+Profile+Action+Direction+"\n")

                                                if go==2:
                                                    
                                                    if not_loop==0:
                                                        pid=int(pid)
                                                        process = psutil.Process(pid)
                                                        parent_name = process.name()
                                                        parent_path = process.exe()
                                                        if parent_path==pro_path and parent_name==pro_name:
                                                            process = psutil.Process(pid)
                                                            process.kill()
                                                        
                                                        toast = Notification(
                                                        app_id="Security Tool",
                                                        title="Firewall Alert",
                                                        msg="Unknown program tried to modify firewall rules.")
                                                        
                                                        toast.show()
                                                        for _ in range(2):
                                                            winsound.Beep(2000, 300)  
                                                            time.sleep(0.2)
                                                    # Kill Process
                                                    # delete the rule from the file
                                                go=1
                                                not_loop=1
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



                                    pro=1 