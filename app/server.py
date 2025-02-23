"""
Ce module définit la logique de routes Flask pour l'application GUDLFT.

Il utilise une instance de `BookingService` pour gérer l'achat de places,
et s'appuie sur des templates Jinja2 pour l'affichage (welcome.html, booking.html, etc.).
"""

from flask import Flask, render_template, request, redirect, flash, url_for, session
from app.booking_manager import BookingService

# Instancie l'application Flask
# `static_folder` pointe vers ../static pour le CSS, etc.
app = Flask(__name__, static_folder="../static")
# Clé secrète pour les messages flash et la session
app.secret_key = "secret_key_xyz"

# Crée le service de réservation, en lisant les fichiers JSON par défaut.
booking_service = BookingService(
    clubs_file="data/clubs.json",
    competitions_file="data/competitions.json"
)


@app.context_processor
def inject_club_email():
    """
    Ajoute à chaque template une variable `club_email` correspondant
    à la session en cours, afin de savoir si un utilisateur est connecté.
    """
    return dict(club_email=session.get('club_email'))


@app.route("/")
def index():
    """
    Page d'accueil du site. Affiche un formulaire de connexion
    (voir template index.html).
    """
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    """
    Reçoit l'email d'un club (depuis index.html) en POST.
    Si l'email existe, on stocke `club_email` en session, puis on affiche
    la page `welcome.html` avec la liste des compétitions.
    Sinon, on redirige vers l'index en flashant un message d'erreur.
    """
    email = request.form.get("email", "")
    club = booking_service.club_manager.find_by_email(email)
    if not club:
        flash("Email inconnu ou invalide.")
        return redirect(url_for("index"))

    session['club_email'] = club.email
    competitions = booking_service.competition_manager.competitions
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Affiche la page de réservation (booking.html) pour un club et une compétition donnés.
    - Si le club ou la compétition n'existent pas, on renvoie un message d'erreur + redirection.
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
    Tente d'acheter 'places' places pour le club donné dans une compétition.
    - Récupère `competition`, `club`, `places` depuis le formulaire.
    - Convertit `places` en int (sinon ValueError => flash + redirection).
    - Si la réservation réussit : flash "Great-booking complete!"
    - Sinon : flash un message d'erreur selon la situation.
    - Redirige vers `show_purchase_result(<club_name>)`.
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
        flash("Something went wrong - please try again.")
        return redirect(url_for("index"))

    # Logique métier : max 12 places, points dispo, places disponibles, etc.
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
        # Si places_requested <= 12 mais échec => pas assez de points ou places
        if places_requested <= 12:
            flash("Le concours est complet ou vous n'avez pas assez de points.")

    return redirect(url_for("show_purchase_result", club_name=club_name))


@app.route("/showPurchaseResult/<club_name>")
def show_purchase_result(club_name):
    """
    Affiche la page `welcome.html` après la réservation, 
    en relisant les données du club (mis à jour) et la liste des compétitions.
    Le message flash (succès ou échec) est montré à l'utilisateur.
    """
    updated_club = booking_service.club_manager.find_by_name(club_name)
    competitions = booking_service.competition_manager.competitions
    return render_template("welcome.html", club=updated_club, competitions=competitions)


@app.route("/clubsPoints")
def clubs_points():
    """
    Affiche la liste des clubs et leurs points dans `clubs_points.html`.
    Page accessible sans authentification (transparence).
    """
    clubs = booking_service.club_manager.clubs
    return render_template("clubs_points.html", clubs=clubs)


@app.route("/logout")
def logout():
    """
    Déconnecte le club (supprime 'club_email' de la session),
    puis redirige vers la page d'accueil.
    """
    session.pop('club_email', None)
    return redirect(url_for("index"))
