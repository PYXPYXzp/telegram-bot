from mongoengine import (
    Document, StringField, LongField,
    DateTimeField, ReferenceField, FloatField,
    ListField, CASCADE
)

import datetime


class User(Document):
    user_id = LongField(required=True, unique=True)
    first_name = StringField(max_length=255, required=True)
    last_name =  StringField(max_length=255)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    city = ReferenceField('City')


class Chat(Document):
    chat_id = LongField(required=True, unique=True)
    user = ReferenceField('User', reverse_delete_rule=CASCADE)


class Region(Document):
    name = StringField(max_length=255, required=True)


class City(Document):
    name = StringField(max_length=255, required=True)
    code = StringField(max_length=255, required=True)
    region = ListField(ReferenceField('Region'))


class CurrencyRate(Document):
    date = DateTimeField(default=datetime.datetime.utcnow)
    currency = ReferenceField('Currency', reverse_delete_rule=CASCADE)
    bid = FloatField()
    ask = FloatField()


class Currency(Document):
    name = StringField(max_length=255, required=True)
    code = StringField(max_length=255, required=True)