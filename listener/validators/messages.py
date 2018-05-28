"""
In this way we can describe json objects and validators
There are several types of objects. In python jsonscehma objects are described as:
* String - 'string'
* Integer - 'integer'
* Float - 'number'
* List - 'array'
* Dict - 'object'

You can validate your message by running
`py.test -v generator`
"""


# ***********************************************************************************
# Main flow (basic) assume driver is auto-bidding.
# ***********************************************************************************

# CP->S
msg_request_ride_basket = {
    "title": "Request to get the basket of driver willing to do the requested ride/journey",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "fromLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
                "address": {"type": "string"},
            },
            "required": ["lat", "lng"],
        },
        "toLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
                "address": {"type": "string"},
            },
            "required": ["lat", "lng"],
        },
        "timeBooking": {"type": "string"},
        "timePickup": {"type": "string"},
        "passengers": {"type": "integer", "minimum": 1, "maximum": 10},
        "luggage": {"type": "integer", "minimum": 1, "maximum": 10},
        "acceptsCash": {"type": "boolean"},
        "price": {"type": "number"},
    },
    "required": [
        "msgId",
        "userId",
        "fromLocation",
        "toLocation",
        "timeBooking",
    ],
}


# S->CP
# the response for get me Home and get Ride,
# this will likely need to be split into a series of messages
# note - the total cars asked is all cars asked, some might not bid and some might bid later via msg_ride_basket_supplimental
msg_ride_basket_response = {
    "title": "Get ride response schema for basket",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "totalCarsAsked": {"type": "integer",  "minimum": 0, "maximum": 12},
        "carBids": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "carId": {"type": "string"},
                    "name": {"type": "string"},
                    "price": {"type": "number", "multipleOf": 0.05},
                    "rating": {"type": "integer", "minimum": 1, "maximum": 5},
                    "details": {"type": "string"},
                    "vehicleType": {"type": "string"},
                    "timePickup": {"type": "integer", "minimum": 1, "maximum": 90},
                    "acceptsCash": {"type": "boolean"},
                    "location": {
                        "type": "object",
                        "properties": {
                            "lat": {"type": "number"},
                            "lng": {"type": "number"},
                        },
                        "required": ["lat", "lng"],
                    },
                },
                "required": [
                    "carId", "name", "price", "rating", "details", "vehicleType", "timePickup", "acceptsCash", "location"
                ],
            },
        },
    },
    "required": ["msgId", "userId", "rideId", "carBids"],
}

# S->CP
# additional ride basket driver/car items that
# arrive later as the drivers are manually bidding
msg_ride_basket_supplimental = {
    "title": "Get ride response additional basket items",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "name": {"type": "string"},
        "price": {"type": "number", "multipleOf": 0.05},
        "rating": {"type": "integer", "minimum": 1, "maximum": 5},
        "details": {"type": "string"},
        "vehicleType": {"type": "string"},
        "timePickup": {"type": "integer", "minimum": 1, "maximum": 90},
        "acceptsCash": {"type": "boolean"},
    },
    "required": [
        "msgId", "userId", "rideId",
        "carId", "name", "price", "details", "rating", "vehicleType", "timePickup"
    ],
}


# CP->S
msg_user_abandans_basket = {
    "title": "Confirmation from the app that the passenger has abandaned the basket",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
    },
    "required": ["msgId", "userId", "rideId"],
}

# S->CP
msg_basket_timed_out = {
    "title": "Push from the server that the basket has timed-out and is abandaned",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "rideId": {"type": "string"},
    },
    "required": ["msgId", "rideId"],
}

# S->CP
msg_remove_driver_from_basket = {
    "title": "Push from the server that a driver is no longer available in basket",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
    },
    "required": ["msgId", "rideId"],
}


# CP->S
msg_book_ride = {
    "title": "Confirmation from the user that they want to book a car in the ride basket",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "carId": {"type": "string"},
        "fromLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
                "address": {"type": "string"},
            },
            "required": ["lat", "lng"],
        },
        "toLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
                "address": {"type": "string"},
            },
            "required": ["lat", "lng"],
        },
    },
    "required": ["msgId", "userId", "carId", "fromLocation", "toLocation"],
}

# S->CP
msg_book_ride_success = {
    "title": "Selected car will pickup passenger",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "rideId": {"type": "string"},
    },
    "required": ["msgId", "rideId"],
}

# S->CP
msg_book_ride_failure = {
    "title": "the car has been booked by another",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": ["msgId", "rideId", "carId"],
}


