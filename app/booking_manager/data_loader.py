# app/booking_manager/data_loader.py

import json
import os
from typing import Any


class JSONDataLoader:
    """
    Classe générique pour charger des données depuis un fichier JSON.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_data(self) -> Any:
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Fichier introuvable : {self.filepath}")
        with open(self.filepath, "r") as f:
            data = json.load(f)
        return data
