def concatinate(s_list):
    result = ""
    for r in s_list:
        result += r
    return result


############## FORUM'S
def forum_create(ins_dict):
    s_list = []
    s_list.append("INSERT INTO Forum( `name`, `short_name`, `user`)")
    s_list.append(" VALUES ('{name}' ".format( name=ins_dict.get("name")))
    s_list.append(" ,'{short_name}', '{user}')".format
                  (short_name=ins_dict.get("short_name"), user=ins_dict.get("user")))
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

def forums_posts(forum, since, limit, order):
    s_list = []
    s_list.append("select * from Post where forum = '{forum}' and isDeleted = false ".format(forum=forum))
    if since != None:
        s_list.append(" and date > '{since}' ".format(since=since))
    if order != None:
        s_list.append(" Order by date DESC ")
    else:
        s_list.append(" Order by date ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)

def forums_threads(forum, since, limit, order):
    s_list = []
    s_list.append("select * from Post where forum = '{forum}' and isDeleted = false ".format(forum=forum))
    if since != None:
        s_list.append(" and date > '{since}' ".format(since=since))
    if order != None:
        s_list.append(" Order by date DESC ")
    else:
        s_list.append(" Order by date ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)

def forums_users(forum, since, limit, order):
    s_list = []
    s_list.append("select * from User where email in ")
    s_list.append(" (select user from Post where forum = '{forum}' and isDeleted = false) ".format(forum=forum))
    if since != None:
        s_list.append(" and id > {since} ' ".format(since=since))
    if order != None:
        s_list.append(" Order by User.email DESC ")
    else:
        s_list.append(" Order by User.email ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)


############## USER'S
def user_create(ins_dict):
    isAnonymous = False
    if "isAnonymous" in ins_dict:
        isAnonymous = ins_dict.get("isAnonymous")

    s_list = []
    s_list.append("INSERT INTO User (`about`, `email`, `isAnonymous`, `name`, `username`)")
    s_list.append(" VALUES ( '{about}','{email}' ".format(about=ins_dict.get("about"), email=ins_dict.get("email")))
    s_list.append(", {isAnonymous} ".format(isAnonymous=isAnonymous))
    s_list.append(",'{name}', '{username}'); ".format(name=ins_dict.get("name"), username=ins_dict.get("username")))
    return concatinate(s_list)

def user_details(email):
    s_list = []
    s_list.append(" select * from User where email = '{email}'".format(email=email))
    return concatinate(s_list)

def user_follows(email):
    s_list = []
    s_list.append("select email2 from Followers where email1 = '{email}'".format(email=email))
    return concatinate(s_list)

def users_followers(email):
    s_list = []
    s_list.append("select email1 from Followers where email2 = '{email}'".format(email=email))
    return concatinate(s_list)

def list_followers_follow(email, since, limit, order, type):
    s_list = []
    s_list.append("select * from User where email in")
    if type == "following":
        s_list.append(" (select email2 from Followers where email1 = '{email}')".format( email = email ))
    elif type == "followers":
        s_list.append(" (select email1 from Followers where email2 = '{email}')".format(email=email))
    if since != None:
        s_list.append(" and id > {since} ".format(since=since))
    if order != None:
        s_list.append(" Order by name DESC ")
    else:
        s_list.append(" Order by name ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)

def users_subscriptions(email):
    s_list = []
    s_list.append("select count(email) from Subscriptions")
    s_list.append(" where email = '{email}' group by email".format(email=email))
    return concatinate(s_list)

def follow_user(key_values):
    s_list = []
    s_list.append("INSERT INTO Followers(`email1`, `email2`)")
    s_list.append("VALUES('{email1}', '{email2}')"
                  .format(email1 = key_values.get("follower"), email2 = key_values.get("followee")))
    return concatinate(s_list)

def user_unfollow(key_values):
    s_list = []
    s_list.append("DELETE FROM Followers WHERE ")
    s_list.append("email1 = '{email1}' and email2 = '{email2}'".format(
        email1 = key_values["follower"], email2 = key_values["followee"]))
    return concatinate(s_list)


############THREAD'S
def thread_create(ins_dict):
    s_list = []
    s_list.append("INSERT INTO Thread (`date`,`forum`,`isClosed`,`isDeleted`,`message`,`slug`,`title`, `user`)")
    s_list.append(" VALUES ( '{date}','{forum}' ".format(date=ins_dict.get("date"), forum=ins_dict.get("forum")))
    s_list.append(", {isClosed}  ".format( isClosed=ins_dict.get("isClosed")))
    s_list.append(",{isDeleted}, '{message}' ".format(isDeleted=ins_dict.get("isDeleted"), message=ins_dict.get("message")))
    s_list.append(",'{slug}', '{title}' ".format(slug=ins_dict.get("slug"), title=ins_dict.get("title")))
    s_list.append(",'{user}'); ".format(user=ins_dict.get("user")))
    return concatinate(s_list)

def thread_details(id, isDeleted = False):
    if(isDeleted == False):
        return "select * from Thread where id = {id} and isDeleted = false".format(id=id)
    else:
        return "select * from Thread where id = {id}".format(id=id)

def thread_posts(thread, since, limit, order):
    s_list = []
    s_list.append("select * from Post where thread = {thread} and isDeleted = false ".format(thread=thread))
    if since != None:
        s_list.append(" and date > '{since}' ".format(since=since))
    if order != None:
        s_list.append(" Order by date DESC ")
    else:
        s_list.append(" Order by date ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)

############POST'S
def post_create(ins_dict):
    isApproved = True
    isHighlighted = True
    isEdited = False
    isSpam = False
    isDeleted = False
    parent = "Null"
    if "isApproved" in ins_dict:
        isApproved = ins_dict.get("isApproved")
    if "isHighlighted" in ins_dict:
        isHighlighted = ins_dict.get("isHighlighted")
    if "isEdited" in ins_dict:
        isEdited = ins_dict.get("isEdited")
    if "isSpam" in ins_dict:
        isSpam = ins_dict.get("isSpam")
    if "isDeleted" in ins_dict:
        isDeleted = ins_dict.get("isDeleted")
    if "parent" in ins_dict:
        parent = ins_dict.get("parent")
        #######
    s_list = []
    s_list.append("INSERT INTO Post (`date`,`forum` ,`isApproved`,`isDeleted` ,`isEdited` ,`isHighlighted`,")
    s_list.append(" `isSpam` ,`message`,`parent` ,`thread` ,`user`,`likes`,`dislikes`,`points`) ")

    s_list.append(" \nVALUES ( '{date}','{forum}' ".format(date=ins_dict.get("date"), forum=ins_dict.get("forum")))
    s_list.append(",{isApproved} ".format(isApproved=isApproved))
    s_list.append(",{isDeleted}, {isEdited} ".format(isDeleted=isDeleted, isEdited=isEdited))
    s_list.append(",{isHighlighted}, {isSpam} ".format(isHighlighted=isHighlighted, isSpam=isSpam))
    s_list.append(",'{message}', {parent} ".format(message=ins_dict.get("message"), parent=parent))
    s_list.append(",{thread}, '{user}' ".format(thread=ins_dict.get("thread"), user=ins_dict.get("user")))
    s_list.append(",{likes}, {dislikes}, {points} ) ".format(likes=0, dislikes=0, points = 0))
    return concatinate(s_list)

def post_details(id):
    return "select * from Post where id = {id} and isDeleted = false".format(id=id)

def remove_restore_post(ins_dict, bool):
    s_list = []
    s_list.append("UPDATE Post Set isDeleted = {bool} Where ".format(bool=bool))
    s_list.append("id = {id} ".format(id=ins_dict.get("post")))
    return concatinate(s_list)

def update_post(ins_dict):
    s_list = []
    s_list.append("UPDATE Post Set message = '{message}' Where ".format(message=ins_dict.get("message")))
    s_list.append("id = {id} ".format(id=ins_dict.get("post")))
    return concatinate(s_list)

def vote(ins_dict, bool):
    s_list = []
    if( bool == True):
        s_list.append("UPDATE Post Set likes = likes + 1, points = points + 1")
    else:
        s_list.append("UPDATE Post Set dislikes = dislikes + 1, points = points - 1 ")
    s_list.append(" Where id = {id}".format(id=ins_dict.get("post")))
    return concatinate(s_list)

def max_id(table):
    return "select max(id) from {table}".format( table = table)

def users_posts(email, since, limit, order):
    s_list = []
    s_list.append("select * from Post where user = '{email}' and isDeleted = false ".format(email=email))
    if since != None:
        s_list.append(" and date > '{since}' ".format(since=since))
    if order != None:
        s_list.append(" Order by date DESC ")
    else:
        s_list.append(" Order by date ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)
