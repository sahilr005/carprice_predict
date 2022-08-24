from flask import Flask,request,jsonify
import pandas as pd
from flasgger import Swagger
import pickle
import sys

app = Flask(__name__)
Swagger(app)

pickle_file = open("car_price_pred","rb")
model = pickle.load(pickle_file)

@app.route("/")
def welcome():

    '''
    Hello Word
    ---
    responses:
        200:
            description: Output value
    '''
    return "Hello Word"

# Present_Price	Kms_Driven	Owner	Individual	Manual	Diesel	Petrol	Age
def pricePrid(Present_Price,Kms_Driven,Owner,Individual,Manual,Diesel,Petrol,Age):
    return model.predict([[Present_Price,Kms_Driven,Owner,Individual,Manual,Diesel,Petrol,Age]])

@app.route("/price")
def price():
    '''
    price Predic
    ---
    parameters:
        -  name: Present Price
           in: query
           type: number
           required: true
        -  name: Kms_Driven
           in: query
           type: number
           required: true
        -  name: Transmission
           type: string
           in: query
           required: true
           enum:  ["Manual","Automatic"]
           default: "Automatic"
        -  name: Seller_Type
           in: query
           required: true
           enum:  ["Dealer","Individual"]
           default: "Dealer"
        -  name: Fuel_Type
           type: string
           in: query
           required: true
           enum:  ["Petrol","Diesel"]
           default: "Petrol"
        -  name: Owner
           type: number
           in: query
           enum:  [0,1,3]
           default: 0
           required: true
        -  name: Age
           in: query
           type: number
           required: true
    responses:
        200:
            description: Output value
    '''

    Present_Price = request.args.get("Present Price",type=int)
    Kms_Driven = request.args.get("Kms_Driven",type=int)
    transmision = request.args.get("Transmission")
    seller = request.args.get("Seller_Type")
    fuel = request.args.get("Fuel_Type")
    owner = request.args.get("Owner")
    age = request.args.get("Age")

    seller_type = 0
    fuel_type = 0
    transmision_type = 0


    if seller == "Dealer":
        seller_type = 0
    else:
        seller_type = 1

    if transmision == "Manual":
        transmision_type = 0
    else:
        transmision_type = 1

    if fuel == "Petrol":
        fuel_type = 0
    elif fuel == "Diesel":
        fuel_type = 1
    else:
        fuel_type = 2

    pred_price = pricePrid(Present_Price=Present_Price,Kms_Driven=Kms_Driven,Owner=owner,Individual=seller_type,Manual=transmision_type,Diesel=fuel_type,Petrol=fuel_type,Age=age)

    return jsonify(pred_price[0])

if __name__ == "main":
    app.run()