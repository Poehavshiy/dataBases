def concatinate(s_list):
    result = ""
    for r in s_list:
        result += r
    return result

def NUll_not_None(dict):
    for k in dict:
        if dict[k] == None:
            dict[k] = "NULL"

############## FORUM'S
def forum_create(ins_dict):
    s_list = []
    s_list.append("INSERT INTO Forum( `name`, `short_name`, `user`)")
    s_list.append(u"VALUES ('{name}' ".format(name=ins_dict.get("name")))
    s_list.append(u" ,'{short_name}', '{user}')".format
                  (short_name=ins_dict.get("short_name"), user=ins_dict.get("user")))
    return concatinate(s_list)


def forum_details(forum):
    s_list = []
    s_list.append(" select * from Forum where short_name = '{forum}' ".format(forum=forum))
    return concatinate(s_list)


def user_by_forum(forum):
    s_list = []
    s_list.append("select * from User where email in (")
    s_list.append(u"select user from Forum where short_name = '{forum}')".format(forum=forum))
    return concatinate(s_list)


def forums_threads(forum, since, limit, order):
    s_list = []
    s_list.append(u"select * from Thread where forum = '{forum}' ".format(forum=forum))
    if since != None:
        s_list.append(u" and date >= '{since}' ".format(since=since))
    if order == "desc":
        s_list.append(u" Order by date DESC ")
    else:
        s_list.append(u" Order by date ")
    if (limit != None):
        s_list.append(u" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)


def forums_users(forum, since, limit, order):
    s_list = []
    s_list.append("select * from User where email in ")
    s_list.append(" (select user from Post where forum = '{forum}' ) ".format(forum=forum))
    s_list.append(" and id >= {since} ".format(since=since))
    if order == "desc":
        s_list.append(" Order by User.name  desc")
    else:
        s_list.append(" Order by User.name ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)


############## USER'S
def user_create(ins_dict):
    NUll_not_None(ins_dict)
    isAnonymous = ins_dict.get("isAnonymous", False)
    #kostil
    about = ins_dict.get("about")
    s_list = []
    if about == "NULL":
        s_list.append("INSERT INTO User (`about`, `email`, `isAnonymous`, `name`, `username`)")
        s_list.append(
                u" VALUES ( {about},'{email}' ".format(about=ins_dict.get("about"), email=ins_dict.get("email")))
        s_list.append(", {isAnonymous} ".format(isAnonymous=isAnonymous))
        s_list.append(
            u",{name}, {username}); ".format(name=ins_dict.get("name"), username=ins_dict.get("username")))
        return concatinate(s_list)
########
    s_list.append("INSERT INTO User (`about`, `email`, `isAnonymous`, `name`, `username`)")
    s_list.append(u" VALUES ( '{about}','{email}' ".format(about=ins_dict.get("about"), email=ins_dict.get("email")))

    s_list.append(", {isAnonymous} ".format(isAnonymous=isAnonymous))
    s_list.append(u",'{name}', '{username}'); ".format(name=ins_dict.get("name"), username=ins_dict.get("username")))
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
    #if type == "following":
    if type == 0:
        s_list.append(" (select email2 from Followers where email1 = '{email}')".format(email=email))
    elif type == 1:
        s_list.append(" (select email1 from Followers where email2 = '{email}')".format(email=email))
    s_list.append(" and id >= {since} ".format(since=since))

    if order == "desc":
        s_list.append(" Order by User.name DESC ")
    else:
        s_list.append(" Order by User.name ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)


def users_subscriptions(email):
    s_list = []
    s_list.append("select tid from Subscriptions")
    s_list.append(" where email = '{email}' ".format(email=email))
    return concatinate(s_list)


def follow_user(key_values):
    s_list = []
    s_list.append("INSERT INTO Followers(`email1`, `email2`)")
    s_list.append("VALUES('{email1}', '{email2}')"
                  .format(email1=key_values.get("follower"), email2=key_values.get("followee")))
    return concatinate(s_list)


def user_unfollow(key_values):
    s_list = []
    s_list.append("DELETE FROM Followers WHERE ")
    s_list.append("email1 = '{email1}' and email2 = '{email2}'".format(
        email1=key_values["follower"], email2=key_values["followee"]))
    return concatinate(s_list)


def user_update(key_values):
    NUll_not_None(key_values)
    s_list = []
    s_list.append(u"UPDATE User Set about = '{about}', name = '{name}'".format(
        about=key_values["about"], name=key_values["name"]))
    s_list.append("Where email = '{email}'".format(email=key_values["user"]))
    return concatinate(s_list)


def users_threads(user, since, limit, order):
    s_list = []
    s_list.append(u"select * from Thread where user = '{user}'  ".format(user=user))
    if since != None:
        s_list.append(" and date >= '{since}' ".format(since=since))
    if order == "desc":
        s_list.append(" Order by date DESC ")
    else:
        s_list.append(" Order by date ")
    if (limit != None):
        s_list.append(" LIMIT {limit} ".format(limit=limit))
    return concatinate(s_list)


############## THREAD'S
def thread_create(ins_dict):
    s_list = []
    s_list.append("INSERT INTO Thread (`date`,`forum`,`isClosed`,"
                  "`isDeleted`,`message`,`slug`,`title`, `user`,`likes`, `dislikes`, `points` , `posts` )")
    s_list.append(u" VALUES ( '{date}','{forum}' ".format(date=ins_dict.get("date"), forum=ins_dict.get("forum")))
    s_list.append(u", {isClosed}  ".format(isClosed=ins_dict.get("isClosed")))
    s_list.append(
        u",{isDeleted}, '{message}' ".format(isDeleted=ins_dict.get("isDeleted", False), message=ins_dict.get("message")))
    s_list.append(u",'{slug}', '{title}' ".format(slug=ins_dict.get("slug"), title=ins_dict.get("title")))
    s_list.append(u",'{user}' ".format(user=ins_dict.get("user")))
    s_list.append(u",{likes}, {dislikes}, {points}, {posts} ) ".format(likes=0, dislikes=0, points=0, posts = 0))
    return concatinate(s_list)


def thread_details(id, likes = None):
    select =  u" date, forum, id, isClosed, isDeleted, message, slug ,title, user, posts "
    if likes != None:
        select += u",dislikes ,likes , points"

    return u"select {select} from Thread where id = {id}".format(select = select, id=id)


def close_open_thread(ins_dict, bool):
    s_list = []
    s_list.append(u"UPDATE Thread Set isClosed = {bool} Where ".format(bool=bool))
    s_list.append(u"id = {id} ".format(id=ins_dict.get("thread")))
    return concatinate(s_list)


def remove_restore_thread(ins_dict, bool):
    s_list = []
    s_list.append("UPDATE Thread Set isDeleted = {bool} ".format(bool = bool))
    if bool == True:
        s_list.append(" ,posts = 0 ")
    s_list.append("Where id = {id} ".format(id=ins_dict.get("thread")))

    return concatinate(s_list)

def count_thread_posts(thread):
    s_list = []
    s_list.append("select count(thread) as c from Post where  ")
    s_list.append ("thread = {thread} and isDeleted = False group by thread".format(thread = thread))
    return concatinate(s_list)

def set_posts(thread, post_c):
    s_list = []
    s_list.append(u"UPDATE Thread Set posts = {post_c} ".format(post_c=post_c))
    s_list.append(u"Where id = {id} ".format(id=thread))
    return concatinate(s_list)


def subscribe(ins_dict):
    s_list = []
    s_list.append(u"INSERT INTO Subscriptions(`email`, `tid`) ")
    s_list.append(u"VALUES('{email}', {thread});".format(email=ins_dict.get("user"),
                                                        thread=ins_dict.get("thread")))
    return concatinate(s_list)


def unsubscribe(ins_dict):
    s_list = []
    s_list.append(u"DELETE FROM Subscriptions ")
    s_list.append(u"Where email = '{email}' and tid = {thread} ;".format(email=ins_dict.get("user"),
                                                                        thread=ins_dict.get("thread")))
    return concatinate(s_list)


def update_thread(ins_dict):
    s_list = []
    s_list.append(u"UPDATE Thread Set message = '{message}', ".format(message=ins_dict.get("message")))
    s_list.append(u"slug = '{slug}'  Where ".format(slug=ins_dict.get("slug")))
    s_list.append(u"id = {id} ".format(id=ins_dict.get("thread")))
    return concatinate(s_list)


def thread_vote(ins_dict, bool):
    s_list = []
    if (bool == True):
        s_list.append(u"UPDATE Thread Set likes = likes + 1, points = points + 1")
    else:
        s_list.append(u"UPDATE Thread Set dislikes = dislikes + 1, points = points - 1 ")
    s_list.append(u" Where id = {id}".format(id=ins_dict.get("thread")))
    return concatinate(s_list)

def threads_posts_change(ins_dict, bool):
    s_list = []
    if (bool == False):#restoring
        s_list.append(u"UPDATE Thread Set posts = posts + 1")
    else:
        s_list.append(u"UPDATE Thread Set posts = posts - 1 ")
    s_list.append(u" Where id = {id}".format(id=ins_dict.get("thread")))
    return concatinate(s_list)


############## POST'S
def post_create(ins_dict):
    parent = -1
    isApproved = ins_dict.get("isApproved", False)
    isHighlighted = ins_dict.get("isHighlighted", False)
    isEdited = ins_dict.get("isEdited", False)
    isSpam = ins_dict.get("isSpam", False)
    isDeleted = ins_dict.get("isDeleted", False)
    parent = ins_dict.get("parent", None)
    if parent == None:
        parent = -1
        #######
    s_list = []
    s_list.append("INSERT INTO Post (`date`,`forum` ,`isApproved`,`isDeleted` ,`isEdited` ,`isHighlighted`,")
    s_list.append(u" `isSpam` ,`message`,`parent` ,`thread` ,`user`,`likes`,`dislikes`,`points`) ")

    s_list.append(u" \nVALUES ( '{date}','{forum}' ".format(date=ins_dict.get("date"), forum=ins_dict.get("forum")))
    s_list.append(u",{isApproved} ".format(isApproved=isApproved))
    s_list.append(u",{isDeleted}, {isEdited} ".format(isDeleted=isDeleted, isEdited=isEdited))
    s_list.append(u",{isHighlighted}, {isSpam} ".format(isHighlighted=isHighlighted, isSpam=isSpam))
    s_list.append(u",'{message}', {parent} ".format(message=ins_dict.get("message"), parent=parent))
    s_list.append(u",{thread}, '{user}' ".format(thread=ins_dict.get("thread"), user=ins_dict.get("user")))
    s_list.append(u",{likes}, {dislikes}, {points} ) ".format(likes=0, dislikes=0, points=0))
    return concatinate(s_list)


def post_details(id):
    return "select * from Post where id = {id} ".format(id=id)


def remove_restore_post(ins_dict, bool):
    s_list = []
    s_list.append(u"UPDATE Post Set isDeleted = {bool} Where ".format(bool=bool))
    s_list.append(u"id = {id} ".format(id=ins_dict.get("post")))
    return concatinate(s_list)

def remove_restore_posts(ins_dict, bool):
    s_list = []
    s_list.append("UPDATE Post Set isDeleted = {bool} Where ".format(bool = bool))
    s_list.append("thread = {thread} ".format(thread=ins_dict.get("thread")))
    return concatinate(s_list)

def update_post(ins_dict):
    s_list = []
    s_list.append(u"UPDATE Post Set message = '{message}' Where ".format(message=ins_dict.get("message")))
    s_list.append("id = {id} ".format(id=ins_dict.get("post")))
    return concatinate(s_list)


def vote(ins_dict, bool):
    s_list = []
    if (bool == True):
        s_list.append(u"UPDATE Post Set likes = likes + 1, points = points + 1")
    else:
        s_list.append(u"UPDATE Post Set dislikes = dislikes + 1, points = points - 1 ")
    s_list.append(" Where id = {id}".format(id=ins_dict.get("post")))
    return concatinate(s_list)


def max_id(table):
    return u"select max(id) from {table}".format(table=table)

def get_path_spath(parent_id):
    q = u"select path, sortpath from Post Where id = {id}".format(id=parent_id)
    return q

def set_path_sortpath(path, sortpath, id):
    path += "/" + str(id)
    q = u"UPDATE Post Set path = '{path}', sortpath = '{sortpath}' Where id = {id}".format(
        path=path, sortpath=sortpath, id=id)
    return q


def list_posts(since, order, sort_type, target, value):
    s_list = []

    s_list.append("select {select} from Post where {target} = {value} ".format(
        select = "*", target=target, value=value))
    if since != None:
        s_list.append(" and date >= '{since}' ".format(since=since))
    type = 0

    if sort_type == "flat":
        type = "date"
    elif sort_type == "tree" or sort_type == "parent_tree":
        type = "sortpath"

    s_list.append(" Order by {type} ".format(type = type))

    #
    if order == "desc" and sort_type == "flat":
        s_list.append(" DESC ")


    return concatinate(s_list)

