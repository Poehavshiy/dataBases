from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import forum_functions as funct
from json_handle import create_responce

def details(request):
    # 'example@mail.ru'
    forum = request.GET['forum']
    user = None
    if 'related' in request.GET:
        user = request.GET['related']
    json_dict = funct.forum_details(forum, user)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)
#####
@csrf_exempt
def create(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        for_inserting = json_data["response"]
        error = funct.create(for_inserting)
        if(error == 0):
            return HttpResponse(request.body)
        else:
            return HttpResponse(error)
#####
def list_posts(request):
    a=1
