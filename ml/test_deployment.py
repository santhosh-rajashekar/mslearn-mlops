import requests
import json

# Replace with your service URI
scoring_uri = "YOUR_SERVICE_URI"

# Example data for prediction
data = {"data": [[41, 1, 2, 1, "Male", "Sales Executive", "Single", 5993, 8, 11, 8, 0, 6, 4, 0, 5]]}
input_data = json.dumps(data)

# Set the content type
headers = {'Content-Type': 'application/json'}

# Make the request
response = requests.post(scoring_uri, data=input_data, headers=headers)
print(response.json())
