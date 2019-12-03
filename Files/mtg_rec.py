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

### route 1: hello world
# define the route
@app.route('/')
# create the controller
def home():
    # return the view
    return render_template('form.html')


### accept the form submission and use it to make a prediction
@app.route('/submit')
def submit():
    raw_data = request.args
    print(raw_data)
    # format the user input
    user_input = raw_data['card']
    form = raw_data['format']

    # load in the pickled dataframe
    #df = pickle.load(open('../Data/filter_rec_df.pkl', 'rb'))

    # make recommendation based on the user data
    rec_cards = list(df.loc[df['legalities_' + form] == 1][user_input].sort_values()[1:11].index)
    card1 = rec_cards[0]
    card2 = rec_cards[1]
    card3 = rec_cards[2]
    card4 = rec_cards[3]
    card5 = rec_cards[4]
    card6 = rec_cards[5]
    card7 = rec_cards[6]
    card8 = rec_cards[7]
    card9 = rec_cards[8]
    card10 = rec_cards[9]
    card1_link = df.loc[card1, 'card_link']
    card2_link = df.loc[card2, 'card_link']
    card3_link = df.loc[card3, 'card_link']
    card4_link = df.loc[card4, 'card_link']
    card5_link = df.loc[card5, 'card_link']
    card6_link = df.loc[card6, 'card_link']
    card7_link = df.loc[card7, 'card_link']
    card8_link = df.loc[card8, 'card_link']
    card9_link = df.loc[card9, 'card_link']
    card10_link = df.loc[card10, 'card_link']
    print(card1_link)

    # return the prediction in the template
    return render_template('results.html', rec_cards_1 = card1, rec_cards_2 = card2, rec_cards_3 = card3, rec_cards_4 = card4, rec_cards_5 = card5, rec_cards_6 = card6, rec_cards_7 = card7, rec_cards_8 = card8, rec_cards_9 = card9, rec_cards_10 = card10, card1_link = card1_link, card2_link = card2_link, card3_link = card3_link, card4_link = card4_link, card5_link = card5_link, card6_link = card6_link, card7_link = card7_link, card8_link = card8_link, card9_link = card9_link, card10_link = card10_link)

# run the app
if __name__ == "__main__":
    app.run(debug=True)
