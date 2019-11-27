# imports
import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine

# initialize the flask app
app = Flask('MTGRecommender')

### route 1: hello world
# define the route
@app.route('/')
# create the controller
def home():
    # return the view
    return render_template('form.html')


### route 3: return some data
# define the route
@app.route('/hc_page.json')
# create the controller
def hc_json():

    # Set up the engine to access the data.
    engine = create_engine('postgres://analytics_student:analyticsga@analyticsga-psql.generalassemb.ly:5432/iowa_liquor_sales_database')
    sql = """
        SELECT COUNT(*)
        FROM stores;
        """
    data_sql = pd.read_sql_query(sql, engine)

    # return the view
    return jsonify(data_sql.to_dict())

### accept the form submission and use it to make a prediction
@app.route('/submit')
def submit():
    raw_data = request.args
    # format the user input
    user_input = raw_data['card']
    form = raw_data['format']

    # load in the pickled dataframe
    df = pickle.load(open('../Data/filter_rec_df.pkl', 'rb'))

    # make recommendation based on the user data
    rec_cards = list(df.loc[df['legalities_' + form] == 1][user_input].sort_values()[1:6].index)
    card1 = rec_cards[0]
    card2 = rec_cards[1]
    card3 = rec_cards[2]
    card4 = rec_cards[3]
    card5 = rec_cards[4]
    # return the prediction in the template
    return render_template('results.html', rec_cards_1 = card1, rec_cards_2 = card2, rec_cards_3 = card3, rec_cards_4 = card4, rec_cards_5 = card5)
    # return render_template('results.html', prediction=round(pred[0], 2))

# run the app
if __name__ == "__main__":
    app.run(debug=True)
