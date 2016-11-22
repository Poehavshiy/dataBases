import queries as Q
import json
import user_functions as uf
import forum_functions as ff
import details as d
import json_handle as jh
from sqlalchemy import exc




def close_open(for_inserting, bool):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.close_open_thread(key_values, bool)
    jh.engine.execute(query)
    return error_resp

def recalculate_posts(thread):
    # count posts with isDeleted = false
    query = Q.count_thread_posts(thread)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)
    post_c = base_dict.get("c")
    #
    query = Q.set_posts(thread, post_c)
    jh.engine.execute(query)

def remove_restore(for_inserting, bool):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)

    json_dict = d.thread_details(key_values.get("thread"), None, None, None)
    # if thread is already deleted
    if json_dict.get("isDeleted") == 1 and bool == True:
        print "bingo"
        return json_dict
    # if thread is already restored
    if json_dict.get("isDeleted") == 0 and bool == False:
        print "bingo"
        return json_dict

    #1st thread
    query = Q.remove_restore_thread(key_values, bool)
    jh.engine.execute(query)
    #2nd post
    query = Q.remove_restore_posts(key_values, bool)
    jh.engine.execute(query)
    #if thread was restored
    if bool == False:#restoring
        thread = for_inserting.get("thread")
        recalculate_posts(thread)
    return error_resp

def subscribe(for_inserting):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.subscribe(key_values)
    try:
        jh.engine.execute(query)
    except exc.SQLAlchemyError:
        return 1, None
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
    answer = d.thread_details(key_values.get("thread"), None, None, "likes")
    return error_resp, answer

def thread_vote(for_inserting, bool):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.thread_vote(key_values, bool)
    jh.engine.execute(query)
    answer = d.thread_details(key_values.get("thread"), None, None, "likes")
    return error_resp, answer

