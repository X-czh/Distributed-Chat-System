# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 19:45:38 2016

@author: chiminghao
"""

from interupter import *
import json
from numpy import *
# regard "msg" as a piece message that is sent in a form of string.
def reliable_send(msg):
    matrix_number = len(msg)//9 + 1 #3*3 matrix
    #convert the message into decimal numbers
    number_list = []
    for i in range(len(msg)):
        number_list.append(ord(msg[i]))
    for i in range(matrix_number*9 - len(msg)):
        number_list.append(0)

    #put the numbers into 3*3 matrixes, fill out the blanks with 0
    msg = [] #since we have imported the values of msg as demical numbers, make msg a blank list for collection
    for i in range(matrix_number):
        matrix = mat(zeros((3,3)))
        #row 1
        for column in range(3):
            matrix[0, column] = number_list[9*i + column]
        #row 2
            matrix[1, column] = number_list[9*i + 3 + column]
        #row 3
            matrix[2, column] = number_list[9*i + 6 + column]
        msg.append(matrix)

    #calculate the checksum
    msg_checksum = []
    for matrix in msg:
        matrix_withsum = mat(zeros((4,4)))
        checksum1 = 0
        checksum2 = 0
        checksum3 = 0
        for i in range(3):
            #row 1
            checksum1 += int(matrix[0, i])
            matrix_withsum[0, i] = matrix[0, i]
            matrix_withsum[0, 3] = checksum1
            #row 2
            checksum2 += int(matrix[1, i])
            matrix_withsum[1, i] = matrix[1, i]
            matrix_withsum[1, 3] = checksum2
            #row 3
            checksum3 += int(matrix[2, i])
            matrix_withsum[2, i] = matrix[2, i]
            matrix_withsum[2, 3] = checksum3
            #row 4
            matrix_withsum[3, i] = matrix[0, i] + matrix[1, i] + matrix[2,i]
            matrix_withsum[3, 3] += int(matrix_withsum[2, i])
        msg_checksum.append(matrix_withsum.tolist())
    msg = json.dumps(msg_checksum)
    return(msg)
            
reliable_send("Hello Franklin")
            
            
#When received, this function will make a checksum again and compare
#it's value with the former checksum, and fix the error automatically
#this part don't need to send the message again, no more overhead
#now, msg is a matrix_withsum with size 4*4
def reliable_receive(msg):
    msg = json.loads(msg)
    temp = ''
    for each_matrix in msg:
        #print(each_matrix)
        #step 1: make the matrix smaller -- get back to a 3*3 matrix
        each_matrix = mat(each_matrix)
        matrix = mat(zeros((3,3)))
        for i in range(3):
            matrix[0, i] = each_matrix[0, i]
            matrix[1, i] = each_matrix[1, i]
            matrix[2, i] = each_matrix[2, i]
        #step 2: make the matrix big again -- calculate the checksum
        matrix_withsum = mat(zeros((4,4)))
        checksum1 = 0
        checksum2 = 0
        checksum3 = 0
        for i in range(3):
            #row 1
            checksum1 += int(matrix[0, i])
            matrix_withsum[0, i] = matrix[0, i]
            matrix_withsum[0, 3] = checksum1
            #row 2
            checksum2 += int(matrix[1, i])
            matrix_withsum[1, i] = matrix[1, i]
            matrix_withsum[1, 3] = checksum2
            #row 3
            checksum3 += int(matrix[2, i])
            matrix_withsum[2, i] = matrix[2, i]
            matrix_withsum[2, 3] = checksum3
            #row 4
            matrix_withsum[3, i] = matrix[0, i] + matrix[1, i] + matrix[2, i]
            matrix_withsum[3, 3] += int(matrix_withsum[2, i])
        #print(matrix_withsum)
            
#change the each_matrix purposefully to see whether the checksum works
        each_matrix[1,2] += 2 #add 2 to the element on row 2 and column 3
        print(each_matrix) 
        print(matrix_withsum)
        #make a contrast between the two matrix above
            
        #step3: make a comparasion between matrix_withsum and msg(the former matrix)
        if matrix_withsum.all() == each_matrix.all(): #if the trans is accurate, convert into a message again with ASCII
            for i in range(0, 3): 
                    temp += (chr(int(matrix[0, i])))
            for i in range(0, 3):                   
                    temp += (chr(int(matrix[1, i])))
            for i in range(0, 3): 
                    temp += (chr(int(matrix[2, i])))

        else: #if the trans is not accurate, find the place with mistakes
        #assume there is only one mistake
            error_row = 0
            error_column = 0
            #row-checksum
            for i in range(3):
                if matrix_withsum[i, 3] != each_matrix[i, 3]:
                    error_row = i #locate the row
            #column-checksum
            for i in range(3):
                if matrix_withsum[3, i] != each_matrix[3, i]:
                    error_column = i #locate the column
            the_error = each_matrix[3, error_column] - matrix_withsum[3, error_column]
            matrix[error_row, error_column] += the_error #fix the error
            #give the message
            for i in range(0, 3): 
                temp += (chr(int(matrix[0, i])))
            for i in range(0, 3):                   
                temp += (chr(int(matrix[1, i])))
            for i in range(0, 3): 
                temp += (chr(int(matrix[2, i])))
    msg = temp.strip('\0')
    print(msg)
    return(msg)
    
reliable_receive(reliable_send("Hello Franklin!"))
reliable_receive(reliable_send(interupter("HelloFranklin", 0)))
