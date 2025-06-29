import subprocess as su
import time
def fireOff(states,timer):
    states="dir"
    # if states=="off":
    #     states="netsh advfirewall set allprofiles states off"
    su.run(states,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
    time.sleep(timer)
   # su.run("netsh advfirewall set allprofiles states on",shell=True,text=True)
    # return 0
    