from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import user_functions as funct
from json_handle import create_responce
import json_handle as jh
import details as d


@csrf_exempt
def create(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except ValueError:
            return HttpResponse(json.dumps(jh.invalid_request))
        error, json_dict = d.create(json_data, "user")
        if json_dict == None:
            return HttpResponse(json.dumps(jh.already_exists))
        json_data = create_responce(json_dict)
        return HttpResponse(json_data)

@csrf_exempt
def follow(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error, json_dict = funct.follow(json_data)
        json_data = create_responce(json_dict)
        if (error == 0):
            return HttpResponse(error)
        else:
            return HttpResponse(error)

def listFollowers(request):
    email = request.GET['user']
    since_id = None
    limit = None
    order = None
    if 'since_id' in request.GET:
        since_id = request.GET['since_id']
    if 'limit' in request.GET:
        limit = request.GET['limit']
    if 'order' in request.GET:
        order = request.GET['order']
    json_dict = funct.list_followers_follow(email, since_id, limit, order, "followers")
    json_data = create_responce(json_dict)
    # check = str(forum) + ' ' + str(since) + ' ' + str(limit) + ' ' + str(order) + ' ' + str(user) + ' ' + str(forum)
    return HttpResponse(json_data)

def listFollowing(request):
    email = request.GET['user']
    since_id = None
    limit = None
    order = None
    if 'since_id' in request.GET:
        since_id = request.GET['since_id']
    if 'limit' in request.GET:
        limit = request.GET['limit']
    if 'order' in request.GET:
        order = request.GET['order']
    json_dict = funct.list_followers_follow(email, since_id, limit, order, "following")
    json_data = create_responce(json_dict)
    # check = str(forum) + ' ' + str(since) + ' ' + str(limit) + ' ' + str(order) + ' ' + str(user) + ' ' + str(forum)
    return HttpResponse(json_data)

def listPosts(request):
    target_user = request.GET['user']
    since = None
    limit = None
    order = None
    if 'since' in request.GET:
        since = request.GET['since']
    if 'limit' in request.GET:
        limit = request.GET['limit']
    if 'order' in request.GET:
        order = request.GET['order']
    json_dict = funct.list_posts(target_user, since, limit, order)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)

@csrf_exempt
def unfollow(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        error, json_dict = funct.unfollow(json_data)
        json_data = create_responce(json_dict)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)

@csrf_exempt
def updateProfile(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except ValueError:
            return HttpResponse(json.dumps(jh.invalid_request))
        error, json_dict = funct.update_user(json_data)
        json_data = create_responce(json_dict)

        return HttpResponse(json_data)
