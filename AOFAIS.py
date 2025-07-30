import random
import asyncio as sa
import smtplib
from email.message import EmailMessage
import pandas as pd
import json
import time
import threading as th
import socket as so
import os





pathfile=os.path.exists("serverSetting.json")
if pathfile==False:
    s='{"email": ""}'
    p=json.loads(s)
    with open("serverSetting.json","w")as f:
        json.dump(p,f,indent=4)
lll=1

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

clients = []
lock = th.Lock()

def handle_client(conn,role):
    

    if role == "client":
        
        with lock:
            clients.append(conn)
            
try:
    def main():
        
        global addr,server,conn
        server = so.socket(so.AF_INET, so.SOCK_STREAM)
        server.bind(("0.0.0.0", 9991))
        server.listen()

        

        while True:
            conn,addr= server.accept()
            role = conn.recv(1024).decode()
            thread = th.Thread(target=handle_client, args=(conn,role))
            thread.start()

    
except Exception:
    pass

th.Thread(target=main).start()
async def h(reder,writer):
    global password1,lll,status,from_
    writer.write('1'.encode())
    await writer.drain()
    try:
        data= await reder.read(9000)
    except Exception:
        data = b''
    addId=data.decode()
    
       
    if addId=="1":
        with open('serverSetting.json', 'r') as f:
            serverSetting = json.load(f)        
            bossemail=serverSetting["email"]
            bossemail=str(bossemail)
            writer.write(bossemail.encode())
            await writer.drain()
    
    elif addId!="add":
        with open('serverSetting.json', 'r') as f:
            serverSetting = json.load(f)
            if serverSetting["email"]=="":
                serverSetting["email"]=addId
                with open('serverSetting.json', 'w') as f:
                    json.dump(serverSetting,f,indent=4)

    with open('serverSetting.json', 'r') as f:
        serverSetting = json.load(f)        
        bossemail=serverSetting["email"]
    


    def clos_fw(command):
                 
        try:
            
            for c in clients:
                try:
                    
                    c.sendall(command.encode())
                except:
                    pass
        except Exception:
            with lock:
                clients.remove(d)
        
    while True:
        print("yes")
        try:
            data= await reder.read(90000)
            if not data:
                break
            dat=data.decode().strip()
            print(dat)
        except Exception:
            pass
        try:

            if dat=="gg":
                
                break
            if dat=="off":
                
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                timerlog=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                T=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
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
            

           
                
                
                
                
                

            if dat=="del":

                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                deleteR=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                timerlog=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                ips=data.decode()
                
                try:
                    s=pd.read_csv(r"D:\projackt\tools\delete rule log.csv")
                except Exception:
                    datafrme={
                        "IP":["IP"],
                        "deleteR":["deleteR"],
                        "TIME":["TIME"]
                    }

                    d=pd.DataFrame(datafrme)
                    d.to_csv(r"D:\projackt\tools\delete rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


                datafrme={
                        "IP":[ips],
                        "deleteR":[deleteR],
                        "TIME":[timerlog]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\delete rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)

            if dat=="on":
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                rulename=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                timerlog=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                T=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                ips=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                RULE=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                constan=data.decode()
                try:
                    s=pd.read_csv(r"D:\projackt\tools\add rule log.csv")
                except Exception:
                    datafrme={
                        "IP":["IP"],
                        "RuleN":["RuleN"],
                        "RULE":["RULE"],
                        "TIMER":["TIMER"],
                        "CONSTAN":["CONSTAN"],
                        "TIME":["TIME"]
                    }

                    d=pd.DataFrame(datafrme)
                    d.to_csv(r"D:\projackt\tools\add rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


                datafrme={
                        "IP":[ips],
                        "RuleN":[rulename],
                        "RULE":[RULE],
                        "TIMER":[timerlog],
                        "CONSTAN":[constan],
                        "TIME":[T]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\add rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
            
            if dat=="firewall states off all":
                T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
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
                        "IP":["ALL"],
                        "FWS":["off"],
                        "TIMER":["null"],
                        "TIME":[T]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                writer.write("1".encode())
                await writer.drain()
                clos_fw(command="off")    
                       

            if dat=="firewall states on all":
                T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
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
                        "IP":["ALL"],
                        "FWS":["on"],
                        "TIMER":["null"],
                        "TIME":[T]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                writer.write("1".encode())
                await writer.drain()
                clos_fw(command="on")

            
            if dat=="hackOff":
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                ips=data.decode()
                T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                try:
                    s=pd.read_csv(r"D:\projackt\tools\issue FWS.csv")
                except Exception:
                    datafrme={
                        "IP":["IP"],
                        "STATE":["STATE"],
                        "TIME":["TIME"]
                    }

                    s=pd.DataFrame(datafrme)
                    s.to_csv(r"D:\projackt\tools\issue FWS.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                datafrme={
                        "IP":[ips],
                        "STATE":["off"],
                        "TIME":[T]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\issue FWS.csv",index=False,encoding='utf-8-sig',mode='a',header=False)

            

            if dat=="hackAdd":
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                ips=data.decode()
                T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                try:
                    s=pd.read_csv(r"D:\projackt\tools\issue rule.csv")
                except Exception:
                    datafrme={
                        "IP":["IP"],
                        "STATE":["STATE"],
                        "TIME":["TIME"]
                    }

                    s=pd.DataFrame(datafrme)
                    s.to_csv(r"D:\projackt\tools\issue rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                datafrme={
                        "IP":[ips],
                        "STATE":["add"],
                        "TIME":[T]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\issue rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


            if dat=="hackDel":
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                ips=data.decode()
                T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                try:
                    s=pd.read_csv(r"D:\projackt\tools\issue rule.csv")
                except Exception:
                    datafrme={
                        "IP":["IP"],
                        "STATE":["STATE"],
                        "TIME":["TIME"]
                    }

                    s=pd.DataFrame(datafrme)
                    s.to_csv(r"D:\projackt\tools\issue rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                datafrme={
                        "IP":[ips],
                        "STATE":["delete"],
                        "TIME":[T]
                    }

                d=pd.DataFrame(datafrme)
                d.to_csv(r"D:\projackt\tools\issue rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


            # if dat=="add new rule":
            #     with open('serverSetting.json', 'r') as f:
            #         serverSetting = json.load(f)
            #         bossemail=serverSetting["email"]
            #     data= await reder.read(90000)
            #     if not data:
            #         break
            #     p=generate_password()
            #     writer.write(p.encode())
            #     await writer.drain() 
            #     rule=data.decode()
                
            #     data= await reder.read(90000)
            #     if not data:
            #         break
            #     ips=data.decode()
                
            #     msg= EmailMessage()
            #     msg["Subject"]="edit rule"
            #     msg["From"]="aofnotification@gmail.com"
            #     msg["To"]=bossemail
            #     msg.set_content(f"the IP '{ips}' want to run these rule in his firewall\n\nrule: {rule}\n\nif you aply for this rule send this password to id'1x'\n\npassword: {password1}")
            #     email="aofnotification@gmail.com"
            #     password="oqgspkawnyeftyjw"
            #     with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            #         smtp.login(email,password)
            #         smtp.send_message(msg)

            if dat=="advance mode":
                with open('serverSetting.json', 'r') as f:
                    serverSetting = json.load(f)
                    bossemail=serverSetting["email"]
                p=generate_password()
                writer.write(p.encode())
                await writer.drain()
                data= await reder.read(90000)
                if not data:
                    break
                ips=data.decode()
                msg= EmailMessage()
                msg["Subject"]="advance mode"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=bossemail
                msg.set_content(f"the IP '{ips}' want to be in 'advance mode'\n\nif you aply for this,send this password to id'1x'\n\npassword: {password1}")
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