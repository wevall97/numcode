def risk_score_add_vrifiy(D_sin,action,Direction,Protocol,Port,Ip):
    Multiplier=1
    bacscore=0
    if D_sin=="Valid":
        bacscore-=50
    if D_sin=="NotSigned":
        bacscore+=30
    if D_sin in ["UntrustedRoot","HashMismatch","Revoked"]:
        bacscore+=40
    if D_sin=="NotTrusted":
        bacscore+=20
    if D_sin in ["UnknownError","Expired"]:
        bacscore+=10

    if action=="Block":
        bacscore+=0
    if action=="Allow":
        bacscore+=20
        
    if Direction=="Inbound":
        bacscore+=25  
    if Direction=="Outbound":
        bacscore+=5
        
    if Protocol=="Any":
        bacscore+=20
    if Protocol=="UDP":
        bacscore+=15
    if Protocol=="TCP":
        bacscore+=10
    if Protocol=="ICMP":
        bacscore+=10
        
    if Port in ["3389", "445", "23"] :
        bacscore+=40
    if Port in ["22", "21"] :
        bacscore+=30
    if Port in ["80", "443"] :
        bacscore+=15
    if Port=="Any":
        bacscore+=20
    
        
    if Ip =="Any" :
        bacscore+=20
    if Ip == "Public IP"  :
        bacscore+=30
    if Ip == "Trusted IP"  :
        bacscore+=10
    if Ip == "Local Network" :
        bacscore+=10  ###
    if Ip == "Localhost" :
        bacscore+=0
    
    



    return bacscore*Multiplier





def risk_score_add_not_vrifiy(action,Direction,Protocol,Port,Ip):
    Multiplier=1
    bacscore=0
    

    if action=="Block":
        bacscore+=30
    if action=="Allow":
        bacscore+=30
        
    if Direction=="Inbound":
        bacscore+=25  
    if Direction=="Outbound":
        bacscore+=25
        
    if Protocol=="Any":
        bacscore+=20
    if Protocol=="UDP":
        bacscore+=10
    if Protocol=="TCP":
        bacscore+=15
    if Protocol=="ICMP":
        bacscore+=10
        
    if Port in ["3389", "445", "23"] :
        bacscore+=40
    if Port in ["22", "21"] :
        bacscore+=30
    if Port in ["80", "443"] :
        bacscore+=15
    if Port=="Any":
        bacscore+=20
    
        
    if Ip =="Any" :
        bacscore+=20
    if Ip == "Public IP"  :
        bacscore+=30
    if Ip == "Trusted IP"  :
        bacscore+=10
    if Ip == "Local Network" :
        bacscore+=10  ###
    if Ip == "Localhost" :
        bacscore-=10
    

    return bacscore*Multiplier






