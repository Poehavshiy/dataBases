import queries as Q
import  json_handle as jh
import details as d


def list_posts(since, limit, order, forum, thread):
    query = ""
    if forum != None:
        query = Q.forums_posts(forum, since, limit, order)
    else:
        query = Q.thread_posts(thread, since, limit, order)
    rs = jh.engine.execute(query)
    base_dict = jh.list_of_dict(rs)
    return base_dict
####
def remove_restore(for_inserting, bool):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.remove_restore_post(key_values, bool)
    jh.engine.execute(query)
    return error_resp
####
def post_update(for_inserting):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.update_post(key_values)
    jh.engine.execute(query)
    answer = d.post_details(key_values.get("post"), None, None, None)
    return error_resp, answer
####
def post_vote(for_inserting, bool):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.vote(key_values, bool)
    jh.engine.execute(query)
    answer = d.post_details(key_values.get("post"), None, None, None)
    return error_resp, answer



r ={"vote": -1, "post": 5}
a, answer = post_vote(r, False)
print answer