# ***********************************************************************************
# Common App messages.
# ***********************************************************************************
# note that in V2 server user-management will move over to AWS Cognito
# therefore there will be no registration and login messages of our own
msg_register_user = {
    "title": "Register user request schema",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "username": {"type": "string"},
        "phone": {"type": "string"},
        "email": {"type": "string"},
        "address": {
            "type": "object",
            "properties": {
                "houseNameNumber": {"type": "string"},
                "streetName": {"type": "string"},
                "townCity": {"type": "string"},
                "postcode": {"type": "string"},
                "country": {"type": "string"},
            },
        },
    },
}


msg_register_user_response = {
    "title": "Register user response schema",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
    },
    "required": ["msgId", "userId"],
}


# ************************************************************************************
# Passenger App messages.
# ************************************************************************************

# the places lists will only be updated if they have changed
msg_check_places = {
    "title": "Check places schema",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "placeType": {"type": "string"},
        "placeHash": {"type": "string"},  # a base 64 encoding of hash
        "location": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
        },
    },
}


msg_places_nochange_response = {
    "title": "Get places list schema",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "placeType": {"type": "string"},
    },
}

# note you only get the places update if
# the app's hash of places is out of date
msg_places_changed_response = {
    "title": "Get places list schema",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "placeType": {"type": "string"},
        "placeHash": {"type": "string"},  # a base 64 encoding of hash
        "places": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "location": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "number"},
                        "lng": {"type": "number"},
                    },
                },
                "info": {"type": "string"},
                "image": {"type": "string"},
            },
        },
    },
}

msg_add_place = {
    "title": "User to add a place to their favourites",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "placeType": {"type": "string"},
        "name": {"type": "string"},
        "location": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
        },
        "info": {"type": "string"},
    },
    "required": [
        "msgId",
        "userId",
        "placeType",
        "name",
        "location",
    ],
}

msg_add_place_response = {
    "title": "User to add a place to their favourites",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "name": {"type": "string"},
        "placeId": {"type": "string"},
    },
    "required": [
        "msgId",
        "name",
        "placeId",
    ],
}

msg_delete_place = {
    "title": "User to add a place to their favourites",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "placeId": {"type": "string"},
    },
    "required": [
        "msgId",
        "userId",
        "placeId",
    ],
}

msg_delete_place_response = {
    "title": "User to add a place to their favourites",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
    },
    "required": [
        "msgId",
    ],
}


msg_get_me_home = {
    "title": "Get me home request schema",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "fromLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
        "timeBooking": {"type": "string"},
        "timePickup": {"type": "string"},
    },
    "required": [
        "msgId",
        "userId",
        "fromLocation",
        "timeBooking",
    ],
}


msg_cancel_ride = {
    "title": "Cancellation request from passenger for ride already booked",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
    },
    "required": ["msgId", "userId", "rideId", "carId"],
}

# todo - penality fees
msg_cancel_ride_response = {
    "title": "Ride confirmation with selected car",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
    },
    "required": ["msgId", "rideId", "carId"],
}

# change time, pick-up or destination or more than 1
msg_change_future_ride_details = {
    "title": "Change the details of a booked ride",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "fromLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
        "toLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
        "timeBooking": {"type": "string"},
        "timePickup": {"type": "string"},
        "passengers": {"type": "integer", "minimum": 1, "maximum": 10},
        "luggage": {"type": "integer", "minimum": 1, "maximum": 10},
    },
    "required": ["msgId", "userId", "rideId", "carId", "timeBooking"],
}


msg_change_current_ride_details = {
    "title": "Change the destination or the request-time on a ride that's already booked",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "toLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
        "timePickup": {"type": "string"},
    },
    "required": ["msgId", "userId", "rideId", "carId"],
}

# note there will be repeated responses to this request
msg_subscribe_to_car = {
    "title": "Subscribe to streamed updates on the position of the car",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
    },
    "required": ["msgId", "userId", "rideId", "carId"],
}

msg_car_subscription_update = {
    "title": "updates of driver car position for interested passenger",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "location": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
    },
    "required": ["msgId", "userId", "rideId", "carId", "location"],
}

# pushed to Passenger app once Driver has told server they have arrived
msg_confirm_youve_been_pickedup = {
    "title": "Pushed to passenger to confirm that the driver has arrived at pick-up",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "mobile_num": {"type": "string"},  # mobile number of driver
    },
    "required": ["msgId", "userId", "rideId", "carId", "mobile_num"],
}

msg_confirm_pickedup_response = {
    "title": "Subscribe to streamed updates on the position of the car",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "pickedUp": {"type": "boolean"},
    },
    "required": ["msgId", "userId", "rideId", "carId", "pickedUp"],
}


