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


def add_entity(url, regex, phone):
    """"""
    entity = UrlRequest(url=url,
                        regex=regex,
                        status='assigned',
                        phone=phone)
    entity.put()
    return {'id': entity.key().id(),
            'entry': {'url': url,
                      'regex': regex,
                      'phone': phone,
                      'status': entity.status
                     }
           }


def delete_entity(id):
    """Givin a id, delete an entity."""
    thing = UrlRequest.get_by_id(id)
    thing.delete()


def delete_all():
    """Reset the database."""
    db.delete(UrlRequest.all())


def retrieve_by_id(id):
    """"""
    thing = UrlRequest.get_by_id(id)
    return {id: {'url': thing.url,
                 'regex': thing.regex,
                 'status': thing.status,
                 'ctime': thing.ctime,
                 'mtime': thing.mtime
                 }
            }


def retrieve_all():
    """Retrieve all the row stored in database.
    
    :return info: dict, key: id, value: dict
    """
    info = {}
    entities = UrlRequest.all()
    for entity in entities:
        id = entity.key().id()
        thing = UrlRequest.get_by_id(id)
        info[id] = {'url': thing.url,
                    'regex': thing.regex,
                    'status': thing.status,
                    'ctime': thing.ctime,
                    'mtime': thing.mtime,
                    'phone': thing.phone
                    }
    return info


def update_entity(id, url=None, regex=None, phone=None, status=None):
    """Given a id, update this entity"""
    thing = UrlRequest.get_by_id(id)
    if not (url or regex or phone or status):
        return
    if url:
        thing.url = url
    if regex:
        thing.regex = regex
    if phone:
        thing.phone = phone
    if status:
        thing.status = status
    thing.put()
    return {'id': thing.key().id(),
            'entry': {'url': thing.url,
                      'regex': thing.regex,
                      'phone': thing.phone,
                      'status': thing.status
                      }
            }


def update_failed(id):
    """If a job is failed, update the entity status to failed."""
    thing = UrlRequest.get_by_id(id)
    thing.status='failed'
    thing.put()
    return thing.key().id()


def update_finished(id):
    """If a job is finished, update the entity status to finished."""
    thing = UrlRequest.get_by_id(id)
    thing.status='finished'
    thing.put()
    return thing.key().id()
