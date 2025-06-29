import socket as sk
import json
import EncDec as ed
import random
import smtplib
from email.message import EmailMessage
import time


# with open('settings.json', 'r') as f:
#         settings = json.load(f)
#         if settings["email"]=="null":
#             emai=input("enter your email: ")
#             encode7=ed.enc(emai)
#             settings["email"]=encode7+'5'
#             with open('settings.json', 'w') as f:
#                 json.dump(settings,f,indent=4)
# with open('settings.json', 'r') as f:
#     settings = json.load(f)
#     check4=settings["email"]
#     check4=str(check4)
#     if check4.endswith("5"):
#         lens=len(check4)
#         decode4=ed.dec(check4[:lens-1])
#         email_rvs=decode4
#         print(email_rvs)
#     else:
#          print("no")

def generate_password():
    global row1,password
    row1 = []
    for _ in range(6):
        ran = random.randint(0, 9)
        ran = str(ran)
        row1.append(ran)
    password = ''.join(map(str,row1))
    row1.clear()
    
generate_password()    

ppp=password
# msg= EmailMessage()
# msg["Subject"]="Enter password"
# msg["From"]="aofnotification@gmail.com"
# msg["To"]=email_rvs
# msg.set_content(f"your password is: {password}")
# email="aofnotification@gmail.com"
# password="oqgspkawnyeftyjw"
# with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
#     smtp.login(email,password)
#     smtp.send_message(msg)

