# imports
import numpy as np
import pandas as pd
import pickle
import sqlite3
from flask import Flask, request, render_template, jsonify


# initialize the flask app
app = Flask('MTGRecommender')

# load in the pickled dataframe
df = pickle.load(open('../Data/filter_rec_df.pkl', 'rb'))


### root route
# define the route
@app.route('/')
# create the controller
def home():
    # return the view
    return render_template('form.html')


### accept the form submission and use it to make recommendation
@app.route('/submit')
def submit():
    # connect to SQL database
    conn = sqlite3.connect('../Data/MTG_Recommender.db')

    raw_data = request.args

    # format the user input
    user_input = raw_data['card']
    form = raw_data['format']
    card_type = raw_data['card_type']

    # build the sql query piece by piece
    sql = """
    SELECT name FROM filter
    WHERE """

    # card type filter
    if card_type != 'None':
        sql += f"card_type_{card_type} != 0 "
    else:
        sql += f"card_type_Creature < 2 " # need a place to start that doesn't begin with 'AND' if no cardtype is used

    # filter by format
    sql += f"AND legalities_{form} != 0"

    # create a list of filtered cards
    filtered_list = list(pd.read_sql_query(sql, conn)['name'].values)

    # make recommendation based on the user data
    #rec_cards = list(df.loc[df['legalities_' + form] == 1][user_input].sort_values()[0:11].index)
    rec_cards = df[filtered_list].T['Shock'].sort_values()[0:11].index

    # error checking to see if the user-inputted card is the same as the first recommended card
    if rec_cards[0] == user_input:
        rec_cards = rec_cards[1:11]
    else:
        rec_cards = rec_cards[0:10]

    # get the links for the recommended cards
    links = []
    for card in rec_cards:
        links.append(df.loc[card, 'card_link'])

    # return the prediction in the template
    return render_template('results.html', len = len(rec_cards), rec_cards = rec_cards, links = links)

# run the app
if __name__ == "__main__":
    app.run(debug=True)
