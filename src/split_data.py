# split the raw data
# save it in data/processed folder
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from get_data import read_params


def split_and_saved_data(config_path):
    config = read_params(config_path)
    train_path = config["split_data"]["train_path"]
    test_path = config["split_data"]["test_path"]
    test_size = config["split_data"]["test_size"]
    raw_path = config["load_data"]["raw_dataset_csv"]
    random_state = config["base"]["random_state"]

    df = pd.read_csv(raw_path, sep=",", encoding="utf-8")
    train, test = train_test_split(df, test_size=test_size, random_state=random_state)
    train.to_csv(train_path, sep=",", encoding="utf-8", index=False)
    test.to_csv(test_path, sep=",", encoding="utf-8", index=False)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)