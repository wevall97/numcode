#gnrat buplc key
#gnrat praivt key
#creat a encrpt masge by using praevt key
#send a encrpt masge it can gst oping whit buplc key     // this step to make suer the user is safi (not hacker)
#use the pblc key to decrpt the file
import math as ma
import random as ra
import numcode as ss
try:
    a=input("enter your name:\n> ")
    row=[]
    l=0
    for i in range (1):
        if a=="":
            break
        gnrKey=ra.randint(10,99)
        n=ra.randint(10,99)
        

    def buplcKey():
        return ma.floor((gnrKey*n)/(n-1))
    buplcKey()


    def praivtKay():
        return ma.floor((gnrKey*n)/buplcKey())
    praivtKay()


    for s in range (len(a)):
        sa=a[l]
        l+=1
        f=ss.numcode(sa)
        f=f+praivtKay()
        row.append(f)
    e=''.join(map(str,row))
    print(f"your publce key: {buplcKey()}")
    print(f"your encrbet text: {gnrKey}{n}{e}")
except Exception:
    print("error")