# pushed to Passenger app once Driver has told server they have dropped-off passenger
msg_confirm_youve_been_droppedoff = {
    "title": "Pushed to passenger to confirm that the driver claims they've been dropped off",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "ratingsItems": {
            "type": "object",
            "properties": {
                "display": {"type": "string"},
                "jsonKey": {"type": "string"},
            },
            "required": ["lat", "lng"],
        }
    },
    "required": ["msgId", "userId", "rideId", "carId"],
}

# at the end of the journey the passenger gets to rate the ride
# the rate ride keys are supplied to app dynamically by server so can not be represented on MockServer
msg_rate_ride = {
    "title": "Rate the driver at journey completion",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        #"rateXYZ": {"type": "integer", "minimum": 1, "maximum": 5},
    },
    "required": ["msgId", "userId", "rideId", "carId"],
}

msg_rate_ride_response = {
    "title": "Acknowledgement of user rating of car and journey",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
    },
    "required": ["msgId"],
}


msg_fetch_account_details = {
    "title": "Request for user account details - the previous journeys made and the available credit",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
    },
    "required": ["msgId", "userId"],
}

msg_account_details_response = {
    "title": "integer of journeys made available credit",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "credit": {"type": "number", "multipleOf": 0.01},
        "journeysMade": {"type": "string"},
    },
    "required": ["msgId", "credit", "journeysMade"],
}

msg_fetch_booking_history = {
    "title": "Request for booking history",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
    },
    "required": ["msgId", "userId"],
}

msg_booking_history_response = {
    "title": "List of total Bookings and Available credit",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "bookingsMade": {"type": "integer"},
        "credit": {"type": "number", "multipleOf": 0.01},
        "journeysMade": {"type": "string"},
        "bookings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "carId": {"type": "string"},
                    "carName": {"type": "string"},
                    "price": {"type": "number", "multipleOf": 0.01},
                    "details": {"type": "string"},
                    "rating": {"type": "integer", "minimum": 1, "maximum": 5},
                    "fromLocation": {
                        "type": "object",
                        "properties": {
                            "lat": {"type": "number"},
                            "lng": {"type": "number"},
                        },
                        "required": ["lat", "lng"],
                    },
                    "toLocation": {
                        "type": "object",
                        "properties": {
                            "lat": {"type": "number"},
                            "lng": {"type": "number"},
                        },
                        "required": ["lat", "lng"],
                    },
                    "timeBooking": {"type": "string"},
                },
                "required": ["carId", "carName", "price", "rating"],
            },
        },
    },
    "required": ["msgId", "credit", "journeysMade"],
}


# todo
msg_use_promo_code = {
    "title": "Use a promotion code",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "code": {"type": "string"},
    },
    "required": [
        "msgId",
        "code"
    ],
}


# *******************************************************************************
# Other Driver App messages.
# *******************************************************************************
# @todo
# the first message sent to the Driver app should sync all driver app info such as coverage
# with what's in the server.


# CD->S
msg_set_auto_bid_parameters = {
    "title": "Details of a Passenger Ride Request for a Driver to bid on",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "carId": {"type": "string"},
        "ratePerKM": {"type": "number"},
        "callOutCharge": {"type": "number"},
    },
    "required": [
        "msgId",
        "carId",
        "ratePerKM",
        "callOutCharge"
    ]
}

# S->CD
msg_set_auto_bid_response = {
    "title": "Details of a Passenger Ride Request for a Driver to bid on",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
    },
}



# S->CD
# Pushed from server to driver (or queued until next msg_driver_position
# (only pushed to drivers who have set to manually bid on work)
msg_ride_for_manual_bid = {
    "title": "Details of a Passenger Ride Request for a Driver to bid on",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "rideId": {"type": "string"},
        "fromLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
        "toLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
        "timeBooking": {"type": "string"},
        "timePickup": {"type": "string"},
        "passengers": {"type": "integer", "minimum": 1, "maximum": 10},
        "luggage": {"type": "integer", "minimum": 1, "maximum": 10},
    },
    "required": [
        "msgId",
        "fromLocation",
        "toLocation",
        "timeBooking"
    ]
}

# CD->S
# this is only sent from Drivers who have configured themselves for manual bidding
msg_manual_bid_on_ride = {
    "title": "A manual bid from a Driver for a pushed Passenger Ride Request",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "rideId": {"type": "string"},
        "carId": {"type": "string"},
        "price": {"type": "number", "multipleOf": 0.01},
    },
    "required": [
        "msgId",
        "price"
    ],
}

