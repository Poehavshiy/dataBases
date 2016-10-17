import queries as Q
import json
import user_functions as uf
import forum_functions as ff
import json_handle as jh

def thread_details(id, user, forum):
    query = Q.thread_details(id)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_responce(rs)
    if(user != None):
        user = base_dict["user"]
        user_dict = uf.user_details(user)
        base_dict['user'] = user_dict
    if(forum != None):
        forum = base_dict["forum"]
        forum_dict = ff.forum_details(forum, None)
        base_dict['forum'] = forum_dict
    return base_dict

print thread_details(3, 'user', 'forum')