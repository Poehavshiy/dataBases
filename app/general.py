from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import  json_handle as jh
import queries as Q
from sqlalchemy import exc


def max_id(table):
    connection = jh.engine.connect()
    rs = connection.execute(Q.max_id(table))
    base_dict = jh.create_dict_base(rs)
    id = base_dict.get("max(id)")
    connection.close()
    return id


class Creator:
    nposts = 0
    nthreads = 0
    nusers = 0
    nforums = 0

    def __init__(self):
        self.nposts = max_id("Post")
        self.nthreads = max_id("Thread")
        self.nusers = max_id("User")
        self.nforums = max_id("Forum")

    def zeros(self):
        self.nposts = 0
        self.nthreads = 0
        self.nusers = 0
        self.nforums = 0

    def general_creation(self, for_inserting, type,counter):
        connection = jh.engine.connect()
        values = jh.create_insert_dict(for_inserting)
        #
        query = None
        query1 = None
        counter = counter + 1
        if type == 0:
            query = Q.post_create_real(values, counter)
            query1 = Q.threads_posts_change(values, False)
        elif type == 1:
            query = Q.thread_create(values)
        elif type == 2:
            query = Q.forum_create(values)
        elif type == 3:
            query = Q.user_create(values)
        #
        try:
            connection.execute(query)
            if query1 != None:
                connection.execute(query1)
        except exc.SQLAlchemyError:
            counter = counter - 1
            connection.close()
            return 1, None

        for_inserting["id"] = counter
        connection.close()
        #
        if type == 0:
            self.nposts = counter
        elif type == 1:
            self.nthreads = counter
        elif type == 2:
            self.nforums = counter
        elif type == 3:
            self.nusers = counter
        #
        return 0, for_inserting


    def create_post(self, for_inserting):
        return self.general_creation(for_inserting, 0, self.nposts)

    def create_thread(self, for_inserting):
        return self.general_creation(for_inserting, 1, self.nthreads)

    def create_forum(self,for_inserting ):
        return self.general_creation(for_inserting, 2, self.nforums)

    def create_user(self, for_inserting):
        return self.general_creation(for_inserting, 3, self.nusers)

creator = Creator()

def clear_all():
    print ' NEW TEST\n\n\n\ '
    query_list  = []
    query_list.append("TRUNCATE TABLE Forum")
    query_list.append("TRUNCATE TABLE User")
    query_list.append("TRUNCATE TABLE Thread")
    query_list.append("TRUNCATE TABLE Post")
    query_list.append("TRUNCATE TABLE Subscriptions")
    query_list.append( "TRUNCATE TABLE Followers")
    query_list.append("ALTER TABLE Post CONVERT TO CHARACTER SET utf8")
    query_list.append("ALTER TABLE Thread CONVERT TO CHARACTER SET utf8")
    query_list.append("ALTER TABLE Forum CONVERT TO CHARACTER SET utf8")
    query_list.append("ALTER TABLE User CONVERT TO CHARACTER SET utf8")
    creator.zeros()

    #jh.engine.execute('SET NAMES utf8;')
    #jh.engine.execute('SET CHARACTER SET utf8;')
    #jh.engine.execute('SET character_set_connection=utf8;')
    connection = jh.engine.connect()
    for q in query_list:
        connection.execute(q)
    connection.close()

@csrf_exempt
def clear(request):
    f = open('workfile', 'w')
    if request.method == 'POST':
        clear_all()
        resp_dict = {"code": 0, "response": "OK"}
        json_data = json.dumps(resp_dict)
        return HttpResponse(json_data)

def calculate():
    tables = ["User", "Thread", "Forum", "Post"]
    query_list = []
    result = []
    connection = jh.engine.connect()
    for t in tables:
        query_list.append("select count(id) as c from {table} ".format(table = t))
    for q in query_list:
        rs = connection.execute(q)
        base_dict = jh.list_of_dict(rs)
        result.append(base_dict[0].get("c"))
    connection.close()
    return result


def status(request):
    tables = calculate()
    data = {"user": tables[0], "thread": tables[1], "forum": tables[2], "post": tables[3]}
    resp_dict = {"code": 0, "response": data}
    json_data = json.dumps(resp_dict)
    return HttpResponse(json_data)


"""tables = calculate()
data = {"user": tables[0], "thread": tables[1], "forum": tables[2], "post": tables[3]}
resp_dict = {"code": 0, "response": data}
print resp_dict"""
#clear_all()

