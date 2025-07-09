import random
import asyncio as sa
import smtplib
from email.message import EmailMessage
import pandas as pd
import json
import time
import threading as th
import socket as so
# edit all "data= await reder.readline()" to be like "data= await reder.read(90000)"
# احاول افكك الكود الموجود في test.py و اشوف لي طرق لي توصيل كل شي مع بعضه




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





async def h(reder,writer):
    global password1,lll
    writer.write('1'.encode())
    await writer.drain()
    
    data= await reder.read(1000)
    
    addId=data.decode()
    
        
    if addId=="1":
        pass
    else:
        with open('serverSetting.json', 'r') as f:
            serverSetting = json.load(f)
            if serverSetting["email"]=="":
                serverSetting["email"]=addId
                with open('serverSetting.json', 'w') as f:
                    json.dump(serverSetting,f,indent=4)
            else:
                bossemail=serverSetting["email"]
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


    def clos_fw(d):
        time.sleep(1)          
        try:
            command = "off"
            print(len(clients))
            for c in clients:
                try:
                    
                    c.sendall(command.encode())
                except:
                    pass
        except Exception:
            with lock:
                clients.remove(d)
        d.close()
        clients.clear()


    if lll==1:
        lll=0
        th.Thread(target=main).start()
    while True:
        print("1")
        try:
            data= await reder.read(90000)
            if not data:
                break
            dat=data.decode()
            print(dat)
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
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(9000)
                if not data:
                    break
                rulename=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(9000)
                if not data:
                    break
                timerlog=data.decode()
                writer.write("1".encode())
                await writer.drain()
                data= await reder.read(9000)
                if not data:
                    break
                T=data.decode()
                writer.write("1".encode())
                await writer.drain()
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
                
                clos_fw(d=conn)    
                       
                
            if dat=="add new rule":
                with open('serverSetting.json', 'r') as f:
                    serverSetting = json.load(f)
                    bossemail=serverSetting["email"]
                data= await reder.read(90000)
                if not data:
                    break
                p=generate_password()
                writer.write(p.encode())
                await writer.drain() 
                rule=data.decode()
                
                data= await reder.read(9000)
                if not data:
                    break
                ips=data.decode()
                
                msg= EmailMessage()
                msg["Subject"]="edit rule"
                msg["From"]="aofnotification@gmail.com"
                msg["To"]=bossemail
                msg.set_content(f"the IP '{ips}' want to run these rule in his firewall\n\nrule: {rule}\n\nif you aply for this rule send this password to id'1x'\n\npassword: {password1}")
                email="aofnotification@gmail.com"
                password="oqgspkawnyeftyjw"
                with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                    smtp.login(email,password)
                    smtp.send_message(msg)

            if dat=="advance mode":
                with open('serverSetting.json', 'r') as f:
                    serverSetting = json.load(f)
                    bossemail=serverSetting["email"]
                p=generate_password()
                writer.write(p.encode())
                await writer.drain()
                data= await reder.read(9000)
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