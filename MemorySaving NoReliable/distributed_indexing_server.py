import indexer
import select
import time
import json
import pickle as pkl
from chat_utils import *

# name of the file needing to be indexed and searched
name = 'Test' 

# read text and allocate indexing and searching tasks to clients, returning the total num of partitions sent
def indexing_allocate(term, sockets):
    file = open(name + '.txt','r')

    num_partitions = 0 # record the num_partitions sent
    send = True # record the sending state
    sock_idx = 1 # record the idx of socks to which the partition is sent; 0 is server_sock

    # main loop for sending partitions
    while send:
        num_partitions += 1
        start_line = (num_partitions - 1) * BLOCK_SIZE # record the start line of the partition sent
        
        # deal with memory shortage:
        # read BLOCK_SIZE of lines, and store it on disk for later use to release the memory
        line_list = []
        for i in range(BLOCK_SIZE):
            line = file.readline()
            if not line:
                send = False
                break
            line_list.append(line)
        pkl.dump(line_list, open(name + str(num_partitions - 1) + '.idx', 'wb'))
        
        msg = '|'.join([term, str(start_line), ''.join(line_list)])
        to_sock = sockets[sock_idx]
        mysend(to_sock, M_DINDEX + msg)
        
        print(num_partitions, 'partitions sent')

        if sock_idx == len(sockets) - 1:
            sock_idx = 1
        else:
            sock_idx += 1

    file.close()

    return num_partitions

# collect search results
def search_result_collect(partitions_received, list_search_idx, msg):
    search_idx = json.loads(msg)
    if len(search_idx) > 0:
        list_search_idx.append(search_idx)
    print(partitions_received, 'partitions received')

# return search results
def search_result_return(from_sock, list_search_idx):
    list_search_idx.sort() # maintain the correct order of results
    for search_idx in list_search_idx:
        msg = []
        file_idx = search_idx[0] // BLOCK_SIZE
        start_line = file_idx * BLOCK_SIZE
        line_list = pkl.load(open(name + str(file_idx) + '.idx','rb'))
        for idx in search_idx:
            msg.append(str(idx) + ', ' + line_list[idx - start_line] + '\n')
        msg = ''.join(msg)
        mysend(from_sock, M_INDEX + msg)
    else:
        mysend(from_sock, M_INDEX + 'finished') # inform client that all results have been returned

'''
converts a string back to a index dict, the string is in the format of
key1,key2:value1_tuple1_l,value1_tuple1_i;value1_tuple2_l,value1_tuple2_i/value2_tuple1_l,value2_tuple1_i

def str2dict(s):
    [str_keys, str_values] = s.split(':')

    keys = str_keys.split(',')
    values = []
    str_value_list = str_values.split('/')
    for str_value in str_value_list:
        tuple_list = []
        str_tuple_list = str_value.split(';')
        for str_tuple in str_tuple_list:
            [l, i] = str_tuple.split(',')
            tuple_list.append((int(l), int(i)))
        values.append(tuple_list)

    d = {}
    for i, key in enumerate(keys):
        d[key] = values[i]

    return d
'''