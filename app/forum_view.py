from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import forum_functions as funct
import details as d
import json_handle as jh
from json_handle import create_responce
from post_functions import Post_listing
from general import Creator



def details(request):
    forum = ""
    if "forum" in request.GET:
        forum = request.GET['forum']
    else:
        return HttpResponse(json.dumps(jh.invalid_request))
    user = None
    if 'related' in request.GET:
        user = request.GET['related']
    json_dict = d.forum_details(forum, user)
    if(json_dict == None):
        return HttpResponse(json.dumps(jh.nothing_found))
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)
#####
def listPosts(request):
    list = Post_listing()
    return list.forum(request)
#####

def list_threads(request):
    #print request
    target_forum = ""
    if "forum" in request.GET:
        target_forum = request.GET['forum']
    else:
        return HttpResponse(json.dumps(jh.invalid_request))
    since = request.GET.get("since", None)
    limit = request.GET.get("limit", None)
    order = request.GET.get("order", "desc")

    user = None
    forum = None
    related = request.GET.getlist('related')
    if 'user' in related:
        user = 'user'
    if 'forum' in related:
        forum = 'forum'
    json_dict = funct.list_threads(target_forum, since, limit, order, user, forum)
    json_data = create_responce(json_dict)
    #print json_data
    #check = str(forum) + ' ' + str(since) + ' ' + str(limit) + ' ' + str(order) + ' ' + str(user) + ' ' + str(forum)
    return HttpResponse(json_data)
#####
def list_users(request):
    target_forum = ""
    if "forum" in request.GET:
        target_forum = request.GET['forum']
    else:
        return HttpResponse(json.dumps(jh.invalid_request))
    since = request.GET.get("since_id", 0)
    limit = request.GET.get("limit", None)
    order = request.GET.get("order", "desc")
    json_dict = funct.list_users(target_forum, since, limit, order)
    #if not json_dict:
    #    return HttpResponse(json.dumps(jh.nothing_found))
    json_data = create_responce(json_dict)
    #print json_data
    return HttpResponse(json_data)
#####
@csrf_exempt
def create(request):
    if request.method == 'POST':
        try:
            #print "forum create\n"
            #print request.body
            json_data = json.loads(request.body)
        except ValueError as error:
            return HttpResponse(json.dumps(jh.invalid_request))

        error, json_dict = Creator.create_forum(json_data)
        if json_dict == None:
            return HttpResponse(json.dumps(jh.already_exists))
        json_data = create_responce(json_dict)
        #print json_data
        return HttpResponse(json_data)

#####

