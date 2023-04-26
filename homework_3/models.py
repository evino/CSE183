"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'bird',
    ### TODO: define here any fields you need.
    ### To help you, here's how to declare the user_email field.
    Field('bird', requires=IS_NOT_EMPTY()),
    Field('weight', requires=IS_DECIMAL_IN_RANGE(0, 1e6)),
    Field('diet', requires=IS_NOT_EMPTY()),
    Field('habitat', requires=IS_NOT_EMPTY()),
    Field('n_sightings', default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    Field('user_email', default=get_user_email),
)

db.bird.id.writable = False
db.bird.user_email.readable = db.bird.user_email.writable = False


db.commit()
