import socket as sk
import time
import random
import threading as th
import json
import EncDec as ed


rowId=['zero','one','two','..']
def generate_password():
    global row1,password
    row1 = []
    while True:
        for _ in range(6):
            ran = random.randint(0, 9)
            ran = str(ran)
            row1.append(ran)
            
        password = ''.join(map(str,row1))
        row1.clear()
        time.sleep(30)
th.Thread(target=generate_password).start()



s=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen(1)
conn, addr = s.accept()


conn.sendall("1".encode('utf-8'))
addId=conn.recv(1024).decode('utf-8')


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
            new=',{"id": "0x", "FWS": "on", "RM": "Disable", "URTM": "Enable", "active": False, "Roule": [], "timer": []}'
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
            conn.sendall(di.encode('utf-8'))
  



while True:
   
        dat = conn.recv(1024).decode('utf-8')
        if dat=='show password':
            check=conn.recv(1024).decode('utf-8')
            if check == '1':
                conn.sendall(password.encode("utf-8"))
            elif check == '0':
                conn.sendall("Invalid request received.".encode("utf-8"))
        else:
            # AI
            pass
        
        if not dat:
            break
    
conn.close() 