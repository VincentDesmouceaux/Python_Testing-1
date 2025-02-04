# app/booking_manager.py

import json
import os
from typing import List, Optional
from app.models import Club, Competition


class BookingManager:
    """Gère la logique de réservation : chargement des données, vérification des règles, etc."""

    def __init__(self, clubs_file: str, competitions_file: str):
        self.clubs: List[Club] = self.load_clubs(clubs_file)
        self.competitions: List[Competition] = self.load_competitions(
            competitions_file)

    @staticmethod
    def load_clubs(filepath: str) -> List[Club]:
        """Charge et retourne la liste de clubs depuis un fichier JSON."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Fichier introuvable : {filepath}")
        with open(filepath, "r") as f:
            data = json.load(f)
        clubs = []
        for c in data["clubs"]:
            clubs.append(
                Club(name=c["name"], email=c["email"], points=int(c["points"]))
            )
        return clubs

    @staticmethod
    def load_competitions(filepath: str) -> List[Competition]:
        """Charge et retourne la liste de compétitions depuis un fichier JSON."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Fichier introuvable : {filepath}")
        with open(filepath, "r") as f:
            data = json.load(f)
        competitions = []
        for c in data["competitions"]:
            competitions.append(
                Competition(
                    name=c["name"],
                    date=c["date"],
                    number_of_places=int(c["numberOfPlaces"])
                )
            )
        return competitions

    def find_club_by_email(self, email: str) -> Optional[Club]:
        return next((club for club in self.clubs if club.email == email), None)

    def find_club_by_name(self, name: str) -> Optional[Club]:
        return next((club for club in self.clubs if club.name == name), None)

    def find_competition_by_name(self, name: str) -> Optional[Competition]:
        return next((c for c in self.competitions if c.name == name), None)

    def purchase_places(self, club_name: str, competition_name: str, places_requested: int) -> bool:
        """Tente d'acheter `places_requested` places pour le `club_name` dans `competition_name`.
           Renvoie True si l’opération réussit, False sinon (règles non respectées).
        """
        club = self.find_club_by_name(club_name)
        competition = self.find_competition_by_name(competition_name)

        # Vérifications basiques
        if not club or not competition:
            return False

        # 1) Pas plus de 12 places en une seule fois
        if places_requested > 12:
            return False

        # 2) Pas plus de places que le club n'a de points
        if places_requested > club.points:
            return False

        # 3) Pas plus de places que celles disponibles dans la compétition
        if places_requested > competition.number_of_places:
            return False

        # Si tout est OK, on décrémente les places
        competition.number_of_places -= places_requested
        club.points -= places_requested
        return True
