'''
Docstring for MS

2.0 V
'''
import time
import json
import pandas as pd
import os


pathfile=os.path.exists(r"D:\MS\ms 2v.json")

if pathfile==False:
    s='{"all_rent": "0"}'
    p=json.loads(s)
    with open(r"D:\MS\ms 2v.json","w",encoding='utf-8')as f:
        json.dump(p,f,indent=4)
t=str(time.strftime('%Y-%m-%d %H:%M:%S'))


while True:
    try:
        
        m1=input("enter the new rent: ")
        m1=int(m1)
        n1=m1/6000
        b1=n1-1

        for _ in range(int(b1)):
            try:
                s=pd.read_csv(r"D:\MS\rent.csv") 
            except Exception:
                datafrme={
                    "Rent":["Rent"],
                    "Time":["Time"]
                }

                s=pd.DataFrame(datafrme)
                s.to_csv(r"D:\MS\rent.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
            datafrme={
                    "Rent":["He did`t pay today"],
                    "Time":[t]
                }

            d=pd.DataFrame(datafrme)
            try:
                d.to_csv(r"D:\MS\rent.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
            except Exception:
                pass
        

        try:
            s=pd.read_csv(r"D:\MS\rent.csv") 
        except Exception:
            datafrme={
                "Rent":["Rent"],
                "Time":["Time"]
            }

            s=pd.DataFrame(datafrme)
            s.to_csv(r"D:\MS\rent.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
        datafrme={
                "Rent":[str(m1)],
                "Time":[t]
            }

        d=pd.DataFrame(datafrme)
        try:
            d.to_csv(r"D:\MS\rent.csv",index=False,encoding='utf-8-sig',mode='a',header=False) 
        except Exception:
            pass


        with open(r'D:\MS\ms 2v.json', 'r',encoding='utf-8') as f:
            settings = json.load(f) 
            mc1=settings["all_rent"]
            print(f"The all rent: {int(mc1)+int(m1)}")
            settings["all_rent"]=str(int(mc1)+int(m1))
            with open(r'D:\MS\ms 2v.json', 'w',encoding='utf-8') as f:
                json.dump(settings,f,indent=4)
    
    except Exception:
        print("error")