
import json
import unittest
import random

import listener


class GenericTestCase(unittest.TestCase):
    def setUp(self):
        listener.app.config['TESTING'] = True
        self.app = listener.app.test_client()

    def bytes_json_to_dict(self, data):
        data = data.decode('utf8')
        return json.loads(data)


class ListenerTestCase(GenericTestCase):
    def test_get_index(self):
        assert self.app.get('/').status_code == 405

    def test_invalid_url(self):
        response = self.app.post('/random')
        assert response.status_code == 404

    def test_post_index_invalid_data(self):
        data_list = [
            {'data': json.dumps({})},
            {'data': json.dumps({'msgId': 'random'})},
            {
                'data': json.dumps({'msgId': 'msgGetPlaces'}),
                'content_type': 'application/xml',
            },
        ]
        for _data in data_list:
            response = self.app.post('/', **_data)
            data = self.bytes_json_to_dict(response.data)
            assert data.get('error') == 400

    def test_valid_data(self):
        data = {
            'data': json.dumps({"msgId": "msgGetPlaces"}),
            'content_type': 'application/json',
        }
        response = self.app.post('/', **data)
        data = self.bytes_json_to_dict(response.data)
        assert data.get('error', '') == ''


class MessagesTestCase(GenericTestCase):
    def setUp(self):
        listener.app.config['TESTING'] = True
        self.app = listener.app.test_client()

    def post(self, **params):
        return self.bytes_json_to_dict(
            self.app.post('/', content_type='application/json', **params).data)

    def get_ride_request(self):
        return self.post(data=json.dumps({
                'msgId': 'msgRideRequest',
                'userId': 123,
                'fromLocation': {'lat': 123, 'lng': 123},
                'toLocation': {'lat': 123, 'lng': 123},
                'timeBooking': '1AM',
            }))

    def book_ride(self, car_bids, ride_id, user_id):
        ride = random.choice(car_bids)
        return self.post(data=json.dumps({
                'msgId': 'msgBookRide',
                'userId': user_id,
                'rideId': ride_id,
                'carId': ride['carId'],
            }))

    def test_get_and_book_scenario(self):
        ride = self.get_ride_request()
        # import pytest; pytest.set_trace()
        car_bids = ride.get('carBids')
        if car_bids:
            ride_id = ride.get('rideId')
            user_id = ride.get('userId')
            response = self.book_ride(car_bids, ride_id, user_id)
            assert ride_id == response['rideId']
        else:
            assert car_bids == []
        # what happens when there is no rides available ?

    def test_get_me_home_scenario(self):
        '''
        basically the same as get_and_book
        '''
        pass

    def test_fetch_account_details(self):
        '''
        send request check
        '''
        pass

    # scenarios in progress
