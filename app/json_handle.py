from sqlalchemy import create_engine
import json
import unicodedata
from datetime import datetime


engine = create_engine('mysql+mysqldb://root:2112916@localhost/true_fdb')

def create_dict_responce(rs):
    quer_res ={}
    keys = rs.keys()
    values = list(rs)[0]
    i = 0
    #print values
    for key in keys:
        if(type(values[i]) == datetime):
            quer_res[key] = values[i].strftime("%Y-%m-%d %H:%M:%S")
        else:
            quer_res[key] = values[i]
        i = i+ 1
    return quer_res

def create_list_response(rs):
    values = list(rs)
    res = []
    for v in values:
        res.append(v[0])
    return res

def create_responce(dict):
    resp_dict = {}
    resp_dict["code"] = 0
    resp_dict["response"] = dict
    json_data = json.dumps(resp_dict)
    return json_data

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