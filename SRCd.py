import math as ma
import numcode as ss
try:
    row=[]
    rows=[]
    row1=[]
    row2=[]
    buplcKey=int(input("enter the buplc key: \n> "))
    x=input("enter your encrpted code:\n> ")
    g=len(x)
    l=4
    for jd in range (g-4):
        row2.append(x[l])
        l+=1

    xx=''.join(map(str,row2))
    gnrKey=int(f"{x[0]}{x[1]}")
    n=int(f"{x[2]}{x[3]}")
    privtKey=ma.floor((gnrKey*n)/buplcKey)

    l=3
    while True:
        l+=1
        s=x[l]
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
                s=x[l]
                row.append(s)
                k=''.join(map(str,row))
                k=int(k)
                ff=k-privtKey
                f=ss.numcode(ff)
                
            rows.append(f)
            row.clear()
        row1.append(k)
        hfj=''.join(map(str,row1))
        if hfj==xx:
            break
        

    q=''.join(map(str,rows))
    rows.clear()
    print(f"your decrbet text: {q}")
except Exception:
    print("your decrbet text: error")


    



