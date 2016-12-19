from django.conf.urls import url

from . import user_view
from . import forum_view
from . import thread_view
from . import post_view
from . import general

"""
/*
CREATE TABLE Followers (
email1 VARCHAR(255) NOT NULL,
email1 VARCHAR(255) NOT NULL,
Primary key (email1, email2)
)
*/
/*
CREATE TABLE Subscriptions (
email VARCHAR(255) NOT NULL,
tid integer NOT NULL,
Primary key (email, tid)
);
*/
/*
CREATE TABLE User(
	about text,
	email VARCHAR(255) unique,
	id INT auto_increment primary key,
	isAnonymous bool,
	name varchar(1024),
	username varchar(1024)
);
*/
/*
CREATE TABLE Post(
	date datetime,
	forum varchar(255),
	id INT auto_increment primary key,
	isApproved bool,
	isDeleted bool,
	isEdited bool,
	isHighlighted bool,
	isSpam bool,
	message text,
	parent INT,
	thread INT,
	user varchar(255),
	likes INT,
	dislikes INT,
	points INT,
	path varchar(1024),
	sortpath varchar(1024)
);
*/
/*
create TABLE Thread(
	date datetime,
	forum varchar(1024),
	id INT auto_increment primary key,
	isClosed bool,
	isDeleted bool,
	message text,
	slug varchar(1024),
	title varchar(1024),
	user varchar(255),
	likes INT,
	dislikes INT,
	points INT,
	posts INT
);
*/
#drop table Forum;
/*
create table Forum(
	id INT auto_increment primary key,
	name varchar(512) Unique,
	short_name varchar(512) Unique,
	user varchar(255)
);
*/"""


urlpatterns = [
    #general
    url('status/', general.status, name='status'),
    url('clear/', general.clear, name='clear'),
    #forum's
    url('forum/create/', forum_view.create, name='create'),
    url('forum/details/', forum_view.details, name='details'),
    url('forum/listPosts/', forum_view.listPosts, name='listPosts'),
    url('forum/listThreads/', forum_view.list_threads, name='list_threads'),
    url('forum/listUsers/', forum_view.list_users, name='list_users'),
    #thread's
    url('thread/create/', thread_view.create, name='create'),
    url('thread/details/', thread_view.details, name='details'),
    url('thread/close/', thread_view.close, name='close'),
    url('thread/open/', thread_view.open, name='open'),
    url('thread/remove/', thread_view.remove, name='remove'),
    url('thread/restore/', thread_view.restore, name='restore'),
    url('thread/list/', thread_view.list, name='list'),
    url('thread/listPosts/', thread_view.listPosts, name='listPosts'),
    url('thread/subscribe/', thread_view.subscribe, name='subscribe'),
    url('thread/unsubscribe/', thread_view.unsubscribe, name='unsubscribe'),
    url('thread/update/', thread_view.update, name='update'),
    url('thread/vote/', thread_view.vote, name='vote'),
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
    url('user/details/', user_view.details, name='details'),
    url('user/follow/', user_view.follow, name='follow'),
    url('user/listFollowers/', user_view.listFollowers, name='listFollowers'),
    url('user/listFollowing/', user_view.listFollowing, name='listFollowing'),
    url('user/listPosts/', user_view.listPosts, name='listPosts'),
    url('user/unfollow/', user_view.unfollow, name='unfollow'),
    url('user/updateProfile/', user_view.updateProfile, name='updateProfile')
]
