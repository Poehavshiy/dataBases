from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import user_functions as funct
from json_handle import create_responce
import json_handle as jh
import details as d
from post_functions import Post_listing

def details(request):
    user = request.GET['user']

    json_dict = d.user_details(user, 1)
    if (json_dict == None):
        return HttpResponse(json.dumps(jh.nothing_found))
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)

@csrf_exempt
def create(request):
    #{"username": null, "about": null, "isAnonymous": true, "name": null, "email": "richard.nixon@example.com"}
    #{"username": "None", "about": "None", "isAnonymous": "True", "name": "None, "email": "richard.nixon@example.com"}
    if request.method == 'POST':
        try:
            #print "user create\n"
            #print request.body
            json_data = json.loads(request.body)
        except ValueError:
            return HttpResponse(json.dumps(jh.invalid_request))
        error, json_dict = d.create(json_data, "user")
        if json_dict == None:
            #print json.dumps(jh.already_exists)
            return HttpResponse(json.dumps(jh.already_exists))
        json_data = create_responce(json_dict)
        #print "\n", json_data
        #return HttpResponse(json.dumps(json_data))
        return HttpResponse(json_data)

#who follows this user
def listFollowers(request):
    email = request.GET['user']
    #print "Get followers of this user"
    since_id = request.GET.get("since_id", 0)
    limit = request.GET.get("limit", None)
    order = request.GET.get("order", "desc")
    #followers -
    json_dict = funct.list_followers_follow(email, since_id, limit, order, 1)
    json_data = create_responce(json_dict)
    #print json_data
    return HttpResponse(json_data)

# who does this person follows
def listFollowing(request):
    email = request.GET['user']
    #print "Get following of this user"
    since_id = request.GET.get("since_id", 0)
    limit = request.GET.get("limit", None)
    order = request.GET.get("order", "desc")
    #following
    json_dict = funct.list_followers_follow(email, since_id, limit, order, 0)
    json_data = create_responce(json_dict)
    #print json_data
    return HttpResponse(json_data)

def listPosts(request):
    list = Post_listing()
    return list.user(request)

@csrf_exempt
def unfollow(request):
    #return HttpResponse(1)
    if request.method == 'POST':
        #print "UN_Follow"
        #print request.body
        json_data = json.loads(request.body)
        error, json_dict = funct.unfollow(json_data)
        json_data = create_responce(json_dict)
        #print json_data
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(error)

@csrf_exempt
def follow(request):
    if request.method == 'POST':
        #print "Follow user to another"
        #print request.body
        json_data = json.loads(request.body)
        error, json_dict = funct.follow(json_data)
        json_data = create_responce(json_dict)
        #print json_data
        if (error == 0):
            return HttpResponse(json_data)
        else:
            return HttpResponse(HttpResponse(json.dumps(jh.invalid_request)))

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
