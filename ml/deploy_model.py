from azureml.core import Workspace, Model, Environment
from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import InferenceConfig

# Initialize workspace
ws = Workspace.from_config()

# Get the registered model
model = Model(ws, "employee_attrition_model")

# Create environment
env = Environment.from_conda_specification(
    name="project_environment", file_path="environment.yml"
)

# Create inference configuration
inference_config = InferenceConfig(entry_script="score.py", environment=env)

# Define the deployment configuration
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

# Deploy the model
service = Model.deploy(
    workspace=ws,
    name="attrition-service",
    models=[model],
    inference_config=inference_config,
    deployment_config=aci_config,
)
service.wait_for_deployment(show_output=True)
