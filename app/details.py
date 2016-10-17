import queries as Q
import  json_handle as jh

def user_details(email, add = None):
    query = Q.user_details(email)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)
    if(add == None ):
        return base_dict
    ##followers
    rs = jh.engine.execute(Q.users_followers(email))
    base_dict["followers"] = jh.create_list_response(rs)
    ##follow
    rs = jh.engine.execute(Q.user_follows(email))
    base_dict["following"] = jh.create_list_response(rs)
    ##subcriptions
    query = Q.users_subscriptions(email)
    rs = jh.engine.execute(query)
    base_dict["subscriptions"] = jh.create_list_response(rs)
    return base_dict


def forum_details(forum, user):
    query = Q.forum_details(forum)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)
    if(user != None):
        user = base_dict["user"]
        user_dict = user_details(user)
        base_dict['user'] = user_dict
    return base_dict

def thread_details(id, user, forum):
    query = Q.thread_details(id)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)
    if(user != None):
        user = base_dict["user"]
        user_dict = user_details(user)
        base_dict['user'] = user_dict
    if(forum != None):
        forum = base_dict["forum"]
        forum_dict = forum_details(forum, None)
        base_dict['forum'] = forum_dict
    return base_dict


def post_details(id, user, forum, thread):
    query = Q.post_details(id)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)
    if(user != None):
        user = base_dict["user"]
        dict = user_details(user)
        base_dict['user'] = dict
    if(forum != None):
        forum = base_dict["forum"]
        dict = forum_details(forum, None)
        base_dict['forum'] = dict
    if (thread != None):
        thread = base_dict["thread"]
        dict = thread_details(thread, None, None)
        base_dict['thread'] = dict
    return base_dict