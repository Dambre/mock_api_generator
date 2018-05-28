import random

from generator import Generate
from .validators.messages import messages
from utils import json_validate


class GenericView(object):
    response_key = ''

    def __init__(self, json):
        self._json = json
        self._id = json['msgId']
        self._messages = messages[self.id]

    @property
    def json(self):
        return self._json

    @property
    def id(self):
        return self._id

    @property
    def messages(self):
        return self._messages

    @property
    def response(self):
        data = Generate().get_data(self.messages['response'])
        data.update({'msgId': self.messages['responseMsgId']})
        return data

    def get_response(self):
        valid, err = json_validate(
            self.json, self.messages['request'])

        if not valid:
            return err
        return self.response


class BookRide(GenericView):
    @property
    def response(self):
        return {
            'msgId': messages[self.id]['responseMsgId'],
            'rideId': self.json['rideId'],
            'carId': self.json['carId'],
        }


class RegisterUser(GenericView):
    @property
    def response(self):
        return {"msgId": self.id, "userId": random.randint(0, 99)}
