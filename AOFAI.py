import socket as sk
import json
import EncDec as ed



with open('settings.json', 'r') as f:
    settings = json.load(f)
    
    
    decode=ed.dec(settings["firstconn"])
    decode1=ed.dec(settings["addid"])
    if decode=="0":
        encode=ed.enc(settings["RM"])
        encode1=ed.enc(settings["URTM"])
        settings["RM"]=encode
        settings["URTM"]=encode1
        ip=input("Enter IP server: ")
        print(f"Using saved IP: {ip}")
        encode4=ed.enc(ip)

        with open('settings.json', 'w') as f:
            settings["IP-S"] = encode4
            encode5=ed.enc("1")
            settings["firstconn"] = encode5
            json.dump(settings, f, indent=4)
    decode2=ed.dec(settings["firstconn"])
    
    if decode2=="1":
        decode3=ed.dec(settings["IP-S"])
        ip = decode3
        addid = decode1
        
    


while True:
    try:
        c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        c.connect((ip, 9999))
        
        check=c.recv(1024).decode('utf-8')
        if check=='1':
            break
    except Exception:
        continue

c.sendall(addid.encode('utf-8'))
if addid=="0":
    di=c.recv(1024).decode('utf-8')

    with open('settings.json', 'r') as f:
        settings = json.load(f)
        with open('settings.json', 'w') as f:
            encode6=ed.enc("1")
            settings["addid"]=encode6
            settings["id"]=di
            json.dump(settings,f,indent=4)
        
        
        
    
while True:
    
    masge=input("enter masge: ")
    if masge == "show password":
        c.sendall(masge.encode('utf-8'))
        c.sendall('0'.encode('utf-8'))
        data = c.recv(1024).decode('utf-8')
        print(data)
    elif masge == "exit":
        c.close()
        break
    else:
        # AI
        c.sendall(masge.encode('utf-8'))
        respons=c.recv(1024).decode("utf-8")
        print(respons)