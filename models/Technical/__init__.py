import json
import os

module_path = os.path.dirname(__file__)


def get_hyperparams():
    with open(module_path + "/hyperparams.json", "r") as json_file:
        hyperparams = json.load(json_file)
    return hyperparams
