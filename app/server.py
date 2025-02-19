# app/server.py

from flask import Flask, render_template, request, redirect, flash, url_for, session
from app.booking_manager import BookingService

app = Flask(__name__, static_folder="../static")
app.secret_key = "secret_key_xyz"

# Instanciation du service de réservation
booking_service = BookingService(
    clubs_file="data/clubs.json",
    competitions_file="data/competitions.json"
)


@app.context_processor
def inject_club_email():
    """
    Permet d'accéder à session['club_email'] dans les templates,
    afin de savoir si un utilisateur est connecté.
    """
    return dict(club_email=session.get('club_email'))


@app.route("/")
def index():
    """
    Page d'accueil.
    Si un utilisateur est connecté, on va quand même afficher index.html,
    mais le bouton "Accueil" le renverra à showSummary.
    """
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    """
    Récupère l'email du club et affiche la page de résumé (welcome.html).
    Si le club n'est pas trouvé, on redirige avec un message d'erreur.
    """
    email = request.form.get("email", "")
    club = booking_service.club_manager.find_by_email(email)
    if not club:
        flash("Email inconnu ou invalide.")
        return redirect(url_for("index"))

    # Stocker l'email en session pour signifier "connecté"
    session['club_email'] = club.email

    competitions = booking_service.competition_manager.competitions
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Affiche la page de réservation (booking.html) pour un club/compétition donné.
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
    """
    competition_name = request.form.get("competition")
    club_name = request.form.get("club")
    places_str = request.form.get("places")

    try:
        places_requested = int(places_str)
    except ValueError:
        flash("Le nombre de places est invalide.")
        return redirect(url_for("index"))

    found_competition = booking_service.competition_manager.find_by_name(
        competition_name)
    found_club = booking_service.club_manager.find_by_name(club_name)

    if not found_competition or not found_club:
        flash("Something went wrong - please try again")
        return redirect(url_for("index"))

    # Logique de réservation : on veut des messages plus précis
    if places_requested > 12:
        flash("Vous ne pouvez pas réserver plus de 12 places.")
        success = False
    else:
        success = booking_service.purchase_places(
            club_name, competition_name, places_requested)

    if success:
        flash(
            f"Great-booking complete! Vous avez réservé {places_requested} places.")
    else:
        # On vérifie pourquoi c'est False :
        # - Soit le club n'a pas assez de points
        # - Soit la compétition n'a pas assez de places (ou est passée)
        # Dans booking_service, on a un return False générique.
        # On va personnaliser le message selon la situation :
        if places_requested <= 12:  # si ce n'est pas déjà la condition "plus de 12"
            # On suppose que c'est un problème de places trop petites ou club pas assez de points
            flash("Le concours est complet (ou il ne reste pas assez de places) ou vous n'avez pas assez de points.")

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
    session.pop('club_email', None)
    return redirect(url_for("index"))
