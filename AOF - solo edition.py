import time
import subprocess as su
import threading as th
import json
import fireSett as fs
import asyncio as sa
import smtplib
from email.message import EmailMessage
import os
import uuid

# check all code
# serish erorr: when i delete a rule without using the system the "aof.py" send to the server "delhac" but nothing alse hapen

with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
    settings = json.load(f) 
    chck2=0
    while True:
        try:
            pathfile=os.path.exists(r"C:\FWSH-files\sent_ids.txt")
            if pathfile==False:
                with open(r"C:\FWSH-files\sent_ids.txt","w",encoding='utf-8')as f:
                    f.write("")

            #check firewall state    
            a=su.run('powershell -Command "Get-NetFirewallProfile | Select-Object Enabled"',shell=True,text=True,capture_output=True)
            a=a.stdout  
            if "False" in a: 
                su.run(r"powershell -Command Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True",shell=True,text=True,capture_output=False,stderr=su.DEVNULL)

            #conn with the praimry conn   
            

            #return D:\FWSH-files\settings.json to the defult
            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f) 
                
                if settings["FWS"]=="":
                    settings["FWS"]="null"
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["timerF"]=="":
                    settings["timerF"]="0"
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["Rolue"]!="null":
                    settings["Rolue"]="null"
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["FWS"]=="off" or settings["FWS"]=="on" or settings["FWS"]=="off-all":
                    settings["FWS"]="null"
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["timerF"]!="0":
                    settings["timerF"]="0"
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["timerR"]!=[]:
                    settings["timerR"]=[]
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["ruleName"]!=[]:
                    settings["ruleName"]=[]
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["checkrulename"]!=[]: 
                    for aa in settings["checkrulename"]:
                        su.run(f'powershell -Command Remove-NetFirewallRule -DisplayName "{aa}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                    settings["checkrulename"]=[]
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                if settings["constan"]!="no":
                    settings["constan"]="no"
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                
                if settings["deleteR"]!="null":
                    settings["deleteR"]="null"
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                email_rvs=settings["email"]
                



            with open(r"C:\FWSH-files\FirewallRules.txt","w",encoding='utf-8')as f:
                    f.write("")
            #cuntant firewall rules lenghth
            su.run(r'powershell -Command "Get-NetFirewallRule | Select-Object -ExpandProperty Name | Out-File "C:\FWSH-files\FirewallRules.txt" -Encoding utf8"',shell=True,text=True,capture_output=False,stderr=su.DEVNULL)
            with open(r"C:\FWSH-files\FirewallRules.txt","r",encoding='utf-8')as f:
                a=f.readlines()
                ld=0
                for _ in a:
                    ld+=1
                rellen=ld

            
            
                chck2=1
            #keys to contrule
            l=1
         
            #function to check the D:\FWSH-files\settings.json evry 10s
            async def check_files():
                global fws,ip,timer,rule,rulename,timerr,ips,constan,deleteR,rellen,enaply,disaply
                
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                

                    rowFWS=["on","off","null"]
                    check4=settings["FWS"]
                    
                    deleteR=settings["deleteR"]

                    if check4 in rowFWS:
                        fws= check4
                            
                        

                    check5=settings["timerF"]
                    
                    timer=int(check5)      


                    constan=settings["constan"]

                    lens=settings["ruleName"]
                    lens=len(lens)
                    rule=settings["Rolue"]
                    if lens!=0 and constan=="no":
                        
                        rulename=settings["ruleName"][0]
                        timerr=settings["timerR"][0]
                        timerr=int(timerr)



                    enaply=settings["Enaply list"]
                    disaply=settings["Disaply list"]
                    
                        
                    
                    
                        

                    

                        
            #function to close the firewall
            def do_ruls():
                global l
                if fws=="off" and l==1:
                    l=0
                    fs.fireOff(fws,timer)
                    with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        settings["FWS"]="null"
                        settings["timerF"]="0"
                        with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                            json.dump(settings,f,indent=4)
                    l=1
                    
            #function to add rules to the firewall
            def add__rule():
                global rulename,rellen,timerr
                
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    a=settings["ruleName"]
                    w=settings["timerR"]
                    a=list(a)
                    w=list(w)
                    a.pop(0)
                    w.pop(0)
                    settings["ruleName"]=a
                    settings["timerR"]=w
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4) 
                

                rulename1=fs.add_rule(rulename,timerr)
                
                rellen=rellen-1
                
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    v=settings["checkrulename"]
                    v=list(v)        
                    v.remove(rulename1)
                    settings["checkrulename"]=v
                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                        json.dump(settings,f,indent=4)
                    
                    

            while True:
                
                # #the main function that contrule in evry things
                async def main():
                    # pass
                    global l,email_rvs,email_rvs,rellen,l3,l4,constan,rule,disaply,enaply
                    
                    
                    #run the check D:\FWSH-files\settings.json function
                    sa.gather(check_files())
                    
                    
                    await sa.sleep(0)
                    #check order from user
                    if fws=="off" and l==1:
                        #run close firewall function
                        th.Thread(target=do_ruls).start()
                    elif fws=="on":
                        #open firewall
                        su.run(r"powershell -Command Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True",shell=True,text=True,capture_output=False,stderr=su.DEVNULL)
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            settings["FWS"]="null"
                            settings["timerF"]="0"
                            with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4)
                        l=1
                    #check if the firewall state is off without the user send any ordurs
                    with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                        settings = json.load(f)
                        check=settings["FWS"]
                    if check=="null":
                        a=su.run('powershell -Command "Get-NetFirewallProfile | Select-Object Enabled"',shell=True,text=True,capture_output=True)
                        a=a.stdout
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                firews=settings["FWS"]
                                firews=str(firews)
                        #run the belwo code if firewall is off without the user send any ordurs to return firewall on   
                        if "False" in a and firews=="null" :
                            su.run('powershell -Command Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True', shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                            #send to server to add to the csv file
                            
                            #send email to the user
                            msg= EmailMessage()
                            msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                            msg["From"]="aofnotification@gmail.com"
                            msg["To"]=email_rvs
                            msg.set_content(f"your firewall state has been off,we rutern it to be open.\ndo the protocol to check your devic if you had been hackt")
                            email="aofnotification@gmail.com"
                            password="oqgspkawnyeftyjw"
                            with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                                smtp.login(email,password)
                                smtp.send_message(msg)


                    #delete rule from the firewall
                    if deleteR!="null":
                        su.run(f'powershell -Command Remove-NetFirewallRule -DisplayName "{deleteR}"',shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                        rellen=rellen-1
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            settings["deleteR"]="null"
                            with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4)



                    #add rule to the firewall 
                    if rule!="null":
                        
                        if constan=="yes":
                            su.run(rule,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                           
                            rellen=rellen+1
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["Rolue"]="null"
                                settings["constan"]="no"
                            
                            with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4)
                        elif constan=="no":
                            
                            su.run(rule,shell=True,stdout=su.DEVNULL,stderr=su.DEVNULL)
                            rellen=rellen+1
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                    settings = json.load(f)
                                    settings["Rolue"]="null"
                                    settings["constan"]="no"
                                    with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                        json.dump(settings,f,indent=4)
                            #run add rules function
                            th.Thread(target=add__rule).start()


                    
                    
                    with open(r"C:\FWSH-files\FirewallRules.txt","w",encoding='utf-8')as f:
                        f.write("")
                    #check firewall rules lenghth
                    
                    su.run(r'powershell -Command "Get-NetFirewallRule | Select-Object -ExpandProperty Name | Out-File "C:\FWSH-files\FirewallRules.txt" -Encoding utf8"',shell=True,text=True,capture_output=True)
                    with open(r"C:\FWSH-files\FirewallRules.txt","r",encoding='utf-8')as f:
                        a=f.readlines()
                        ld=0
                        
                        for _ in a:
                            
                            ld+=1
                    #if there a rule add to the firewall without ordars from the user the belwo code will run
                    
                    if ld>rellen:
                        
                    
                        l3=ld-rellen
                        rellen+=l3
                        #send to the server to add csv file
                        
                        #send email to user
                        msg= EmailMessage()
                        msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                        msg["From"]="aofnotification@gmail.com"
                        msg["To"]=email_rvs
                        msg.set_content(f"there are strange rule had been add to your firewall\ndo the protocol to check your devic if you had been hackt")
                        email="aofnotification@gmail.com"
                        password="oqgspkawnyeftyjw"
                        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                            smtp.login(email,password)
                            smtp.send_message(msg)
                                

                    #if there a rule delete from the firewall without ordars from the user the belwo code will run        
                    elif ld<rellen:
                        
                        l4=rellen-ld
                        rellen-=l4
                        #send to the server to add csv file
                        
                        #send email to user
                        msg= EmailMessage()
                        msg["Subject"]=f"edit rule - ID({str(uuid.uuid4())[:8]})"
                        msg["From"]="aofnotification@gmail.com"
                        msg["To"]=email_rvs
                        msg.set_content(f"there are some rule had been delete from your firewall\ndo the protocol to check your devic if you had been hackt")
                        email="aofnotification@gmail.com"
                        password="oqgspkawnyeftyjw"
                        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                            smtp.login(email,password)
                            smtp.send_message(msg)
                                
                    with open(r"C:\FWSH-files\FirewallRules.txt","w",encoding='utf-8')as f:
                        f.write("")
                    


                    if enaply !=[] :
                        def enaply_action():
                            global enaply
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                enaply=list(enaply)
                                enaply1=enaply.pop(0)
                                settings["Enaply list"]=enaply
                            with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4) 
                            action="e"
                            if enaply1.endswith("m") or enaply1.endswith("h"):
                                z=enaply1.index("^")
                                bb=enaply1[z:]
                                aa=enaply1.replace(bb,"")
                                bb=bb.replace("^","")
                                if bb.endswith("m"):
                                    lens=len(bb)
                                    bb=bb[:lens-1]
                                    bb=int(bb)
                                    bb*=60
                                    bb=str(bb)
                                    


                                elif bb.endswith("h"):
                                    lens=len(bb)
                                    bb=bb[:lens-1]
                                    bb=int(bb)
                                    bb*=3600
                                    bb=str(bb)
                            
                            fs.action_rule(bb,aa,action)
                        th.Thread(target=enaply_action).start()
                    


                    if disaply !=[] :
                        
                        def disaply_action():
                            global disaply
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                disaply=list(disaply)
                                disaply1=disaply.pop(0)
                                settings["Disaply list"]=disaply
                            with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                json.dump(settings,f,indent=4) 
                            action="d"
                            if disaply1.endswith("m") or disaply1.endswith("h"):
                                z=disaply1.index("^")
                                bb=disaply1[z:]
                                aa=disaply1.replace(bb,"")
                                bb=bb.replace("^","")
                                if bb.endswith("m"):
                                    lens=len(bb)
                                    bb=bb[:lens-1]
                                    bb=int(bb)
                                    bb*=60
                                    bb=str(bb)
                                    


                                elif bb.endswith("h"):
                                    lens=len(bb)
                                    bb=bb[:lens-1]
                                    bb=int(bb)
                                    bb*=3600
                                    bb=str(bb)
                            
                            fs.action_rule(bb,aa,action)
                        th.Thread(target=disaply_action).start()

                #run the main function
                sa.run(main())
                
                #return to do this loop evry 10s
                time.sleep(10)
        except Exception:
            print("there are error")
            continue