# S->CD, a push confirmation to a Driver that they have won a Passenger ride.
# This will be sent to Drivers for both manual and auto bids.
msg_ride_confirmation_to_driver = {
    "title": "Send the Driver the passenger name and phone number",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "phone": {"type": "integer"},
        "name": {"type": "string"},
        "fromLocation": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
        "timePickup": {"type": "string"},
        "passengers": {"type": "integer", "minimum": 1, "maximum": 10},
        "luggage": {"type": "integer", "minimum": 1, "maximum": 10},
    },
    "required": [
        "msgId", "phone", "name", "fromLocation", "timePickup",
    ],
}

# CD->S
# From Driver app when Driver has picked up passenger
# todo enumeration of pick-up and drop-off options/eventualities
msg_driver_confirms_arrival = {
    "title": "Driver confirms at collection or drop-off location",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "carId": {"type": "string"},
        # TBD on below
        "locationType": {"type": "number", "minimum": 1, "maximum": 2},  # actually an enumeration: pick-up, drop-off,
    },
    "required": [
        "msgId",
        "carId",
        "locationType"
    ],
}

# S->CD
# for courier/man & van apps this could include special drop-off instructions
msg_driver_confirms_arrival_response = {
    "title": "Driver confirm drop-off location response",
    "type": "object",
    "properties": {
    }
}

# CD->S
msg_driver_position_update = {
    "title": "Update of the current position of an active Driver",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "carId": {"type": "string"},
        "location": {
            "type": "object",
            "properties": {
                "lat": {"type": "number"},
                "lng": {"type": "number"},
            },
            "required": ["lat", "lng"],
        },
    },
    "required": [
        "msgId",
        "userId",
        "carId",
        "location"
    ],
}

# todo
msg_update_shift_rota = {
    "title": "Driver change shift patterns and holidays",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "carId": {"type": "string"},
    },
    "required": [
        "msgId",
        "userId",
        "carId",
    ],
}

# todo
msg_update_shift_rota_response = {
    "title": "Driver change shift patterns and holidays",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
    },
    "required": [
        "msgId",
    ],
}

msg_update_coverage = {
    "title": "Driver change to coverage (range for jobs)",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
        "userId": {"type": "integer"},
        "carId": {"type": "string"},
        "coverage": {"type": "number", "multipleOf": 0.5, "minimum": 0.5, "maximum": 5},
    },
    "required": [
        "msgId",
        "userId",
        "carId",
        "coverage",
    ],
}


# Many messages are push only without a response,
# this is here purely to enable the MockServer to send a response that the app will ignore
msg_dummy = {
    "title": "Dummy MockServer Only",
    "type": "object",
    "properties": {
        "msgId": {"type": "string"},
    },
    "required": [
        "msgId",
    ],
}




# ******************************************************


messages = {
    "msgRideRequest": {
        "request": msg_request_ride_basket,
        "response": msg_ride_basket_response,
        "responseMsgId": "msgRideBasket",
    },
    "msgGetMeHome": {
        "request": msg_get_me_home,
        "response": msg_ride_basket_response,
        "responseMsgId": "msgRideBasket",
    },
    "msgRideForManualBid": {
        "request": msg_ride_for_manual_bid,
        "response": msg_manual_bid_on_ride,
        "responseMsgId": "msgManualBidOnRide",
    },
    "msgBookRide": {
        "request": msg_book_ride,
        "response": msg_book_ride_success,
        "responseMsgId": "msgBookRideResponse",
    },
    "msgDriverConfirmsArrival": {
        "request": msg_driver_confirms_arrival,
        "response": msg_driver_confirms_arrival_response,
        "responseMsgId": "msgDriverConfirmsArrivalResponse",
    },
    "msgFetchAccountDetails": {
        "request": msg_fetch_account_details,
        "response": msg_account_details_response,
        "responseMsgId": "msgAccountDetails",
    },
    "msgFetchBookings": {
        "request": msg_fetch_booking_history,
        "response": msg_booking_history_response,
        "responseMsgId": "msgBookingHistory",
    },
    "msgGetPlaces": {
        "request": msg_check_places,
        "response": msg_places_changed_response,
        "responseMsgId": "msgPlacesChangedResponse",
    },
    "msgRegisterUser": {
        "request": msg_register_user,
        "response": msg_register_user_response,
        "responseMsgId": "msgRegisterUserResponse",
    },
    "msgUpdateShiftRota": {
        "request": msg_update_shift_rota,
        "response": msg_update_shift_rota_response,
        "responseMsgId": "msgUpdateShiftRotaResponse",
    },
    "msgSubscribeToCar": {
        "request": msg_subscribe_to_car,
        "response": msg_car_subscription_update,
        "responseMsgId": "msgCarSubscriptionUpdate",
    },
    "msgDriverPositionUpdate": {
        "request": msg_driver_position_update,
        "response": msg_dummy,
        "responseMsgId": "msgDummy",
    },
}
