import queries as Q
import json
import  json_handle as jh
import details as dt

######
def list_posts(target_forum, since = None, limit=None, order=None, user=None, forum=None, thread=None):
    query = Q.forums_posts(target_forum, since, limit, order)
    rs = jh.engine.execute(query)
    base_dict = jh.list_of_dict(rs)
    result = []
    for post in base_dict:
        if user != None:
            user = post['user']
            post['user'] = dt.user_details(user)
        if forum != None:
            post['forum'] = dt.forum_details(post['forum'], None)
        if thread != None:
            post['thread'] = dt.thread_details(post['thread'], None, None)
    return base_dict
######
def list_threads(target_forum, since = None, limit=None, order=None, user=None, forum=None):
    query = Q.forums_threads(target_forum, since, limit, order)
    rs = jh.engine.execute(query)
    base_dict = jh.list_of_dict(rs)
    for post in base_dict:
        if user != None:
            user = post['user']
            post['user'] = dt.user_details(user)
        if forum != None:
            post['forum'] = dt.forum_details(post['forum'], None)
    return base_dict
#####
def list_users(target_forum, since=None, limit=None, order=None):
    query = Q.forums_users(target_forum, since, limit, order)
    rs = jh.engine.execute(query)
    base_dict = jh.list_of_dict(rs)
    return base_dict

a = list_users('f1', None, None, None)
print a