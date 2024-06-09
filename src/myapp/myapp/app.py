from flask import Flask, request, render_template
import json
import os
import ssl
import urllib.request
 
app = Flask(__name__)
 
 
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if (
        allowed
        and not os.environ.get("PYTHONHTTPSVERIFY", "")
        and getattr(ssl, "_create_unverified_context", None)
    ):
        ssl._create_default_https_context = ssl._create_unverified_context
 
 
allowSelfSignedHttps(True)
# this line is needed if you use self-signed certificate
# in your scoring service.
 
 
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        patient_id = request.form["PatientID"]
        pregnancies = request.form["Pregnancies"]
        plasma_glucose = request.form["PlasmaGlucose"]
        diastolic_blood_pressure = request.form["DiastolicBloodPressure"]
        triceps_thickness = request.form["TricepsThickness"]
        serum_insulin = request.form["SerumInsulin"]
        bmi = request.form["BMI"]
        diabetes_pedigree = request.form["DiabetesPedigree"]
        age = request.form["Age"]
 
        # Format input data
        input_data = {
            "input_data": {
                "columns": [
                    "PatientID",
                    "Pregnancies",
                    "PlasmaGlucose",
                    "DiastolicBloodPressure",
                    "TricepsThickness",
                    "SerumInsulin",
                    "BMI",
                    "DiabetesPedigree",
                    "Age",
                ],
                "index": [0],
                "data": [
                    [
                        patient_id,
                        pregnancies,
                        plasma_glucose,
                        diastolic_blood_pressure,
                        triceps_thickness,
                        serum_insulin,
                        bmi,
                        diabetes_pedigree,
                        age,
                    ]
                ],
            }
        }
 
        body = str.encode(json.dumps(input_data))
        # Get the AZURE_ML_ENDPOINT_URL environment variable passed from App Service Application settings
        url = os.environ["AZURE_ML_ENDPOINT_URL"]
        # Get the API_KEY environment variable passed from App Service Application settings
        api_key = os.environ["API_KEY"]
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")
 
        # The azureml-model-deployment header will force the request
        # to go to a specific deployment.
        # Remove this header to have the request observe the endpoint
        # traffic rules
        headers = {
            "Content-Type": "application/json",
            "Authorization": ("Bearer " + api_key),
            "azureml-model-deployment": "mlflow-deployment",
        }
 
        req = urllib.request.Request(url, body, headers)
 
        try:
            response = urllib.request.urlopen(req)
 
            result = json.loads(response.read())
 
            # Display result
            if result[0] == 1:
                return render_template("result.html", result="The patient is diabetic.")
            else:
                return render_template(
                    "result.html", result="The patient is not diabetic."
                )
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))
 
            # Print the headers - they include the requert ID and the
            # timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", "ignore"))
    else:
        return render_template("index.html")
 
 
if __name__ == "__main__":
    app.run()