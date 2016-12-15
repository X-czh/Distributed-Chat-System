# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 15:56:41 2016

@author: chiminghao
"""
from interupter import *
import pickle as pkl
from numpy import *
#the overhead of this program is 7bits per 8 bits
# regard "msg" as a piece message that is sent in a form of string.
def reliable_send(msg):
    msg_list = []
    for i in range(len(msg)):
        msg_list.append(msg[i])
    
    #make the separate string binary code in ASCII
    binarycode_of_each_element = []
    for i in msg_list:
        #prepare to fit into a 2*4 matrix
        binarycode_of_each_element.append('0' + bin(ord(i))[2:])
    print(binarycode_of_each_element)

    #create a blank list for the collection of matrix        
    msg = []
    
    #put the binary code into a 2*4 matrix   
    for item in binarycode_of_each_element:
        matrix = mat(zeros((2,4)))
        for i in range(4):
            matrix[0, i] = item[i]
            matrix[1, i] = item[i+4]
            

    #add rebundancy into the matrix, prepare the matrix for trans
        matrix_withsum = mat(zeros((3,5)))
        checksum1 = 0
        checksum2 = 0
        for i in range(4):
            #row 1
            checksum1 += int(matrix[0, i])
            matrix_withsum[0, i] = matrix[0, i]
            matrix_withsum[0, 4] = checksum1
            #row 2
            checksum2 += int(matrix[1, i])
            matrix_withsum[1, i] = matrix[1, i]
            matrix_withsum[1, 4] = checksum2
            #row 3
            matrix_withsum[2, i] = matrix[0, i] + matrix[1, i]
            matrix_withsum[2, 4] += int(matrix_withsum[2, i])
        msg.append(matrix_withsum)
    print(msg)
    return(msg)


#When received, this function will make a checksum again and compare
#it's value with the former checksum, and fix the error automatically
#this part don't need to send the message again, no more overhead
#now, msg is a matrix_withsum with size 3*5
def reliable_receive(msg):
    collection_of_string = []
    for each_matrix in msg:
        #step 1: make the matrix smaller -- get back to a 2*4 matrix
        matrix = mat(zeros((2,4)))
        for i in range(4):
            matrix[0, i] = each_matrix[0, i]
            matrix[1, i] = each_matrix[1, i]
        #step 2: make the matrix big again -- calculate the checksum
        matrix_withsum = mat(zeros((3,5)))
        checksum1 = 0
        checksum2 = 0
        for i in range(4):
            #row 1
            checksum1 += int(matrix[0, i])
            matrix_withsum[0, i] = matrix[0, i]
            matrix_withsum[0, 4] = checksum1
            #row 2
            checksum2 += int(matrix[1, i])
            matrix_withsum[1, i] = matrix[1, i]
            matrix_withsum[1, 4] = checksum2
            #row 3
            matrix_withsum[2, i] = matrix[0, i] + matrix[1, i]
            matrix_withsum[2, 4] += int(matrix_withsum[2, i])
        
        #step3: make a comparasion between matrix_withsum and msg(the former matrix)
        if matrix_withsum.all() == each_matrix.all(): #if the trans is accurate, convert into a message again with ASCII
            temp = []
            for i in range(1, 4): #delete the first bit that is added to form a matrix
                temp.append(matrix[0, i])
            for i in range(4):
                temp.append(matrix[1, i])
            temp_msg = "" #the elements in the list msg is strings, put them in temp_msg
            for i in temp:
                temp_msg += str(int(i))
            temp = int(temp_msg, base = 2)#become ASCII again
            temp = chr(temp)
            collection_of_string.append(temp)
            
            
        
        else: #if the trans is not accurate, find the place with mistakes
            error_row = 0
            error_column = 0
            #row-checksum
            for i in range(2):
                if matrix_withsum[i, 4] != msg[i, 4]:
                    error_row = i #locate the row
            #column-checksum
            for i in range(4):
                if matrix_withsum[2, i] != msg[2, i]:
                    error_column = i #locate the column
                
            #change the value
            if matrix[error_row, error_column] == '0':
                matrix[error_row, error_column] == '1'
            else:
                matrix[error_row, error_column] == '0'
            #then convert into masseage from ASCII    
            temp = []
            for i in range(1, 4): #delete the first bit that is added to form a matrix
                temp.append(matrix[0, i])
            for i in range(4):
                temp.append(matrix[1, i])
            temp_msg = "" #the elements in the list msg is strings, put them in temp_msg
            for i in temp:
                temp_msg += str(int(i))
            temp = int(temp_msg, base = 2)#become ASCII again
            temp = chr(temp)
            collection_of_string.append(temp)
        #sum up the string from the list called "collection of string"
    msg = ''
    for i in collection_of_string:
        msg += i
    print(msg)
    return msg
     
reliable_receive(reliable_send(interupter('Hello', 0)))
#reliable_receive(reliable_send(interupter('Hey', 0)))
