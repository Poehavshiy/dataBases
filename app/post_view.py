from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import post_functions as funct
import details as d
import json_handle as jh
from json_handle import create_responce

def details(request):
    id = 0
    if "post" in request.GET:
        id = request.GET['post']
    else:
        return HttpResponse(json.dumps(jh.invalid_request))
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
    if (json_dict == None):
        return HttpResponse(json.dumps(jh.nothing_found))
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)
######
@csrf_exempt
def list(request):
    since = None
    limit = None
    order = None

    if 'since' in request.GET:
        since = request.GET['since']
    if 'limit' in request.GET:
        limit = request.GET['limit']
    if 'order' in request.GET:
        order = request.GET['order']
    forum = None
    thread = None
    if 'forum' in request.GET:
        forum = request.GET['forum']
    if 'thread' in request.GET:
        thread = 'thread'
    json_dict = funct.list_posts(since, limit, order, forum, thread)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)
#####
@csrf_exempt
def remove(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error = funct.remove_restore(json_data, True)
        json_data = create_responce(json_data)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)

@csrf_exempt
def restore(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
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
        error, json_dict = funct.post_update(json_data)
        json_data = create_responce(json_dict)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)

@csrf_exempt
def vote(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        bool = True
        if(json_data.get("vote") < 0):
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
            json_data = json.loads(request.body)
        except ValueError:
            return HttpResponse(json.dumps(jh.invalid_request))
        error, json_dict = d.create(json_data, "post")
        json_data = create_responce(json_dict)
        return HttpResponse(json_data)

