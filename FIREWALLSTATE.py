import time
import subprocess as su

while True:
    s=su.run('netsh advfirewall show allprofiles', shell=True, capture_output=True, text=True)
    f=s.stdout
    if 'State Off' in f or len(f) != 2094 :
        su.run('netsh advfirewall set allprofiles state on', shell=True)
        with open(r'C:\Users\ibrah\logfirewall\firewall state.txt', '+a') as file:
            file.write(f'Firewall was off at {time.strftime('%Y-%m-%d %H:%M:%S')} \n')
    time.sleep(30)  