# app/server.py

from flask import Flask, render_template, request, redirect, flash, url_for, session
from app.booking_manager import BookingService

app = Flask(__name__, static_folder="../static")
app.secret_key = "secret_key_xyz"

booking_service = BookingService(
    clubs_file="data/clubs.json",
    competitions_file="data/competitions.json"
)


@app.context_processor
def inject_club_email():
    return dict(club_email=session.get('club_email'))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
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
    found_competition = booking_service.competition_manager.find_by_name(
        competition)
    found_club = booking_service.club_manager.find_by_name(club)
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

    found_competition = booking_service.competition_manager.find_by_name(
        competition_name)
    found_club = booking_service.club_manager.find_by_name(club_name)

    if not found_competition or not found_club:
        flash("Something went wrong - please try again.")
        return redirect(url_for("index"))

    # Logique de réservation
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
        if places_requested <= 12:
            flash("Le concours est complet ou vous n'avez pas assez de points.")

    return redirect(url_for("show_purchase_result", club_name=club_name))


@app.route("/showPurchaseResult/<club_name>")
def show_purchase_result(club_name):
    updated_club = booking_service.club_manager.find_by_name(club_name)
    competitions = booking_service.competition_manager.competitions
    return render_template("welcome.html", club=updated_club, competitions=competitions)


@app.route("/clubsPoints")
def clubs_points():
    clubs = booking_service.club_manager.clubs
    return render_template("clubs_points.html", clubs=clubs)


@app.route("/logout")
def logout():
    session.pop('club_email', None)
    return redirect(url_for("index"))
