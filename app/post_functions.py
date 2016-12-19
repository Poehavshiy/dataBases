import queries as Q
import json_handle as jh
import details as det
from django.http import HttpResponse
import json


class Post_listing:
    since = None
    limit = None
    order = None
    sort = None
    target = None
    related = []

    def since_limit_order(self, request):
        self.since = request.GET.get('since', None)
        self.limit = request.GET.get('limit', None)
        if self.limit != None:
            self.limit = int(self.limit)
        self.order = request.GET.get('order', "Decs")

    def repair(self, base_dict):
        for d in base_dict:
            if d["parent"] == -1:
                d["parent"] = None
            d.pop("path")
            d.pop("sortpath")

    def user(self, request):
        connection = jh.engine.connect()
        # print request
        self.since_limit_order(request)
        user = "'" + request.GET["user"] + "'"
        query = Q.list_posts(self.since, self.order, "flat", "user", user)
        rs = connection.execute(query)
        base_dict = jh.list_of_dict(rs)
        if self.limit == None:
            self.limit = len(base_dict)
        base_dict = base_dict[:self.limit]
        if not base_dict:
            json_data = jh.create_responce(base_dict)
            connection.close()
            return HttpResponse(json_data)
        self.repair(base_dict)
        json_data = jh.create_responce(base_dict)
        # print json_data
        connection.close()
        return HttpResponse(json_data)

    def forum(self, request):
        connection = jh.engine.connect()
        self.since_limit_order(request)
        forum = "'" + request.GET["forum"] + "'"
        query = Q.list_posts(self.since, self.order, "flat", "forum", forum)
        rs = connection.execute(query)
        base_dict = jh.list_of_dict(rs)
        if self.limit == None:
            self.limit = len(base_dict)
        base_dict = base_dict[:self.limit]
        if not base_dict:
            json_data = jh.create_responce(base_dict)
            # print json_data
            connection.close()
            return HttpResponse(json_data)
        self.repair(base_dict)

        related = request.GET.getlist("related", None)
        users = {}
        threads = {}
        forum = {}
        if related:
            if 'user' in related:
                query = Q.forums_users(base_dict[0].get("forum"), None, None, None)
                rs = connection.execute(query)
                user_list = jh.list_of_dict(rs)
                for user in user_list:
                    users.update({user.get("email"): user})
            if 'forum' in related:
                forum = det.forum_details(base_dict[0]['forum'], None)
            if 'thread' in related:
                query = Q.forums_threads(base_dict[0].get("forum"), None, None, None)
                rs = connection.execute(query)
                thread_list = jh.list_of_dict(rs)
                for thread in thread_list:
                    threads.update({thread.get("id"): thread})

        for post in base_dict:
            if users:
                user = post.get("user")
                post["user"] =  users.get(user)
            if threads:
                thread = post.get("thread")
                post["thread"] = threads.get(thread)
            if forum:
                post["forum"] = forum

        json_data = jh.create_responce(base_dict)
        # print json_data
        connection.close()
        return HttpResponse(json_data)

    def thread(self, request):
        connection = jh.engine.connect()

        self.since_limit_order(request)
        self.sort = request.GET.get('sort', "flat")
        thread = request.GET["thread"]
        query = Q.list_posts(self.since, self.order, self.sort, "thread", thread)
        rs = connection.execute(query)

        base_dict = jh.list_of_dict(rs)
        if not base_dict:
            json_data = jh.create_responce(base_dict)
            connection.close()
            return HttpResponse(json_data)

        if self.sort == "flat":
            if self.limit == None:
                self.limit = len(base_dict)
            base_dict = base_dict[:self.limit]

        elif self.sort == "tree" or self.sort == "parent_tree":
            if self.order == "desc":
                base_dict = repair_desc_tree(base_dict, self.limit, self.order, self.sort)
            elif self.order == "asc":
                if self.sort == "tree":
                    base_dict = base_dict[:self.limit]
                else:
                    base_dict = repair_parent_tree(base_dict, self.limit)
        self.repair(base_dict)
        json_data = jh.create_responce(base_dict)
        # print json_data
        connection.close()
        return HttpResponse(json_data)

    def post(self, request):
        if 'forum' in request.GET:
            return self.forum(request)
        if 'thread' in request.GET:
            return self.thread(request)


def repair_parent_tree(dict, limit):
    i = 0
    count = 0
    while count <= limit and i < len(dict):
        if dict[i]["path"].count("/") == 1:
            count = count + 1
        if count <= limit:
            i = i + 1
    new_dict = dict[:i]
    return new_dict


def repair_desc_tree(base_dict, limit, order, sort_type):
    if order == "asc":
        base_dict = base_dict[:limit]
        return base_dict
    else:
        new_dict = []
        end = len(base_dict) - 1
        i = end
        while i >= 0:
            if base_dict[i]["path"].count("/") == 1:
                new_dict.extend(base_dict[i:end + 1])
                end = i - 1
            i = i - 1
        if sort_type == "tree":
            new_dict = new_dict[:limit]
        else:
            new_dict = repair_parent_tree(new_dict, limit)
        return new_dict


####
def remove_restore(for_inserting, bool):
    connection = jh.engine.connect()
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    json_dict = det.post_details(key_values.get("post"), None, None, None)
    # if post is already deleted
    if json_dict.get("isDeleted") == 1 and bool == True:
        connection.close()
        return 0
    # if post is already restored
    if json_dict.get("isDeleted") == 0 and bool == False:
        connection.close()
        return 0
    query = Q.remove_restore_post(key_values, bool)
    connection.execute(query)
    # change threads posts
    query = Q.threads_posts_change(json_dict, bool)
    connection.execute(query)
    connection.close()
    return error_resp


####
def post_update(for_inserting):
    connection = jh.engine.connect()
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.update_post(key_values)
    connection.execute(query)
    answer = det.post_details(key_values.get("post"), None, None, None)
    connection.close()
    return error_resp, answer


####
def post_vote(for_inserting, bool):
    connection = jh.engine.connect()
    error_resp = 0
    key_values = jh.create_insert_dict(for_inserting)
    query = Q.vote(key_values, bool)
    connection.execute(query)
    answer = det.post_details(key_values.get("post"), None, None, None)
    connection.close()
    return error_resp, answer

# r ={"vote": -1, "post": 5}
# answer = list_posts(None, None, None,None, "Forum", "forum1")
# print answer
