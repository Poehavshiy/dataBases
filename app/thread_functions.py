import queries as Q
import json
import user_functions as uf
import forum_functions as ff
import details as d
import json_handle as jh
from sqlalchemy import exc




def close_open(for_inserting, bool):
    connection = jh.engine.connect()
    #
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.close_open_thread(key_values, bool)
    connection.execute(query)
    connection.close()
    return error_resp

def recalculate_posts(thread):
    connection = jh.engine.connect()
    #
    # count posts with isDeleted = false
    query = Q.count_thread_posts(thread)
    rs = connection.execute(query)
    base_dict = jh.create_dict_base(rs)
    post_c = base_dict.get("c")
    #
    query = Q.set_posts(thread, post_c)
    connection.execute(query)
    connection.close()

def remove_restore(for_inserting, bool):
    connection = jh.engine.connect()
    #
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)

    json_dict = d.thread_details(key_values.get("thread"), None, None, None)
    # if thread is already deleted
    if json_dict.get("isDeleted") == 1 and bool == True:
        connection.close()
        return json_dict
    # if thread is already restored
    if json_dict.get("isDeleted") == 0 and bool == False:
        connection.close()
        return json_dict

    #1st thread
    query = Q.remove_restore_thread(key_values, bool)
    connection.execute(query)
    #2nd post
    query = Q.remove_restore_posts(key_values, bool)
    connection.execute(query)
    #if thread was restored
    if bool == False:#restoring
        thread = for_inserting.get("thread")
        recalculate_posts(thread)
    connection.close()
    return error_resp

def subscribe(for_inserting):
    connection = jh.engine.connect()
    #
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.subscribe(key_values)
    try:
        connection.execute(query)
    except exc.SQLAlchemyError:
        connection.close()
        return 1, None
    connection.close()
    return error_resp

def unsubscribe(for_inserting):
    connection = jh.engine.connect()
    #
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.unsubscribe(key_values)
    connection.execute(query)
    connection.close()
    return error_resp

def list_threads(since, limit, order, forum, user):
    connection = jh.engine.connect()
    #
    query = ""
    if forum != None:
        query = Q.forums_threads(forum, since, limit, order)
    else:
        query = Q.users_threads(user, since, limit, order)
    rs = connection.execute(query)
    base_dict = jh.list_of_dict(rs)
    connection.close()
    return base_dict

def thread_update(for_inserting):
    connection = jh.engine.connect()
    #
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.update_thread(key_values)
    connection.execute(query)
    answer = d.thread_details(key_values.get("thread"), None, None, "likes")
    connection.close()
    return error_resp, answer

def thread_vote(for_inserting, bool):
    connection = jh.engine.connect()
    #
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.thread_vote(key_values, bool)
    connection.execute(query)
    answer = d.thread_details(key_values.get("thread"), None, None, "likes")
    connection.close()
    return error_resp, answer

