import queries as Q
import json
import  json_handle as jh
import user_functions as uf
import MySQLdb, sys


def forum_details(forum, user):
    query = Q.forum_details(forum)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_responce(rs)
    if(user != None):
        user = base_dict["user"]
        user_dict = uf.user_details(user)
        base_dict['user'] = user_dict
    return base_dict


def create(for_inserting):
    error_resp = 0
    values = jh.create_insert_dict(for_inserting)
    query = Q.forum_create(values)
    jh.engine.execute(query)
    return error_resp

