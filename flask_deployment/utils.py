from crypt import methods
from distutils.log import debug
import re
from flask import Flask, render_template, request, url_for
import pandas as pd
import numpy as np
from flask_bootstrap import Bootstrap
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import warnings
import pickle



def get_mile_range(mileage):
    """
    This Function to get the usage level of car
    arguments: mileage, float that represents the mileage made by each car
    returns: Usage level
    """
    if mileage < 25000:
        return "Low"
    elif (25000 <= mileage) and (mileage < 80000 ):
        return "Medium"
    else:
        return "High"


def city_importance(city):
    """
    This function to get the importance of the city according to the population
    arguments: city, String to represent the city 
    returns: importance of the city
    """
    low_cities = pd.read_csv("models/low_cities.csv")
    medium_citeis =  pd.read_csv("models/medium_cities.csv")
    low_cities = [c.upper() for c in low_cities]
    Midium_cities = [c.upper() for c in medium_citeis]
    if city in low_cities:
        return "Low"
    elif city in Midium_cities:
        return "Medium"
    else:
        return "High"

def get_mean_price(city):
    mean_prices = pd.read_csv("models/city_mean_prices.csv")
    if(city in list(mean_prices["City"].value_counts().index)):
    	mean_price = mean_prices[mean_prices["City"] == city]["Price"]
    else:
    	mean_price = mean_prices["Price"].mean()
    return mean_price


def state_importance(state):
    low_state = pd.read_csv("models/low_states.csv")
    medium_state = pd.read_csv("models/medium_states.csv")
    low_state = [c.upper() for c in low_state]
    medium_state = [c.upper() for c in medium_state]
    if state in low_state:
        return "Low"
    elif state in medium_state:
        return "Medium"
    else:
        return "High"





def popullariy(brand):
    """
    This function to get the popularity of the brand that make the care according input lists
    that contains the names of the top ad medium sellers
    arguments: df to convert, top 10 sellers, medium 20 sellers
    returns: dataframe with added features the level of the seller popularity 3: high populrity, 2: medium,
                                                1:low popular brands
    """
    top = pd.read_csv("models/popular_brands.csv")
    med = pd.read_csv("models/medium_brands.csv")
    top = top.index.to_list()
    med = med.index.to_list()
    if(brand in top):
        return 3
    elif(brand in med):
        return 2
    else:
        return 1



def model_level(model):
    top = pd.read_csv("models/top_models.csv")
    med = pd.read_csv("models/medium_models.csv")
    top = top.index.to_list()
    med = med.index.to_list()
    if(model in top):
        return 3
    elif(model in med):
        return 2
    else:
        return 1


def oh_encoder(df):
    """
    This Function to Do one hot Ending for the categorical variables
    
    """
    num_cols = df.select_dtypes(exclude = "object").columns.to_list()
    object_cols = df.select_dtypes("object" ).columns.to_list()

    with open("models/encoder.pkl", "rb") as f:
        encoder = pickle.load(f) 
        data = pd.DataFrame(encoder.transform(df[object_cols]))
        cols = list(encoder.get_feature_names_out())  
        data.index = df.index
        data.columns = list(cols)
        f_data = pd.concat([data, df[num_cols]], axis = 1)    
    return f_data