def risk_score_delete_not_vrifiy(dn_n,program,action,Direction,Protocol,Port,Ip,pro_true):
    bacscore=0
    security_vendors = ["Microsoft","Microsoft Corporation","Windows Defender","Microsoft Defender","Symantec","Symantec Corporation","Norton","NortonLifeLock","Gen Digital","Broadcom","Broadcom Inc","McAfee","McAfee LLC","McAfee Corp","Trellix","FireEye","FireEye Inc","Kaspersky","Kaspersky Lab","Kaspersky Labs","Kaspersky Lab ZAO","ESET","ESET spol","ESET, spol. s r.o.","Avast","Avast Software","AVG","AVG Technologies","Avira","Avira GmbH","Bitdefender","Bitdefender SRL","Sophos","Sophos Ltd","Sophos Group","Trend Micro","Trend Micro Inc","Malwarebytes","Malwarebytes Inc","Panda","Panda Security","F-Secure","F-Secure Corporation","WithSecure","G Data","G Data Software","Comodo","Comodo Security","Xcitium","ZoneAlarm","Check Point","Check Point Software","Webroot","Webroot Inc","Fortinet","Fortinet Inc","CrowdStrike","CrowdStrike Inc","CrowdStrike Holdings","SentinelOne","SentinelOne Inc","Carbon Black","CarbonBlack","VMware Carbon Black","Cisco","Cisco Systems","Elastic","Elastic NV","Cybereason","Cybereason Inc","SecureWorks","Secureworks Inc","Quick Heal","QuickHeal","Seqrite","K7 Computing","K7 Security","TotalAV","Protected.net"]
    for vendor in security_vendors:
        if vendor.lower() in program.lower():
            compony=True
            break
        else:
            compony=False
            break


    if program=="System":
        return("Block")
    
    if "WINDOWS\system32" in program:
        return("Block")
    
    if program=="Any" and "microsoft" in dn_n.lower():
        bacscore+=60
    
    if ("microsoft" or "windows" in dn_n.lower()) and (program!="Any"):
        bacscore+=60
    
    if program not in ["System","Any"] and "WINDOWS\system32" not in program and pro_true=="True" and compony==True:
        bacscore+=40
    
    if program not in ["System","Any"] and "WINDOWS\system32" not in program and pro_true=="False" and compony==True:
        bacscore+=10
    
    if program not in ["System","Any"] and "WINDOWS\system32" not in program and pro_true=="False" and compony==False:
        bacscore+=0
    
    if program not in ["System","Any"] and "WINDOWS\system32" not in program and pro_true=="True" and compony==False:
        bacscore+=30
        print(1)    
    
    


    if action=="Block":
        bacscore+=30
        print(2)
    Port=str(Port)
    if Port in [21,22,23,25,53,69,80,110,119,123,135,137,138,139,143,161,389,443,445,465,500,512,513,514,515,520,587,636,989,990,1433,1521,2049,2082,2083,2181,2222,2375,2376,2483,2484,3000,3128,3306,3389,3690,4444,4567,4848,5000,5060,5432,5601,5631,5900,5985,5986,6000,6379,6667,7001,7002,7070,7474,8000,8008,8009,8080,8081,8088,8090,8443,8888,9000,9042,9092,9200,9418,10000]:
        bacscore+=20
        Port=int(Port)

    if action=="Allow":
        bacscore+=20##

    

    if  Direction=="Inbound" and Protocol=="TCP" and Ip in ["Any","Public IP"]:
        bacscore+=20

    if  Direction=="Inbound" and Protocol=="UDP" and Ip in ["Any","Public IP"]:
        bacscore+=20
        print(3)

    if  Direction=="Inbound" and Protocol=="Any" and Ip in ["Any","Public IP"]:
        bacscore+=25

    

    if  Direction=="Outbound" and Protocol=="UDP" and Ip in ["Any","Public IP"]:
        bacscore+=30
        

    if  Direction=="Outbound" and Protocol=="Any" and Ip in ["Any","Public IP"]:
        bacscore+=35

    if  Direction=="Outbound" and Protocol=="TCP" and Ip in ["Any","Public IP"]:
        bacscore+=30

    

    if  Ip=="Localhost":
        bacscore-=50
        
    if Port in ['80','443'] and Direction=="Outbound":
        bacscore-=50
 
    if Port == 53 and Direction=="Outbound":
        bacscore-=50
 
    if  Ip=="Local Network":
        bacscore-=20


        
    return bacscore




