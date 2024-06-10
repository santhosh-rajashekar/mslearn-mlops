import json
import joblib
import numpy as np
from azureml.core.model import Model


def init():
    global model
    model_path = Model.get_model_path("employee_attrition_model")
    model = joblib.load(model_path)


def run(data):
    try:
        data = np.array(json.loads(data)["data"])
        result = model.predict(data)
        return json.dumps({"prediction": result.tolist()})
    except Exception as e:
        error = str(e)
        return json.dumps({"error": error})
