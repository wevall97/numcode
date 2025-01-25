
import random as rm
import time as ti




gg=input("enter your cheak file :\n> ")
ww=input("enter your v files :\n> ")
rows=[]
while True:
        
        
        row=[]
        for i in range(3):
            x=rm.randint(0,9)
            row.append(x)
        a=''.join(map(str,row))
        row.clear()
        with open(gg,"r") as f:
            lines = f.readlines()
        with open(ww,"+a") as d:
            l=0
            for line in lines:
                if a!=lines[l].strip() :
                    l=l+1
                elif a==lines[l].strip():
                    l=l+1
                    break
            if a!=lines[l-1].strip() :
                rows.append(a)
                d.write(a+'\n')
                with open(gg,"+a") as c:
                    c.write(a+'\n')
        if len(rows)==91:
            rows.clear() 
            break  
        elif ti.process_time()==10:
            print("out of time")
            break 
        

