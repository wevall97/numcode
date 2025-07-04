import time
import random
import threading as th
import EncDec as ed
import asyncio as sa
import smtplib
from email.message import EmailMessage
import pandas as pd
# remove all codes of add data to "UsersRolus.json" and instaed add new way to gust read and give new id 
# edit all "data= await reder.readline()" to be like "data= await reder.read(90000)"
# remove "show password"
# edit "generate_password()" to work when server want to send password
# in "add new rule" let the boss send his email so "AOFAIS" send the email to him




def generate_password():
    global row1,password1
    row1 = []
    for _ in range(6):
        ran = random.randint(0, 9)
        ran = str(ran)
        row1.append(ran)
        
    password1 = ''.join(map(str,row1))
    row1.clear()
    return password1   




rowse=set()
async def h(reder,writer):
    global password1
    writer.write('1'.encode())
    await writer.drain()
    
    data= await reder.read(1000)
    
    addId=data.decode()
    if addId=="add":
        
        rowse.add(writer)
    

    while True:
        try:
            data= await reder.read(1000)
            if not data:
                break
            dat=data.decode()
        except Exception:
            pass
        try:
            if dat=="off":
                
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(1000)
                if not data:
                    break
                timerlog=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(1000)
                if not data:
                    break
                T=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(1000)
                if not data:
                    break
                ips=data.decode()
                
                try:
                    s=pd.read_csv(r"D:\projackt\tools\firewall log.csv")
                except Exception:
                    datafrme={
                        "IP":["IP"],
                        "FWS":["FWS"],
                        "TIMER":["TIMER"],
                        "TIME":["TIME"]
                    }

                    s=pd.DataFrame(datafrme)
                    s.to_csv(r"D:\projackt\tools\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                datafrme={
                        "IP":[ips],
                        "FWS":["off"],
                        "TIMER":[timerlog],
                        "TIME":[T]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
            if dat=="on":
                data= await reder.read(9000)
                if not data:
                    break
                rulename=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.readline()
                if not data:
                    break
                timerlog=data.decode().strip()
                data= await reder.readline()
                if not data:
                    break
                T=data.decode().strip()
                data= await reder.read(1000)
                if not data:
                    break
                ips=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(900000)
                if not data:
                    break
                RULE=data.decode()
                try:
                    s=pd.read_csv(r"D:\projackt\tools\add rule log.csv")
                except Exception:
                    datafrme={
                        "IP":["IP"],
                        "RuleN":["RuleN"],
                        "RULE":["RULE"],
                        "TIMER":["TIMER"],
                        "TIME":["TIME"]
                    }

                    d=pd.DataFrame(datafrme)
                    d.to_csv(r"D:\projackt\tools\add rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


                datafrme={
                        "IP":[ips],
                        "RuleN":[rulename],
                        "RULE":[RULE],
                        "TIMER":[timerlog],
                        "TIME":[T]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\add rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
            
            if dat=="firewall states off all":
                
                for writer in range(1):# if something hapned rename 'writer' to "dgdgh"
                    print("1")
                    try:
                        writer.write('off'.encode())#edit
                        await writer.drain()
                        rowse.remove(writer)
                    except Exception:
                        rowse.remove(writer)



            if dat=="add new rule":
                data= await reder.read(1000)
                if not data:
                    break
                p=generate_password()
                writer.write(p.encode())
                await writer.drain() 
                rule=data.decode()
                msg= EmailMessage()
                msg["Subject"]="edit rule"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]="aliwevall77@gmail.com"
                msg.set_content(f"the id '1x' want to run these rule in his firewall\n\nrule: {rule}\n\nif you aply for this rule send this password to id'1x'\n\npassword: {password1}")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)

            if dat=="advance mode":
                p=generate_password()
                writer.write(p.encode())
                await writer.drain() 
                msg= EmailMessage()
                msg["Subject"]="advance mode"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]="aliwevall77@gmail.com"
                msg.set_content(f"the id '1x' want to be in 'advance mode'\n\nif you aply for this,send this password to id'1x'\n\npassword: {password1}")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)

        except Exception:
            break





    try:          
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass

async def m():
    s=await sa.start_server(h,'0.0.0.0',9999)
    async with s:
        await s.serve_forever()
sa.run(m())