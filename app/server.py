# app/server.py

from flask import Flask, render_template, request, redirect, flash, url_for
from app.booking_manager import BookingService

app = Flask(__name__, static_folder="../static")
app.secret_key = "secret_key_xyz"

# Instanciation du service de réservation, avec les JSON par défaut.
# Si vous souhaitez utiliser des fichiers de test différents,
# configurez-les dans le code ou via des variables d'environnement.
booking_service = BookingService(
    clubs_file="data/clubs.json",
    competitions_file="data/competitions.json"
)


@app.route("/")
def index():
    """
    Page d'accueil de l'application.
    """
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    """
    Récupère l'email du club et affiche la page de résumé (welcome.html).
    Si le club n'est pas trouvé, renvoie vers la page d'accueil avec un message d'erreur.
    """
    email = request.form.get("email", "")
    club = booking_service.club_manager.find_by_email(email)
    if not club:
        flash("Email inconnu ou invalide.")
        return redirect(url_for("index"))

    # Affiche la liste des compétitions disponibles
    competitions = booking_service.competition_manager.competitions
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Affiche la page de réservation (booking.html) pour un club et une compétition donnés.
    Si le club ou la compétition n'existe pas, renvoie vers l'index.
    """
    found_competition = booking_service.competition_manager.find_by_name(
        competition)
    found_club = booking_service.club_manager.find_by_name(club)
    if not found_competition or not found_club:
        flash("Something went wrong - please try again")
        return redirect(url_for("index"))

    return render_template("booking.html", club=found_club, competition=found_competition)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    """
    Tente d'acheter 'places' places pour un club et une compétition.
    - Si la réservation réussit, on affiche 'Great-booking complete!'
    - Sinon, on affiche 'Impossible de réserver...'
    """
    competition_name = request.form.get("competition")
    club_name = request.form.get("club")
    places_str = request.form.get("places")

    try:
        places_requested = int(places_str)
    except ValueError:
        flash("Le nombre de places est invalide.")
        return redirect(url_for("index"))

    # Vérification de l'existence du club et de la compétition
    found_competition = booking_service.competition_manager.find_by_name(
        competition_name)
    found_club = booking_service.club_manager.find_by_name(club_name)
    if not found_competition or not found_club:
        flash("Something went wrong - please try again")
        return redirect(url_for("index"))

    # Appel à la logique métier
    success = booking_service.purchase_places(
        club_name, competition_name, places_requested)
    if success:
        flash("Great-booking complete!")
    else:
        flash("Impossible de réserver ces places (Règle non respectée).")

    # Recharger les données du club et de la compétition (après mise à jour)
    updated_club = booking_service.club_manager.find_by_name(club_name)
    competitions = booking_service.competition_manager.competitions

    return render_template("welcome.html", club=updated_club, competitions=competitions)


@app.route("/clubsPoints")
def clubs_points():
    """
    Affiche la liste des clubs et leurs points disponibles.
    Page publique, sans besoin de login.
    """
    clubs = booking_service.club_manager.clubs
    return render_template("clubs_points.html", clubs=clubs)


@app.route("/logout")
def logout():
    """
    Déconnecte le club (retour à l'accueil).
    """
    return redirect(url_for("index"))
