import socket as sk
import json
import EncDec as ed



#p=16,d=4,f=6,a=1,r=18,u=22,o=15,t=21
with open('settings.json', 'r') as f:
    settings = json.load(f)
    
    check=settings["firstconn"]
    check=str(check)
    lens=len(check)
    if check.endswith("6"):
        decode=ed.dec(check[:lens-1])
    else:
        # the notification for server
        pass

    

    check1=settings["addid"]
    check1=str(check1)
    lens=len(check1)
    if check1.endswith("1"):
        decode1=ed.dec(check1[:lens-1])    
    else:
        # the notification for server
        pass
    

    if decode=="0":
        # encode=ed.enc(settings["RM"])#####################
        # encode1=ed.enc(settings["URTM"])##################
        # settings["RM"]=encode
        # settings["URTM"]=encode1
        ip=input("Enter IP server: ")
        print(f"Using saved IP: {ip}")
        encode4=ed.enc(ip)

        with open('settings.json', 'w') as f:
            settings["IP-S"] = encode4+'16'
            encode5=ed.enc("1")
            settings["firstconn"] = encode5+'6'
            json.dump(settings, f, indent=4)


    check2=settings["firstconn"]
    check2=str(check2)
    lens=len(check2)
    if check2.endswith("6"):
        decode2=ed.dec(check2[:lens-1])
    else:
        # the notification for server
        pass
    
    
    if decode2=="1":
        check3=settings["IP-S"]
        check3=str(check3)
        lens=len(check3)
        if check3.endswith("16"):
            decode3=ed.dec(check3[:lens-2])
        else:
            # the notification for server
            pass
    
        ip = decode3
        addid = decode1
        
    


while True:
    try:
        c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        c.connect((ip, 9999))
        
        chek=c.recv(1024).decode('utf-8')
        if chek=='1':
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
            settings["addid"]=encode6+'1'
            settings["id"]=di+'4'
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