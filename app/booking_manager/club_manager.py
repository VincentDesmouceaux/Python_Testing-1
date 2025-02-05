from typing import List, Optional
from app.models import Club
from .data_loader import JSONDataLoader


class ClubManager:
    """
    Gère le chargement et la recherche des clubs.
    """

    def __init__(self, clubs_file: str):
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
                    points=int(c["points"])
                )
            )
        return clubs

    def find_by_email(self, email: str):
        return next((club for club in self.clubs if club.email == email), None)

    def find_by_name(self, name: str):
        return next((club for club in self.clubs if club.name == name), None)
