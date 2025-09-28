import subprocess as su
import time
import json

def fireOff(states,timer):
    if states=="off":
        states="netsh advfirewall set allprofiles state off"
        su.run(states,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
        time.sleep(timer)
        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            timerF=settings["timerF"]
            if timerF != "0":
                su.run("netsh advfirewall set allprofiles state on",shell=True,text=True)
    return 0


def add_rule(ruleName,timer):
    
    time.sleep(timer)
    print("time auot")
    su.run(f'netsh advfirewall firewall delete rule name="{ruleName}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    return ruleName
  
    
    
    