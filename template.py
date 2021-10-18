import os

dirs = ["data_given", "src", "saved_models", os.path.join("data", "raw"), os.path.join("data", "processed")]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    gitkeep_path = os.path.join(dir_, ".gitkeep")
    with open(gitkeep_path, "w") as f:
        pass

files = ["config.yaml", "dvc.yaml", "params.yaml", ".gitignore", "README.md", "requirements.txt"]

for file_ in files:
    with open(file_, "w") as f:
        pass