checkpass=ppp
if checkpass==ppp:
    print("hi")
    rowId=['zero','one','two','..']
    rowChIpId=["zero","one"]
    #p=16,d=4,f=6,a=1,r=18,u=22,o=15,t=21,e=5
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        
        check4=settings["email"]
        check4=str(check4)
        if check4.endswith("5"):
            lens=len(check4)
            decode4=ed.dec(check4[:lens-1])
            email_rvs=decode4
            print(email_rvs)
        else:
            print("no")

        check=settings["firstconn"]
        check=str(check)
        lens=len(check)
        if check.endswith("6"):
            decode=ed.dec(check[:lens-1])
            if decode in rowChIpId:
                decode=str(rowChIpId.index(decode))
            else:
                decode="2"
                msg= EmailMessage()
                msg["Subject"]="edit file"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=email_rvs
                msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '5' ")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
                 
        else:
            decode="2"
            msg= EmailMessage()
            msg["Subject"]="edit file"
            msg["From"]="aofnotification@gmail.com"
            msg["To"]=email_rvs
            msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '5' ")
            email="aofnotification@gmail.com"
            password="oqgspkawnyeftyjw"
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(email,password)
                smtp.send_message(msg)
            pass

        # if decode=="2":
        #     print("error1")
        #     # the notification for server
        #     exit()


        check1=settings["addid"]
        check1=str(check1)
        lens=len(check1)
        if check1.endswith("1"):
            decode1=ed.dec(check1[:lens-1])
            if decode1 in rowChIpId:
                decode1=str(rowChIpId.index(decode1))

            else:
                decode1="2"
                msg= EmailMessage()
                msg["Subject"]="edit file"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=email_rvs
                msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '6' ")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
                 
        else:
            decode1="2"
            
            msg= EmailMessage()
            msg["Subject"]="edit file"
            msg["From"]="aofnotification@gmail.com"
            msg["To"]=email_rvs
            msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '6' ")
            email="aofnotification@gmail.com"
            password="oqgspkawnyeftyjw"
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(email,password)
                smtp.send_message(msg)
        # if decode1=="2":
        #     print("error2")
        #     # the notification for server
        #     exit()


        if decode=="0":
    
            ip=input("Enter IP server: ")
            print(f"Using saved IP: {ip}")
            
            encode4=ed.enc(ip)
           

            with open('settings.json', 'w') as f:
                settings["IP-S"] = encode4+'16'
                
                encode5=ed.enc("one")
                settings["firstconn"] = encode5+'6'
                json.dump(settings, f, indent=4)


        check2=settings["firstconn"]
        check2=str(check2)
        lens=len(check2)
        if check2.endswith("6"):
            decode2=ed.dec(check2[:lens-1])
            if decode2 in rowChIpId:
                decode2=str(rowChIpId.index(decode2))
            else:
                decode2="2"
                msg= EmailMessage()
                msg["Subject"]="edit file"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=email_rvs
                msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '5' ")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
        else:
            decode2="2"
            msg= EmailMessage()
            msg["Subject"]="edit file"
            msg["From"]="aofnotification@gmail.com"
            msg["To"]=email_rvs
            msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '5' ")
            email="aofnotification@gmail.com"
            password="oqgspkawnyeftyjw"
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(email,password)
                smtp.send_message(msg)

        # if decode2=="2":
        #     print("error1")
        #     # the notification for server
        #     exit()
        
        
        if decode2=="1":
            check3=settings["IP-S"]
            check3=str(check3)
            lens=len(check3)
            if check3.endswith("16"):
                decode3=ed.dec(check3[:lens-2])
            else:
                msg= EmailMessage()
                msg["Subject"]="edit file"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=email_rvs
                msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '2' ")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
        
            ip = decode3
            addid = decode1
            print(addid)
        


    while True:
        try:
            c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
            try:
                c.connect((ip, 9999))
            except ConnectionRefusedError:
                print("the server is shot downe")
                exit()
                break 
            except Exception:
                print(f"somethig hapned to the ip server it is change to '{ip}'")
                exit()
                break
            
            chck=c.recv(1024).decode('utf-8')
            if chck=='1':
                
                break
        except Exception:
            
            continue
    
    c.sendall(addid.encode('utf-8'))
    if addid=="0":
        di=c.recv(1024).decode('utf-8')

        with open('settings.json', 'r') as f:
            settings = json.load(f)
            with open('settings.json', 'w') as f:
                encode6=ed.enc("one")
                settings["addid"]=encode6+'1'
                settings["id"]=di+'4'
                json.dump(settings,f,indent=4)
            
            
            
        
    while True:
        
        masge=input("enter masge: ")
        
        if masge == "show password":
            masge=masge+'\n'# give all sendall '\n'
            c.sendall(masge.encode('utf-8'))
            
            c.sendall('0'.encode('utf-8'))
            data = c.recv(1024).decode('utf-8')
            print(data)
        elif masge == "exit":
            c.close()
            break
        elif masge=="show id":
            check1=settings["id"]
            check1=str(check1)
            lens=len(check1)
            if check1.endswith("4"):
                decode1=ed.dec(check1[:lens-1])
                
                if decode1 in rowId:
                    ID= str(rowId.index(decode1))
                    ID=ID+'x'
                    print(ID)
                else:
                    msg= EmailMessage()
                    msg["Subject"]="edit file"
                    msg["From"]="aofnotification@gmail.com"
                    msg["To"]=email_rvs
                    msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '3' ")
                    email="aofnotification@gmail.com"
                    password="oqgspkawnyeftyjw"
                    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                        smtp.login(email,password)
                        smtp.send_message(msg)
                
            else:
                msg= EmailMessage()
                msg["Subject"]="edit file"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=email_rvs
                msg.set_content(f"your file setting has been edit,it is them there are hacker in your devic,use the protocol to stop traking by hacker\n\nthe edit hapned in 'settings.json' line '3' ")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)
        elif masge=="firewall states":
            check1=settings["id"]
            check1=str(check1)
            lens=len(check1)
            if check1.endswith("4"):
                decode1=ed.dec(check1[:lens-1])
                
                if decode1 in rowId:
                    ID= str(rowId.index(decode1))
                    ID=ID+'x'
            c.sendall(masge.encode('utf-8'))
            rolu=input("enter firewall states:  ")
            timer=input("enter timer:  ")
            c.sendall(ID.encode('utf-8'))
            c.sendall(rolu.encode('utf-8'))
            
            addrolu=c.recv(1024).decode("utf-8")
            
            
            with open('settings.json', 'r') as f:
                data = json.load(f)
                data["FWS"]=addrolu
                data["timerF"]=timer+'21'
                
                with open('settings.json', 'w') as f:
                    json.dump(data,f,indent=4)
            print("firewall states change")
else:
    print("try agen")
    time.sleep(1)
    exit()