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
import imaplib
import email as email1
import uuid
import random
# check all code


pathfile=os.path.exists(r"C:\FWSH-files\sent_ids.txt")
if pathfile==False:
    with open(r"C:\FWSH-files\sent_ids.txt","w")as f:
        pass

#check firewall state       
a=su.run("netsh advfirewall show allprofiles",shell=True,text=True,capture_output=True)
a=a.stdout
if "State                                 OFF" in a or len(a) != 2094:
    su.run('netsh advfirewall set allprofiles state on', shell=True)

#conn with the praimry conn   
while True:
    try:
        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f) 
            ip=settings["IP-S"]
        
        c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        c.connect((ip, 9999))
        #vrefiy the server to end the loop
        chck=c.recv(1024).decode('utf-8')
        if chck=='1':
            
            c.sendall("add".encode())
        break
    except Exception:
        
        continue
        
        
            
    



#return D:\FWSH-files\settings.json to the defult
with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f) 
    if settings["user-state"]=="USER":
        bossemail=settings["bossemail"]
    if settings["FWS"]=="":
        settings["FWS"]="null"
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["timerF"]=="":
        settings["timerF"]="0"
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["Rolue"]!="null":
        settings["Rolue"]="null"
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["FWS"]=="off" or settings["FWS"]=="on" or settings["FWS"]=="off-all":
        settings["FWS"]="null"
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["timerF"]!="0":
        settings["timerF"]="0"
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["timerR"]!=[]:
        settings["timerR"]=[]
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["ruleName"]!=[]:
        settings["ruleName"]=[]
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["checkrulename"]!=[]: 
        for aa in settings["checkrulename"]:
            su.run(f'netsh advfirewall firewall delete rule name="{aa}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
        settings["checkrulename"]=[]
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["constan"]!="no":
        settings["constan"]="no"
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["advance-mode"]!="0":
        settings["advance-mode"]="0"
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    if settings["deleteR"]!="null":
        settings["deleteR"]="null"
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
    email_rvs=settings["email"]
    user_state=settings["user-state"]



with open(r"C:\FWSH-files\check.txt","w")as f:
        f.write("")
#cuntant firewall rules lenghth
su.run(r"netsh advfirewall firewall show rule name=all > C:\FWSH-files\check.txt",shell=True,text=True,capture_output=False,stdout=su.DEVNULL,stderr=su.DEVNULL)
with open(r"C:\FWSH-files\check.txt","r",encoding='utf-8')as f:
    a=f.readlines()
    ld=0
    for line in a:
        if "Rule Name:" in line:
            ld+=1
    rellen=ld

def get_wifi_mac():
    result = su.check_output("netsh wlan show interfaces", shell=True, text=True)

    for line in result.splitlines():
        if "Physical address" in line:
            mac = line.split(":", 1)[1].strip()  
            return mac 

def ckeck_email():
    
    with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        ips=settings["IP-U"]
    global status,from_,timer
    while True:
        print("1")
        IMAP_SERVER = "imap.gmail.com"
        EMAIL_ACCOUNT = "aofnotification@gmail.com"
        EMAIL_PASSWORD = "oqgspkawnyeftyjw"
        with open(r"C:\FWSH-files\sent_ids.txt", "r", encoding='utf-8') as f:
            sent_ids=f.read().strip()
            
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")


        status, messages = mail.search(None, f'(FROM "{bossemail}")')  

        for num in messages[0].split():
            status, data = mail.fetch(num, '(RFC822)')
            msg1 = email1.message_from_bytes(data[0][1])
            in_reply_to = msg1.get("In-Reply-To")
            
            from_ = msg1.get("From")
            
            if in_reply_to and in_reply_to.strip() in sent_ids:
                
                if msg1.is_multipart():
                    for part in msg1.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            firest=body.strip().splitlines()[0]
                            firest=str(firest.strip()).lower()
                           
                            sent_ids=sent_ids.replace(in_reply_to,"")
                            
                            with open(r"C:\FWSH-files\sent_ids.txt", "w") as f:
                                sent_id="".join(map(str,sent_ids))
                                f.write(sent_id)
                            with open(r"C:\FWSH-files\sent_ids.txt", "r") as f:
                                sent_ids=f.readlines()
                                for line in sent_ids:
                                    if line.startswith("|") or line.startswith("#") or line.startswith("%"):
                                        l1=line
                                        l2=line[:1]
                                        l=line[1:]
                                        if "~" in l:
                                            chck1=l.index("~")
                                            l=l[:chck1]
                                            l1=l
                                            with open(r"C:\FWSH-files\sent_ids.txt", "r") as f:
                                                sent_ids=f.read()
                                                sent_ids=sent_ids.replace("#","")  
                                                
                                                
                                            with open(r"C:\FWSH-files\sent_ids.txt", "w") as f:
                                                sent_id="".join(map(str,sent_ids))
                                                f.write(sent_id)  
                                           
                                            
                            with open(r"C:\FWSH-files\sent_ids.txt", "r") as f:
                                sent_ids=f.read()
                                
                                sent_ids=sent_ids.replace(l1,"")  
                                
                            with open(r"C:\FWSH-files\sent_ids.txt", "w") as f:
                                sent_id="".join(map(str,sent_ids))
                                f.write(sent_id)     

                            if firest=="approved" and l2=="%": 
                                
                                ran = random.randint(100000, 999999)
                                ran=str(ran)
                                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    settings["advance-password"]=ran
                                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                        json.dump(settings,f,indent=4)
                                msg= EmailMessage()
                                msg["Subject"]=f"Enter Password - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=email_rvs
                                msg.set_content(f"your password: {ran}")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)   
                                
                            elif firest!="approved"  and l2=="%": 
                                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    settings["advance-mode"]="0"
                                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                        json.dump(settings,f,indent=4)
                                msg= EmailMessage()
                                msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=email_rvs
                                msg.set_content(f"he dont allowed you")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)

                                   
                            if firest=="approved" and l2=="|":
                                
                                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    settings["deleteR"]=l
                                    
                                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                        json.dump(settings,f,indent=4)
                                on="del"
                                c.sendall(on.encode())
                                c.recv(1024).decode()
                                c.sendall(l.encode())
                                c.recv(1024).decode()
                                c.sendall(str(time.strftime('%Y-%m-%d %H:%M:%S')).encode())
                                c.recv(1024).decode()
                                ips=str(ips)
                                c.sendall(ips.encode())
                                c.recv(1024).decode()
                                c.sendall(get_wifi_mac().encode())
                                msg= EmailMessage()
                                msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=email_rvs
                                msg.set_content("rule delete successfully.")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)
                            elif firest!="approved"  and l2=="|":
                                
                                msg= EmailMessage()
                                msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=email_rvs
                                msg.set_content("the adminstretor do not acsybt to DELETE the rule")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)
                            


                            if firest=="approved"  and l2=="#":
                                
                                l=l.replace("#","")
                        

                                with open(r"C:\FWSH-files\sent_ids.txt", "r") as f:
                                    sent_ids=f.readlines()
                                    for line in sent_ids:
                                        if line.startswith("~"):
                                            l1=line
                                            
                                            timer=line[1:]
                                            
                                            
                                with open(r"C:\FWSH-files\sent_ids.txt", "r") as f:
                                    sent_ids=f.read()
                                    sent_ids=sent_ids.replace(l1,"")  
                                    
                                with open(r"C:\FWSH-files\sent_ids.txt", "w") as f:
                                    sent_id="".join(map(str,sent_ids))
                                    f.write(sent_id) 
                                
                                row=[]
                                row1=[]


                                for i in l:
                                    row1.append(i)
                                    if i =="'" or i=='"':
                                        break
                                d=''.join(row1)
                                e=l.removeprefix(d)
                                for i in e:
                                    if i =="'" or i=='"':
                                        break
                                    row.append(i)
                                rulename=''.join(row)
                                
                                row.clear()
                                row1.clear()
                                on="on"
                                c.sendall(on.encode())
                                c.recv(1024).decode()
                                c.sendall(rulename.encode())
                                c.recv(1024).decode()
                                timerlog=timer
                                c.sendall(timerlog.encode())
                                c.recv(1024).decode()
                                c.sendall(str(time.strftime('%Y-%m-%d %H:%M:%S')).encode())
                                c.recv(1024).decode()
                                ips=str(ips)
                                c.sendall(ips.encode())
                                c.recv(1024).decode()
                                c.sendall(l.encode())
                                c.recv(1024).decode()
                                c.sendall("no".encode())
                                c.recv(1024).decode()
                                c.sendall(get_wifi_mac().encode())
                                if timer.endswith("m"):
                                    lens=len(timer)
                                    timer=timer[:lens-1]
                                    timer=int(timer)
                                    timer*=60
                                    timer=str(timer)
                                    


                                elif timer.endswith("h"):
                                    lens=len(timer)
                                    timer=timer[:lens-1]
                                    timer=int(timer)
                                    timer*=3600
                                    timer=str(timer)
                                    
                                
                            
                                    
                                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    
                                    s=settings["checkrulename"]
                                    s=list(s)
                                    s.append(rulename)
                                    settings["checkrulename"]=s 
                                    s=settings["ruleName"]
                                    s=list(s)
                                    s.append(rulename)
                                    settings["ruleName"]=s 
                                    s=settings["timerR"]
                                    s=list(s)
                                    s.append(timer)
                                    settings["timerR"]=s
                                    settings["Rolue"]=l
                                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                                        json.dump(settings,f,indent=4)
                                msg= EmailMessage()
                                msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=email_rvs
                                msg.set_content("rule ADD successfully.")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)



                            elif firest!="approved" and l2=="#":
                                with open(r"C:\FWSH-files\sent_ids.txt", "r") as f:
                                    sent_ids=f.readlines()
                                    for line in sent_ids:
                                        if line.startswith("~"):
                                            l1=line   
                                with open(r"C:\FWSH-files\sent_ids.txt", "r") as f:
                                    sent_ids=f.read()
                                    sent_ids=sent_ids.replace(l1,"") 
                                    
                                with open(r"C:\FWSH-files\sent_ids.txt", "w") as f:
                                    sent_id="".join(map(str,sent_ids))
                                    f.write(sent_id) 

                                msg= EmailMessage()
                                msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                                msg["From"]="aofnotification@gmail.com"
                                msg["To"]=email_rvs
                                msg.set_content("the adminstretor do not acsybt to ADD the rule")
                                email="aofnotification@gmail.com"
                                password="oqgspkawnyeftyjw"
                                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                    smtp.login(email,password)
                                    smtp.send_message(msg)


                            mail.store(num,"+FLAGS","\\Deleted")
                            mail.expunge()
        mail.logout()
        time.sleep(5)
