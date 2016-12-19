from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import thread_functions as funct
import details as d
import json_handle as jh
from json_handle import create_responce
from post_functions import Post_listing
from general import creator


def check_keys(list, check_list):
    for item in list:
        if item not in check_list:
            return False
    return True


def details(request):
    # 'example@mail.ru'
    id = request.GET['thread']
    id = int(id)
    if id < 1 or id > creator.nthreads:
        return HttpResponse(json.dumps(jh.nothing_found))
    user = None
    forum = None
    related = request.GET.getlist('related')

    if not check_keys(related, ("user", "forum")):
        return HttpResponse(json.dumps(jh.invalid_request))

    if 'user' in related:
        user = 'user'
    if 'forum' in related:
        forum = 'forum'
    json_dict = d.thread_details(id, user, forum, 1)
    if json_dict == None:
        return HttpResponse(json.dumps(jh.nothing_found))

    json_data = create_responce(json_dict)
    # print json_data
    return HttpResponse(json_data)


@csrf_exempt
def create(request):
    if request.method == 'POST':
        try:
            # print "post create\n"
            #print request.body
            json_data = json.loads(request.body)
        except ValueError:
            return HttpResponse(json.dumps(jh.invalid_request))
    # print "thread crate\n"
    # print request.body
    json_data = json.loads(request.body)
    error, json_dict = creator.create_thread(json_data)
    json_data = create_responce(json_dict)
    # print json_data
    if (error == 0):
        return HttpResponse(json_data)
    else:
        return HttpResponse(error)


@csrf_exempt
def close(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        id = json_data['thread']
        if id < 1 or id > creator.nthreads:
            return HttpResponse(json.dumps(jh.nothing_found))

        error = funct.close_open(json_data, True)
        json_data = create_responce(json_data)
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


def list(request):
    since = request.GET.get("since", None)
    limit = request.GET.get("limit", None)
    order = request.GET.get("order", "desc")

    forum = None
    user = None
    if 'forum' in request.GET:
        forum = request.GET['forum']
    if 'user' in request.GET:
        user = request.GET['user']

    # print "listthreads\n"
    # print request
    json_dict = funct.list_threads(since, limit, order, forum, user)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)


def listPosts(request):
    list = Post_listing()
    answer = list.thread(request)
    #print answer
    return answer


@csrf_exempt
def open(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        id = json_data['thread']
        if id < 1 or id > creator.nthreads:
            return HttpResponse(json.dumps(jh.nothing_found))
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
        id = json_data['thread']
        if id < 1 or id > creator.nthreads:
            return HttpResponse(json.dumps(jh.nothing_found))
        # print "thread remove"
        # print json_data
        error = funct.remove_restore(json_data, True)
        json_data = create_responce(json_data)
        # print json_data
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def restore(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        id = json_data['thread']
        if id < 1 or id > creator.nthreads:
            return HttpResponse(json.dumps(jh.nothing_found))
        # print "thread restore"
        # print json_data
        error = funct.remove_restore(json_data, False)
        json_data = create_responce(json_data)
        # print json_data
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)


@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        id = json_data['thread']
        if id < 1 or id > creator.nthreads:
            return HttpResponse(json.dumps(jh.nothing_found))
        # print "subscribe\n"
        # print json_data
        error = funct.subscribe(json_data)
        json_data = create_responce(json_data)
        # print json_data
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(json.dumps(jh.already_exists))


@csrf_exempt
def unsubscribe(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        id = json_data['thread']
        if id < 1 or id > creator.nthreads:
            return HttpResponse(json.dumps(jh.nothing_found))
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
        id = json_data['thread']
        if id < 1 or id > creator.nthreads:
            return HttpResponse(json.dumps(jh.nothing_found))
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
        id = json_data['thread']
        if id < 1 or id > creator.nthreads:
            return HttpResponse(json.dumps(jh.nothing_found))
        bool = True
        if (json_data.get("vote") < 0):
            bool = False
        error, json_dict = funct.thread_vote(json_data, bool)
        json_data = create_responce(json_dict)
        return HttpResponse(json_data)
