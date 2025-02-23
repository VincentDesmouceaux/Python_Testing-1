"""
Module central qui orchestre la réservation de places
en s'appuyant sur ClubManager et CompetitionManager.
"""

from app.booking_manager.club_manager import ClubManager
from app.booking_manager.competition_manager import CompetitionManager


class BookingService:
    """
    Ordonne le processus d'achat de places :
    - Lit/écrit via ClubManager et CompetitionManager
    - Vérifie les règles (max 12 places, points dispo, etc.).
    """

    def __init__(self, clubs_file: str, competitions_file: str):
        self.club_manager = ClubManager(clubs_file)
        self.competition_manager = CompetitionManager(competitions_file)

    def purchase_places(self, club_name: str, competition_name: str, places_requested: int) -> bool:
        """
        Tente d'acheter 'places_requested' places pour le club 'club_name' 
        dans la compétition 'competition_name'.

        Règles :
        - Le club et la compétition doivent exister
        - Max 12 places à la fois
        - Le club doit avoir assez de points
        - La compétition doit avoir assez de places
        Si tout est bon, on décrémente et on sauvegarde. Sinon, False.
        """
        club = self.club_manager.find_by_name(club_name)
        competition = self.competition_manager.find_by_name(competition_name)

        if not club or not competition:
            return False
        if places_requested > 12:
            return False
        if places_requested > club.points:
            return False
        if places_requested > competition.number_of_places:
            return False

        # Mise à jour
        competition.number_of_places -= places_requested
        club.points -= places_requested

        # Sauvegarde dans les fichiers JSON
        self.club_manager.save_clubs()
        self.competition_manager.save_competitions()

        return True
