from django.conf.urls import url

from . import user_view
from . import forum_view
from . import thread_view
from . import post_view

urlpatterns = [
    #forum's
    url('forum/details/', forum_view.details, name='details'),
    url('forum/create/', forum_view.create, name='create'),
    url('forum/listPosts/', forum_view.list_posts, name='list_posts'),
    url('forum/listThreads/', forum_view.list_threads, name='list_threads'),
    url('forum/listUsers/', forum_view.list_users, name='list_users'),
    #thread's
    url('thread/details/', thread_view.details, name='details'),
    #post's
    url('post/details/',post_view.details, name='details')
]
