# Datastore API
# Author monkeyly
# Date: Nov 14 2012
import datetime

from google.appengine.ext import db
from google.appengine.api import users


class UrlRequest(db.Model):

    """The request entity."""
    url = db.StringProperty(required=True)
    regex = db.StringProperty(required=True)
    status = db.StringProperty(required=True,
                               choices=set(['assigned', 'finished', 'failed']))
    phone = db.PhoneNumberProperty(required=True)
    ctime = db.DateTimeProperty(auto_now_add=True)
    mtime = db.DateTimeProperty(auto_now=True)


def add_entity(url, regex, phone):
    """"""
    entity = UrlRequest(url=url,
                        regex=regex,
                        status='assigned',
                        phone=phone)
    entity.put()


def delete_entity(id):
    """Givin a id, delete an entity."""
    thing = UrlRequest.get_by_id(id)
    thing.delete()


def delete_all():
    """Reset the database."""
    db.delete(UrlRequest.all())


def retrieve_all():
    """Retrieve all the row stored in database.
    
    :return shit: dict, key: id, value: dict
    """
    shit = {}
    entities = UrlRequest.all()
    for entity in entities:
        id = entity.key().id()
        thing = UrlRequest.get_by_id(id)
        shit[id] = {'url': thing.url,
                    'regex': thing.regex,
                    'status': thing.status,
                    'ctime': thing.ctime,
                    'mtime': thing.mtime}
    return shit


def update_entity(id, url=None, regex=None, phone=None):
    """Given a id, update this entity"""
    thing = UrlRequest.get_by_id(id)
    if not (url or regex or phone):
        return
    if url:
        thing.url = url
    if regex:
        thing.regex = regex
    if phone:
        thing.phone = phone
    thing.put()


def update_failed(id):
    """If a job is failed, update the entity status to failed."""
    thing = UrlRequest.get_by_id(id)
    thing.status='failed'
    thing.put()


def update_finished(id):
    """If a job is finished, update the entity status to finished."""
    thing = UrlRequest.get_by_id(id)
    thing.status='finished'
    thing.put()