def risk_score_modify_not_vrifiy(program,action,Direction,Protocol,Port,Ip,action1,Direction1,Protocol1,Port1,Ip1):
    bacscore=0
    def risk_score_PORT(whitch_unit,bacscore1,action,Direction,Protocol,Ip):
        bacscore=bacscore1

        if Port in ['3389','22','445','135','139','1433'] and whitch_unit!="ip":
            bacscore+=30
    
        if Port in ['443','80'] and whitch_unit!="ip":
            bacscore+=25

        if action=="Block":
            bacscore+=30
        
        if action=="Allow":
            bacscore+=30
        
        if Direction == "Inbound":
            bacscore+=20
    
        if Direction == "Outbound":
            bacscore+=30
    
        if Ip in ["Any","Public IP"] and whitch_unit!="Ip":
            bacscore+=30
    
        if Ip == "Local Network" and whitch_unit!="Ip":
            bacscore+=10
    
        if Ip == "Localhost" and whitch_unit!="Ip":
            bacscore-=50
    
        if Protocol == "TCP" and whitch_unit!="pro":
            bacscore+=15
    
        if Protocol == "Any" and whitch_unit!="pro":
            bacscore+=20
    
        if Protocol == "UDP" and whitch_unit!="pro":
            bacscore+=10

        return bacscore
    
    if action=="Block" and action1=="Allow":
        bacscore+=40
        security_vendors = ["Microsoft","Microsoft Corporation","Windows Defender","Microsoft Defender","Symantec","Symantec Corporation","Norton","NortonLifeLock","Gen Digital","Broadcom","Broadcom Inc","McAfee","McAfee LLC","McAfee Corp","Trellix","FireEye","FireEye Inc","Kaspersky","Kaspersky Lab","Kaspersky Labs","Kaspersky Lab ZAO","ESET","ESET spol","ESET, spol. s r.o.","Avast","Avast Software","AVG","AVG Technologies","Avira","Avira GmbH","Bitdefender","Bitdefender SRL","Sophos","Sophos Ltd","Sophos Group","Trend Micro","Trend Micro Inc","Malwarebytes","Malwarebytes Inc","Panda","Panda Security","F-Secure","F-Secure Corporation","WithSecure","G Data","G Data Software","Comodo","Comodo Security","Xcitium","ZoneAlarm","Check Point","Check Point Software","Webroot","Webroot Inc","Fortinet","Fortinet Inc","CrowdStrike","CrowdStrike Inc","CrowdStrike Holdings","SentinelOne","SentinelOne Inc","Carbon Black","CarbonBlack","VMware Carbon Black","Cisco","Cisco Systems","Elastic","Elastic NV","Cybereason","Cybereason Inc","SecureWorks","Secureworks Inc","Quick Heal","QuickHeal","Seqrite","K7 Computing","K7 Security","TotalAV","Protected.net"]
        for vendor in security_vendors:
            if vendor.lower() in program.lower():
                compony=True
                
                break
            else:
                compony=False
                break
        
        if "windows" or "system" in program.lower():
            bacscore+=20

        if compony:
            bacscore+=10

        if Port in ['3389','22','23']:
            bacscore+=30
    
        if Port in ['135','139','445']:
            bacscore+=20
    
        if Direction == "Inbound":
            bacscore+=20
    
        if Direction == "Outbound":
            bacscore+=10
    
        if Ip in ["Any","Public IP"]:
            bacscore+=30
    
        if Ip == "Local Network":
            bacscore+=10
    
        if Ip == "Localhost":
            bacscore-=50
    
        if Protocol == "TCP":
            bacscore+=15
    
        if Protocol == "Any":
            bacscore+=20
    
        if Protocol == "UDP":
            bacscore+=10

        return bacscore
    
    if action=="Allow" and action1=="Block":
        bacscore+=40
        security_vendors = ["Microsoft","Microsoft Corporation","Windows Defender","Microsoft Defender","Symantec","Symantec Corporation","Norton","NortonLifeLock","Gen Digital","Broadcom","Broadcom Inc","McAfee","McAfee LLC","McAfee Corp","Trellix","FireEye","FireEye Inc","Kaspersky","Kaspersky Lab","Kaspersky Labs","Kaspersky Lab ZAO","ESET","ESET spol","ESET, spol. s r.o.","Avast","Avast Software","AVG","AVG Technologies","Avira","Avira GmbH","Bitdefender","Bitdefender SRL","Sophos","Sophos Ltd","Sophos Group","Trend Micro","Trend Micro Inc","Malwarebytes","Malwarebytes Inc","Panda","Panda Security","F-Secure","F-Secure Corporation","WithSecure","G Data","G Data Software","Comodo","Comodo Security","Xcitium","ZoneAlarm","Check Point","Check Point Software","Webroot","Webroot Inc","Fortinet","Fortinet Inc","CrowdStrike","CrowdStrike Inc","CrowdStrike Holdings","SentinelOne","SentinelOne Inc","Carbon Black","CarbonBlack","VMware Carbon Black","Cisco","Cisco Systems","Elastic","Elastic NV","Cybereason","Cybereason Inc","SecureWorks","Secureworks Inc","Quick Heal","QuickHeal","Seqrite","K7 Computing","K7 Security","TotalAV","Protected.net"]
        for vendor in security_vendors:
            if vendor.lower() in program.lower():
                compony=True
                
                break
            else:
                compony=False
                break
        if Port in ['433','53']:
            bacscore+=30
    #RPC   RPCEPMap
        if Port in ['80']: 
            bacscore+=20
    
        if Direction == "Inbound":
            bacscore+=30
    
        if Direction == "Outbound":
            bacscore+=20
        
        if Ip in ["Any","Public IP"]:
            bacscore+=30
    
        if Ip == "Local Network":
            bacscore+=10
    
        if Ip == "Localhost":
            bacscore-=50
    
        if "windows" or "system" in program.lower():
            bacscore+=20
