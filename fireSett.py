import subprocess as su
import time
import json

def fireOff(states,timer):
    if states=="off":
        states="powershell -Command Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False"
        su.run(states,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
        time.sleep(timer)
        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            timerF=settings["timerF"]
            if timerF != "0":
                su.run("powershell -Command Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True",shell=True,text=True)
    return 0


def add_rule(ruleName,timer):
    
    time.sleep(timer)
    su.run(f'powershell -Command Remove-NetFirewallRule -DisplayName "{ruleName}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    return ruleName
  


def action_rule(timer,ruleN,action):
    print("also in")
    timer=int(timer)
    if action =="e":
        su.run(f'powershell -Command Set-NetFirewallRule -DisplayName "{ruleN}" -Enabled True',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    else:
        su.run(f'powershell -Command Set-NetFirewallRule -DisplayName "{ruleN}" -Enabled False',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    time.sleep(timer)
    if action =="d":
        su.run(f'powershell -Command Set-NetFirewallRule -DisplayName "{ruleN}" -Enabled True',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    else:
        su.run(f'powershell -Command Set-NetFirewallRule -DisplayName "{ruleN}" -Enabled False',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    
    