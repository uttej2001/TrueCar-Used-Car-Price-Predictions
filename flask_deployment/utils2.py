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



def Company_Popularity(make):
    top_10_sellers = ["FORD","CHEVROLET","TOYOTA","HONDA","NISSAN","VOLSWAGEN","HUNDAI","JEEP","MAZDA","GM"]
    medium_20_sellers =["DODGE","FCA","KIA","SUBARU","DAIMLER","BMW","MITSUBISHI","VOLVO","PACCAR","PROCHE","TESLA",
    "INTERNATIONAL","LAND ROVER","BUICK","LEXUS","ACURA","AUDI","LINCOLN","MERCEDES-BENZ","CADILLAC"]    
    top_10_sellers = [c.upper() for c in top_10_sellers]
    medium_20_sellers=[c.upper() for c in medium_20_sellers]
    if make in top_10_sellers:
        return "High"
    elif make in medium_20_sellers:
        return "Medium"
    else:
        return "Low"



def luxury(model):
    top_10_most_luxury= ["LFALFA","LFA2DR","675LT2DR","GTC4LUSSOCOUPE","AVENTADORCONVERTIBLE","AVENTADORCOUPE",
                  "488","DAWNCONVERTIBLE","SLR","F12BERLINETTA2DR"]
    top_20_most_luxury = ["DAWN2DR","GTCOUPE","AVENTADOR","PHANTOMSEDAN","F12BERLINETTACOUPE","GT2DR",
                  "HURACANSPYDER","PHANTOM","MULSANNESPEED","5992DR","458","HURACANLP",
                  "BENTAYGAW12","WRAITHCOUPE","CALIFORNIA","HURACANRWD","GHOSTSEDAN","CONTINENTALGT","650SSPIDER","AVENTADOR2DR"]
    top_10_most_luxury = [m.upper() for m in top_10_most_luxury]
    top_20_most_luxury = [m.upper() for m in top_20_most_luxury]
    if model in top_10_most_luxury:
        return "High"
    elif model in top_20_most_luxury:
        return "Medium"
    else:
        return "Low"

def convert_into_cat(data):
    for col in ['Luxury', 'Usage_level', 'City_imporatnce',"Company_popularity"]:
        data[col] = data[col].astype('category')
    return data

def one_hot_encoding(data):
    dummy = pd.get_dummies(data[['Luxury', 'Usage_level', 'City_imporatnce','Company_popularity']])
    return dummy
