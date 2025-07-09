import subprocess as su
import time

def fireOff(states,timer):
    if states=="off":
        states="netsh advfirewall set allprofiles state off"
        su.run(states,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
        time.sleep(timer)
    su.run("netsh advfirewall set allprofiles state on",shell=True,text=True)
    return 0


def add_rule(ruleName,rule,timer):
    su.run(rule,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    rown=[ruleName]
    rowt=[timer]
    row=[]
    while True:
        for i in rowt:
            i-=1
            row.append(i)
        rowt=row.copy()
        row.clear()
        if 0 in rowt:
            t=rowt.index(0)
            rowt.remove(0)
            n=rown[t]
            rown.pop(t)
            su.run(f'netsh advfirewall firewall delete rule name="{n}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
        if rown==[]:
            break
        time.sleep(1)
  
    
    
    