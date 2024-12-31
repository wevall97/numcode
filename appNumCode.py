import numCode as ts






print("Welcome to the numCode")

while True:

    

    print("If you want to code your word prss (1) or prss (2) to code your file if you want to return your word or file prss (3)")

    gg=input("> ")

    if gg=='1':
        
            
                theInput=input("Enter your word:\n> ").lower()
                
                l=0

                row=[]

                for i in theInput:

                    s=theInput[l]

                    transform=ts.numCode(s)

                    row.append(transform)

                    numcode=''.join(map(str,row))

                    l=l+1

                print("Your code:")

                print(numcode)



    elif gg=='3':
        
            
                theInput=(input("Enter your code: \n> "))
                
                y=len(theInput)

                row=[]

                l1=0
                l2=1
                l3=2

                if y==3 or y>=3:

                    u=y/3

                for i in range(int(u)):

                    x1=theInput[l1]
                    x2=theInput[l2]
                    x3=theInput[l3]

                    p=x1+x2+x3

                    transform=ts.numCode(p)

                    row.append(transform)

                    numcode=''.join(map(str,row))

                    l1=l1+3
                    l2=l2+3
                    l3=l3+3
                print("Your word:")

                print(numcode)



    elif gg=='2':
           

           try:

            print("please enter your url of your file ")

            print("example : \nnames/ali/etc/example")

            theInput=input("Enter your file:\n> ").lower()

            d=open(theInput)

            f=d.read()
            d=open(theInput,'w')
            l=0

            row=[]

            for i in f:

                s=f[l]

                transform=ts.numCode(s)

                row.append(d.write(transform))

                numcode=''.join(map(str,row))

                l=l+1

           # print("Your code:")

           # print(numcode)

            d.close()

           except Exception:

            print(f"{theInput} : can not found")
            
    
    
    else:
           print(f"{gg} : it is not defined")