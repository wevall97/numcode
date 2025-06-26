import time
import subprocess as su
import socket as sk
import threading as th
import json
import EncDec as ed

rowFWS=["on","off"]
rowCheck=["Enable","Disable"]
rowId=['zero','one','two','..']
#p=16,d=4,f=6,a=1,r=18,u=22,o=15,t=21,s=19
with open('settings.json', 'r') as f:
    settings = json.load(f)
    

    check=settings["IP-S"]
    check=str(check)
    lens=len(check)
    if check.endswith("16"):
        decode=ed.dec(check[:lens-2])
        ip = decode
        print(ip)
    else:
        print("no")
        # the notification for server
        pass
    
    



    check1=settings["id"]
    check1=str(check1)
    lens=len(check1)
    if check1.endswith("4"):
        decode1=ed.dec(check1[:lens-1])
        
        if decode1 in rowId:
            ID= str(rowId.index(decode1))
            ID=ID+'x'
            print(ID)
        else:
            print("non")
          # the notification for server
            pass  
        
    else:
        print("no")
        # the notification for server
        pass
    
    
    


    
    check2=settings["RM"]
    check2=str(check2)
    lens=len(check2)
    if check2.endswith("18"):
        decode2=ed.dec(check2[:lens-2])
        if decode2 in rowCheck:
            rm= decode2
            print(rm)
        else:
            print("non")
            # the notification for server
            pass
    else:
        print("no")
        # the notification for server
        pass
    
    


    check3=settings["URTM"]
    check3=str(check3)
    lens=len(check3)
    if check3.endswith("22"):
        decode3=ed.dec(check3[:lens-2])
        if decode3 in rowCheck:
            utrm= decode3
            print(utrm)
        else:
            print("non")
            # the notification for server
            pass
        
    else:
        print("no")
        # the notification for server
        pass
    
    

    check4=settings["FWS"]
    check4=str(check4)
    lens=len(check4)
    if check4.endswith("19"):
        decode4=ed.dec(check4[:lens-2])
        if decode4 in rowFWS:
            fws = decode4
            print(fws)
        else:
            print("no")
            # the notification for server
            pass
    else:
        print("no")
        # the notification for server
        pass


# while True:
#     try:
#         c=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
#         try:
#             c.connect((ip, 9999))
#         except ConnectionRefusedError:
#             print("the server is shot downe")
#             break 
#         except Exception:
#             print(f"somethig hapned to the ip server it is change to '{ip}'")
#             break
        
#         chck=c.recv(1024).decode('utf-8')
#         if chck=='1':
            
#             break
#     except Exception:
        
#         continue
    

# while True:
    
        
#     s=su.run('netsh advfirewall show allprofiles', shell=True, capture_output=True, text=True)
#     f=s.stdout
#     if 'RemoteManagement                      Enable' in f:
#         pass
#     if 'UnicastResponseToMulticast            Disable' in f:
#         pass
#     if 'State                                 OFF' in f or len(f) != 2094 :
        
#         su.run('netsh advfirewall set allprofiles state on', shell=True)
#         with open(r'C:\Users\ibrah\logfirewall\firewall state.txt', '+a') as file:
#             file.write(f'Firewall was off at {time.strftime('%Y-%m-%d %H:%M:%S')} \n')
    
#     time.sleep(30)  
    