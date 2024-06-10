import os
import pandas as pd
from azureml.core import Run, Dataset
from azureml.core.model import Model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Get the current run context
run = Run.get_context()

# Load the dataset
dataset = run.input_datasets["attrition_data"].to_pandas_dataframe()

# Data preprocessing
X = dataset.drop(columns=["Attrition"])
y = dataset["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
run.log("accuracy", accuracy)

# Save the model
os.makedirs("outputs", exist_ok=True)
joblib.dump(model, "outputs/model.joblib")

# Register the model
model = Model.register(
    workspace=run.experiment.workspace,
    model_path="outputs/model.joblib",
    model_name="employee_attrition_model",
)

run.complete()
