import time
import subprocess as su
import socket as sk
import threading as th
import json
import EncDec as ed
import fireSett as fs
import asyncio as sa
import smtplib
from email.message import EmailMessage
# added "email" form ".json"
#in line "269" check why "clos_fw" going into a loop





# while True:
#     try:
#         c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
#         try:
#             c.connect(("192.168.1.13", 9999))
#         except ConnectionRefusedError:
#             print("the server is shot downe")
#             break 
#         except Exception:
#             print(f"somethig hapned to the ip server it is change to ''")
#             break
        
#         chck=c.recv(1024).decode('utf-8')
#         if chck=='1':
            
#             c.sendall("add".encode())
#             break
#     except Exception:
        
#         continue
# print("end")

a=su.run("netsh advfirewall show allprofiles",shell=True,text=True,capture_output=True)
a=a.stdout
if "State                                 OFF" in a or len(a) != 2094:
    su.run('netsh advfirewall set allprofiles state on', shell=True)

with open('settings.json', 'r') as f:
    settings = json.load(f) 
    if settings["FWS"]=="":
        settings["FWS"]="null"
        with open('settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["timerF"]=="":
        settings["timerF"]="0"
        with open('settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["Rolue"]=="":
        settings["Rolue"]="null"
        with open('settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["FWS"]=="off" or settings["FWS"]=="on":
        settings["FWS"]="null"
        with open('settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["timerF"]!="0":
        settings["timerF"]="0"
        with open('settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
l=1
async def check_files():
    global fws,utrm,ip,rm,timer,rule,rulename,timerr,lensrule
    # rowCheck=["Enable","Disable"]
    
    #p=16,d=4,f=6,a=1,r=18,u=22,o=15,t=21,s=19
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        

        check=settings["IP-S"]
        # check=str(check)
        # lens=len(check)
        # if check.endswith("16"):
        #     decode=ed.dec(check[:lens-2])
        ip = check
            
        # else:
        #     print("no")
        #     # the notification for server
        #     pass
        
                
        # check2=settings["RM"]
       
        # rm= check2
                
        #     else:
        #         print("non")
        #         # the notification for server
        #         pass
        # else:
        #     print("no")
        #     # the notification for server
        #     pass
        
        


        # check3=settings["URTM"]
        
        # utrm= check3
                
        #     else:
        #         print("non")
        #         # the notification for server
        #         pass
            
        # else:
        #     print("no")
        #     # the notification for server
        #     pass
        

        rowFWS=["on","off","null"]
        check4=settings["FWS"]
        # check4=str(check4)
        # lens=len(check4)
        # if check4.endswith("19"):
        #     decode4=ed.dec(check4[:lens-2])
        
        if check4 in rowFWS:
            fws= check4
                
                
        #     else:
        #         print("non")
        #         # the notification for server
        #         pass
            
        # else:
        #     print("no")
        #     # the notification for server
        #     pass
        

        check5=settings["timerF"]
        # check5=str(check5)
        # decode5=ed.dec(check5)
        # timer= decode5
        timer=int(check5)      


        
         # edit       
        lens=settings["ruleName"]
        lens=len(lens)
        lensrule=lens
        rule=settings["Rolue"]
        if lens!=0:
            
            rulename=settings["ruleName"][lens-1]
            timerr=settings["timerR"][lens-1]
            timerr=int(timerr)
            
# edit
def do_ruls():
    global l
    if fws=="off" and l==1:
        l=0
        fs.fireOff(fws,timer)
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            settings["FWS"]="null"
            settings["timerF"]="0"
            with open('settings.json', 'w') as f:
                json.dump(settings,f,indent=4)
        l=1
        
# edit
def add__rule():

    fs.add_rule(rulename,rule,timerr)
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        a=settings["ruleName"]
        w=settings["timerR"]
        a=list(a)
        w=list(w)
        a.pop(0)
        w.pop(0)
        settings["ruleName"]=a
        settings["timerR"]=w
        with open('settings.json', 'w') as f:
            json.dump(settings,f,indent=4) 
    print("end1")





# def clos_fw():# edit
        
#         ch=c.recv(1024).decode('utf-8')
#         print(ch)
#         # if ch=="off":
#         print("off")
            # su.run("netsh advfirewall set allprofiles states off",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)

    

while True:

    # edit
    async def main():
        global l
        await sa.sleep(5)
        sa.gather(check_files())
        await sa.sleep(0)
        if fws=="off" and l==1:
            
            th.Thread(target=do_ruls).start()
        elif fws=="on":
            # edit
            su.run("netsh advfirewall set allprofiles state on",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                settings["FWS"]="null"
                settings["timerF"]="0"
                with open('settings.json', 'w') as f:
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
            # msg["To"]=email_rvs
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
            
            th.Thread(target=add__rule).start()
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                settings["Rolue"]="null"
                with open('settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)
    sa.run(rules())
        

    async def check_len_rule():
        su.run("netsh advfirewall firewall show rule name=all > check.txt",shell=True,text=True,capture_output=True)
        with open("check.txt","r")as f:
            a=f.readlines()
            l=0
            for line in a:
                if "Rule Name:" in line:
                    l+=1
            if l>793 and lensrule==0:
                
                msg= EmailMessage()
                msg["Subject"]="add strange rule"
                msg["From"]="aofnotification@gmail.com"
                # msg["To"]=email_rvs
                msg.set_content(f"there are strange rule had been add to your firewall\ndo the protocol to check your devic if you had been hackt")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
                
            elif l<793 and lensrule==0:
                
                msg= EmailMessage()
                msg["Subject"]="delete strange rule"
                msg["From"]="aofnotification@gmail.com"
                # msg["To"]=email_rvs
                msg.set_content(f"there are some rule had been delete from your firewall\ndo the protocol to check your devic if you had been hackt")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
                
            with open("check.txt","w")as f:
                    f.write("")
    sa.run(check_len_rule())





    # th.Thread(target=clos_fw).start()