import queries as Q
import json
import user_functions as uf
import forum_functions as ff
import details as d
import json_handle as jh



def close_open(for_inserting, bool):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.close_open_thread(key_values, bool)
    jh.engine.execute(query)
    return error_resp

def remove_restore(for_inserting, bool):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.remove_restore_thread(key_values, bool)
    jh.engine.execute(query)
    return error_resp

def subscribe(for_inserting):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.subscribe(key_values)
    jh.engine.execute(query)
    return error_resp

def unsubscribe(for_inserting):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.unsubscribe(key_values)
    jh.engine.execute(query)
    return error_resp

def list_threads(since, limit, order, forum, user):
    query = ""
    if forum != None:
        query = Q.forums_threads(forum, since, limit, order)
    else:
        query = Q.users_threads(user, since, limit, order)
    rs = jh.engine.execute(query)
    base_dict = jh.list_of_dict(rs)
    return base_dict

def thread_update(for_inserting):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.update_thread(key_values)
    jh.engine.execute(query)
    answer = d.thread_details(key_values.get("thread"), None, None)
    return error_resp, answer

def thread_vote(for_inserting, bool):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.thread_vote(key_values, bool)
    jh.engine.execute(query)
    answer = d.thread_details(key_values.get("thread"), None, None)
    return error_resp, answer



r ={"vote": 1, "thread": 1}
a, answer = thread_vote(r, True)
print answer