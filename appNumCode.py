import numcode as ts


print("Welcome to the numCode")

print("enter .h for help")


while True:

    try:

        gg=input("1> ")

        if gg==".h":
            
            print(".en      to encrypt one line of words\n.de      to decrypt one line of words\n.enf     to encrypt a file\n.def     to decrypt a file")
        else:

            while True:

                

                

                
                
                if gg=='.en':
                    
                        try:

                            print("\n'.exit' to exit")

                            theInput=input("Enter your words:\n> ").lower()

                            if theInput==".exit":

                                print("bye!!\n")

                                break
                            l=0

                            row=[]

                            for i in theInput:

                                s=theInput[l]

                                transform=ts.numcode(s)

                                row.append(transform)

                                numcode=''.join(map(str,row))

                                l=l+1

                            print(f"Your code: {numcode}")

                        
                        except :

                            print("you has been enter a ronge valu\ntry again")

                            continue


                elif gg=='.de':
                    
                        try:
                            print("\n'.exit' to exit")

                            theInput=(input("Enter your code:\n> "))

                            if theInput==".exit":

                                print("bye!!\n")

                                break

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

                                transform=ts.numcode(p)

                                row.append(transform)

                                numcode=''.join(map(str,row))

                                l1=l1+3
                                l2=l2+3
                                l3=l3+3

                            print(f"Your words: {numcode}")

                        

                        except :

                            print("you has been enter a ronge valu\ntry again")

                            continue

                elif gg=='.enf':
                    

                    try:
                        print("\n'.exit' to exit")

                        theInput = input("Enter the url of your file:\n> ")

                        if theInput==".exit":

                            print("bye!!\n")

                            break

                        with open(theInput, "+a") as d:

                            d.write("\n")

                        with open(theInput, 'r') as d:
                        
                            lines = d.readlines()
                        
                        with open(theInput, 'w') as d:

                            for line in lines:

                                row = []

                                for s in line:

                                    if s=='\n':

                                        d.write("\n")

                                        continue

                                    transform = ts.numcode(s.lower())

                                    row.append(transform)

                                numcode = ''.join(map(str,row))

                                d.write(numcode )

                            d.write("\n")

                            print("Your file has been encrypted")

                    except :

                        print(f"{theInput} : can not found")
                        
                
                elif gg==".def":

                    try:

                        print("\n'.exit' to exit")

                        theInput=(input("Enter the url of your file: \n> "))

                        if theInput==".exit":

                            print("bye!!\n")

                            break

                        with open(theInput,'r') as f:

                            lines=f.readlines()

                        with open(theInput,'w') as f:

                            rows=[]   
                            
                            for line in lines:

                                if line=="\n":

                                    f.write("\n")

                                    continue

                                y=len(line.strip())
                                
                                row=[]

                                l1=0
                                l2=1
                                l3=2

                                if y==3 or y>=3:

                                    u=y/3

                                for i in range(int(u)):

                                    x1=line[l1]
                                    x2=line[l2]
                                    x3=line[l3]

                                    p=x1+x2+x3

                                    transform=ts.numcode(p)

                                    row.append(transform)

                                    numcode=''.join(map(str,row))
                                    
                                    l1=l1+3
                                    l2=l2+3
                                    l3=l3+3

                                row.clear()

                                rows.append(numcode)

                                g=''.join(map(str,rows))

                                f.write(g+'\n')

                                rows.clear()

                            print("Your file has been decrypted")

                    except:

                        print(f"{theInput} : can not found")                    

                else:

                    print(f"{gg} : it is not defined")

                    break
    except:

        print("you has been enter a ronge valu\ntry again")

        continue



