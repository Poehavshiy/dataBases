from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import forum_functions as funct
import details as d
from json_handle import create_responce


def details(request):
    forum = request.GET['forum']
    user = None
    if 'related' in request.GET:
        user = request.GET['related']
    json_dict = funct.forum_details(forum, user)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)
#####
def list_posts(request):
    target_forum = request.GET['forum']
    since = None
    limit = None
    order = None

    if 'since' in request.GET:
        since = request.GET['since']
    if 'limit' in request.GET:
        limit = request.GET['limit']
    if 'order' in request.GET:
        order = request.GET['order']
    user = None
    forum = None
    thread = None
    related = request.GET
    if 'user' in related:
        user = 'user'
    if 'forum' in related:
        forum = 'forum'
    if 'thread' in related:
        thread = 'thread'
    json_dict = funct.list_posts(target_forum, since, limit, order, user, forum, thread)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)
#####
def list_threads(request):
    target_forum = request.GET['forum']
    since = None
    limit = None
    order = None
    if 'since' in request.GET:
        since = request.GET['since']
    if 'limit' in request.GET:
        limit = request.GET['limit']
    if 'order' in request.GET:
        order = request.GET['order']
    user = None
    forum = None
    related = request.GET.getlist('related')
    if 'user' in related:
        user = 'user'
    if 'forum' in related:
        forum = 'forum'
    json_dict = funct.list_threads(target_forum, since, limit, order, user, forum)
    json_data = create_responce(json_dict)
    #check = str(forum) + ' ' + str(since) + ' ' + str(limit) + ' ' + str(order) + ' ' + str(user) + ' ' + str(forum)
    return HttpResponse(json_data)
#####
def list_users(request):
    target_forum = request.GET['forum']
    since = None
    limit = None
    order = None
    if 'since' in request.GET:
        since = request.GET['since']
    if 'limit' in request.GET:
        limit = request.GET['limit']
    if 'order' in request.GET:
        order = request.GET['order']
    json_dict = funct.list_users(target_forum, since, limit, order)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)
#####
@csrf_exempt
def create(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error, json_dict = d.create(json_data, "forum")
        json_data = create_responce(json_dict)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)
#####