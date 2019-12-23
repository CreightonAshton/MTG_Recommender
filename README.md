# MTG Recommender

**Author: [Creighton Ashton](https://www.linkedin.com/in/creightonashton/)**

---

## Problem Statement

Building a deck in Magic can be difficult. There have been nearly 20,000 different tournament-legal cards printed throughout the history of the game. I will use data on Magic: the Gathering cards to build a content-based recommender system that suggests similar cards based on cosine similarity in order to improve card selection during the deck building process.

---

## Executive Summary

The goal of this project is to develop a flask app where a user can input a Magic: The Gathering card and select a format, then the recommender system will return the top 10 most similar cards to the user-inputted card legal in the format they selected. The card data will be collected from Scryfall's open source [bulk data.](https://archive.scryfall.com/json/scryfall-oracle-cards.json) From there the data needs to be cleaned and formatted by removing unneeded card attributes and using certain regular expressions to format the oracle text of each card. Once cleaned I'll be using CountVectorizer to convert the oracle text into numerical data and using a variance threshold to reduce the data to only the most relevant words. After converting all the data to numerical versions a recommender system can be built using cosine similarity. Then a custom filter table can be tacked on to the recommender table to assist with filtering. Finally a flask app can be built using a pickled final version of the recommender system table.

---

## Software Requirements

Codes are written in Jupyter Notebook with Python. Users are recommended to know the Python libraries `Numpy`, `Pandas`, `Scikit-learn`, `nltk`, visualization with `matplotlib` and `seaborn`.

---

## Content with Jupyter Notebooks



### 1. Cleaning

The raw [data](https://archive.scryfall.com/json/scryfall-oracle-cards.json) from Scryfall is in the format of nested JSON objects so there is quite a bit of cleaning to be done. To start I dropped any unneeded columns and through some EDA filtered and removed any cards that are either not legal or are considered other cards. For example the raw data includes tokens, archenemy cards, avatar cards (cards that only exist on Magic: Online for a specific game type and not actual magic cards), joke cards (unstable, unhinged, unglued, etc.), and even oversized cards (promotional cards that are 10 times larger than normal). I also had to break out data from the nested JSON objects in regards to double-faced/dual cards so that each row in the final clean version of the table is a single magic card and each column is an attribute of that card. This means that there will be many empty values for cards that don't have certain attributes that other cards have. For example instants and sorceries don't have any power or toughness, though creatures do. So, for now those cells will be imputed as 'NONE'. This process is broken down even further in the cleaning notebook.

- [Cleaning Notebook](./Code/01-Cleaning.ipynb)  
- [Data Dictionary](./Files/Data_Dictionary.ipynb)

### 2. EDA

EDA in this regard was mostly dedicated to the oracle text of Magic cards. I wanted to get an idea of what common words/phrases appear most often. This kind of insight helped guide how many nGrams should be considered when building the recommender system. For example the phrases 'Draw a card', 'Enter's the battlefield', or 'deals combat damage to a player' appears over many Magic cards so the number of nGrams should include them.

- [EDA](./Code/02-EDA.ipynb)

### 3. Recommender System

The recommender system was built piece by piece starting with just considering the oracle text of cards. The cosine similarity metric was used when building the model. After using CountVectorizer with an nGram range of 1 to 6, a variance threshold was used to reduce the overall number of features to only those that appeared on a certain number of cards. For example if a certain nGram phrase only appears on one card, then it's not going to be useful to the final recommender model. From here more card attributes such as converted mana cost, power, toughness, whether a card has an activated/triggered ability where added to improve the model. More detail is provided in the Jupyter notebook.

- [Recommender System](./Code/03-Recommender_system.ipynb)

### 4. Filter

Currently scratch work for building out a more robust filtering method.

- [Filter](./Code/04-Filter.ipynb)

### 5. Flask App

The flask app is fairly simple and imports the final recommender system table as a pickled object then takes the user-inputted card along with a selected format and looks up on the recommender table the top 10 most similar cards filtered by format and returns the results.

- [Flask app](./Files/mtg_rec.py)

## Conclusion/Next steps

There are several things that could be improved upon here. One stretch goal would be to host this somewhere and get user-feedback to start collecting data for a user-based collaborative recommender system. Dealing with the overal size of the recommender system model is also a challenge. As it stands right now, the table/model itself is over 3 GB and is too large to host anywhere for free. I would like to find more efficient ways of storing and accessing the data to cut down on the run time of the app. There are also a few cosmetic things I would like to implement such as a mouse-over the card link to get a picture of the card, but that is more on the front end side of things and not really a data science issue. Something that IS a data science problem that I'd like to address at some point would be recommending better cards (i.e. Lightning Bolt is better than Shock). The trouble I see with that is how do I quantify what "better" means in order for a computer to understand that.

---

## Sources

- [ScryFall Card Data](https://scryfall.com/docs/api/bulk-data)  
- [Scryfall Oracle Cards](https://archive.scryfall.com/json/scryfall-oracle-cards.json)  
- [MTG Wiki](https://mtg.gamepedia.com/Main_Page)  
- [Magic: The Gathering is Turing Complete](https://arxiv.org/pdf/1904.09828.pdf)  
