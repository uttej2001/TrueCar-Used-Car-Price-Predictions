from copyreg import pickle
from crypt import methods
from distutils.log import debug
import re
from flask import Flask, render_template, request, url_for
import pandas as pd
import numpy as np
from flask_bootstrap import Bootstrap
from sklearn.pipeline import Pipeline
import utils
import utils2
import tensorflow as tf
import pickle

app = Flask(__name__, template_folder = "templates")
Bootstrap(app)





@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/results", methods = ["GET", "POST"])
def results():
    year = int(request.form['year'])
    mileage = float(request.form['mileage'])
    city = request.form['city']
    state = request.form['state']
    make = request.form['make']
    model = request.form['model']
    algo = int(request.form['algo'])
    encoding = int(request.form['encoding'])

    #Convering to a dataframe
    query = {"Year": [year], "Mileage":[mileage], "City": [city] ,"State":[state], "Make":[make], "Model":[model]}
    query_df = pd.DataFrame(query)
    print(query_df)
	

    with open("models/DT.pkl", "rb") as dt:
        DT = pickle.load(dt)
    with open("models/RF.pkl", "rb") as rf:
        RF = pickle.load(rf)
    with open("models/Ridge.pkl", "rb") as lr:
        LR = pickle.load(lr)
    with open("models/lgbm1.pkl", "rb") as lgbm:
        LGBM = pickle.load(lgbm)
    with open("models/data_ver2/lightGBM.pkl", "rb") as lgbm2:
        LGBM2 = pickle.load(lgbm2)
#     with open("models/DNN1.h5", "rb") as dnn:
#         DNN = tf.keras.models.load_model(dnn)

    if encoding ==  1:
        # Getting Usage Level
        print(query_df)
        query_df["Usage_level"] = query_df["Mileage"].apply(utils.get_mile_range)
        # Getting City Imporane Level
        print(query_df)
        query_df["City_imporatnce"] = query_df["City"].apply(utils.city_importance)
        # Get Mean Price on the city
        print(query_df)
        query_df["City_mean_price"] = query_df["City"].apply(utils.get_mean_price)
        # State Importance
        print(query_df)
        query_df["State_imporatnce"] = query_df["State"].apply(utils.state_importance)
        # Company popularity
        print(query_df)
        query_df["Brand_popularity"] = query_df["Make"].apply(utils.popullariy)
        # Model Level
        print(query_df)
        query_df["Model_level"] = query_df["Model"].apply(utils.model_level)
        #Bofore One Hot encoding
        print(query_df["Make"])
        
        
        
        query_df = query_df.drop(columns = ["Make", "Model", "City"])
        print(query_df)
        # Choose Encoding encoding
        query_df = utils.oh_encoder(query_df)

        # Decide the model
        if algo == 1:
            model_predict = LR.predict(query_df)
            r2_score = 0.608
            nrmse_score = 0.1
            mape = 0.32

        elif algo == 2:
            model_predict = DT.predict(query_df)
            r2_score = 0.67
            nrmse_score = 0.09
            mape = 0.24

        elif algo == 3:
            model_predict = RF.predict(query_df)
            r2_score = 0.68
            nrmse_score = 0.09
            mape = 0.24
        

        elif algo == 5:
            model_predict = DNN.predict(query_df)
            r2_score = 0.39
            nrmse_score = "Not Calculated"
            mape = "Not Calculated"

        else:
            model_predict = LGBM.predict(query_df)
            r2_score = 0.85
            nrmse_score = "Not Calculated"
            mape = "Not Calculated"



    else: 
        #Getting ready for label encoding
        query_df["Usage_level"] = query_df["Mileage"].apply(utils.get_mile_range)
        query_df["City_imporatnce"] = query_df["City"].apply(utils.city_importance)
        query_df["Company_popularity"] = query_df["Make"].apply(utils2.Company_Popularity)
        query_df["Luxury"] = query_df["Model"].apply(utils2.luxury)
        #Label Encoder
        query_df["City_n"] = utils2.city_encoder(query_df["City"])
        query_df["State_n"] = utils2.state_encoder(query_df["State"])
        query_df["Make_n"] = utils2.brand_encoder(query_df["Make"])
        query_df["Model_n"] = utils2.model_encoder(query_df["Model"])
        query_df=query_df.drop(["City","State","Make","Model"],axis="columns")
        query_df = utils2.convert_into_cat(query_df)            

        #One Hot Encoder encoding
        query_enc = utils2.one_hot_encoding(query_df)
        query_df = pd.concat([query_df, query_enc], axis=1)
        query_df=query_df.drop(["City_imporatnce","Usage_level","Company_popularity","Luxury"],axis="columns")

        model_predict = LGBM2.predict(query_df)
        r2_score = 0.85
        nrmse_score = 0.09
        mape = 0.24

    
    return render_template("results.html", mape_ = mape,predictions = model_predict, score = r2_score, nrmse = nrmse_score)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'



if __name__ == "__main__":
    app.run(port = 7000)
