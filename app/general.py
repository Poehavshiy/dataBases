from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import  json_handle as jh

def clear_all():
    print ' NEW TEST\n\n\n\ '
    query_list  = []
    query_list.append("TRUNCATE TABLE Forum")
    query_list.append("TRUNCATE TABLE User")
    query_list.append("TRUNCATE TABLE Thread")
    query_list.append("TRUNCATE TABLE Post")
    query_list.append("TRUNCATE TABLE Subscriptions")
    query_list.append( "TRUNCATE TABLE Followers")

    jh.engine.execute('SET NAMES utf8;')
    jh.engine.execute('SET CHARACTER SET utf8;')
    jh.engine.execute('SET character_set_connection=utf8;')

    for q in query_list:
        jh.engine.execute(q)

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
    for t in tables:
        query_list.append("select count(id) as c from {table} ".format(table = t))
    for q in query_list:
        rs = jh.engine.execute(q)
        base_dict = jh.list_of_dict(rs)
        result.append(base_dict[0].get("c"))
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

