# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 17:12:36 2016

@author: chiminghao
"""
from numpy import *

def generate_matrix(msg): #msg is a string
    msgs_list = [ord(text) for text in msg] #make the string a list
    N = int(len(msgs_list)**0.5) + 1  #the row/column length of the matrix
    
    
    matrix = mat(zeros((N, N))) #create a zero matrix
    #change the elements in the rows without 0 been added at the end
    for row in range(len(msgs_list)//N):
        for column in range(N):
            matrix[row, column] = msgs_list[(row)*N + column]
            
    #change the elements in the rows with some 0 been added at the end
    for i in range(len(msgs_list) % N):
        matrix[len(msgs_list)//N, i] = msgs_list[N*(len(msgs_list)//N) + i]
    print(matrix)        
    return(matrix)
    
generate_matrix('Hello! Franklin! How are you!')
    
        
    
    
    