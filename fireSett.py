import subprocess as su
import time
# edit
def fireOff(states,timer):
    states="dir"
    # if states=="off":
    #     states="netsh advfirewall set allprofiles states off"
    su.run(states,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    time.sleep(timer)
   # su.run("netsh advfirewall set allprofiles states on",shell=True,text=True)
    # return 0

#edit
def add_rule(ruleName,rule,timer):
    rule="dir"
    su.run(rule,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    time.sleep(timer)
    ruleName="dir"
    su.run(ruleName,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    # su.run(f'netsh advfirewall firewall delete rule name="{ruleName}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)