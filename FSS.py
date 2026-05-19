import asyncio as sa
import pandas as pd
import json
import time
import threading as th
import socket as so
import os

# type "Rule" instad of anythings sayed "rule name"
# check all code
# اذكر انك لازم في كتلوج المستخدمين انو netsh سوف يتم حذفها عبر مايكرسوفت عشان كده النظام بيدعم اوامر power shell يس

try:
    
    os.mkdir(r"C:\FS-Server")
except Exception:
     pass

pathfile=os.path.exists(r"C:\FS-Server\serverSetting.json")

if pathfile==False:
    s='{"email": ""}'
    p=json.loads(s)
    with open(r"C:\FS-Server\serverSetting.json","w",encoding='utf-8')as f:
        json.dump(p,f,indent=4)
#lll=1
with open(r'C:\FS-Server\serverSetting.json', 'r',encoding='utf-8') as f:
    settings = json.load(f) 
  

    clients = []
    lock = th.Lock()

    def handle_client(conn, role):
        if role == "client":
            with lock:
                clients.append(conn)
            
            # ابقَ حياً حتى ينقطع الاتصال
            try:
                while True:
                    # نحاول القراءة لنكتشف إذا انقطع الاتصال
                    data = conn.recv(1024)
                    if not data:
                        break  # الاتصال انقطع
            except Exception:
                pass
            finally:
                with lock:
                    if conn in clients:
                        clients.remove(conn)
                conn.close()
                
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
        #global lll
        writer.write('1'.encode())
        await writer.drain()
        try:
            data= await reder.read(9000)
        except Exception:
            data = b''
        addId=data.decode()
        
        
        if addId=="1":
            with open(r'C:\FS-Server\serverSetting.json', 'r',encoding='utf-8') as f:
                serverSetting = json.load(f)        
                bossemail=serverSetting["email"]
                #bossemail=str(bossemail)
                writer.write(bossemail.encode())
                await writer.drain()
        
        elif addId!="add":
            with open(r'C:\FS-Server\serverSetting.json', 'r',encoding='utf-8') as f:
                serverSetting = json.load(f)
                #if serverSetting["email"]=="":
                serverSetting["email"]=addId
                with open(r'C:\FS-Server\serverSetting.json', 'w',encoding='utf-8') as f:
                    json.dump(serverSetting,f,indent=4)

        with open(r'C:\FS-Server\serverSetting.json', 'r',encoding='utf-8') as f:
            serverSetting = json.load(f)        
            bossemail=serverSetting["email"]
        


        def clos_fw(command):
            global clients
            dead = []
            for c in clients:
                try:
                    c.sendall(command.encode())
                except Exception:
                    dead.append(c)
            with lock:
                for c in dead:
                    if c in clients:
                        clients.remove(c)
            
        while True:
            
            try:
                data= await reder.read(90000)
                if not data:
                    break
                dat=data.decode().strip()
                
            except Exception:
                pass
            try:

                # if dat=="gg":
                #      make a test in this
                #     break
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
                        s=pd.read_csv(r"C:\FS-Server\Firewall_log.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "FWS":["FWS"],
                            "TIMER":["TIMER"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-Server\Firewall_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "FWS":[dat],
                            "TIMER":[timerlog],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Firewall_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
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
                        s=pd.read_csv(r"C:\FS-Server\Delete_rule.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Delete_Rule":["Delete_Rule"],
                            "TIME":["TIME"]
                        }

                        d=pd.DataFrame(datafrme)
                        d.to_csv(r"C:\FS-Server\Delete_rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 


                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Delete_Rule":[deleteR],
                            "TIME":[timerlog]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Delete_rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
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
                        s=pd.read_csv(r"C:\FS-Server\Add_rule_log.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Rule_Name":["Rule_Name"],
                            "RULE":["RULE"],
                            "TIMER":["TIMER"],
                            "Permanent":["Permanent"],
                            "TIME":["TIME"]
                        }

                        d=pd.DataFrame(datafrme)
                        d.to_csv(r"C:\FS-Server\Add_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False)


                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Rule_Name":[rulename],
                            "RULE":[RULE],
                            "TIMER":[timerlog],
                            "Permanent":[constan],# get for it a new name
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Add_rule_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("add rule log.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()
                


                if dat=="firewall state off all" or dat=="5" :
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    T=data.decode()
                    writer.write("1".encode())
                    await writer.drain()

                    try:
                        s=pd.read_csv(r"C:\FS-Server\Firewall_log.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "FWS":["FWS"],
                            "TIMER":["TIMER"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-Server\Firewall_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":["ALL"],
                            "MAC":["ALL"],
                            "FWS":["off"],
                            "TIMER":["null"],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Firewall_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("firewall log.csv".encode())
                        await writer.drain()

                    # writer.write("1".encode())
                    # await writer.drain()
                    time.sleep(1.5)
                    # writer.write("1".encode())
                    # await writer.drain()
                    clos_fw(command="off")    



                # delete it because it is not insasary
                if dat=="firewall state on all" or dat=="6" :
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    T=data.decode()
                    writer.write("1".encode())
                    await writer.drain()

                    try:
                        s=pd.read_csv(r"C:\FS-Server\Firewall_log.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "FWS":["FWS"],
                            "TIMER":["TIMER"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-Server\Firewall_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":["ALL"],
                            "MAC":["ALL"],
                            "FWS":["on"],
                            "TIMER":["null"],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Firewall_log.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("firewall log.csv".encode())
                        await writer.drain()

                    # writer.write("1".encode())
                    # await writer.drain()
                    time.sleep(1.5)
                    # writer.write("1".encode())
                    # await writer.drain()
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
                    T=str(time.strftime('%Y-%m-%d %H:%M:%S'))#check it 
                    try:
                        s=pd.read_csv(r"C:\FS-Server\Firewall_Tamper.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "STATE":["STATE"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-Server\Firewall_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "STATE":["off"],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Firewall_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("issue FWS.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()

                

                if dat=="hackDel":
                    
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    Program_Name=data.decode()

                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    Program_Path=data.decode()
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
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    dn=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    na=data.decode()

                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    white=data.decode()
                    
                    try:
                        s=pd.read_csv(r"C:\FS-Server\Delete_Rule_Tamper.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Program_Name":["Program_Name"],
                            "Program_Path":["Program_Path"],
                            "white list":["white list"],
                            "DisplayName":["DisplayName"],
                            "Name":["Name"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-Server\Delete_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Program_Name":[Program_Name],
                            "Program_Path":[Program_Path],
                            "white list":[white],
                            "DisplayName":[dn],
                            "Name":[na],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Delete_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("issue rule.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()



                if dat=="hackMod":

                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    Program_Name=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    Program_Path=data.decode()
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
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    dn=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    na=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    ii=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    gema=data.decode()
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
                    white=data.decode()
                    
                    try:
                        s=pd.read_csv(r"C:\FS-Server\Modified_Rule_Tamper.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Program_Name":["Program_Name"],
                            "Program_Path":["Program_Path"],
                            "white list":["white list"],
                            "DisplayName":["DisplayName"],
                            "Name":["Name"],
                            "Modified item":["Modified item"],
                            "New value":["New value"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-Server\Modified_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Program_Name":[Program_Name],
                            "Program_Path":[Program_Path],
                            "white list":[white],
                            "DisplayName":[dn],
                            "Name":[na],
                            "Modified item":[ii],
                            "New value":[gema],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Modified_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("issue rule.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()

                


                if dat=="hackAdd":
                    
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    Program_Name=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    Program_Path=data.decode()
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
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    dn=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    na=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    di=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    ac=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    pr=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    en=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    pro=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    lo=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    re=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    pg=data.decode()
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
                    white=data.decode()
                    
                    try:
                        s=pd.read_csv(r"C:\FS-Server\Add_Rule_Tamper.csv") 
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "Program_Name":["Program_Name"],
                            "Program_Path":["Program_Path"],
                            "white list":["white list"],
                            "DisplayName":["DisplayName"],
                            "Name":["Name"],
                            "Direction":["Direction"],
                            "Action":["Action"],
                            "Profile":["Profile"],
                            "Enabled":["Enabled"],
                            "Protocol":["Protocol"],
                            "LocalPort":["LocalPort"],
                            "RemotePort":["RemotePort"],
                            "Program":["Program"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-Server\Add_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "Program_Name":[Program_Name],
                            "Program_Path":[Program_Path],
                            "white list":[white],
                            "DisplayName":[dn],
                            "Name":[na],
                            "Direction":[di],
                            "Action":[ac],
                            "Profile":[pr],
                            "Enabled":[en],
                            "Protocol":[pro],
                            "LocalPort":[lo],
                            "RemotePort":[re],
                            "Program":[pg],
                            "TIME":[T]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\Add_Rule_Tamper.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
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
                    component=data.decode()

                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    newvalue=data.decode()

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
                        s=pd.read_csv(r"C:\FS-Server\State_rule.csv")
                    except Exception:
                        datafrme={
                            "IP":["IP"],
                            "MAC":["MAC"],
                            "RULE":["RULE"],
                            "component":["Component"],
                            "newvalue":["NewValue"],
                            "TIME":["TIME"]
                        }

                        s=pd.DataFrame(datafrme)
                        s.to_csv(r"C:\FS-Server\State_rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False)
                    datafrme={
                            "IP":[ips],
                            "MAC":[mac],
                            "RULE":[rulename],
                            "Component":[component],
                            "NewValue":[newvalue],
                            "TIME":[timerlog]
                        }

                    d=pd.DataFrame(datafrme)
                    try:
                        d.to_csv(r"C:\FS-Server\State_rule.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
                    except Exception:
                        writer.write("action rule log.csv".encode())
                        await writer.drain()
                    writer.write("1".encode())
                    await writer.drain()


                if dat=="settings":
                    writer.write("1".encode())
                    await writer.drain()
                    data= await reder.read(90000)
                    if not data:
                        break
                    email=data.decode()
                    writer.write("1".encode())
                    await writer.drain()
                    with open(r'C:\FS-Server\serverSetting.json', 'r',encoding='utf-8') as f:
                        serverSetting = json.load(f)
                        serverSetting["email"]=email
                        with open(r'C:\FS-Server\serverSetting.json', 'w',encoding='utf-8') as f:
                            json.dump(serverSetting,f,indent=4)
                    time.sleep(1.5)
                    clos_fw(command=email)
                    
            except Exception:
            
                break


        try:          
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

    async def m():
        server=await sa.start_server(h,'0.0.0.0',9999)
        async with server:
            await server.serve_forever()
    sa.run(m())