# if program == any , get the name and displayname to chick if it belong to system rules
        if compony: 
            bacscore+=10
        
        if Protocol == "TCP":
            bacscore+=15
    #ICMPv6
        if Protocol == "Any":  
            bacscore+=20
    
        if Protocol == "UDP":
            bacscore+=10
        
        return bacscore
        
    if Direction=="Outbound" and Direction1=="Inbound":
        security_vendors = ["Microsoft","Microsoft Corporation","Windows Defender","Microsoft Defender","Symantec","Symantec Corporation","Norton","NortonLifeLock","Gen Digital","Broadcom","Broadcom Inc","McAfee","McAfee LLC","McAfee Corp","Trellix","FireEye","FireEye Inc","Kaspersky","Kaspersky Lab","Kaspersky Labs","Kaspersky Lab ZAO","ESET","ESET spol","ESET, spol. s r.o.","Avast","Avast Software","AVG","AVG Technologies","Avira","Avira GmbH","Bitdefender","Bitdefender SRL","Sophos","Sophos Ltd","Sophos Group","Trend Micro","Trend Micro Inc","Malwarebytes","Malwarebytes Inc","Panda","Panda Security","F-Secure","F-Secure Corporation","WithSecure","G Data","G Data Software","Comodo","Comodo Security","Xcitium","ZoneAlarm","Check Point","Check Point Software","Webroot","Webroot Inc","Fortinet","Fortinet Inc","CrowdStrike","CrowdStrike Inc","CrowdStrike Holdings","SentinelOne","SentinelOne Inc","Carbon Black","CarbonBlack","VMware Carbon Black","Cisco","Cisco Systems","Elastic","Elastic NV","Cybereason","Cybereason Inc","SecureWorks","Secureworks Inc","Quick Heal","QuickHeal","Seqrite","K7 Computing","K7 Security","TotalAV","Protected.net"]
        for vendor in security_vendors:
            if vendor.lower() in program.lower():
                compony=True
                
                break
            else:
                compony=False
                break
        bacscore+=20
        if action=="Block":
            bacscore+=30
        
        if action=="Allow":
            bacscore+=30
        
        if Port in ['3389','22','445','135','139','1433']:
            bacscore+=30
    
        if Port in ['443','80']:
            bacscore+=25
    
        if "windows" or "system" in program.lower():
            bacscore+=20
# if program == any , get the name and displayname to chick if it belong to system rules
        if compony: 
            bacscore+=10
        
        if Ip in ["Any","Public IP"]:
            bacscore+=30
    
        if Ip == "Local Network":
            bacscore+=10
    
        if Ip == "Localhost":
            bacscore-=20

        if Protocol == "TCP":
            bacscore+=15
    
        if Protocol == "Any":
            bacscore+=20
    
        if Protocol == "UDP":
            bacscore+=10
            
        return bacscore
    
    if Direction=="Inbound" and Direction1=="Outbound":
        security_vendors = ["Microsoft","Microsoft Corporation","Windows Defender","Microsoft Defender","Symantec","Symantec Corporation","Norton","NortonLifeLock","Gen Digital","Broadcom","Broadcom Inc","McAfee","McAfee LLC","McAfee Corp","Trellix","FireEye","FireEye Inc","Kaspersky","Kaspersky Lab","Kaspersky Labs","Kaspersky Lab ZAO","ESET","ESET spol","ESET, spol. s r.o.","Avast","Avast Software","AVG","AVG Technologies","Avira","Avira GmbH","Bitdefender","Bitdefender SRL","Sophos","Sophos Ltd","Sophos Group","Trend Micro","Trend Micro Inc","Malwarebytes","Malwarebytes Inc","Panda","Panda Security","F-Secure","F-Secure Corporation","WithSecure","G Data","G Data Software","Comodo","Comodo Security","Xcitium","ZoneAlarm","Check Point","Check Point Software","Webroot","Webroot Inc","Fortinet","Fortinet Inc","CrowdStrike","CrowdStrike Inc","CrowdStrike Holdings","SentinelOne","SentinelOne Inc","Carbon Black","CarbonBlack","VMware Carbon Black","Cisco","Cisco Systems","Elastic","Elastic NV","Cybereason","Cybereason Inc","SecureWorks","Secureworks Inc","Quick Heal","QuickHeal","Seqrite","K7 Computing","K7 Security","TotalAV","Protected.net"]
        for vendor in security_vendors:
            if vendor.lower() in program.lower():
                compony=True
                
                break
            else:
                compony=False
                break
        bacscore+=20

        if action=="Block":
            bacscore+=30
        
        if action=="Allow":
            bacscore+=30
        #RPC
        if Port in ["80","22"]:
            bacscore+=20
    
        if Port in ['443','53']:
            bacscore+=30
    
        if "windows" or "system" in program.lower():
            bacscore+=20
