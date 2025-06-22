import socket as sk
import json

with open('sh.json', 'r') as f:
    settings = json.load(f)
    if settings["firstconn"]=="0":
        ip=input("Enter IP server: ")
        with open('sh.json', 'w') as f:
            settings["IP-S"] = ip
            settings["firstconn"] = "1"
            json.dump(settings, f, indent=4)
    if settings["firstconn"]=="1":
        ip = settings["IP-S"]
        addid = settings["addid"]
        print(f"Using saved IP: {ip}")


while True:
    try:
        c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        c.connect(('192.168.1.13', 9999))
        check=c.recv(1024).decode('utf-8')
        if check=='1':
            break
    except Exception:
        continue


addid=str(addid)
c.sendall(addid.encode('utf-8'))
di=c.recv(1024).decode('utf-8')
with open('sh.json', 'r') as f:
    settings = json.load(f)
    with open('sh.json', 'w') as f:
        settings["addid"]="1"
        settings["id"]=di
        json.dump(settings,f,indent=4)



while True:
    masge=input("enter masge: ")
    if masge=="show password":
        c.sendall(masge.encode('utf-8'))
        c.sendall('1'.encode('utf-8'))
        password=c.recv(1024).decode("utf-8")
        print(password)
    elif masge == "exit":
        c.close()
        break
    else:
        # AI
        c.sendall(masge.encode('utf-8'))
        respons=c.recv(1024).decode("utf-8")
        print(respons)