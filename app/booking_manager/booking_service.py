from app.booking_manager.club_manager import ClubManager
from app.booking_manager.competition_manager import CompetitionManager


class BookingService:
    """
    Ordonne le processus de réservation en utilisant les gestionnaires de clubs et de compétitions.
    """

    def __init__(self, clubs_file: str, competitions_file: str):
        self.club_manager = ClubManager(clubs_file)
        self.competition_manager = CompetitionManager(competitions_file)

    def purchase_places(self, club_name: str, competition_name: str, places_requested: int) -> bool:
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

        competition.number_of_places -= places_requested
        club.points -= places_requested
        return True
