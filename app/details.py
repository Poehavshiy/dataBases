import queries as Q
import json_handle as jh
from sqlalchemy import exc

def max_id(table):
    rs = jh.engine.execute(Q.max_id(table))
    base_dict = jh.create_dict_base(rs)
    id = base_dict.get("max(id)")
    return id

def user_details(email, add=None):
    query = Q.user_details(email)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_base(rs)
    if (add == None):
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


def thread_details(id, user, forum):
    query = Q.thread_details(id, True)
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
        dict = thread_details(thread, None, None)
        base_dict['thread'] = dict
    return base_dict


def create(for_inserting, entity):
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
        try:
            jh.engine.execute(query)
        except exc.SQLAlchemyError:
            return 1, None
        answer = post_details(max_id("Post"), None, None, None)

    elif entity == "thread":
        query = Q.thread_create(values)
        try:
            jh.engine.execute(query)
        except exc.SQLAlchemyError:
            return 1, None
        answer = thread_details(max_id("Thread"), None, None)
    return error_resp, answer




"""j = {"forum": "f3", "title": "Thread With Sufficiently Large Title", "isClosed": True,
     "user": "example3@mail.ru", "date": "2014-01-01 00:00:01",
     "message": "hey hey hey hey!", "slug": "Threadwithsufficientlylargetitle", "isDeleted": True}

a, answer = create(j, "thread")
#answer = max_id("Thread")
print answer"""

answer  = forum_details("f123412414", None)
print answer