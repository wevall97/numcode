import json
import os
'''
RegsNote v1.0
Author: wevall

This tool is designed to help you take notes on the general-purpose registers (GPRs) in x86-64 assembly language. 
It allows you to record information about the value of each register, where it comes from, how it is used, and any other relevant details. 
The notes are stored in a JSON file, which can be easily accessed and updated as needed.


Copyright (c) 2026 wevall. All rights reserved.
This software is licensed under the MIT License.'''





try:
           
    os.mkdir(r"D:\DBGtools")
except Exception:
    pass


try:
           
    os.mkdir(r"D:\DBGtools\RegsNote")
except Exception:
    pass

pathfile=os.path.exists(r"D:\DBGtools\RegsNote\settings.json")

if pathfile==False:
    s='{"rax":{"1":"null","2":"null","3":"null","4":"null","5":"null","n":"null"},"rbx":{"1":"null","2":"null","3":"null","4":"null","5":"null","6":"null","n":"null"},"rcx":{"1":"null","2":"null","3":"null","4":"null","5":"null","6":"null","n":"null"},"rdx":{"1":"null","2":"null","3":"null","4":"null","5":"null","6":"null","7":"null","n":"null"},"rsi":{"1":"null","2":"null","3":"null","4":"null","5":"null","6":"null","n":"null"},"rdi":{"1":"null","2":"null","3":"null","n":"null"},"rsp":{"1":"null","2":"null","3":"null","4":"null","5":"null","6":"null","7":"null","8":"null","n":"null"},"rbp":{"1":"null","2":"null","3":"null","4":"null","5":"null","6":"null","7":"null","8":"null","n":"null"},"r8":{"1":"null","2":"null","3":"null","4":"null","n":"null"},"r9":{"1":"null","2":"null","3":"null","4":"null","n":"null"},"r10":{"1":"null","2":"null","3":"null","n":"null"},"r11":{"1":"null","2":"null","3":"null","n":"null"},"r12":{"1":"null","2":"null","3":"null","4":"null","n":"null"},"r13":{"1":"null","2":"null","3":"null","4":"null","n":"null"},"r14":{"1":"null","2":"null","3":"null","4":"null","n":"null"},"r15":{"1":"null","2":"null","3":"null","4":"null","n":"null"},"rip":{"1":"null","2":"null","3":"null","4":"null","5":"null","6":"null","7":"null","8":"null","9":"null","10":"null","n":"null"} }'
    p=json.loads(s)
    with open(r"D:\DBGtools\RegsNote\settings.json","w",encoding='utf-8')as f:
        json.dump(p,f,indent=4)

def deleteinformation(register):
    with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
        info=json.load(f)
        for i in range(len(info[register])-1):
            info[register][str(i+1)]="null"
        info[register]["n"]="null"
        with open(r"D:\DBGtools\RegsNote\settings.json","w")as f:
            json.dump(info,f,indent=4)



def information(messge,qution_number):
    with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
        info=json.load(f)
        value=info[messge][qution_number]
        if qution_number !="n":
            print(f"The old value: {value}\n")
            newvalue=input("Enter the new value: ").strip()
            info[messge][qution_number]=newvalue
            with open(r"D:\DBGtools\RegsNote\settings.json","w") as f:
                json.dump(info,f,indent=4) 
        elif qution_number=="n":
            print(f"The old note: {value}\n")
            newvalue=input("Enter your not: ").strip()
            if value !="null":
                info[messge][qution_number]=f"{value} \n{newvalue}"
            else:
                info[messge][qution_number]=f"{newvalue}"
            with open(r"D:\DBGtools\RegsNote\settings.json","w") as f:
                json.dump(info,f,indent=4) 



while True:

    msg=input("Enter the GPR: ").lower().strip()


    if msg =="rax":
        qutions='''
[1] Where it value come from?
[2] What is the value?
[3] Where is it used?
[4] It is important or mediator?
[5] Does its value in the code make sense?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4","5"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Where is it used: {info[msg]["3"]}
It is important or mediator: {info[msg]["4"]}
Does its value in the code make sense: {info[msg]["5"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="rbx":
        qutions='''
