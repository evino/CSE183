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
from .models import get_username, get_user_id

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
    )

@action("get_users")
@action.uses(db, auth.user)
def get_users():
    # Implement.

    # q = request.params.get('q')
    # results = [q + 'str']
    # return dict(results=results)

    # print('In get users!')
    rows = db(db.auth_user).select().as_list()
    return dict(rows=rows)

@action("get_following")
@action.uses(db, auth.user)
def get_following():
    # print(get_user_id())
    user_id = get_user_id()
    following = db(db.follow.follower_id == user_id).select().as_list()
    print('db:', following)
    return dict(following=following)


@action("set_follow", method="POST")
@action.uses(db, auth.user, url_signer.verify())
# def set_follow(username=None, follower=None):
def set_follow():
    # assert username is not None
    # assert follower is not None

    print('Controller called')

    req = request.json['id']
    print('The JSON:', req)
    print(auth.user)

    # req = request.json.get.id
    # print(req)
    db.follow.insert(following_id=req)

    # username = db.followers[username]
    # follower = db.followers[follower]

    # print(username)
    # Implement. 
    # Use request.json.get.id to get ID's insert into follower db
    return "ok"

@action("set_unfollow", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def set_unfollow():
    # assert follower_id is not None
    # assert following_id is not None


    print(request.json['id'])

    db(db.follow.follower_id == get_user_id() and db.follow.following_id == request.json['id']).delete()
    return "ok"

@action("search")
@action.uses(db, auth.user, url_signer.verify())
def search():
    print("SEARCH CONTROLLER CALLED")
    q = request.params.get("q")
    print('Q:', q)
    results = db(db.auth_user).select().as_list()
    return dict(results=results)


@action("post_meow", method="POST")
@action.uses(db, auth.user, url_signer.verify())
def post_meow():
    print('post_meow controller called')
    print('request:', request)
    req = request.json['id']
    print('ID:', req)
    db.meow.insert

    return "ok"
