"""
Gère le chargement et la sauvegarde des compétitions depuis un fichier JSON,
ainsi que la recherche par nom.
"""

import json
import os
import shutil
from typing import List, Optional
from app.models import Competition
from .data_loader import JSONDataLoader


class CompetitionManager:
    """
    Gère la logique CRUD (en lecture/sauvegarde) pour les compétitions.
    """

    def __init__(self, competitions_file: str):
        """
        Initialise le manager avec un fichier JSON spécifié (competitions_file).
        Charge immédiatement les données dans self.competitions.
        """
        self.competitions_file = competitions_file
        self.loader = JSONDataLoader(competitions_file)
        data = self.loader.load_data()
        self.competitions: List[Competition] = self._parse_competitions(data)

    def _parse_competitions(self, data: dict) -> List[Competition]:
        """
        Convertit le dictionnaire `data` (clé 'competitions')
        en une liste d'objets Competition.
        """
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
        """
        Retourne la compétition portant le nom 'name', ou None si introuvable.
        """
        return next((comp for comp in self.competitions if comp.name == name), None)

    def save_competitions(self, filepath: Optional[str] = None) -> None:
        """
        Sauvegarde les compétitions actuelles dans un fichier JSON (par défaut self.competitions_file).
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

    def reset_data(self, fresh_filepath: str) -> None:
        """
        Copie le fichier fresh_filepath (contenant l'état initial)
        vers self.competitions_file, puis recharge en mémoire.
        """
        if not os.path.exists(fresh_filepath):
            raise FileNotFoundError(
                f"Fichier source introuvable : {fresh_filepath}")

        # Écrase le fichier de travail par le fichier 'frais'
        shutil.copy(fresh_filepath, self.competitions_file)

        # Recharge en mémoire
        data = self.loader.load_data()
        self.competitions = self._parse_competitions(data)
