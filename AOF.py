import time
import subprocess as su
import socket as sk
import threading as th
import json
import fireSett as fs
import asyncio as sa
import smtplib
from email.message import EmailMessage
import os




try:
    os.mkdir(r"D:\AOF-files")
except FileExistsError:
    pass
with open(r"D:\AOF-files\check.txt","w")as f:
        f.write("")
su.run("netsh advfirewall firewall show rule name=all > D:\AOF-files\check.txt",shell=True,text=True,capture_output=False,stdout=su.DEVNULL,stderr=su.DEVNULL)
with open(r"D:\AOF-files\check.txt","r",encoding='utf-8')as f:
    a=f.readlines()
    ld=0
    for line in a:
        if "Rule Name:" in line:
            ld+=1
    rellen=ld
    

pathfile=os.path.exists(r"D:\AOF-files\settings.json")
if pathfile==False:
    s='{"email": "","IP-S": "","firstconn": "0","FWS": "","timerF": "","ruleName": [],"Rolue": "null","timerR": [],"length": 0,"length2": 0}'
    p=json.loads(s)
    with open(r"D:\AOF-files\settings.json","w")as f:
        json.dump(p,f,indent=4)
with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f) 
    ip=settings["IP-S"]
while True:
    try:
        
        c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        c.connect((ip, 9999))
        
        chck=c.recv(1024).decode('utf-8')
        if chck=='1':
            
            c.sendall("add".encode())
        break
    except Exception:
        
        continue
        
        
            
    


a=su.run("netsh advfirewall show allprofiles",shell=True,text=True,capture_output=True)
a=a.stdout
if "State                                 OFF" in a or len(a) != 2094:
    su.run('netsh advfirewall set allprofiles state on', shell=True)

with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f) 
    if settings["FWS"]=="":
        settings["FWS"]="null"
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["timerF"]=="":
        settings["timerF"]="0"
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["Rolue"]=="":
        settings["Rolue"]="null"
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["FWS"]=="off" or settings["FWS"]=="on" or settings["FWS"]=="off-all":
        settings["FWS"]="null"
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["timerF"]!="0":
        settings["timerF"]="0"
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["length"]!=0:
        settings["length"]=0
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["length2"]!=0:
        settings["length2"]=0
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    email_rvs=settings["email"]
l=1
ll=1
l1=1
adad=0

def clos_fw():
    
    global ll
    ll=0
    while True:
        try:
            c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            c.connect((ip, 9991))
            c.sendall("client".encode())
            close=c.recv(1024).decode('utf-8')
            if close=="off":
                su.run("netsh advfirewall set allprofiles state off",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    settings["FWS"]="off-all"
                    settings["timerF"]="0"
                    with open(r'D:\AOF-files\settings.json', 'w') as f:
                        json.dump(settings,f,indent=4)
            ll=1
            break
        except Exception:
            
            continue




async def check_files():
    global fws,ip,timer,rule,rulename,timerr
    
    with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        

        check=settings["IP-S"]
        
        ip = check
            
        

        rowFWS=["on","off","null"]
        check4=settings["FWS"]
        
        
        if check4 in rowFWS:
            fws= check4
                
             

        check5=settings["timerF"]
        
        timer=int(check5)      


        lens=settings["ruleName"]
        lens=len(lens)
        rule=settings["Rolue"]
        if lens!=0:
            
            rulename=settings["ruleName"][0]
            timerr=settings["timerR"][0]
            timerr=int(timerr)
            
# edit
def do_ruls():
    global l
    if fws=="off" and l==1:
        l=0
        fs.fireOff(fws,timer)
        with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            settings["FWS"]="null"
            settings["timerF"]="0"
            with open(r'D:\AOF-files\settings.json', 'w') as f:
                json.dump(settings,f,indent=4)
        l=1
        
# edit
def add__rule():
    print("yes")
    time.sleep(1)
    with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        a=settings["ruleName"]
        w=settings["timerR"]
        a=list(a)
        w=list(w)
        a.pop(0)
        w.pop(0)
        settings["ruleName"]=a
        settings["timerR"]=w
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4) 
    print("start")
    fs.add_rule(rulename,rule,timerr)
    print("done")
    with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        settings["length"]=settings["length"]-1
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
        

while True:
    
    # edit
    async def main():
        global l,ll,email_rvs
        await sa.sleep(7)
        print("run")
        sa.gather(check_files())
        print("run1")
        if ll==1:
            th.Thread(target=clos_fw).start()
        await sa.sleep(0)
        if fws=="off" and l==1:
            
            th.Thread(target=do_ruls).start()
        elif fws=="on":
            # edit
            su.run("netsh advfirewall set allprofiles state on",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
            with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                settings["FWS"]="null"
                settings["timerF"]="0"
                with open(r'D:\AOF-files\settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)
            l=1
        
        # #edit
        a=su.run("netsh advfirewall show allprofiles",shell=True,text=True,capture_output=True)
        a=a.stdout
        if "State                                 OFF" in a or len(a) != 2094 and fws=="null" :
           
            su.run('netsh advfirewall set allprofiles state on', shell=True)
            msg= EmailMessage()
            msg["Subject"]="closeing firewall"
            msg["From"]="aofnotification@gmail.com"
            msg["To"]=email_rvs
            msg.set_content(f"your firewall state has been off,we rutern it to be open.\ndo the protocol to check your devic if you had been hackt")
            email="aofnotification@gmail.com"
            password="oqgspkawnyeftyjw"
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(email,password)
                smtp.send_message(msg)

    sa.run(main())


    # edit
    async def rules():
        
        
        if rule!="null":
            
            
            with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                settings["Rolue"]="null"
                with open(r'D:\AOF-files\settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)
            th.Thread(target=add__rule).start()
    sa.run(rules())
        

    def check_len_rule():
        
        global email_rvs,rellen,l1,adad
        with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                adad=settings["length"]
                adad2=settings["length2"]
                if adad2<adad:
                    
                    adad2=adad
                    with open(r'D:\AOF-files\settings.json', 'w') as f:
                        settings["length2"]=adad2
                        json.dump(settings,f,indent=4)
                    rellen=rellen+1
                if adad2>adad:
                    
                    adad2=adad
                    with open(r'D:\AOF-files\settings.json', 'w') as f:
                        settings["length2"]=adad2
                        json.dump(settings,f,indent=4)
                    rellen=rellen-1
        with open(r"D:\AOF-files\check.txt","w")as f:
            f.write("")
        su.run("netsh advfirewall firewall show rule name=all > D:\AOF-files\check.txt",shell=True,text=True,capture_output=True)
        with open(r"D:\AOF-files\check.txt","r",encoding='utf-8')as f:
            a=f.readlines()
            ld=adad
            
            for line in a:
                if "Rule Name:" in line:
                    ld+=1
            print(ld)
            print(rellen)
            if ld>rellen:
                l1=0
                
                msg= EmailMessage()
                msg["Subject"]="add strange rule"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=email_rvs
                msg.set_content(f"there are strange rule had been add to your firewall\ndo the protocol to check your devic if you had been hackt")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
                time.sleep(1800)
                l1=1
            elif ld<rellen:
                l1=0
                
                msg= EmailMessage()
                msg["Subject"]="delete strange rule"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=email_rvs
                msg.set_content(f"there are some rule had been delete from your firewall\ndo the protocol to check your devic if you had been hackt")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
                time.sleep(1800)
                l1=1
                
            with open(r"D:\AOF-files\check.txt","w")as f:
                f.write("")
    if l1==1:
        check_len_rule()
  