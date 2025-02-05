from typing import List, Optional
from app.models import Competition
from .data_loader import JSONDataLoader


class CompetitionManager:
    """
    Gère le chargement et la recherche des compétitions.
    """

    def __init__(self, competitions_file: str):
        loader = JSONDataLoader(competitions_file)
        data = loader.load_data()
        self.competitions: List[Competition] = self._parse_competitions(data)

    def _parse_competitions(self, data: dict) -> List[Competition]:
        competitions = []
        for c in data.get("competitions", []):
            competitions.append(
                Competition(
                    name=c["name"],
                    date=c["date"],
                    number_of_places=int(c["numberOfPlaces"])
                )
            )
        return competitions

    def find_by_name(self, name: str) -> Optional[Competition]:
        return next((comp for comp in self.competitions if comp.name == name), None)
