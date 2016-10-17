def concatinate(s_list):
    result = ""
    for r in s_list:
        result += r
    return result


############## FORUM'S
def forum_create(ins_dict):
    s_list = []
    s_list.append("INSERT INTO Forum(`id`, `name`, `short_name`, `user`)")
    s_list.append(" VALUES ({id},'{name}' ".format(id=ins_dict.get("id"), name=ins_dict.get("name")))
    s_list.append(
        " ,'{short_name}', '{user}'); ".format(short_name=ins_dict.get("short_name"), user=ins_dict.get("user")))
    return concatinate(s_list)


def forum_details(forum):
    s_list = []
    s_list.append(" select * from Forum where short_name = '{forum}' ".format(forum=forum))
    return concatinate(s_list)


def user_by_forum(forum):
    s_list = []
    s_list.append("select * from User where email in (")
    s_list.append("select user from Forum where short_name = '{forum}')".format(forum=forum))
    return concatinate(s_list)

############## USER'S
def user_details(email):
    s_list = []
    s_list.append(" select * from User where email = '{email}'".format(email=email) )
    return concatinate(s_list)

def user_follows(email):
    s_list = []
    s_list.append ( "select email2 from Followers where email1 = '{email}'".format(email=email) )
    return concatinate(s_list)

def users_followers(email):
    s_list = []
    s_list.append ( "select email1 from Followers where email2 = '{email}'".format(email=email) )
    return concatinate(s_list)

def users_subscriptions(email):
    s_list = []
    s_list.append( "select count(email) from Subscriptions" )
    s_list.append ( " where email = '{email}' group by email".format(email=email) )
    return concatinate(s_list)

#THREAD'S
def thread_details(id):
    return "select * from Thread where id = {id}".format(id=id)