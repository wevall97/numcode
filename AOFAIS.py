import socket as sk
import time
import random
import threading as th
import json
import EncDec as ed

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
        new=',{"id": "0x", "RM": "Disable", "URTM": "Enable", "active": False, "Roule": [], "timer": []}'

        with open('UsersRolus.json', 'r') as f:
            data = json.load(f)
            decode=ed.dec(data["len"])
            if decode=="9":
                break
            p=decode
            
            pp=int(p)
            pp+=1
            pp=str(pp)
            data=str(data)
            
            n=new.replace("0x",pp+"x")
            
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
           
            j["USERS"][pp+1]["id"]=encode0
            j["USERS"][pp+1]["RM"]=encode1
            j["USERS"][pp+1]["URTM"]=encode2
            j["USERS"][pp+1]["active"]=encode3
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
else:
    pass    



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