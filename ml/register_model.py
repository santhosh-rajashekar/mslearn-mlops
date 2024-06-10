import joblib
from azureml.core import Run, Model

run = Run.get_context()

# Register the model
model = Model.register(
    workspace=run.experiment.workspace,
    model_path="outputs/model.joblib",
    model_name="employee_attrition_model",
)