[1] Where it value come from?
[2] What is the value?
[3] Is it used as a base?
[4] Is its value fixed or variable?
[5] Does it use push or pop in it?
[6] If I change its value, will the program crash?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4","5","6"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Is it used as a base: {info[msg]["3"]}
Is its value fixed or variable: {info[msg]["4"]}
Does it use push or pop in it: {info[msg]["5"]}
If I change its value, will the program crash: {info[msg]["6"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="rcx":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] What will its value be used for?
[4] Does its value change or is it fixed?
[5] Is it an input value for a function?
[6] If its value were changed, what would happen?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4","5","6"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
What will its value be used for: {info[msg]["3"]}
Does its value change or is it fixed: {info[msg]["4"]}
Is it an input value for a function: {info[msg]["5"]}
If its value were changed, what would happen: {info[msg]["6"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="rdx":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] Is it an input value for a function?
[4] Is it used in multiplication and division?
[5] Is it remainder?
[6] Does it change after calling a function?
[7] Does it use as pointer?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4","5","6","7"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Is it an input value for a function: {info[msg]["3"]}
Is it used in multiplication and division: {info[msg]["4"]}
Is it remainder: {info[msg]["5"]}
Does it change after calling a function: {info[msg]["6"]}
Does it use as pointer: {info[msg]["7"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)
    

    elif msg=="rbp":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] Does it exist in the code or not?
[4] What is the size of the stack frame?
[5] What is the value that stored in the offset?
[6] Are all the spaces below the RBP used?
[7] Is offset fixed or variable?
[8] Can I draw a complete stack frame map?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4","5","6","7","8"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
                
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Does it exist in the code or not: {info[msg]["3"]}
What is the size of the stack frame: {info[msg]["4"]}
What is the value that stored in the offset: {info[msg]["5"]}
Are all the spaces below the RBP used: {info[msg]["6"]}
Is offset fixed or variable: {info[msg]["7"]}
Can I draw a complete stack frame map: {info[msg]["8"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)



    elif msg=="rsp":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] Did the RSP increase or decrease, and why?
[4] Did it happen pop or push?
[5] If there any stack frame is bing bulit rght now?
[6] Is there any space reserved via "sub rsp"?
[7] where am i in the stack rght now?
[8] Does it RSP Aligned correctly?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4","5","6","7","8"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Did the RSP increase or decrease, and why: {info[msg]["3"]}
Did it happen pop or push: {info[msg]["4"]}
If there any stack frame is bing bulit rght now: {info[msg]["5"]}
Is there any space reserved via "sub rsp": {info[msg]["6"]}
where am i in the stack rght now: {info[msg]["7"]}
Does it RSP Aligned correctly: {info[msg]["8"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)



    elif msg=="rsi":
        qutions='''
[1] Where it value come form (keyboard input / network packet / file read)?
[2] What is the value?
[3] What type of data does (text/array/struct/buffer) refer to?
[4] Does it value fixed or variable?
[5] Inside the function, is it important or not?
[6] If I change its value, will the program crash?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4","5","6"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
                
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
What type of data does it refer to: {info[msg]["3"]}
Does it value fixed or variable: {info[msg]["4"]}
Inside the function, is it important or not: {info[msg]["5"]}
If I change its value, will the program crash: {info[msg]["6"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="r8":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] Does it use as prameter for a function?
[4] If there any pop or push instruction use it?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Does it use as prameter for a function: {info[msg]["3"]}
If there any pop or push instruction use it: {info[msg]["4"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="r9":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] Does it use as prameter for a function?
[4] If there any pop or push instruction use it?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Does it use as prameter for a function: {info[msg]["3"]}
If there any pop or push instruction use it: {info[msg]["4"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="r10":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] If there any pop or push instruction use it?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
If there any pop or push instruction use it: {info[msg]["3"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="r11":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] If there any pop or push instruction use it?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
If there any pop or push instruction use it: {info[msg]["3"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="r12":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] If there any pop or push instruction use it?
[4] What will happen if I change its value?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
If there any pop or push instruction use it: {info[msg]["3"]}
What will happen if I change its value: {info[msg]["4"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)


    elif msg=="r13":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] If there any pop or push instruction use it?
[4] What will happen if I change its value?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
If there any pop or push instruction use it: {info[msg]["3"]}
What will happen if I change its value: {info[msg]["4"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)



    elif msg=="r14":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] If there any pop or push instruction use it?
[4] What will happen if I change its value?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
If there any pop or push instruction use it: {info[msg]["3"]}
What will happen if I change its value: {info[msg]["4"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)




    elif msg=="r15":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] If there any pop or push instruction use it?
[4] What will happen if I change its value?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
If there any pop or push instruction use it: {info[msg]["3"]}
What will happen if I change its value: {info[msg]["4"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)



    elif msg=="rip":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] Where am I standing right now (.text / .data / .bss / ...)?
[4] What does the current command do?
[5] What is the order that precedes this order?
[6] What is the order that follows this order?
[7] If there any thing controll RIP?
[8] Does it going to strange place in code?
[9] If there any RIP-relative instruction?
[10] What will happen if I change its value?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3","4","5","6","7","8","9","10"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Where am I standing right now: {info[msg]["3"]}
What does the current command do: {info[msg]["4"]}
What is the order that precedes this order: {info[msg]["5"]}
What is the order that follows this order: {info[msg]["6"]}
If there any thing controll RIP: {info[msg]["7"]}
Does it going to strange place in code: {info[msg]["8"]}
If there any RIP-relative instruction: {info[msg]["9"]}
What will happen if I change its value: {info[msg]["10"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)




    elif msg=="rdi":
        qutions='''
[1] Where it value come form?
[2] What is the value?
[3] Does it value fixed or variable?
[n] for note
[r] for result
[d] for delete information
[e] to exit

'''
        print(qutions)
        while True:
            inqu=input("Enter the number: ").lower().strip()
            if inqu not in ["e","r","n","d","1","2","3"]:
                print("Invalid input, try again.\n")
                continue
            if inqu=="d":
                deleteinformation(msg)
                print("Information deleted successfully.\n")
            if inqu=="e":
                break
            if inqu =="r":
                with open(r"D:\DBGtools\RegsNote\settings.json","r") as f:
                    info=json.load(f)
                    
                    result=f'''

It is come from: {info[msg]["1"]}
What is the value: {info[msg]["2"]}
Does it value fixed or variable: {info[msg]["3"]}
Your nots:\n \n{info[msg]["n"]}

'''
                    
                    print(result)
            if inqu not in ["r","d"]:
                information(msg,inqu)



    else:
        print("Invalid GPR, try again.\n")
        continue