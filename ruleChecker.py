import json
import subprocess as su


def check_state(num,state):
    num=str(num)
    if state=="Direction":
        if num=="1":
            return "Inbound"
        elif num=="2":
            return "Outbound"
    
    if state=="Action":
        if num=="2":
            return "Allow"
        elif num=="1":
            return "Block"
    
    if state=="Profile":
        if num=="1":
            return "Domain"
        elif num=="2":
            return "Private"
        elif num=="4":
            return "Public"
        elif num=="3":
            return "Domain + Private"
        elif num=="5":
            return "Domain + Public"
        elif num=="6":
            return "Private + Public"
        elif num=="7":
            return "Domain + Private + Public"
        elif num=="0":
            return "Any"
        
    if state=="Enabled":
        if num=="1":
            return "True"
        else:
            return "False"
        
def poewrshell(ordar):
    p = su.Popen(
        ["powershell.exe", "-NoExit", "-Command", "-"],
        stdin=su.PIPE,
        stdout=su.PIPE,
        stderr=su.PIPE,
        text=True
    )
    p.stdin.write(ordar)
    p.stdin.flush()


while True:
    input(">")

    op1=0
    op=0
    with open(r"D:\projects\python\firewallcopy.json", "r", encoding="utf-8-sig") as fc:
        firecopy = json.load(fc)

    with open(r"D:\projects\python\firewall_light.json", "r", encoding="utf-8-sig") as f:
        firelight = json.load(f)

    for i in firelight:
        if i not in firecopy:
            op=1

    for i in firecopy:
        if i not in firelight:
            op1=1

    if op==1 and op1==0:
        for i in firelight:
            if i not in firecopy:
                DisplayName=i["DisplayName"]
                Name=i["Name"]
                Direction=i["Direction"]
                Direction=check_state(Direction,"Direction")

                Action=i["Action"]
                Action=check_state(Action,"Action")

                Profile=i["Profile"]
                Profile=check_state(Profile,"Profile")

                Enabled=i["Enabled"]
                Enabled=check_state(Enabled,"Enabled")

                Protocol=i["Protocol"]
                LocalPort=i["LocalPort"]
                RemotePort=i["RemotePort"]
                Program=i["Program"]
                addrule=f'powershell -Command New-NetFirewallRule -DisplayName "{DisplayName}" -Name "{Name}" -Direction {Direction} -Action {Action} -Profile {Profile} -Enabled {Enabled} -Protocol {Protocol} -LocalPort {LocalPort} -RemotePort {RemotePort} -Program "{Program}"'
                #poewrshell(addrule)
                print(addrule)
            
            


    if op==0 and op1==1:
        for i in firecopy:
            if i not in firelight:
                poewrshell(f'Remove-NetFirewallRule -Name "{i["Name"]}"')
                
            


    if op==1 and op1==1:
        for i in firelight:
            if i not in firecopy:
                dat=firelight.index(i)
                for ii in i:
                    if i[ii] != firecopy[dat][ii]:
                        Name=i["Name"]
                        if ii in ["Direction","Action","Profile","Enabled","DisplayName"]:
                            if ii in ["Direction","Action","Profile","Enabled"]:
                                w=check_state(i[ii],ii)
                                #poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} {w}\n')
                                print(f'powershell -Command Set-NetFirewallRule -Name "{Name}" -{ii} {w}')
                            else:
                                print(f'powershell -Command Set-NetFirewallRule -Name "{Name}" -{ii} "{i[ii]}"')
                                #poewrshell(f'Set-NetFirewallRule -Name "{Name}" -{ii} "{i[ii]}"\n')
                        elif ii in ["Protocol","LocalPort","RemotePort"]:
                            print(f'powershell -Command Set-NetFirewallPortFilter -AssociatedNetFirewallRule (Get-NetFirewallRule -Name "{Name}") -{ii} {i[ii]}')
                            #poewrshell(f'Set-NetFirewallPortFilter -AssociatedNetFirewallRule (Get-NetFirewallRule -Name "{Name}") -{ii} {i[ii]}\n')
                        elif ii == "Program":
                            print(f'powershell -Command $rule = Get-NetFirewallRule -Name "{Name}"; Set-NetFirewallApplicationFilter -AssociatedNetFirewallRule $rule -Program "{i[ii]}"')
                            #poewrshell(f'$rule = Get-NetFirewallRule -Name "{Name}"; Set-NetFirewallApplicationFilter -AssociatedNetFirewallRule $rule -Program "{i[ii]}"\n')
