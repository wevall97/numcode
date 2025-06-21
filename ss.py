import json
for _ in range(1):
    rows=[]
    row=[]
    new=',{"id": "0x", "RemoteManagement": "Disable", "UnicastResponseToMulticast": "Enable", "active": False, "Roule": [], "timer": []}'
    
    with open('UsersRolus.json', 'r') as f:
        data = json.load(f)
        
        p=data["len"]
        
        pp=int(p)
        pp+=1
        pp=str(pp)
        data=str(data)
        
        n=new.replace("0x",pp+"x")
        
        l=len(data)
       
        for i in data:
            if i=="'":
                i='"'
                row.append(i)
            else:
                row.append(i)
        
        
        for ii in n:
            rows.append(ii)
        row=row[:l-2]+rows+row[l-2:]
        
        d=''.join(row)
        row.clear()
        rows.clear()
        dd=d.replace('True', 'true').replace('False', 'false')
        
        
        
        j=json.loads(dd)
        j["len"]=pp
       
    with open('UsersRolus.json', 'w') as f:
        json.dump(j, f, indent=4)
    


