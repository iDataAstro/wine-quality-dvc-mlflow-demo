import os
import yaml
import json
import joblib
import numpy as np


param_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_min_max.json")


class NotInRange(Exception):
    def __init__(self, message="Value must be in valid range"):
        self.message = message
        super().__init__(self.message)


class NotInCols(Exception):
    def __init__(self, message="Not in columns"):
        self.message = message
        super().__init__(self.message)


def read_params(config_path=param_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def predict(data):
    config = read_params(param_path)
    model_path = config["webapp_model_dir"]
    model = joblib.load(model_path)
    prediction = model.predict(data).tolist()[0]
    try:
        if 3 <= prediction <= 8:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected result!!"


def get_schema(schema_file_path=schema_path):
    with open(schema_file_path) as json_file:
        schema = json.load(json_file)
    return schema


def validate_input(dict_request):
    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()

        if not (schema[col]["min"] <= float(val) <= schema[col]["max"]):
            raise NotInRange

    for col, val in dict_request.items():
        _validate_cols(col)
        _validate_values(col, val)

    return True


def form_response(dict_request):
    try:
        if validate_input(dict_request):
            data = [list(map(float, dict_request.values()))]
            response = {"response": predict(data)}
            return response
    except NotInRange as e:
        return {"the_exected_range": get_schema(), "response": str(e)}
    except NotInCols as e:
        return {"the_exected_cols": get_schema().keys(), "response": str(e)}
    except Exception as e:
        return {"response": str(e)}


def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.values())])
            response = {"response": predict(data)}
            return response
    except NotInRange as e:
        return {"the_exected_range": get_schema(), "response": str(e)}
    except NotInCols as e:
        return {"the_exected_cols": get_schema().keys(), "response": str(e)}
    except Exception as e:
        return {"response": str(e)}
