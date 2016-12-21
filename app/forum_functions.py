import queries as Q
import json
import  json_handle as jh
import details as dt


##rewrite
def list_threads(target_forum, since = None, limit=None, order=None, user=None, forum=None):
    connection = jh.engine.connect()
    query = Q.forums_threads(target_forum, since, limit, order)
    rs = connection.execute(query)
    base_dict = jh.list_of_dict(rs)

    forum_details = {}
    users = {}
    if(base_dict):
        if forum != None:
            forum_details = dt.forum_details(base_dict[0]['forum'], None)
        else:
            forum_details = base_dict[0]['forum']

        if user != None:
            query = Q.users_with_thread_inforum(target_forum)
            rs = connection.execute(query)
            user_list =  jh.list_of_dict(rs)
            for user in user_list:
                dt.repair_userr_add(user)
                users.update({user.get("email"): user})

    for thread in base_dict:
        if user != None:
            user = thread['user']
            thread['user'] = users.get(user)
        thread['forum'] = forum_details

    connection.close()
    return base_dict

#####
def list_users(target_forum, since=None, limit=None, order=None):
    connection = jh.engine.connect()
    #
    query = Q.users_additional(target_forum, since, limit, order)
    rs = connection.execute(query)
    base_dict = jh.list_of_dict(rs)
    for item in base_dict:
        debug = item["subscriptions"].split(",")
        debug = [ int(x) for x in debug if x != "" ]
        item["followers"] = item["followers"].split()
        item["following"] = item["following"].split()
        item["subscriptions"] = debug
    connection.close()
    return base_dict
