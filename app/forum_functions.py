import queries as Q
import json
import  json_handle as jh
import details as dt

######
def list_threads(target_forum, since = None, limit=None, order=None, user=None, forum=None):
    query = Q.forums_threads(target_forum, since, limit, order)
    rs = jh.engine.execute(query)
    base_dict = jh.list_of_dict(rs)

    for post in base_dict:
        if user != None:
            user = post['user']
            post['user'] = dt.user_details(user, 1)
        if forum != None:
            post['forum'] = dt.forum_details(post['forum'], None)
    return base_dict
#####
def list_users(target_forum, since=None, limit=None, order=None):
    query = Q.forums_users(target_forum, since, limit, order)
    rs = jh.engine.execute(query)
    base_dict = jh.list_of_dict(rs)
    for user in base_dict:
        rs = jh.engine.execute(Q.users_followers(user["email"]))
        user["followers"] = jh.create_list_response(rs)
        ##follow
        rs = jh.engine.execute(Q.user_follows(user["email"]))
        user["following"] = jh.create_list_response(rs)
        #subscr
        rs = jh.engine.execute(Q.users_subscriptions(user["email"]))
        user["subscriptions"] = jh.create_list_response(rs)
    return base_dict