# if program == any , get the name and displayname to chick if it belong to system rules
        if compony: 
            bacscore+=10
        
        if Ip in ["Any","Public IP"]:
            bacscore+=25
    
        if Ip == "Local Network":
            bacscore+=10
    
        if Ip == "Localhost":
            bacscore-=50
        
        if Protocol == "TCP":
            bacscore+=15
    
        if Protocol == "Any":
            bacscore+=20
    
        if Protocol == "UDP":
            bacscore+=10
            
        return bacscore
    
    if (Port1=="Any" or "-" in Port1) and (Port!="Any"):
        bacscore+=40
        return risk_score_PORT("ip",bacscore,action,Direction,Protocol,Ip)

    if Port in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"] and Port1 in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"]:
        bacscore+=40
        return risk_score_PORT("ip",bacscore,action,Direction,Protocol,Ip)

    if Port in ["80","110","143","443","8080","8443"] and Port1 in ["80","110","143","443","8080","8443"]:
        bacscore+=30
        return risk_score_PORT(1,bacscore,action,Direction,Protocol,Ip)

    if (Port not in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"] or Port not in ["80","110","143","443","8080","8443"]) and (Port1 in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"] ):
        bacscore+=50
        return risk_score_PORT("ip",bacscore,action,Direction,Protocol,Ip)

    if (Port not in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"] or Port not in ["80","110","143","443","8080","8443"]) and (Port1 in ["80","110","143","443","8080","8443"]):
        bacscore+=35
        return risk_score_PORT("ip",bacscore,action,Direction,Protocol,Ip)

    if Port in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"] and Port1 in ["80","110","143","443","8080","8443"]:
        bacscore+=20
        return risk_score_PORT("ip",bacscore,action,Direction,Protocol,Ip)

    if Port in ["80","110","143","443","8080","8443"] and Port1 in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"]:
        bacscore+=25
        return risk_score_PORT("ip",bacscore,action,Direction,Protocol,Ip)

    if (Port  in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"] ) and (Port1 not in ["21","22","23","25","53","135","137","138","139","1433","3389","445","5900","5985","5986"] ):
        bacscore+=50
        return risk_score_PORT("ip",bacscore,action,Direction,Protocol,Ip)

    if (Port  in ["80","110","143","443","8080","8443"]) and (Port1 not in ["80","110","143","443","8080","8443"]):
        bacscore+=35
        return risk_score_PORT("ip",bacscore,action,Direction,Protocol,Ip)



    if Protocol1=="Any":
        bacscore+=30
        return risk_score_PORT("pro",bacscore,action,Direction,Protocol,Ip)

    if Protocol=="TCP" and Protocol1=="UDP":
        bacscore+=15
        return risk_score_PORT("pro",bacscore,action,Direction,Protocol,Ip)

    if Protocol=="UDP" and Protocol1=="TCP":
        bacscore+=20
        return risk_score_PORT("pro",bacscore,action,Direction,Protocol,Ip)

    if Protocol=="Any" and Protocol1 in ["TCP","UDP","ICMP"]:
        bacscore+=25
        return risk_score_PORT("pro",bacscore,action,Direction,Protocol,Ip)

    


    if Ip1=="Any" or Ip1=="Public IP":
        bacscore+=50
        return risk_score_PORT("Ip",bacscore,action,Direction,Protocol,Ip)

    if Ip=="Localhost" and Ip1 =="Local Network":
        bacscore+=10
        return risk_score_PORT("Ip",bacscore,action,Direction,Protocol,Ip)

    if Ip=="Local Network" and Ip1 =="Localhost":
        bacscore-=30
        return risk_score_PORT("Ip",bacscore,action,Direction,Protocol,Ip)
    # make one for 'Trusted IP'






