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


l=1
async def check_files():
    global fws,utrm,ip,rm,timer,rule,rulename,timerr
    rowCheck=["Enable","Disable"]
    rowId=['zero','one','two','..']
    #p=16,d=4,f=6,a=1,r=18,u=22,o=15,t=21,s=19
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        

        check=settings["IP-S"]
        check=str(check)
        lens=len(check)
        if check.endswith("16"):
            decode=ed.dec(check[:lens-2])
            ip = decode
            
        else:
            print("no")
            # the notification for server
            pass
        
        



        check1=settings["id"]
        check1=str(check1)
        lens=len(check1)
        if check1.endswith("4"):
            decode1=ed.dec(check1[:lens-1])
            
            if decode1 in rowId:
                ID= str(rowId.index(decode1))
                ID=ID+'x'
            
            else:
                print("non")
            # the notification for server
                pass  
            
        else:
            print("no")
            # the notification for server
            pass
        
        
        


        
        check2=settings["RM"]
        check2=str(check2)
        lens=len(check2)
        if check2.endswith("18"):
            decode2=ed.dec(check2[:lens-2])
            if decode2 in rowCheck:
                rm= decode2
                
            else:
                print("non")
                # the notification for server
                pass
        else:
            print("no")
            # the notification for server
            pass
        
        


        check3=settings["URTM"]
        check3=str(check3)
        lens=len(check3)
        if check3.endswith("22"):
            decode3=ed.dec(check3[:lens-2])
            if decode3 in rowCheck:
                utrm= decode3
                
            else:
                print("non")
                # the notification for server
                pass
            
        else:
            print("no")
            # the notification for server
            pass
        

        rowFWS=["on","off","null"]
        check4=settings["FWS"]
        check4=str(check4)
        lens=len(check4)
        if check4.endswith("19"):
            decode4=ed.dec(check4[:lens-2])
            
            if decode4 in rowFWS:
                fws= decode4
                
                
            else:
                print("non")
                # the notification for server
                pass
            
        else:
            print("no")
            # the notification for server
            pass
        

        check5=settings["timerF"]
        check5=str(check5)
        decode5=ed.dec(check5)
        timer= decode5
        timer=int(timer)      


        
         # edit       
        lens=settings["ruleName"]
        lens=len(lens)
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
            settings["FWS"]="609811010411211219"
            settings["timerF"]="755283"
            with open('settings.json', 'w') as f:
                json.dump(settings,f,indent=4)
        print("end")
        l=1
        
# edit
def add__rule():

    fs.add_rule(rulename,rule,timerr)
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        a=settings["ruleName"]
        a=list(a)
        a.pop(0)
        settings["ruleName"]=a
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
        await sa.sleep(5)
        sa.gather(check_files())
        await sa.sleep(0)
        if fws=="off" and l==1:
            print("off")
            th.Thread(target=do_ruls).start()
        elif fws=="on":
            # edit
            print("on")
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                settings["FWS"]="609811010411211219"
                with open('settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)
        else:
            print("null")
        #edit
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
    # async def rules():
        
        
    #     if rule!="null":
            
    #         th.Thread(target=add__rule).start()
    #         with open('settings.json', 'r') as f:
    #             settings = json.load(f)
    #             settings["Rolue"]="null"
    #             with open('settings.json', 'w') as f:
    #                 json.dump(settings,f,indent=4)
    # sa.run(rules())
        

    
    # th.Thread(target=clos_fw).start()