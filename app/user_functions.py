import queries as Q
import json_handle as jh
import details as d


def follow(for_inserting):
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.follow_user(key_values)
    jh.engine.execute(query)
    answer = d.user_details(key_values.get("follower") , 1)
    return error_resp, answer

def list_followers_follow(email, since_id, limit, order, type):
    query = Q.list_followers_follow(email, since_id, limit, order, type)
    rs = jh.engine.execute(query)
    base_dict = jh.list_of_dict(rs)
    for user in base_dict:
        rs = jh.engine.execute(Q.users_followers(user["email"]))
        user["followers"] = jh.create_list_response(rs)
        ##follow
        rs = jh.engine.execute(Q.user_follows(user["email"]))
        user["following"] = jh.create_list_response(rs)
        # subscr
        rs = jh.engine.execute(Q.users_subscriptions(user["email"]))
        user["subscriptions"] = jh.create_list_response(rs)

    return base_dict

def unfollow(for_inserting):
    error_resp = 0
    query = Q.user_unfollow(for_inserting)
    jh.engine.execute(query)
    return error_resp, d.user_details(for_inserting.get("follower") ,1)

def update_user(for_inserting):
    error_resp = 0
    query = Q.user_update(for_inserting)
    jh.engine.execute(query)
    return error_resp, d.user_details(for_inserting.get("user"), 1)
