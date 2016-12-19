import queries as Q
import json_handle as jh
from sqlalchemy import exc
from general import max_id

def repair_userr_add(base_dict):
    if base_dict["followers"] == None:
        base_dict["followers"] = []
    else:
        base_dict["followers"] = base_dict["followers"].split()

    if base_dict["following"] == None:
        base_dict["following"] = []
    else:
        base_dict["following"] = base_dict["following"].split()

    if base_dict["subscriptions"] == None:
        base_dict["subscriptions"] = []
    else:
        debug = base_dict["subscriptions"].split(",")
        debug = [int(x) for x in debug if x != ""]
        base_dict["subscriptions"] = debug

def user_details(email, add = None):
    connection = jh.engine.connect()
    #
    if add == None:
        query = Q.user_details(email)
        rs = connection.execute(query)
        base_dict = jh.create_dict_base(rs)
        connection.close()
        return base_dict
    else:
        query = Q.user_details_real(email)
        rs = connection.execute(query)
        base_dict = jh.create_dict_base(rs)
        repair_userr_add(base_dict)
        connection.close()
        return base_dict


def forum_details(forum, user):
    connection = jh.engine.connect()
    #
    query = Q.forum_details(forum)
    rs = connection.execute(query)
    base_dict = jh.create_dict_base(rs)
    if(base_dict == None):
        connection.close()
        return base_dict

    if (user != None):
        user = base_dict["user"]
        user_dict = user_details(user)
        base_dict['user'] = user_dict
    connection.close()
    return base_dict


def thread_details(id, user, forum, likes):
    connection = jh.engine.connect()
    #
    query = Q.thread_details(id, likes)
    rs = connection.execute(query)
    base_dict = jh.create_dict_base(rs)
    if base_dict == None:
        connection.close()
        return base_dict
    if (user != None):
        user = base_dict["user"]
        user_dict = user_details(user)
        base_dict['user'] = user_dict
    if (forum != None):
        forum = base_dict["forum"]
        forum_dict = forum_details(forum, None)
        base_dict['forum'] = forum_dict
    connection.close()
    return base_dict

def get_path_sortpath(parent_id):
    connection = jh.engine.connect()
    #
    query = Q.get_path_spath(parent_id)
    rs = connection.execute(query)
    data = list(rs)
    path = data[0][0]
    sortpath = data[0][1]
    connection.close()
    return path, sortpath

def build_post_path_sortpath(answer):
    connection = jh.engine.connect()
    #
    id = answer.get("id")
    parent_id = answer.get("parent")
    if parent_id == -1:
        sortpath = answer.get("date")
        query = Q.set_path_sortpath("", sortpath,id)
        connection.execute(query)
        connection.close()
        return
    path, sortpath = get_path_sortpath(parent_id)
    sortpath += " " + answer.get("date")
    query = Q.set_path_sortpath(path, sortpath, id)
    connection.execute(query)
    connection.close()
    return

def post_details(id, user, forum, thread):
    connection = jh.engine.connect()
    #
    query = Q.post_details(id)
    rs = connection.execute(query)
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
    connection.close()
    return base_dict

def create(for_inserting, entity):
    connection = jh.engine.connect()
    #
    #print "CREATE"
    #print for_inserting
    error_resp = 0
    values = jh.create_insert_dict(for_inserting)
    query = ""
    answer = {}
    if entity == "user":
        query = Q.user_create(values)
        try:
            connection.execute(query)
        except exc.SQLAlchemyError:
            connection.close()
            return 1, None
        answer = user_details(for_inserting.get("email"))

    elif entity == "forum":
        query = Q.forum_create(values)
        try:
            connection.execute(query)
        except exc.SQLAlchemyError:
            connection.close()
            return 1, None
        key = for_inserting.get("short_name")
        answer = forum_details(key, None)

    elif entity == "post":
        query = Q.post_create(values)
        query1 = Q.threads_posts_change(values, False)
        try:
            connection.execute(query)
            connection.execute(query1)
        except exc.SQLAlchemyError:
            connection.close()
            return 1, None
        answer = post_details(max_id("Post"), None, None, None)
        build_post_path_sortpath(answer)

    elif entity == "thread":
        query = Q.thread_create(values)
        try:
            connection.execute(query)
        except exc.SQLAlchemyError:
            connection.close()
            return 1, None
        answer = thread_details(max_id("Thread"), None, None, None)
    connection.close()
    return error_resp, answer


data = {u'name': u'\u0424\u043e\u0440\u0443\u043c \u0422\u0440',
        u'short_name': u'forum320', u'user': u'example@mail.ru'}
#eror, answer= create(data, "forum")
#print u'\u0424\u043e\u0440\u0443\u043c \u0422\u0440\u0438'
#print answer