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

import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner


from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url

from .models import get_user_id


url_signer = URLSigner(session)


# The auth.user below forces login.
@action('index')
@action.uses('index.html', db, auth.user, url_signer)
def index():
    # rows = db(str(db.contact.created_by) == get_user_email()).select()
    rows = db(db.contact.created_by == get_user_id()).select()
    # return dict(rows=rows, url_signer=url_signer)
    return dict(rows=rows, url_signer=url_signer)


@action('add_contact', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add_contact.html')
def add():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('edit_contact/<created_by:int>', method=["GET", "POST"])
@action.uses(db, session,auth.user, url_signer.verify(), 'edit_contact.html')
def edit_contact(created_by=None):
    assert created_by is not None
    id = db.contact[created_by]
    if id is None:
        redirect(URL('index'))
    
    # Edit form
    form = Form(db.contact, record=id, deletable=False, csrf_session=session, formstyle=FormStyleBulma)

    if form.accepted:
        # Update already happened
        redirect(URL('index'))
    return dict(form=form)


@action('del_contact/<contact_id:int>')
@action.uses(db, session, url_signer.verify())
def del_contact(contact_id=None):
    assert contact_id is not None
    db(db.contact.id == contact_id).delete()
    redirect(URL('index'))

