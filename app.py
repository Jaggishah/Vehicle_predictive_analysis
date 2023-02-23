from flask import Flask, render_template ,request
import jsonify
import requests,pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    Fuel_type_diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_price = float(request.form['Present_Price'])
        Kms_driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_type_Petrol = request.form['Fuel_Type_Petrol']
        if(Fuel_type_Petrol == 'Petrol'):
            Fuel_type_Petrol = 1
            Fuel_type_diesel = 0
        else:
            Fuel_type_Petrol = 0
            Fuel_type_diesel = 1
        Year = 2020-Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Mannual = request.form['Transmission_Mannual']
        if (Transmission_Mannual == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
        print([Present_price,Kms_driven,Owner,Year,Fuel_type_diesel,Fuel_type_Petrol,Seller_Type_Individual,Transmission_Mannual])
        prediction = model.predict([[Present_price,Kms_driven,Owner,Year,Fuel_type_diesel,Fuel_type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output = round(prediction[0],2)
        if output < 0:
            return render_template('index.html',prediction_text ="Sorry You cannot Sell This Car")
        else:
            return render_template('index.html',prediction_text=f"You can Sell this at {output}")
        
    else:
        return render_template('index.html',prediction_text ="Error ")
if __name__ == "__main__":
    app.run(debug=True)