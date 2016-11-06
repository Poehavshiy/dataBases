from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import thread_functions as funct
import details as d
from json_handle import create_responce
from post_functions import list_posts


def details(request):
    # 'example@mail.ru'
    id = request.GET['thread']
    user = None
    forum = None
    related = request.GET.getlist('related')
    if 'user' in related:
        user = 'user'
    if 'forum' in related:
        forum = 'forum'
    json_dict = funct.thread_details(id, user, forum)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)


@csrf_exempt
def create(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error, json_dict = d.create(json_data, "thread")
        json_data = create_responce(json_dict)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def close(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error = funct.close_open(json_data, True)
        json_data = create_responce(json_data)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


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
    user = None
    if 'forum' in request.GET:
        forum = request.GET['forum']
    if 'user' in request.GET:
        user = 'thread'
    json_dict = funct.list_threads(since, limit, order, forum, user)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)


def listPosts(request):
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
    thread = 'thread'
    json_dict = list_posts(since, limit, order, forum, thread)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)


def open(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error = funct.close_open(json_data, False)
        json_data = create_responce(json_data)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


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
def subscribe(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error = funct.subscribe(json_data)
        json_data = create_responce(json_data)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def unsubscribe(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error = funct.unsubscribe(json_data)
        json_data = create_responce(json_data)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def update(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error, json_dict = funct.thread_update(json_data)
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
        if (json_data.get("vote") < 0):
            bool = False
        error, json_dict = funct.thread_vote(json_data, bool)
        json_data = create_responce(json_dict)
        return HttpResponse(json_data)
