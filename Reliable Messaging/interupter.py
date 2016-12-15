import random

def interupter(msg, error_chance):
    out_message = ''
    msg_list = []
    for i in range(len(msg)):
        msg_list.append(msg[i])
    binarycode_of_each_element = []
    for i in msg_list:
        binarycode_of_each_element.append('0' + bin(ord(i))[2:])
        #print(binarycode_of_each_element)
    for j in range(len(msg)):
        for i in binarycode_of_each_element[j]:
            a = [0, error_chance, 1]
            e = random.uniform(0,1)
            a.append(e)
            a.sort()
            if a.index(e) == 1:
                out_message += str(abs(int(i)-1))
            else:
                out_message += i
    interrupted_binary_code = []
    for i in range(len(out_message)//8):
        interrupted_binary_code.append(out_message[8*i: 8+8*i])
    #print(out_message)
    #print(interrupted_binary_code)
    
    out_message = ''
    for i in interrupted_binary_code:
        temp = int(i, base = 2)
        temp = chr(temp)
        out_message += temp
    print(out_message)
    
    return out_message
    
#interupter('helloFranklin', 0)




