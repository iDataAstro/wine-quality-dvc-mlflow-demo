# read the data from data source
# save it in the data/raw for further process
import argparse
from get_data import read_params, get_data


def load_and_save(config_path):
    config = read_params(config_path)
    df = get_data(config_path)
    raw_dataset_csv = config["load_data"]["raw_dataset_csv"]
    new_cols = [cols.replace(" ", "_") for cols in df.columns]
    df.to_csv(raw_dataset_csv, index=False, header=new_cols)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)
