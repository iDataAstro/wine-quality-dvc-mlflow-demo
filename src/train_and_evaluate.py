# load the train and test
# train algo
# save the metrices, params
import os
import argparse
import pandas as pd
import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import json

from get_data import read_params


def eval_metrics(y_test, y_pred):
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return rmse, mae, r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    train_path = config["split_data"]["train_path"]
    test_path = config["split_data"]["test_path"]
    model_dir = config["model_dir"]

    alpha = config["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = config["estimators"]["ElasticNet"]["params"]["l1_ratio"]

    target = [config["base"]["target_col"]]
    random_state = config["base"]["random_state"]

    train = pd.read_csv(train_path, sep=",", encoding="utf-8")
    test = pd.read_csv(test_path, sep=",", encoding="utf-8")

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    train_y = train[target]
    test_y = test[target]

    clf = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)
    clf.fit(train_x, train_y)

    preds = clf.predict(test_x)

    (rmse, mae, r2) = eval_metrics(test_y, preds)

    print(f"ElasticNet Model (alpth={alpha} l1_ratio={l1_ratio}")
    print(f"    RMSE: {rmse}")
    print(f"    MAE: {mae}")
    print(f"    R2: {r2}")

    ##############################################
    score_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    with open(score_file, "w") as f:
        scores = {"rmse": rmse, "mae": mae, "r2": r2}
        json.dump(scores, f, indent=4)

    with open(params_file, "w") as f:
        params = {"alpha": alpha, "l1_ratio": l1_ratio}
        json.dump(params, f, indent=4)

    ##############################################
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(clf, model_path)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)
