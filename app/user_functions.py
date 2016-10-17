import queries as Q
import json_handle as jh

def user_details(email):
    query = Q.user_details(email)
    rs = jh.engine.execute(query)
    base_dict = jh.create_dict_responce(rs)
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
