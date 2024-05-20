class flight:
    origin = ''
    destination = ''
    leave_time = ''
    arrival_time = ''
    price = ''
    airline_name = ''

    def __init__(self, origin, destination, leave_time, arrival_time, price, airline_name):
        self.origin = origin
        self.destination = destination
        self.leave_time = leave_time
        self.arrival_time = arrival_time
        self.price = price
        self.airline_name = airline_name

    def to_dict(self):
        return {
            'origin': self.origin,
            'destination': self.destination,
            'leave_name': self.leave_time,
            'arrival_time': self.arrival_time,
            'price': self.price,
            'airline_name': self.airline_name
        }

