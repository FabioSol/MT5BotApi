import json
import os

module_path = os.path.dirname(__file__)

def get_hyperparams():
    with open(module_path+"/hyperparams.json", "r") as json_file:
        hyperparams_data = json.load(json_file)

    model_metadata = hyperparams_data.get("metadata")
    pipeline_params = hyperparams_data.get("pipeline_params")
    hyperparams = hyperparams_data.get("hyperparams")
    return model_metadata,pipeline_params,hyperparams

model_metadata,pipeline_params,hyperparams = get_hyperparams()

