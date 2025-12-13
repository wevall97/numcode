import asyncio as sa
import pandas as pd
import json
import time
import threading as th
import socket as so
import os

# check all code

try:
    
    os.mkdir(r"C:\FWSH-file")
except Exception:
     pass

pathfile=os.path.exists(r"C:\FWSH-file\serverSetting.json")
print("1")
if pathfile==False:
    s='{"email": ""}'
    p=json.loads(s)
    with open(r"C:\FWSH-file\serverSetting.json","w",encoding='utf-8')as f:
        json.dump(p,f,indent=4)
lll=1
with open(r'C:\FWSH-file\serverSetting.json', 'r',encoding='utf-8') as f:
    settings = json.load(f) 
  

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
            with open(r'C:\FWSH-file\serverSetting.json', 'r',encoding='utf-8') as f:
                serverSetting = json.load(f)        
                bossemail=serverSetting["email"]
                bossemail=str(bossemail)
                writer.write(bossemail.encode())
                await writer.drain()
        
        elif addId!="add":
            with open(r'C:\FWSH-file\serverSetting.json', 'r',encoding='utf-8') as f:
                serverSetting = json.load(f)
                if serverSetting["email"]=="":
                    serverSetting["email"]=addId
                    with open(r'C:\FWSH-file\serverSetting.json', 'w',encoding='utf-8') as f:
                        json.dump(serverSetting,f,indent=4)

        with open(r'C:\FWSH-file\serverSetting.json', 'r',encoding='utf-8') as f:
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
                if dat=="off" or dat=="on":
                    
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
                    mac=data.decode()
                    
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\firewall log.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "FWS":["FWS"],
                            "TIMER":["TIMER"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FWSH-file\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "FWS":[dat],
                            "TIMER":[timerlog],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("firewall log.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()
                

            
                    
                    
                    
                    
                    

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

                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    mac=data.decode()
                    
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\delete rule log.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Delete_Ru":["Delete_Ru"],
                            "TIME":["TIME"]
                        }

                        d=pd.DataFrame(datafrme)
                        d.to_csv(r"C:\FWSH-file\delete rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 


                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Delete_Ru":[deleteR],
                            "TIME":[timerlog]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\delete rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("delete rule log.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()

                if dat=="addrule":
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

                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    mac=data.decode()
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\add rule log.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Rule_Name":["Rule_Name"],
                            "RULE":["RULE"],
                            "TIMER":["TIMER"],
                            "CONSTAN":["CONSTAN"],
                            "TIME":["TIME"]
                        }

                        d=pd.DataFrame(datafrme)
                        d.to_csv(r"C:\FWSH-file\add rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Rule_Name":[rulename],
                            "RULE":[RULE],
                            "TIMER":[timerlog],
                            "CONSTAN":[constan],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\add rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("add rule log.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()
                
                if dat=="firewall state off all" or dat=="5" :
                    T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\firewall log.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "FWS":["FWS"],
                            "TIMER":["TIMER"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FWSH-file\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":["ALL"],
                            "MAC":["ALL"],
                            "FWS":["off"],
                            "TIMER":["null"],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("firewall log.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()
                    time.sleep(1.5)
                    writer.write("1".encode())
                    await writer.drain()
                    clos_fw(command="off")    
                        
                
                if dat=="firewall state on all" or dat=="6" :
                    T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\firewall log.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "FWS":["FWS"],
                            "TIMER":["TIMER"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FWSH-file\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":["ALL"],
                            "MAC":["ALL"],
                            "FWS":["on"],
                            "TIMER":["null"],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\firewall log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("firewall log.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()
                    time.sleep(1.5)
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
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    mac=data.decode()
                    T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\issue FWS.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "STATE":["STATE"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FWSH-file\issue FWS.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "STATE":["off"],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\issue FWS.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("issue FWS.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()

                

                if dat=="hackAdd":
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
                    mac=data.decode()
                    T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\issue rule.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "STATE":["STATE"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FWSH-file\issue rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "STATE":["add"],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\issue rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("issue rule.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()


                if dat=="hackDel":
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
                    mac=data.decode()
                    T=str(time.strftime('%Y-%m-%d %H:%M:%S'))
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\issue rule.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "STATE":["STATE"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FWSH-file\issue rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "STATE":["delete"],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\issue rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("issue rule.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()




                if dat=="rua":
                    
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
                    T=data.decode()

                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    action=data.decode()

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

                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    mac=data.decode()
                    
                    try:
                        s=pd.read_csv(r"C:\FWSH-file\action rule log.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "RULE_Name":["RULE_Name"],
                            "ACTION":["ACTION"],
                            "TIMER":["TIMER"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FWSH-file\action rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "RULE_Name":[rulename],
                            "ACTION":[action],
                            "TIMER":[T],
                            "TIME":[timerlog]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FWSH-file\action rule log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("action rule log.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()




                

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