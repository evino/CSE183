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
    rows = db(db.contact.created_by == get_user_id()).select().as_list()
    # return dict(rows=rows, url_signer=url_signer)

    for row in rows:
        # print(row['id'])

        row["phone_numbers"] = ""

        # print(row)
        s = db(db.phones.contact_id == row['id']).select().as_list()
        # s = db(db.phones.contact_id == get_user_id()).select().as_list()
        if len(s) > 0:
            # print("db", s)
            for i in s:
                # print('i:', i['number'])
                row["phone_numbers"] += (i['number'] + '(' + i['type'] + ')' + ', ')

        # row["phone_numbers"] = s
            row["phone_numbers"] = row["phone_numbers"].rstrip(', ')
            # print('db:', row["phone_numbers"])


    return dict(rows=rows, url_signer=url_signer)


@action('add_contact', method=["GET", "POST"])
# @action.uses(db, session, auth.user, url_signer.verify(), 'add_contact.html')
@action.uses(db, session, auth.user, 'add_contact.html')
def add_contact():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)

@action('edit_contact/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session,auth.user, url_signer.verify(), 'edit_contact.html')
def edit_contact(contact_id=None):
    assert contact_id is not None
    id = db.contact[contact_id]
    if id is None:
        redirect(URL('index'))
    
    # Edit form
    form = Form(db.contact, record=id, deletable=False, csrf_session=session, formstyle=FormStyleBulma)

    if form.accepted:
        # Update already happened
        redirect(URL('index'))
    return dict(form=form)


@action('delete_contact/<contact_id:int>')
@action.uses(db, session, url_signer.verify())
def delete_contact(contact_id=None):
    assert contact_id is not None
    db(db.contact.id == contact_id).delete()
    redirect(URL('index'))



# @action('edit_phones')
# @action.uses(db, session, auth.user)
# def edit_phones(contact_id=None):
#     # assert contact_id is not None


#     # if id is None:
#     #     print("Is none")
#     #     redirect(URL('index'))

#     rows = db(db.phones.contact_id == contact_id).select().as_list()
#     return dict(rows=rows)


@action('add_phone/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify(), 'add_phone.html')
def add_phone(contact_id=None):
    assert contact_id is not None

    form = Form([Field('phone'), Field('type')], csrf_session=session,
      formstyle=FormStyleBulma)

    if form.accepted:
        # print("DEBUG:", form.vars)
        db.phones.insert(
            contact_id=contact_id,
            number=form.vars['phone'],
            type=form.vars['type']
        )
        redirect(URL('edit_phones', contact_id, signer=url_signer))

    return dict(form=form, contact_id=contact_id)



@action('edit_phones/<contact_id:int>')
@action.uses(db, session, auth.user, url_signer.verify(), 'edit_phones.html')
def edit_phones(contact_id=None):
    assert contact_id is not None


    if id is None:
        print("Is none")
        redirect(URL('index'))

    phone_rows = db(db.phones.contact_id == contact_id).select().as_list()
    contact_rows = db(db.contact.id == contact_id).select().as_list()


    return dict(phone_rows=phone_rows, contact_rows=contact_rows, contact_id=contact_id, url_signer=url_signer)


@action('edit_phone/<contact_id:int>/<phone_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify(), 'edit_phone.html')
def edit_phone(contact_id=None, phone_id=None):
    assert contact_id is not None
    assert phone_id is not None

    row_id = db.phones[phone_id]
    if row_id is None:
        redirect(URL('index'))
    

    if phone_id is None or contact_id is None:
        print("Is none")
        redirect(URL('index'))
    
    # print(db.phones.id)

    # row = db(db.phones.id == phone_id).select()  # Nubmer to edit
    # print("ROW:", row_id)
    # redirect(URL('edit_phones', contact_id, signer=url_signer))

    form = Form(db.phones, record=row_id, deletable=False, csrf_session=session, formstyle=FormStyleBulma)

    phone_rows = db(db.phones.contact_id == contact_id).select().as_list()
    contact_rows = db(db.contact.id == contact_id).select().as_list()

    # form = Form([Field('phone'), Field('type')], csrf_session=session,
    #   formstyle=FormStyleBulma)

    if form.accepted:
        # Update already happened
        # redirect(URL('index'))

        # db.phones.update(
        #     number=form.vars['phone'],
        #     type=form.vars['type']
        # )

        redirect(URL('edit_phones', contact_id, signer=url_signer))
    return dict(form=form, contact_id=contact_id, contact_rows=contact_rows, phone_rows=phone_rows, url_signer=url_signer)

    # return dict()


@action('delete_phone/<contact_id:int>/<phone_id:int>')
@action.uses(db, session, auth.user, url_signer.verify(), 'edit_phones.html')
def delete_phone(contact_id=None, phone_id=None):
    # print("IN FUNC")
    assert contact_id is not None
    assert phone_id is not None

    if phone_id is None or contact_id is None:
        print("Is none")
        redirect(URL('index'))
    
    # print(db.phones.id)

    db(db.phones.id == phone_id).delete()
    redirect(URL('edit_phones', contact_id, signer=url_signer))

    return dict()

    # return dict(id)




    # rows = db(db.contact.created_by == get_user_id()).select().as_list()

    # return dict(rows)
    # return dict(form=form)


# @action('edit_phones/<contact_id:int>', method=["GET", "POST"])
# @action.uses(db, session, auth.user, url_signer.verify(), 'edit_phones.html')
# def edit_phones(contact_id=None):
#     assert contact_id is not None

#     # id = db.phones[contact_id]
#     # if id is None:
#     #     redirect(URL('index'))

#     form = Form(db.phones, csrf_session=session, formstyle=FormStyleBulma)

#     # form = Form(db.phones, csrf_session=session, formstyle=FormStyleBulma)
#     if form.accepted:
#         redirect(URL('index'))
#     return dict(form=form)