# app/models.py

class Competition:
    def __init__(self, name, date, number_of_places):
        self.name = name
        self.date = date
        self.number_of_places = number_of_places


class Club:
    def __init__(self, name, email, points, id=None):
        self.name = name
        self.email = email
        self.points = points
        self.id = id
