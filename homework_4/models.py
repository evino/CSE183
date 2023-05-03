"""
This file defines the database models
"""
import datetime

from . common import db, Field, auth
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None


def get_user_id():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

db.define_table(
    'contact',
    Field('created_by', 'reference auth_user', default=get_user_id),
    Field('first_name', requires=IS_NOT_EMPTY()),
    Field('last_name', requires=IS_NOT_EMPTY())
)

db.contact.id.writable = False

db.contact.id.readable = False

db.contact.created_by.readable = db.contact.created_by.writable = False


db.commit()