if user_state=="USER":
    th.Thread(target=ckeck_email).start()
#keys to contrule
l=1
ll=1
l5=0
#function to conn to the seconed conn in the server
def clos_fw():
    
    global ll
    ll=0
    c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    c.connect((ip, 9991))
    c.sendall("client".encode())
    while True:
        try:
            #the orders that admenstretor want to run
            close=c.recv(1024).decode('utf-8')
            if close=="off":
                
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    settings["FWS"]="off-all"
                    settings["timerF"]="0"
                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                        json.dump(settings,f,indent=4)
                su.run("netsh advfirewall set allprofiles state off",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
            elif close=="on":
                su.run("netsh advfirewall set allprofiles state on",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    settings["FWS"]="null"
                    settings["timerF"]="0"
                    with open(r'C:\FWSH-files\settings.json', 'w') as f:
                        json.dump(settings,f,indent=4)
            
        except Exception:
            
            continue



#function to check the D:\FWSH-files\settings.json evry 10s
async def check_files():
    global fws,ip,timer,rule,rulename,timerr,ips,constan,deleteR,rellen
    
    with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
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


            
#function to close the firewall
def do_ruls():
    global l
    if fws=="off" and l==1:
        l=0
        fs.fireOff(fws,timer)
        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            settings["FWS"]="null"
            settings["timerF"]="0"
            with open(r'C:\FWSH-files\settings.json', 'w') as f:
                json.dump(settings,f,indent=4)
        l=1
        
#function to add rules to the firewall
def add__rule():
    global rulename,rellen,timerr,rellen1,l5
    time.sleep(0.5)
    with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        a=settings["ruleName"]
        w=settings["timerR"]
        a=list(a)
        w=list(w)
        a.pop(0)
        w.pop(0)
        settings["ruleName"]=a
        settings["timerR"]=w
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4) 
    

    rulename1=fs.add_rule(rulename,timerr)
    l5=1
    rellen1=rellen-1
    
    with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
        settings = json.load(f)
        v=settings["checkrulename"]
        v=list(v)        
        v.remove(rulename1)
        settings["checkrulename"]=v
        with open(r'C:\FWSH-files\settings.json', 'w') as f:
            json.dump(settings,f,indent=4)
        
        

while True:
    
    # #the main function that contrule in evry things
    async def main():
        # pass
        global l,ll,email_rvs,ips,email_rvs,rellen,ips,l3,l4,constan,rule,rellen1,l5
        
        if ll==1:
            #run the seconed conn function
            th.Thread(target=clos_fw).start()
        #run the check D:\FWSH-files\settings.json function
        sa.gather(check_files())
        
        
        await sa.sleep(0)
        #check order from user
        if fws=="off" and l==1:
            #run close firewall function
            th.Thread(target=do_ruls).start()
        elif fws=="on":
            #open firewall
            su.run("netsh advfirewall set allprofiles state on",shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                settings["FWS"]="null"
                settings["timerF"]="0"
                with open(r'C:\FWSH-files\settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)
            l=1
        #check if the firewall state is off without the user send any ordurs
        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)
            check=settings["FWS"]
        if check=="null":
            a=su.run("netsh advfirewall show allprofiles",shell=True,text=True,capture_output=True)
            a=a.stdout
            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    firews=settings["FWS"]
                    firews=str(firews)
            #run the belwo code if firewall is off without the user send any ordurs to return firewall on   
            if "State                                 OFF" in a and firews=="null" :
                su.run('netsh advfirewall set allprofiles state on', shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                #send to server to add to the csv file
                c.sendall("hackOff".encode())
                c.recv(1024).decode()
                ips=str(ips)
                c.sendall(ips.encode())
                c.recv(1024).decode()
                c.sendall(get_wifi_mac().encode())
                #send email to the user
                msg= EmailMessage()
                msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=email_rvs
                msg.set_content(f"your firewall state has been off,we rutern it to be open.\ndo the protocol to check your devic if you had been hackt")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)


        #delete rule from the firewall
        if deleteR!="null":
            su.run(f'netsh advfirewall firewall delete rule name="{deleteR}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
            rellen=rellen-1
            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                settings["deleteR"]="null"
                with open(r'C:\FWSH-files\settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)



        #add rule to the firewall 
        if rule!="null":
            
            if constan=="yes":
                su.run(rule,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                print("in side")
                rellen=rellen+1
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    settings["Rolue"]="null"
                    settings["constan"]="no"
                
                with open(r'C:\FWSH-files\settings.json', 'w') as f:
                    json.dump(settings,f,indent=4)
            elif constan=="no":
                
                su.run(rule,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                rellen=rellen+1
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        settings["Rolue"]="null"
                        settings["constan"]="no"
                        with open(r'C:\FWSH-files\settings.json', 'w') as f:
                            json.dump(settings,f,indent=4)
                #run add rules function
                th.Thread(target=add__rule).start()


        
        
        with open(r"C:\FWSH-files\check.txt","w")as f:
            f.write("")
        #check firewall rules lenghth
        
        su.run(r"netsh advfirewall firewall show rule name=all > C:\FWSH-files\check.txt",shell=True,text=True,capture_output=True)
        with open(r"C:\FWSH-files\check.txt","r",encoding='utf-8')as f:
            a=f.readlines()
            ld=0
            
            for line in a:
                if "Rule Name:" in line:
                    ld+=1
        #if there a rule add to the firewall without ordars from the user the belwo code will run
        if l5==1:
            rellen=rellen1
            l5=0
        if ld>rellen:
            
        
            l3=ld-rellen
            rellen+=l3
            #send to the server to add csv file
            c.sendall("hackAdd".encode())
            c.recv(1024).decode()
            ips=str(ips)
            c.sendall(ips.encode())
            c.recv(1024).decode()
            c.sendall(get_wifi_mac().encode())
            #send email to user
            msg= EmailMessage()
            msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
            msg["From"]="aofnotification@gmail.com"
            msg["To"]=email_rvs
            msg.set_content(f"there are strange rule had been add to your firewall\ndo the protocol to check your devic if you had been hackt")
            email="aofnotification@gmail.com"
            password="oqgspkawnyeftyjw"
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(email,password)
                smtp.send_message(msg)
                    

        #if there a rule delete from the firewall without ordars from the user the belwo code will run        
        elif ld<rellen:
            
            l4=rellen-ld
            rellen-=l4
            #send to the server to add csv file
            c.sendall("hackDel".encode())
            c.recv(1024).decode()
            ips=str(ips)
            c.sendall(ips.encode())
            c.recv(1024).decode()
            c.sendall(get_wifi_mac().encode())
            #send email to user
            msg= EmailMessage()
            msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
            msg["From"]="aofnotification@gmail.com"
            msg["To"]=email_rvs
            msg.set_content(f"there are some rule had been delete from your firewall\ndo the protocol to check your devic if you had been hackt")
            email="aofnotification@gmail.com"
            password="oqgspkawnyeftyjw"
            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                smtp.login(email,password)
                smtp.send_message(msg)
                    
        with open(r"C:\FWSH-files\check.txt","w")as f:
            f.write("")
    #run the main function
    sa.run(main())
    #return to do this loop evry 10s
    time.sleep(10)