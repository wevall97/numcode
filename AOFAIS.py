import socket as sk
import time
import random
import threading as th




s=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen(1)
sip=sk.gethostbyname(sk.gethostname())

conn, addr = s.accept()
addId=conn.recv(1024).decode('utf-8')

def generate_password():
    global row,password
    row = []
    while True:
        for _ in range(6):
            ran = random.randint(0, 9)
            ran = str(ran)
            row.append(ran)
            
        password = ''.join(map(str,row))
        row.clear()
        time.sleep(30)
th.Thread(target=generate_password).start()



while True:
   
        data = conn.recv(1024).decode('utf-8')
        if data=='show password':
            check=conn.recv(1024).decode('utf-8')
            if check == '1':
                conn.sendall(password.encode("utf-8"))
            elif check == '0':
                conn.sendall("Invalid request received.".encode("utf-8"))
        else:
            # AI
            pass
        
        if not data:
            break
    
conn.close()

    