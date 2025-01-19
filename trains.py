
class Train:
    def __init__(self, number, departure_date, departure_time, origin, destination, seats):
        self.number = number
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.origin = origin
        self.destination = destination
        self.seats = seats

    def to_dict(self):
        return {
            "number": self.number,
            "departure_date": self.departure_date,
            "departure_time": self.departure_time,
            "origin": self.origin,
            "destination": self.destination,
            "seats": self.seats
        }

    @staticmethod
    def from_dict(data):
        return Train(
            number=data["number"],
            origin=data["origin"],
            destination=data["destination"],
            departure_date=data["departure_date"],
            departure_time=data["departure_time"],
            seats=data["seats"]
        )
