import queries as Q
import json_handle as jh
from sqlalchemy import exc


def max_id(table):
    rs = jh.engine.execute(Q.max_id(table))
    base_dict = jh.create_dict_base(rs)
    id = base_dict.get("max(id)")
    return id

def user_details(email, add = None):
    query = Q.user_details(email)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)
    if add == None:
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
    if(base_dict == None):
        return base_dict
    if (user != None):
        user = base_dict["user"]
        user_dict = user_details(user)
        base_dict['user'] = user_dict
    return base_dict


def thread_details(id, user, forum, likes):
    query = Q.thread_details(id, likes)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)
    if (user != None):
        user = base_dict["user"]
        user_dict = user_details(user)
        base_dict['user'] = user_dict
    if (forum != None):
        forum = base_dict["forum"]
        forum_dict = forum_details(forum, None)
        base_dict['forum'] = forum_dict
    return base_dict

def get_path_sortpath(parent_id):
    query = Q.get_path_spath(parent_id)
    rs = jh.engine.execute(query)
    data = list(rs)
    path = data[0][0]
    sortpath = data[0][1]
    return path, sortpath

def build_post_path_sortpath(answer):
    id = answer.get("id")
    parent_id = answer.get("parent")
    if parent_id == -1:
        sortpath = answer.get("date")
        query = Q.set_path_sortpath("", sortpath,id)
        jh.engine.execute(query)
        return
    path, sortpath = get_path_sortpath(parent_id)
    sortpath += " " + answer.get("date")
    query = Q.set_path_sortpath(path, sortpath, id)
    jh.engine.execute(query)
    return

def post_details(id, user, forum, thread):
    query = Q.post_details(id)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)

    if (user != None):
        user = base_dict["user"]
        dict = user_details(user)
        base_dict['user'] = dict
    if (forum != None):
        forum = base_dict["forum"]
        dict = forum_details(forum, None)
        base_dict['forum'] = dict
    if (thread != None):
        thread = base_dict["thread"]
        dict = thread_details(thread, None, None, "likes")
        base_dict['thread'] = dict
    return base_dict

def create(for_inserting, entity):
    #print "CREATE"
    #print for_inserting
    error_resp = 0
    values = jh.create_insert_dict(for_inserting)
    query = ""
    answer = {}
    if entity == "user":
        query = Q.user_create(values)
        try:
            jh.engine.execute(query)
        except exc.SQLAlchemyError:
            return 1, None
        answer = user_details(for_inserting.get("email"))

    elif entity == "forum":
        query = Q.forum_create(values)
        try:
            jh.engine.execute(query)
        except exc.SQLAlchemyError:
            return 1, None
        key = for_inserting.get("short_name")
        answer = forum_details(key, None)

    elif entity == "post":
        query = Q.post_create(values)
        query1 = Q.threads_posts_change(values, False)
        try:
            jh.engine.execute(query)
            jh.engine.execute(query1)
        except exc.SQLAlchemyError:
            return 1, None
        answer = post_details(max_id("Post"), None, None, None)
        build_post_path_sortpath(answer)

    elif entity == "thread":
        query = Q.thread_create(values)
        try:
            jh.engine.execute(query)
        except exc.SQLAlchemyError:
            return 1, None
        answer = thread_details(max_id("Thread"), None, None, None)
    return error_resp, answer


data = {u'name': u'\u0424\u043e\u0440\u0443\u043c \u0422\u0440',
        u'short_name': u'forum320', u'user': u'example@mail.ru'}
#eror, answer= create(data, "forum")
#print u'\u0424\u043e\u0440\u0443\u043c \u0422\u0440\u0438'
#print answer