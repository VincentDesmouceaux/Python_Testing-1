"""
Module contenant la classe JSONDataLoader,
permettant de charger un fichier JSON et d'en retourner le contenu.
"""

import json
import os
from typing import Any


class JSONDataLoader:
    """
    Classe générique pour charger des données depuis un fichier JSON.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath  # Chemin vers le fichier JSON

    def load_data(self) -> Any:
        """
        Lit le fichier JSON et renvoie son contenu sous forme de dictionnaire.
        Lève FileNotFoundError si le fichier n'existe pas.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Fichier introuvable : {self.filepath}")
        with open(self.filepath, "r") as f:
            data = json.load(f)
        return data
