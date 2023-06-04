"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user_name():
    return auth.current_user.get('username') if auth.current_user else None

def get_user_id():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'follow',
    Field('follower_id', 'reference auth_user', default=get_user_id),
    Field('following_id', 'reference auth_user',requires=IS_NOT_EMPTY())
)

db.commit()


db.define_table(
    'meow',
    Field('author', 'reference auth_user', default=get_user_id),
    Field('uname', requires=IS_NOT_EMPTY()),
    Field('timestamp', requires=IS_NOT_EMPTY()),
    Field('content', requires=IS_NOT_EMPTY()),
)


# db(db.meow).delete()


db.commit()



# TESTING
# def add_users_for_testing(num_users):
#    # Test user names begin with "_".
#    # Counts how many users we need to add.
#    db(db.meow).delete()
#    db(db.follow).delete()
#    db(db.auth_user.username.startswith("_")).delete()
#    num_test_users = db(db.auth_user.username.startswith("_")).count()
#    num_new_users = num_users - num_test_users
#    print("Adding", num_new_users, "users.")
#    for k in range(num_test_users, num_users):
#        first_name = random.choice(FIRST_NAMES)
#        last_name = first_name = random.choice(LAST_NAMES)
#        username = "_%s%.2i" % (first_name.lower(), k)
#        user = dict(
#            username=username,
#            email=username + "@ucsc.edu",
#            first_name=first_name,
#            last_name=last_name,
#            password=username,  # To facilitate testing.
#        )
#        print("USER DICT:", user)
#        auth.register(user, send=False)
#        # Adds some content for each user.
#        ts = datetime.datetime.utcnow()
#        print('DEBUG:', username, ts)

#    db.meow.insert(author=1, timestamp=ts, content='TEST CONTENT')

    #    for n in range(3):
    #        ts -= datetime.timedelta(seconds=random.uniform(60,  1000))
    #        m = dict(
    #            author=username,
    #            timestamp = ts,
    #            content=" ".join(random.choices(list(IUP.keys()), k=20))
    #        )
    #        db.meow.insert(**m)
#    db.commit()
# TESTING




def add_users_for_testing(num_users):
    # Test user names begin with "_".
    # Counts how many users we need to add.
    db(db.auth_user.username.startswith("_")).delete()
    num_test_users = db(db.auth_user.username.startswith("_")).count()
    num_new_users = num_users - num_test_users
    print("Adding", num_new_users, "users.")
    for k in range(num_test_users, num_users):
        first_name = random.choice(FIRST_NAMES)
        last_name = first_name = random.choice(LAST_NAMES)
        username = "_%s%.2i" % (first_name.lower(), k)
        user = dict(
            username=username,
            email=username + "@ucsc.edu",
            first_name=first_name,
            last_name=last_name,
            password=username,  # To facilitate testing.
        )
        auth.register(user, send=False)

    # db.meow.insert(author=get_user_id(), timestamp=get_time(), content='TEST CONTENT')
    db.commit()
    
# Comment out this line if you are not interested. 
add_users_for_testing(5)
