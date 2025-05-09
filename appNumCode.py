#bering the moduls
import numcode as ss #'numcode' is a modul i have made by my self
import math as ma
import random as ra


print("Welcome to the numCode")

print("copy raigt : mohammedmajadaldeen@gmail.com")

print("1.4.v\n")

print("Enter '.h' for help or '.exit' to exit ")


while True:

    try:

        gg=input("1> ")
        # chosing the difrent tools like ".en / .de / .enf / .def "
        if gg==".h":
            
            print(".en      to encrypt one line of words\n.de      to decrypt one line of words\n.enf     to encrypt a file\n.def     to decrypt a file")
            
            print("WORRING!!: WHEN YOU USE '.enf' OR '.def' AND IF YOU ENTER THE WRONG PUBLCE KEY YOUR FLIE WHILE BE AMPTY\n")
        elif gg==".exit":
            print("bay!")
            break

        else:


            while True:

                if gg=='.en':
                    
                        try:

                            print("\n Enter '.exit' to exit")

                            theInput=input("Enter your words:\n> ")

                            if theInput==".exit":

                                print("bye!!\n")

                                break
                            try:
                                row=[]
                                l=0
                                # prebar for the publce key
                                for i in range (1):
                                    if theInput=="":
                                        break
                                    gnrKey=ra.randint(10,99)
                                    gnrKey1=ra.randint(10,99)
                                    

                                def buplcKey():
                                    # the method of how to making the publce key
                                    return ma.floor((gnrKey*gnrKey1)/(gnrKey1-1))
                                buplcKey()


                                def praivtKay():
                                    # the method of making the praivt key
                                    # the praivt key is the scrit key that the user don't know it
                                    return ma.floor((gnrKey*gnrKey1)/buplcKey())
                                praivtKay()

                                # take the words and transform it from "numcode modul"
                                for s in range (len(theInput)):

                                    sa=theInput[l]

                                    l+=1

                                    f=ss.numcode(sa)

                                    f=f+praivtKay()

                                    row.append(f)

                                e=''.join(map(str,row))

                                print(f"your publce key: {buplcKey()}")

                                print(f"your encrbet text: {gnrKey}{gnrKey1}{e}")

                            except Exception:

                                print("error")
                        
                        except :

                            print("you has been enter a wronge valu\ntry again")

                            continue


                elif gg=='.de':
                    
                        try:
                            print("\n'.exit' to exit")

                            pulcKey=int(input("enter the publce key (you can not enter '.exit' her): \n> "))

                            theInput=(input("Enter your code:\n> "))

                            if theInput==".exit":

                                print("bye!!\n")

                                break
                            
                            try:

                                row=[]

                                rows=[]

                                row1=[]

                                row2=[]
                                
                                
                                g=len(theInput)

                                l=4

                                for jd in range (g-4):

                                    row2.append(theInput[l])

                                    l+=1

                                xx=''.join(map(str,row2))

                                gnrKey=int(f"{theInput[0]}{theInput[1]}")

                                gnrKey1=int(f"{theInput[2]}{theInput[3]}")

                                privtKey=ma.floor((gnrKey*gnrKey1)/pulcKey)

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

                                print(f"your decrbet text: {q}")

                            except Exception:

                                print("your decrbet text: error")

                        

                        except :

                            print("you has been enter a ronge valu\ntry again")

                            continue

                elif gg=='.enf':
                    

                    print("\n'.exit' to exit")
                    try:
                        theInput = input("Enter the url of your file:\n> ")

                        if theInput==".exit":

                            print("bye!!\n")

                            break

                        
                            
                        gnrKey=ra.randint(10,99)

                        gnrKey1=ra.randint(10,99)

                        def buplcKey():
                            return ma.floor((gnrKey*gnrKey1)/(gnrKey1-1))
                        buplcKey()

                        def praivtKay():
                            return ma.floor((gnrKey*gnrKey1)/buplcKey())
                        praivtKay()

                        with open(theInput, 'r') as d:
                            
                            lines = d.readlines()


                        with open(theInput, 'w') as d:
                            
                            fg=0
                            
                            for line in lines:
                                    
                                    fg=1
                                    row5 = []
                                

                                    for s in line:

                                        

                                        try:
                                            
                                                row=[]

                                                f=ss.numcode(s)

                                                f=f+praivtKay()

                                                row.append(f)
                                                    
                                                e=''.join(map(str,row))

                                                row.clear()
                                                
                                                row5.append(e)
                                                
                                        except Exception:

                                            pass
                                    
                                    we=''.join(map(str,row5))

                                    row5.clear()

                                    if f==None:

                                        break

                                    d.write(f"{gnrKey}{gnrKey1}")

                                    d.write(we)

                                    d.write("\n")

                            if fg==1 and f!=None:
                                    
                                print(f"your publce key: {buplcKey()}")

                                print("Your file has been encrypted")
                            
                            elif fg==0:

                                print("error: emty file")

                            else:

                                print("error: there is strange data to encrypt")

                    except Exception:

                        print(f"error: '{theInput}' not found")
                        
                
                elif gg==".def":

                    try:
                        print("\n'.exit' to exit")

                        theInput=(input("Enter the url of your file: \n> "))

                        if theInput==".exit":

                            print("bye!!\n")

                            break

                        
                        buplcKey=int(input("enter the buplc key: \n> "))

                        with open(theInput,'r') as fq:

                            lines=fq.readlines()

                        with open(theInput,'w') as fq:

                               
                            gh=0
                            for line in lines:
                                
                                gh=1

                                row=[]
                                rows1=[]
                                row1=[]
                                row2=[]
                                
                                
                                g=len(line.strip())

                                l=4

                                for jd in range (g-4):

                                    row2.append(line.strip()[l])

                                    l+=1

                                xx=''.join(map(str,row2))

                                gnrKey=int(f"{line.strip()[0]}{line.strip()[1]}")

                                gnrKey1=int(f"{line.strip()[2]}{line.strip()[3]}")

                                privtKey=ma.floor((gnrKey*gnrKey1)/buplcKey)

                                l=3

                                while True:

                                    l+=1

                                    s=line.strip()[l]

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

                                            s=line.strip()[l]

                                            row.append(s)

                                            k=''.join(map(str,row))

                                            k=int(k)

                                            ff=k-privtKey

                                            f=ss.numcode(ff)

                                            
                                        rows1.append(f)

                                        row.clear()

                                    row1.append(k)

                                    hfj=''.join(map(str,row1))

                                    if hfj==xx:

                                        break
                                    

                                q=''.join(map(str,rows1))

                                rows1.clear()
                                if q=="\n":
                                    fq.write(q)
                                    continue
                                    
                                fq.write(q)
                                
                                

                            if gh==1:
                                
                                print("your file has been decrypted")

                            elif gh==0:

                                print("your file is empty")

                    except FileNotFoundError:

                        print(f"error: '{theInput}' not found")
                    
                    except IndexError:

                        print("error: you have enter the wrong public key")

                    except ValueError:

                        print("error: you have not enter the public key")                  

                else:

                    print(f"{gg} : it is not defined")

                    break

    except KeyboardInterrupt:

        print("bay!")

        break

    except:

        print("you has been enter a ronge valu\ntry again")

        continue
    



