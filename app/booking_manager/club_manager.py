"""
Gère le chargement/sauvegarde des clubs depuis un fichier JSON,
ainsi que la recherche par email ou nom.
"""

import json
import os
import shutil
from typing import List, Optional
from app.models import Club
from .data_loader import JSONDataLoader


class ClubManager:
    """
    Gère la logique CRUD pour les clubs (lecture, sauvegarde, reset).
    """

    def __init__(self, clubs_file: str):
        """
        Initialise le manager avec un fichier JSON. Charge tout de suite dans self.clubs.
        """
        self.clubs_file = clubs_file
        self.loader = JSONDataLoader(clubs_file)
        data = self.loader.load_data()
        self.clubs: List[Club] = self._parse_clubs(data)

    def _parse_clubs(self, data: dict) -> List[Club]:
        """
        Transforme le dictionnaire en liste d'objets Club.
        """
        clubs = []
        for c in data.get("clubs", []):
            clubs.append(
                Club(
                    name=c["name"],
                    email=c["email"],
                    points=int(c["points"]),
                    id=c.get("id")
                )
            )
        return clubs

    def find_by_email(self, email: str) -> Optional[Club]:
        """
        Retourne un club dont l'email correspond, ou None si introuvable.
        """
        return next((club for club in self.clubs if club.email == email), None)

    def find_by_name(self, name: str) -> Optional[Club]:
        """
        Retourne un club dont le nom correspond, ou None si introuvable.
        """
        return next((club for club in self.clubs if club.name == name), None)

    def save_clubs(self, filepath: Optional[str] = None) -> None:
        """
        Sauvegarde la liste des clubs dans un fichier JSON (ou self.clubs_file).
        """
        if filepath is None:
            filepath = self.clubs_file
        clubs_data = {"clubs": []}
        for club in self.clubs:
            club_dict = {
                "id": club.id,
                "name": club.name,
                "email": club.email,
                "points": str(club.points)
            }
            clubs_data["clubs"].append(club_dict)
        with open(filepath, "w") as f:
            json.dump(clubs_data, f, indent=4)

    def reset_data(self, fresh_filepath: str) -> None:
        """
        Restaure les données initiales (fichier fresh_filepath)
        dans self.clubs_file, puis recharge en mémoire.
        """
        if not os.path.exists(fresh_filepath):
            raise FileNotFoundError(
                f"Fichier source introuvable : {fresh_filepath}")

        shutil.copy(fresh_filepath, self.clubs_file)
        data = self.loader.load_data()
        self.clubs = self._parse_clubs(data)
