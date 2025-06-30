import socket as sk
import time
import random
import threading as th
import json
import EncDec as ed
import asyncio as sa
import smtplib
from email.message import EmailMessage


rowId=['zero','one','two','..']
def generate_password():
    global row1,password1
    row1 = []
    while True:
        for _ in range(6):
            ran = random.randint(0, 9)
            ran = str(ran)
            row1.append(ran)
            
        password1 = ''.join(map(str,row1))
        row1.clear()
        time.sleep(3600)
th.Thread(target=generate_password).start()




async def h(reder,writer):
    global password1
    writer.write('1'.encode())
    await writer.drain()
    
    data= await reder.read(1000)
    
    addId=data.decode()
    
    if addId=="0":
        for _ in range(1): 

            rows=[]
            row=[]
            

            with open('UsersRolus.json', 'r') as f:
                data = json.load(f)
                decode=ed.dec(data["len"])
                if decode=="9":
                    break
                p=decode
                
                pp=int(p)
                pp+=1
                new=',{"id": "0x", "FWS": "on", "RM": "Disable", "URTM": "Enable", "active": False, "Roule": []}'
                n=new.replace("0x",rowId[pp])
            
                pp=str(pp)
                data=str(data)
                
                
                l=len(data)
                
                for i in data:
                    if i=="'":
                        i='"'
                        row.append(i)
                    else:
                        row.append(i)
                
                
                for ii in n:
                    rows.append(ii)
                row=row[:l-2]+rows+row[l-2:]
                
                d=''.join(row)
                row.clear()
                rows.clear()
                dd=d.replace('True', 'true').replace('False', 'false')
                
                
                pp=int(pp)
                j=json.loads(dd)
                
                encode0=ed.enc(j["USERS"][pp+1]["id"])
                encode1=ed.enc(j["USERS"][pp+1]["RM"])
                encode2=ed.enc(j["USERS"][pp+1]["URTM"])
                encode3=ed.enc(str(j["USERS"][pp+1]["active"]))
                encode4=ed.enc(j["USERS"][pp+1]["FWS"])

                j["USERS"][pp+1]["id"]=encode0
                j["USERS"][pp+1]["RM"]=encode1
                j["USERS"][pp+1]["URTM"]=encode2
                j["USERS"][pp+1]["active"]=encode3
                j["USERS"][pp+1]["FWS"]=encode4+'19'
                pp=str(pp)
                
                pp=ed.enc(pp)
                j["len"]=pp
                
            with open('UsersRolus.json', 'w') as f:
                json.dump(j, f, indent=4)
            with open('UsersRolus.json', 'r') as f:
                data=json.load(f)
                pp=ed.dec(pp)
                pp=int(pp)
                
                di=data["USERS"][pp+1]["id"]
                di=str(di)
                writer.write(di.encode())
                await writer.drain()

    while True:
        data= await reder.read(1000)
        if not data:
            break
        dat=data.decode()
          
        if dat=='show password':
            writer.write(password.encode())
            await writer.drain()
        if dat=="firewall states off all":
            # let all users firewall off
            # save the data in encrpt file
            pass        
        if dat=="add new rule":
            data= await reder.read(1000)
            if not data:
                break
            writer.write(password1.encode())
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
            writer.write(password1.encode())
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







               
    writer.close()
    await writer.wait_closed()


async def m():
    s=await sa.start_server(h,'0.0.0.0',9999)
    async with s:
        await s.serve_forever()
sa.run(m())