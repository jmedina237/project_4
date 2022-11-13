import pandas as pd
import numpy as np
import requests
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
import numpy as np
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

#getting everything FROM  BRANCH
@app.route("/sql/<disney_branch>", )
def reviews_from_branches (disney_branch):
    return jsonify(esecuele.get_everything_from_branch(disney_branch))

#getting everything FROM  COUNTRY
@app.route("/sql/<country>", )
def reviews_from_locations (country):
    return jsonify(esecuele.get_everything_from_location(country))


#getting everything FROM  YEAR
@app.route("/sql/<year>", )
def reviews_from_year (year):
    return jsonify(esecuele.get_everything_from_year(year))


#getting Reviews & Compound FROM BRANCH

@app.route("/sa/<disney_branch>/", )
def sa_from_branch (disney_branch):
    everything = esecuele.get_just_reviews_from_branch(disney_branch)
    #return jsonify(everything)
    return jsonify([sia.polarity_scores(i["Review_Text"])["compound"] for i in everything])

#getting Reviews & Compound FROM  COUNTRY

@app.route("/sa/<country>/", )
def sa_from_country (country):
    everything = esecuele.get_just_reviews_from_country(country)
    #return jsonify(everything)
    return jsonify([sia.polarity_scores(i["Review_Text"])["Compound"] for i in everything])

#getting Reviews & Compound FROM YEAR

@app.route("/sa/<year>/", )
def sa_from_year (year):
    everything = esecuele.get_just_reviews_from_year(year)
    #return jsonify(everything)
    return jsonify([sia.polarity_scores(i["Review_Text"])["compound"] for i in everything])


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