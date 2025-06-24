#bering the moduls
import numcode as ss #'numcode' is a modul i have made by my self
import math as ma
import random as ra


        
def enc(theInput):           

    row=[]
    l=0
    # prebar for the publce key
    for _ in range (1):
        
        gnrKey=ra.randint(10,99)
        gnrKey1=ra.randint(10,99)
        


        # the method of how to making the publce key
    bublcekey=ma.floor((gnrKey*gnrKey1)/(gnrKey1-1))
   



        # the method of making the praivt key
        # the praivt key is the scrit key that the user don't know it
    praivtkey=ma.floor((gnrKey*gnrKey1)/bublcekey)
    

    # take the words and transform it from "numcode modul"
    for _ in range (len(theInput)):

        sa=theInput[l]

        l+=1

        f=ss.numcode(sa)

        f=f+praivtkey

        row.append(f)

    e=''.join(map(str,row))

   
    gnrKey=str(gnrKey)
    gnrKey1=str(gnrKey1)
    return f"{gnrKey}{gnrKey1}{e}"




def dec(theInput):


    row=[]

    rows=[]

    row1=[]

    row2=[]


    g=len(theInput)

    l=4

    for _ in range (g-4):

        row2.append(theInput[l])

        l+=1

    xx=''.join(map(str,row2))

    gnrKey=int(f"{theInput[0]}{theInput[1]}")

    gnrKey1=int(f"{theInput[2]}{theInput[3]}")

    bublcekey=ma.floor((gnrKey*gnrKey1)/(gnrKey1-1))
    privtKey=ma.floor((gnrKey*gnrKey1)/bublcekey)

    l=3

    while True:

        l+=1

        s=theInput[l]

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

                s=theInput[l]

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

    return q

   