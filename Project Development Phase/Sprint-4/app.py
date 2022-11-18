import numpy as np
from flask import Flask, render_template,request
from tensorflow.keras.models import load_model
import ast
import requests
import json 

app=Flask(__name__,template_folder='template')
model = load_model('crude.h5')

@app.route('/') 
def home():
    return render_template("index.html") 

@app.route('/about')
def homel():
    return render_template("index.html") 

@app.route('/predict')
def home2():
    return render_template("web.html") 

@app.route('/price', methods = ['POST']) 
def login():
    x_input=str(request.form['year'])
    x_input=(x_input.split(','))
    #print(x_input)
    x=[float(ele) for ele in x_input]
    converted=[list((x[i:i+1])) for i in range(0, len(x), 1) ]
    print(converted)

    API_KEY = "nFDWeM8RsZZpNyUczE8HmCUT6mi6PdwuFC3Cxk3asOr1"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}    
    payload_scoring = {"input_data": [{"field": ["Closing Value"], "values": [list(converted)] }]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2d99dc94-3e6c-4546-ba30-873a31f48f3c/predictions?version=2022-11-17', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})

    print("Scoring response")
    result=response_scoring.json()
    print(result)
    final=result['predictions'][0]['values'][0][0]
    return render_template("web.html", showcase = 'The next day predicted value is: '+str(final))
    
if __name__=="__main__":
    app.run(debug =True, port=5000)