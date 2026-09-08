import subprocess as su
import time
import json


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


def fireOff(states,timer):
    if states=="off":
        states="Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False"
        poewrshell(states)
        time.sleep(timer)
        with open(r'C:\FS-File\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            timerF=settings["timerF"]
            if timerF != "0":
                poewrshell("Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True")
    return 0



    
    