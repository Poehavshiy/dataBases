from sqlalchemy import create_engine
import json
import unicodedata
from datetime import datetime

engine = create_engine('mysql+mysqldb://root:2112916@localhost/true_fdb')

#dict from keys and values tuples
def create_simple_dict(keys, values):
    quer_res = {}
    i = 0
    for key in keys:
        if (type(values[i]) is unicode):
            unicodedata.normalize('NFKD', values[i]).encode('ascii', 'ignore')
            quer_res[key] = values[i]

        if (type(values[i]) == datetime):
            quer_res[key] = values[i].strftime("%Y-%m-%d %H:%M:%S")

        else:
            quer_res[key] = values[i]
        i = i + 1
    return quer_res

#basic dict for details body
def create_dict_base(rs):
    keys = rs.keys()
    values = list(rs)[0]
    return create_simple_dict(keys, values)

#list entity (listposts)
def list_of_dict(rs):
    query_res = []
    keys = rs.keys()
    data = list(rs)
    for i in range (0, len(data)):
        query_res.append( create_simple_dict(keys, data[i]) )
    return query_res

#for inserting list in response (etc followers)
def create_list_response(rs):
    values = list(rs)
    res = []
    for v in values:
        res.append(v[0])
    return res

#create final response
def create_responce(dict):
    resp_dict = {}
    resp_dict["code"] = 0
    resp_dict["response"] = dict
    json_data = json.dumps(resp_dict)
    return json_data

#create error response
def create_error_responce(error_code, error):
    resp_dict = {}
    resp_dict["code"] = error_code
    resp_dict["response"] = error
    json_data = json.dumps(resp_dict)
    return json_data

def create_insert_dict(dictionary):
    key_values = {}
    for key, value in dictionary.iteritems():
        if (type(value) is unicode):
            unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        else:
            str(value)
        key_values[key] = value
    return key_values
