import subprocess as su
import time

def fireOff(states,timer):
    
    if states=="off":
        states="netsh advfirewall set allprofiles state off"
        su.run(states,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
        time.sleep(timer)
    su.run("netsh advfirewall set allprofiles state on",shell=True,text=True)
    return 0

#edit
def add_rule(ruleName,rule,timer):
    
    su.run(rule,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    time.sleep(timer)
    print(ruleName)
    su.run(f'netsh advfirewall firewall delete rule name="{ruleName}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)