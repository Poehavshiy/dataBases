from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import post_functions as funct
import json_handle as jh
from json_handle import create_responce

def details(request):
    # 'example@mail.ru'
    id = request.GET['post']
    user = None
    forum = None
    thread = None
    related = request.GET.getlist('related')
    if 'user' in related:
        user = 'user'
    if 'forum' in related:
        forum = 'forum'
    if 'thread' in related:
        thread = 'thread'
    json_dict = funct.post_details(id, user, forum, thread)
    json_data = create_responce(json_dict)
    return HttpResponse(json_data)
