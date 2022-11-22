from config.sql_connection import engine
import pandas as pd



####################################   getting everything   ###########@##############################

def get_everything ():
    query = """SELECT * FROM df_disney;"""
    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")

########################    getting everything  FROM  BRANCH, COUNTRY and YEAR   #######################


def get_everything_from_location (country):
    query = f"""SELECT * 
    FROM df_disney
    WHERE Reviewer_Location = '{country}';"""

    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")



########################   getting just REVIEWS  FROM  BRANCH, CONTRY and YEAR   #######################


def get_just_reviews_from_branch (disney_branch):
    query = f"""SELECT Review_Text 
    FROM df_disney
    WHERE Branch = '{disney_branch}';"""

    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")


######################################################################### COMPOUND PER YEAR #################€


def get_compound_per_year (disney_branch, year):
    query = f"""SELECT Branch, Year, AVG (Compound) as "Average Compound"
    FROM df_disney
    WHERE Branch = '{disney_branch}'
    AND Year = '{year}'
    GROUP BY Branch 
    ORDER BY AVG (Compound) DESC;"""

    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")



#########################################################################    main countries reviewers         #################€

def get_main_countries ():
    query = f"""SELECT Reviewer_Location, COUNT(Branch) as "Count"
    FROM df_disney
    GROUP BY Reviewer_Location 
    ORDER BY COUNT(Branch) DESC;"""



    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")

#########################################################################    main countries reviewers  by branch       #################€

def get_main_countries_branch (disney_branch):
    query = f"""SELECT Reviewer_Location, COUNT(Branch) as "Count"
    FROM df_disney
    WHERE Branch = '{disney_branch}'
    GROUP BY Reviewer_Location 
    ORDER BY COUNT(Branch) DESC;"""



    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")


#########################################################################    main countries reviewers  by branch       #################€

def get_positives_branch ():
    query = f"""SELECT Branch, AVG (Positive) as "Positives"
    FROM df_disney
    GROUP BY Branch 
    ORDER BY AVG (Positive) DESC;"""



    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")


########################################   inserting rows   ###########################################



def insert_one_row (Reviewer_Location, Review_Text, Branch,Year):
    query = f"""INSERT INTO df_disney
     (Reviewer_Location, Review_Text, Branch, Year) 
        VALUES ('{Reviewer_Location}', '{Review_Text}', '{Branch}', {Year});
    """
    engine.execute(query)
    return f"Correctly introduced!"

