# import necessary libraries
# from models import create_classes
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, or_
from sqlalchemy.ext.automap import automap_base

import pickle

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

engine = create_engine("sqlite:///data/movies.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
print(Base.classes.keys())

Movies = Base.classes.movies
Actors = Base.classes.actors

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


# ---------------------------------------------------------
# Web site
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():

    return render_template("data.html")

@app.route("/analysis")
def actors():
    return render_template("analysis.html")

@app.route("/model" , methods=["POST"])
def model():

    rooms = float(request.form["rooms"])
    bedrooms = float(request.form["bedrooms"])

    income = request.form["income"]
    if income == "":
        income = 68000
    income = float(income)

    age = request.form["age"]
    if age == "":
        age = 6
    age = float(age)

    population = request.form["population"]
    if population == "":
        population = 36000

    prediction = 0

    X = [[income, age, rooms, bedrooms, population]]

    print(X)

    filename = './data/housing.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    prediction = loaded_model.predict(X)[0][0]

    prediction = "${0:,.2f}".format(prediction)

    print(prediction)

    return render_template("analysis.html", prediction = prediction)

# ---------------------------------------------------------
# API
@app.route("/api/movies")
def movie_grid():

    session = Session(engine)

    results = session.query(Movies.title, Movies.director, Movies.year, Movies.rating, Movies.imdb_votes, Movies.imdb_score).all()

    results = [list(r) for r in results]

    table_results = {
        "table": results
    }

    session.close()

    return jsonify(table_results)

@app.route("/api/years/<year>")
def years(year):

    session = Session(engine)

    if year == "before":
        results = session.query(Movies.title, Movies.director, Movies.year, 
            Movies.rating, Movies.imdb_votes, Movies.imdb_score).filter(Movies.year < 2000).all()
    else:
        results = session.query(Movies.title, Movies.director, Movies.year, 
            Movies.rating, Movies.imdb_votes, Movies.imdb_score).filter(Movies.year >= 2000).all()

    results = [list(r) for r in results]

    rating = [result[3] for result in results]
    votes = [result[4] for result in results]

    year_results = {
        "rating": rating,
        "votes": votes,
    }

    session.close()

    return jsonify(year_results)


@app.route("/api/directors/<director>")
def directors(director):

    print(director)

    if director == "chaplin":
        name = "Charles Chaplin"
    elif director == "hitchcock":
        name = "Alfred Hitchcock"
    elif director == "nolan":
        name = "Christopher Nolan"
    else:
        name = "Akira Kurosawa"

    session = Session(engine)

    G_results = session.query(func.avg(Movies.imdb_score)).filter(Movies.rating=="G").filter(Movies.director == name).all()
    PG_results = session.query(func.avg(Movies.imdb_score)).filter(Movies.rating=="PG").filter(Movies.director == name).all()
    PG_plus_results = session.query(func.avg(Movies.imdb_score)).filter(or_(Movies.rating=="PG+", Movies.rating=="PG-13")).filter(Movies.director == name).all()
    R_results = session.query(func.avg(Movies.imdb_score)).filter(Movies.rating=="R").filter(Movies.director == name).all()
    Other_results = session.query(func.avg(Movies.imdb_score)).filter(or_(Movies.rating=="APPROVED",Movies.rating=="NOT RATED", Movies.rating=="N\A", Movies.rating=="PASSED")).filter(Movies.director == name).all()

    results = [G_results[0][0], PG_results[0][0], PG_plus_results[0][0], R_results[0][0], Other_results[0][0]]
    labels = ["G", "PG", "PG+", "R", "Other"]

    director_results = {
        "labels": labels,
        "scores": results,
    }

    session.close()

    return jsonify(director_results)

if __name__ == "__main__":
    app.run()
