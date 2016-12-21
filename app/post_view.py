from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import post_functions as funct
import details as d
import json_handle as jh
from json_handle import create_responce
from general import Creator, max_id


def details(request):
    id = 0
    if "post" in request.GET:
        id = request.GET['post']
        id = int(id)
    if id < 1:
        return HttpResponse(HttpResponse(json.dumps(jh.nothing_found)))
    # print request
    user = None
    forum = None
    thread = None
    related = None
    if 'related' in request.GET:
        related = request.GET.getlist('related')
        if 'user' in related:
            user = 'user'
        if 'forum' in related:
            forum = 'forum'
        if 'thread' in related:
            thread = 'thread'
    json_dict = d.post_details(id, user, forum, thread)
    list_pop_fields = ["path", "sortpath"]
    for iter in list_pop_fields:
        json_dict.pop(iter)

    if json_dict["parent"] == -1:
        json_dict["parent"] = None

    if (json_dict == None):
        return HttpResponse(json.dumps(jh.nothing_found))
    json_data = create_responce(json_dict)
    # print json_data
    return HttpResponse(json_data)


######
@csrf_exempt
def list(request):
    list = funct.Post_listing()
    return list.post(request)


#####
@csrf_exempt
def remove(request):
    if request.method == 'POST':
       # print request.body
        json_data = json.loads(request.body)
        # print json_data
        error = funct.remove_restore(json_data, True)
        json_data = create_responce(json_data)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def restore(request):
    if request.method == 'POST':
      #  print request.body
        json_data = json.loads(request.body)
        # print json_data
        error = funct.remove_restore(json_data, False)
        json_data = create_responce(json_data)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def update(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        # print json_data
        error, json_dict = funct.post_update(json_data)
        list_pop_fields = ["path", "sortpath"]
        for iter in list_pop_fields:
            json_dict.pop(iter)
        if json_dict["parent"] == -1:
            json_dict["parent"] = None

        json_data = create_responce(json_dict)
        #  print json_data
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def vote(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        bool = True
        if (json_data.get("vote") < 0):
            bool = False
        error, json_dict = funct.post_vote(json_data, bool)
        json_data = create_responce(json_dict)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def create(request):
    if request.method == 'POST':
        try:
           # print request.body
            json_data = json.loads(request.body)
            if json_data["thread"] < 1 or json_data["thread"] > max_id("Thread"):
                return HttpResponse(json.dumps(jh.nothing_found))
        except ValueError:
            return HttpResponse(json.dumps(jh.invalid_request))
        # print "\n"
        # print request.body
        error, json_dict = Creator.create_post(json_data)
        if "parent" not in json_dict:
            json_dict["parent"] = None

        json_data = create_responce(json_dict)
        # print json_data
        return HttpResponse(json_data)
