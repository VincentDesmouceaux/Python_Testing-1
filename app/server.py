# app/server.py

from flask import Flask, render_template, request, redirect, flash, url_for
from app.booking_manager import BookingManager

# Indique que le dossier statique se trouve dans ../static (à la racine du projet)
# Les templates seront recherchés par défaut dans "templates" situé dans ce même dossier (ici "app/templates")
app = Flask(__name__, static_folder="../static")
app.secret_key = "secret_key_xyz"

# Instanciation du manager avec les chemins de fichiers en paramètre
manager = BookingManager(
    clubs_file="data/clubs.json",
    competitions_file="data/competitions.json"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    email = request.form.get("email", "")
    club = manager.find_club_by_email(email)
    if not club:
        flash("Email inconnu ou invalide.")
        return redirect(url_for("index"))
    return render_template("welcome.html", club=club, competitions=manager.competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_competition = manager.find_competition_by_name(competition)
    found_club = manager.find_club_by_name(club)
    if not found_competition or not found_club:
        flash("Something went wrong - please try again")
        return redirect(url_for("index"))
    return render_template("booking.html", club=found_club, competition=found_competition)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    competition_name = request.form.get("competition")
    club_name = request.form.get("club")
    places_str = request.form.get("places")
    try:
        places_requested = int(places_str)
    except ValueError:
        flash("Le nombre de places est invalide.")
        return redirect(url_for("index"))

    success = manager.purchase_places(
        club_name, competition_name, places_requested)
    if success:
        flash("Great-booking complete!")
    else:
        flash("Impossible de réserver ces places (Règle non respectée).")

    club = manager.find_club_by_name(club_name)
    return render_template("welcome.html", club=club, competitions=manager.competitions)


@app.route("/clubsPoints")
def clubs_points():
    return render_template("clubs_points.html", clubs=manager.clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
