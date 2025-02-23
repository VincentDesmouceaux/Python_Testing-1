"""
Module contenant les classes de base du domaine :
 - Competition : représente une compétition
 - Club : représente un club
"""


class Competition:
    """
    Représente une compétition, avec :
    - name : nom de la compétition (str)
    - date : date sous forme de chaîne (str)
    - number_of_places : nombre de places restantes (int)
    """

    def __init__(self, name, date, number_of_places):
        self.name = name
        self.date = date
        self.number_of_places = number_of_places


class Club:
    """
    Représente un club sportif, avec :
    - name : nom du club (str)
    - email : email de contact (str)
    - points : points disponibles pour réserver (int)
    - id : identifiant optionnel (str ou None)
    """

    def __init__(self, name, email, points, id=None):
        self.name = name
        self.email = email
        self.points = points
        self.id = id
