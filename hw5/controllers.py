"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import datetime
import random

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_name, get_user_id, get_time

url_signer = URLSigner(session)

# Some constants.
MAX_RETURNED_USERS = 20 # Our searches do not return more than 20 users.
MAX_RESULTS = 20 # Maximum number of returned meows. 

@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    return dict(
        # COMPLETE: return here any signed URLs you need.
        search_url = URL('search', signer=url_signer),
        get_users_url = URL('get_users', signer=url_signer),
        get_following_url = URL('get_following', signer=url_signer),
        set_follow_url=URL('set_follow', signer=url_signer),
        set_unfollow_url=URL('set_unfollow', signer=url_signer),
        post_meow_url=URL('post_meow', signer=url_signer),
        get_posts_url=URL('get_posts', signer=url_signer),
    )

@action("get_users")
@action.uses(db, auth.user, url_signer.verify())
def get_users():
    rows = db(db.auth_user).select().as_list()
    return dict(rows=rows)

@action("get_following")
@action.uses(db, auth.user, url_signer.verify())
def get_following():
    user_id = get_user_id()
    following = db(db.follow.follower_id == user_id).select().as_list()
    return dict(following=following)


@action("set_follow", method="POST")
@action.uses(db, auth.user, url_signer.verify())
# def set_follow(username=None, follower=None):
def set_follow():
    req = request.json['id']
    db.follow.insert(following_id=req)

    # Implement. 
    # Use request.json.get.id to get ID's insert into follower db
    return "ok"

@action("set_unfollow", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def set_unfollow():
    db(db.follow.follower_id == get_user_id() and db.follow.following_id == request.json['id']).delete()
    return "ok"

@action("search")
@action.uses(db, auth.user, url_signer.verify())
def search():
    results = db(db.auth_user).select().as_list()
    return dict(results=results)


@action("post_meow", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def post_meow():
    post_content = request.json['post_content']
    uname = get_user_name()
    db.meow.insert(author=get_user_id(), uname=uname, timestamp=get_time(), content=post_content)
    return "ok"


@action("get_posts")
@action.uses(db, auth.user, url_signer.verify())
def get_posts():
    feed_type = request.params['feed_type']
    meows = []
    following_list = db(db.follow.follower_id == get_user_id()).select().as_list()

    if (feed_type == "Your Feed" or feed_type == "Default"):
        if (len(following_list) == 0):
            meows = db(db.meow).select().as_list()
        else:
            for following in following_list:
                post = db(db.meow.author == following['following_id']).select().as_list()
                if len(post) > 0:
                    meows += post
    elif (feed_type == "Your Meows"):
        print("your meows")
        post = db(db.meow.author == get_user_id()).select().as_list()
        meows += post
    elif (feed_type == "Recent Meows"):
        meows = db(db.meow).select().as_list()

    # TODO: Get meows only from person that you follow
    # Need following_id. ensure following.
    # elif (feed_type == "Person")

    # print('post controller calls')
    # rows = db(db.meow).select().as_list()

    meows = meows[-20:]  # Get up to the last 20 Meows in list
    meows.reverse()  # Reverse to get most recent at top

    # for meow in meows:
    #     print("DEBUG:", meow)
    return dict(meows=meows)
