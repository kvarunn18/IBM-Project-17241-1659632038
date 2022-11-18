import requests
import json 
API_KEY = "nFDWeM8RsZZpNyUczE8HmCUT6mi6PdwuFC3Cxk3asOr1"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": ["Closing Value"], "values": [[[4.1],[4.2],[4.5],[4.8],
                                                            [4.9],[4.1],[4.2],[4.5],[4.8],[4.9]]]}]}
response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2d99dc94-3e6c-4546-ba30-873a31f48f3c/predictions?version=2022-11-17', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})

print("Scoring response")
result=response_scoring.json()
print(result)
print(result['predictions'][0]['values'][0][0])