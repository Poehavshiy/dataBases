from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import thread_functions as funct
import details as d
from json_handle import create_responce

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


