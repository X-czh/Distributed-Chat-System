import indexer
import json
from chat_utils import *

def client_indexing(msg):
    [term, str_start_line, str_lines] = msg.split('|')
    start_line = int(str_start_line)
    lines = str_lines.split('\n')

    client_indexer = indexer.Index('ClientIndexer', start_line)
    for line in lines:
        client_indexer.add_msg_and_index(line)
    msg = json.dumps(client_indexer.search_idx(term)) # convert list to string
    del client_indexer
    
    return msg

'''
converts a index dict to a string in the format as follows:
key1,key2:value1_tuple1_l,value1_tuple1_i;value1_tuple2_l,value1_tuple2_i/value2_tuple1_l,value2_tuple1_i

def dict2str(d):
    str_keys = ','.join(d.keys())

    value_list = []
    for value in d.values():
        tuple_list = []
        for e in value:
            tuple_list.append(','.join([str(e[0]), str(e[1])]))
        value_list.append(';'.join(tuple_list))
    str_values = '/'.join(value_list)

    str_d = ':'.join([str_keys, str_values])

    return str_d
'''