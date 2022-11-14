import pandas as pd
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt


from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from langdetect import detect


import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords


from flask import Flask, request, jsonify
import random
import markdown.extensions.fenced_code
import tools.sql_queries as esecuele


sia = SentimentIntensityAnalyzer()

app = Flask(__name__)

# Render the markdwon
@app.route("/")
def readme ():
    readme_file = open("README.md", "r")
    return markdown.markdown(readme_file.read(), extensions = ["fenced_code"])

# GET ENDPOINTS: SQL 

# SQL get everything
@app.route("/sql/")
def sql ():
    return jsonify(esecuele.get_everything())


#getting everything FROM  COUNTRY -----------------------------------------------EMPTY LIST---------------------
@app.route("/<country>" )
def reviews_from_locations (country):
    return jsonify(esecuele.get_everything_from_location(country))

#getting Reviews & Compound FROM BRANCH

@app.route("/sa/<disney_branch>/")
def sa_from_branch (disney_branch):
    everything = esecuele.get_just_reviews_from_branch(disney_branch)
    #return jsonify(everything)
    return jsonify([sia.polarity_scores(i["Review_Text"])["compound"]for i in everything])


#getting the compound per year------------------------------------------------------------------------------------

@app.route("/avg/<disney_branch>/<year>/")
def compounds_from_year (disney_branch,year):
    return jsonify(esecuele.get_compound_per_year(disney_branch, year))


#getting countries ------------------------------------------------------------------------------------


@app.route("/countries/")
def main_countries ():
    return jsonify(esecuele.get_main_countries())

#getting countries per branch------------------------------------------------------------------------------------


@app.route("/countries/<disney_branch>/")
def main_countries_branch (disney_branch):
    return jsonify(esecuele.get_main_countries_branch(disney_branch))


#getting countries per branch------------------------------------------------------------------------------------

@app.route("/positives/")
def positives_branch ():
    return jsonify(esecuele.get_positives_branch ())




####### POST

@app.route("/insertrow", methods=["POST"])
def try_post ():
    # Decoding params
    my_params = request.args
    Reviewer_Location = my_params["Reviewer_Location"]
    Review_Text = my_params["Review_Text"]
    Branch = my_params["Branch"]
    Year = my_params["Year"]

    
    # Passing to my function: do the insert
    esecuele.insert_one_row(Reviewer_Location, Review_Text, Branch, Year)
    return f"Query succesfully inserted"





if __name__ == "__main__":
    app.run(port=8000, debug=True)