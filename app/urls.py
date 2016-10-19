from django.conf.urls import url

from . import user_view
from . import forum_view
from . import thread_view
from . import post_view

urlpatterns = [
    #forum's
    url('forum/create/', forum_view.create, name='create'),
    url('forum/details/', forum_view.details, name='details'),
    url('forum/listPosts/', forum_view.list_posts, name='list_posts'),
    url('forum/listThreads/', forum_view.list_threads, name='list_threads'),
    url('forum/listUsers/', forum_view.list_users, name='list_users'),
    #thread's
    url('thread/create/', thread_view.create, name='create'),
    url('thread/details/', thread_view.details, name='details'),
    #post's
    url('post/create/', post_view.create, name='create'),
    url('post/details/',post_view.details, name='details'),
    url('post/list/',post_view.list, name='list'),
    url('post/remove/',post_view.remove, name='remove'),
    url('post/restore/',post_view.restore, name='restore'),
    url('post/update/',post_view.update, name='update'),
    url('post/vote/',post_view.vote, name='vote'),
    #user's
    url('user/create/', user_view.create, name='create'),
    url('user/follow/', user_view.follow, name='follow'),
    url('user/listFollowers/', user_view.listFollowers, name='listFollowers'),
    url('user/listFollowing/', user_view.listFollowing, name='listFollowing'),
    url('user/listPosts/', user_view.listPosts, name='listPosts'),
    url('user/unfollow/', user_view.unfollow, name='unfollow')
]
