import socket as sk



while True:
    try:
        c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        c.connect(('192.168.1.13', 9999))
        check=c.recv(1024).decode('utf-8')
        if check=='1':
            break
    except Exception:
        continue
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