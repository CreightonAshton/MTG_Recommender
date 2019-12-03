# imports
import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine

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
    raw_data = request.args

    # format the user input
    user_input = raw_data['card']
    form = raw_data['format']

    # make recommendation based on the user data
    rec_cards = list(df.loc[df['legalities_' + form] == 1][user_input].sort_values()[0:11].index)

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
