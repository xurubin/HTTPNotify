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
                               choices=set(['assigned',
                                            'finished',
                                            'failed']))
    phone = db.PhoneNumberProperty(required=True)
    ctime = db.DateTimeProperty(auto_now_add=True)
    mtime = db.DateTimeProperty(auto_now=True)

def entity_dict(entity):
    """Convert an entity to a dict."""
    return {'id': entity.key().id()
            'url': entity.url,
            'regex': entity.regex,
            'phone': entity.phone,
            'ctime': entity.ctime,
            'mtime': entity.mtime,
            'status': entity.status}


def add_entity(url, regex, phone):
    """"""
    entity = UrlRequest(url=url,
                        regex=regex,
                        status='assigned',
                        phone=phone)
    entity.put()
    return entity_dict(entity)


def delete_entity(id):
    """Givin a id, delete an entity."""
    entity = UrlRequest.get_by_id(id)
    entity.delete()


def delete_all():
    """Reset the database."""
    db.delete(UrlRequest.all())


def retrieve_by_id(id):
    """"""
    entity = UrlRequest.get_by_id(id)
    return entity_dict(entity)


def retrieve_all():
    """Retrieve all the row stored in database.
    
    :return info: dict, key: id, value: dict
    """
    info = []
    entities = UrlRequest.all()
    for entity in entities:
        info.append(entity_dict(entity))
    return info


def update_entity(id, url=None, regex=None, phone=None, status=None):
    """Given a id, update this entity"""
    entity = UrlRequest.get_by_id(id)
    if not (url or regex or phone or status):
        return
    if url:
        entity.url = url
    if regex:
        entity.regex = regex
    if phone:
        entity.phone = phone
    if status:
        entity.status = status
    entity.put()
    return entity_dict(entity)


def update_failed(id):
    """If a job is failed, update the entity status to failed."""
    entity = UrlRequest.get_by_id(id)
    entity.status='failed'
    entity.put()
    return entity_dict(entity)


def update_finished(id):
    """If a job is finished, update the entity status to finished."""
    entity = UrlRequest.get_by_id(id)
    entity.status='finished'
    entity.put()
    return entity_dict(entity)
