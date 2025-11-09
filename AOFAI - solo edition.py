import json
import random
import os




# check all code

l=1
while True:
    try:
        try:
           
            os.mkdir(r"C:\FWSH-files")
        except Exception:
           pass

        pathfile=os.path.exists(r"C:\FWSH-files\settings.json")

        if pathfile==False:
            s='{"email": "","FWS": "","timerF": "","deleteR": "null","checkrulename": [],"ruleName": [],"Rolue": "null","constan": "no","timerR": [],"Enaply list": [],"Disaply list": []}'
            p=json.loads(s)
            with open(r"C:\FWSH-files\settings.json","w",encoding='utf-8')as f:
                json.dump(p,f,indent=4)
        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
            settings = json.load(f)         
            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    
                    if settings["email"]=="":
                        while True:
                            emai=input("Email Address: ")
                            if "@" in emai and ".com" in emai:
                                
                                emai=emai.strip()
                                settings["email"]=emai
                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                                    break
                            else:
                                print("Please enter a valid email address.")
                                continue
            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                settings = json.load(f)
                check4=settings["email"]
                

            def generate_password():
                password=random.randint(111111,999999)
                password=str(password)
                return password
            
            if l==1:
                l=0
                ppp=generate_password()
                # print("Preparing to send the password to your email.")
                # msg= EmailMessage()
                # msg["Subject"]=f"Enter Password - ID({str(uuid.uuid4())[:8]})"
                # msg["From"]="aofnotification@gmail.com"
                # msg["To"]=check4
                # msg.set_content(f"your password is: {ppp}")
                # email="aofnotification@gmail.com"
                # password="oqgspkawnyeftyjw"
                # with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
                #     smtp.login(email,password)
                #     smtp.send_message(msg)

                # checkpass=input("Enter password: ")
                # checkpass=checkpass.strip()
                checkpass=ppp   
            if checkpass==ppp or l==0:
                
                
                
                

                        
                with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                    settings = json.load(f)
                    
                    email_rvs=settings["email"]
                
                    
                        
                
                                
                print("enter (help) for help")
                while True:
                    

                    masge=input("Enter your message: ")
                    masge=masge.lower()
                    masge=masge.strip()
                    
                    if masge=="help" or masge=="h":
                        help='''

1. firewall state : to change firewall state (off / on).
2. add new rule : to add one new rule for firewall.
3. delete rule : to delete one rule from firewall.
4. advance mode : it is a mode make you to add meny rules and make the rule conest or not. 

'''
                        print(help)
                    if masge=="firewall state" or masge=="1":
                        print("if you wont to exit enter (exit)")
                        while True:
                            rolu=input("Enter firewall state (on to enable, off to disable): ")
                            rolu=rolu.strip()
                            rolu=rolu.lower()
                            if rolu=="on" or rolu=="off" or rolu=="exit":
                                
                                break
                            else:
                                print("Enter 'on' or 'off'")
                                continue
                        if rolu=="off":
                            while True:
                                timer=input("Enter the timer value: ")
                                timer=timer.strip()
                                timer=timer.lower()
                                if timer.endswith("m") or timer.endswith("h"):
                                    break
                                else:
                                    print("Please enter a valid timer value.")
                                    continue
                            timerlog=timer
                            if timer.endswith("m"):
                                lens=len(timer)
                                timer=timer[:lens-1]
                                timer=int(timer)
                                timer*=60
                                timer=str(timer)
                                


                            elif timer.endswith("h"):
                                lens=len(timer)
                                timer=timer[:lens-1]
                                timer=int(timer)
                                timer*=3600
                                timer=str(timer)
                                

                            
                                

                          
                        
                        if rolu!="exit":
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                data = json.load(f)
                                data["FWS"]=rolu
                                if rolu=="off":
                                    data["timerF"]=timer
                                
                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(data,f,indent=4)
                            print("Firewall state has been changed.")
                        
                        

                    
                        
                        



                    elif masge=="delete rule" or masge=="3":
                        with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                            settings = json.load(f)
                            check6=settings["checkrulename"]
                            check6=list(check6)
                        
                        print("if you wont to exit enter (exit)")
                        
                        
                        while True:
                            delrule=input("Enter the rule name: ")
                            delrule=delrule.strip()
                            if "#" in delrule or "|" in delrule or "%" in delrule or "~" in delrule:
                                print("try agean")
                                continue
                            if delrule in check6:
                                print("try agean")
                                continue
                            
                            else:
                                break
                        if delrule!="exit":
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["deleteR"]=delrule
                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)

                            
                            print(f"Rule '{delrule}' deleted successfully.")
                        
                        

                            
                    

                    elif masge=="advance mode" or masge=="4":
                               
                        while True:
                            
                            while True:
                                rolu=input("Enter the rule or (exit): ")
                                rolu=rolu.strip()
                                rule=rolu.replace("'",'"')
                                if rule=="exit":
                                    break
                                if "#" in rule or "|" in rule or "%" in rule or "~" in rule or ";" in rule or "&" in rule or "\\" in rule:
                                    print("try agean")
                                    continue
                                if "-or" in rule.lower() or "if" in rule.lower() or "try" in rule.lower() or "catch" in rule.lower():
                                    print("try agean")
                                    continue
                                if "new-netfirewallrule" not in rule.lower()  or "-displayname" not in rule.lower():
                                    print("try agean")
                                    continue
                                
                                else:
                                    break
                            if rule=="exit":
                                
                                break
                            while True:
                                constan=input("Enter state constant (yes for permanent rule, no for temporary): ")
                                constan=constan.strip()
                                constan=constan.lower()
                                if constan=="yes" or constan=="no":
                                    break
                                else:
                                    print("enter 'yes' or 'no'")
                                    continue
                            constan=constan.strip()
                            if constan=="no":
                                while True:
                                    timer=input("Enter the timer value: ")
                                    timer=timer.strip()
                                    timer=timer.lower()
                                    if timer.endswith("h") or timer.endswith("m"):
                                        break
                                    else:
                                        print("Try again.")
                                        continue


                            row=[]
                            row1=[]


                            for i in rule:
                                row1.append(i)
                                if i =="'" or i=='"':
                                    break
                            d=''.join(row1)
                            e=rule.removeprefix(d)
                            for i in e:
                                if i =="'" or i=='"':
                                    break
                                row.append(i)
                            rulename=''.join(row)
                            row.clear()
                            row1.clear()
                            
            


                            if constan=="no":
                                if timer.endswith("m"):
                                    lens=len(timer)
                                    timer=timer[:lens-1]
                                    timer=int(timer)
                                    timer*=60
                                    timer=str(timer)
                                    


                                elif timer.endswith("h"):
                                    lens=len(timer)
                                    timer=timer[:lens-1]
                                    timer=int(timer)
                                    timer*=3600
                                    timer=str(timer)
                                
                            
                            
                            rule=f'powershell -Command {rule}'   
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                settings["constan"]=constan
                                if constan=="no":
                                    
                                    
                                    s=settings["checkrulename"]
                                    s=list(s)
                                    s.append(rulename)
                                    settings["checkrulename"]=s 

                                    s=settings["ruleName"]
                                    s=list(s)
                                    s.append(rulename)
                                    settings["ruleName"]=s
                                
                                    s=settings["timerR"]
                                    s=list(s)
                                    s.append(timer)
                                    settings["timerR"]=s
                                settings["Rolue"]=rule
                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)
                            print("Rule added successfully.")




                    elif masge=="rule action" or masge=="5":
                        print("if you wont to exit enter (exit)")
                        
                        
                        while True:
                            ruleac=input("Enter the rule name: ")
                            ruleac=ruleac.strip()
                            
                            if "#" in ruleac or "|" in ruleac or "%" in ruleac or "~" in ruleac or ";" in ruleac or "&" in ruleac or "\\" in ruleac:
                                print("try agean")
                                continue
                            if "-or" in ruleac.lower() or "if" in ruleac.lower() or "try" in ruleac.lower() or "catch" in ruleac.lower():
                                print("try agean")
                                continue
                            if "new-netfirewallrule" in ruleac.lower()  or "-displayname"  in ruleac.lower():
                                print("try agean")
                                continue
                            else:
                                break


                        while True:
                            action=input("Enter Rule Action (Enably , Disaply): ").lower().strip()
                            if action=="enably" or action=="disaply":
                                break
                            else:
                                print("try agean")
                                continue

                        if action=="enably":
                            action1="e"
                        else:
                            action1="d"

                        while True:
                            timer=input("Enter the timer value: ")
                            timer=timer.strip()
                            timer=timer.lower()
                            if timer.endswith("h") or timer.endswith("m"):
                                break
                            else:
                                print("Try again.")
                                continue
                        if ruleac!="exit":
                            
                            with open(r'C:\FWSH-files\settings.json', 'r',encoding='utf-8') as f:
                                settings = json.load(f)
                                if action1=="e":
                                    settings["Enaply list"]=[ruleac+"^"+timer]
                                    
                                else:
                                    settings["Disaply list"]=[ruleac+"^"+timer]
                                    
                                with open(r'C:\FWSH-files\settings.json', 'w',encoding='utf-8') as f:
                                    json.dump(settings,f,indent=4)


                            
                            

                            print("wait until the adminstretor check your email\nif the adminstretor respons we will send email to you\n")
            else:
                print("Try again.")
                continue
    except  Exception:
        print("there are error")
        continue
    