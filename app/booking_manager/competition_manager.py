# app/booking_manager/competition_manager.py

import json
from typing import List, Optional
from app.models import Competition
from .data_loader import JSONDataLoader


class CompetitionManager:
    """
    Gère le chargement, la recherche et la sauvegarde des compétitions.
    """

    def __init__(self, competitions_file: str):
        self.competitions_file = competitions_file  # Pour la sauvegarde
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

    def save_competitions(self, filepath: Optional[str] = None) -> None:
        """
        Sauvegarde l'état actuel des compétitions dans un fichier JSON.
        """
        if filepath is None:
            filepath = self.competitions_file
        competitions_data = {"competitions": []}
        for comp in self.competitions:
            comp_dict = {
                "name": comp.name,
                "date": comp.date,
                "numberOfPlaces": str(comp.number_of_places)
            }
            competitions_data["competitions"].append(comp_dict)
        with open(filepath, "w") as f:
            json.dump(competitions_data, f, indent=4)
