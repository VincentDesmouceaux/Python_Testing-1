# app/booking_manager/club_manager.py

import json
from typing import List, Optional
from app.models import Club
from .data_loader import JSONDataLoader


class ClubManager:
    """
    Gère le chargement, la recherche et la sauvegarde des clubs.
    """

    def __init__(self, clubs_file: str):
        self.clubs_file = clubs_file  # Pour la sauvegarde
        loader = JSONDataLoader(clubs_file)
        data = loader.load_data()
        self.clubs: List[Club] = self._parse_clubs(data)

    def _parse_clubs(self, data: dict) -> List[Club]:
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
        return next((club for club in self.clubs if club.email == email), None)

    def find_by_name(self, name: str) -> Optional[Club]:
        return next((club for club in self.clubs if club.name == name), None)

    def save_clubs(self, filepath: Optional[str] = None) -> None:
        """
        Sauvegarde l'état actuel des clubs dans un fichier JSON.
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
