import time
import subprocess as su
import socket as sk
import threading as th
import json
import FWSetting as fs
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
    s='{"email": "","IP-S": "","IP-U": "","firstconn": "0","FWS": "","timerF": "","deleteR": "null","ruleName": [],"Rolue": "null","constan": "no","timerR": [],"length": 0,"length2": 0}'
    p=json.loads(s)
    with open(r"D:\AOF-files\settings.json","w")as f:
        json.dump(p,f,indent=4)

    
while True:
    try:
        with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f) 
            ip=settings["IP-S"]
        
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
    if settings["Rolue"]!="null":
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
    if settings["timerR"]!=[]:
        settings["timerR"]=[]
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["ruleName"]!=[]:
        settings["ruleName"]=[]
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["constan"]!="no":
        settings["constan"]="no"
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["deleteR"]!="null":
        settings["deleteR"]="null"
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    email_rvs=settings["email"]
l=1
ll=1
adad=0
lw=1
def clos_fw():
    
    global ll
    ll=0
    c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    c.connect((ip, 9991))
    c.sendall("client".encode())
    while True:
        try:
            
            close=c.recv(1024).decode('utf-8')
            if close=="off":
                
                with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    settings["FWS"]="off-all"
                    settings["timerF"]="0"
                    with open(r'D:\AOF-files\settings.json', 'w') as f:
                        json.dump(settings,f,indent=4)
                su.run("netsh advfirewall set allprofiles state off",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
            elif close=="on":
                su.run("netsh advfirewall set allprofiles state on",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    settings["FWS"]="null"
                    settings["timerF"]="0"
                    with open(r'D:\AOF-files\settings.json', 'w') as f:
                        json.dump(settings,f,indent=4)
            
        except Exception:
            
            continue




async def check_files():
    global fws,ip,timer,rule,rulename,timerr,ips,constan,deleteR,adad,adad2,rellen
    
    with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        

        check=settings["IP-S"]
        
        ip = check
            
        ips=settings["IP-U"]

        rowFWS=["on","off","null"]
        check4=settings["FWS"]
        
        deleteR=settings["deleteR"]

        if check4 in rowFWS:
            fws= check4
                
             

        check5=settings["timerF"]
        
        timer=int(check5)      


        constan=settings["constan"]

        lens=settings["ruleName"]
        lens=len(lens)
        rule=settings["Rolue"]
        if lens!=0 and constan=="no":
            
            rulename=settings["ruleName"][0]
            timerr=settings["timerR"][0]
            timerr=int(timerr)



        
        adad=settings["length"]
        adad2=settings["length2"]
        if adad2<adad:
            
            adad2=adad
            with open(r'D:\AOF-files\settings.json', 'w') as f:
                settings["length2"]=adad2
                json.dump(settings,f,indent=4)
            rellen=rellen+1
        elif adad2>adad:
            
            adad2=adad
            with open(r'D:\AOF-files\settings.json', 'w') as f:
                settings["length2"]=adad2
                json.dump(settings,f,indent=4)
            rellen=rellen-1
            
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
    global lw
    time.sleep(0.5)
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
    time.sleep(1)
    lw=1
    fs.add_rule(rulename,rule,timerr)
    
    with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        settings["length"]=settings["length"]-1
        with open(r'D:\AOF-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
        

while True:
    
    # edit
    async def main():
        global l,ll,email_rvs,ips,email_rvs,rellen,adad,ips,l3,l4,lw
        
        if ll==1:
            th.Thread(target=clos_fw).start()
        
        sa.gather(check_files())
        
        
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
        
        with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            check=settings["FWS"]
        if check=="null":
            a=su.run("netsh advfirewall show allprofiles",shell=True,text=True,capture_output=True)
            a=a.stdout
            with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    firews=settings["FWS"]
                    firews=str(firews)
                    
            if "State                                 OFF" in a and firews=="null" :
                su.run('netsh advfirewall set allprofiles state on', shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                c.sendall("hackOff".encode())
                c.recv(1024).decode()
                ips=str(ips)
                c.sendall(ips.encode())
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



        if deleteR!="null":
            su.run(f'netsh advfirewall firewall delete rule name="{deleteR}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
            rellen=rellen-1
            with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                settings["deleteR"]="null"
                with open(r'D:\AOF-files\settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)




        if rule!="null":
            
            if constan=="yes":
                su.run(rule,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                rellen=rellen+1
            with open(r'D:\AOF-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                settings["Rolue"]="null"
                settings["constan"]="no"
                
                with open(r'D:\AOF-files\settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)
            if constan=="no":
                lw=0
                th.Thread(target=add__rule).start()


        
        
        with open(r"D:\AOF-files\check.txt","w")as f:
            f.write("")
        
        if lw==0:
            time.sleep(3)
        su.run("netsh advfirewall firewall show rule name=all > D:\AOF-files\check.txt",shell=True,text=True,capture_output=True)
        with open(r"D:\AOF-files\check.txt","r",encoding='utf-8')as f:
            a=f.readlines()
            ld=0
            
            for line in a:
                if "Rule Name:" in line:
                    ld+=1
        
        if ld>rellen:
            
        
            l3=ld-rellen
            rellen+=l3
            
            c.sendall("hackAdd".encode())
            c.recv(1024).decode()
            ips=str(ips)
            c.sendall(ips.encode())
            
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
                    

                
        elif ld<rellen:
            
            l4=rellen-ld
            rellen-=l4
           
            c.sendall("hackDel".encode())
            c.recv(1024).decode()
            ips=str(ips)
            c.sendall(ips.encode())
            
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
                    
        with open(r"D:\AOF-files\check.txt","w")as f:
            f.write("")

    sa.run(main())
    time.sleep(7)