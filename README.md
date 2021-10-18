# wine quality test

## install packages
```bash
pip install -r requirements.txt
```

## create repo
```bash
git init
```

## dvc init
```bash
dvc init
```
## add data to dvc 
```bash
dvc add data_given/winequality.csv
```

## commit to remote repo
1. first create empty repo on github
2. change your local branch name from "master" to "main"
```bash
git branch -m main
```
3. commit to remote branch
```bash
git add .
git commit -m "first commit"
git remote add origin https://github.com/jrk90210us/wine-quality-dvc-mlflow-demo.git
```
## using dvc 
1. create dvc.yaml file with different stages
2. now reproduce all stages by following command
```bash
dvc repro
```
3. check diff metrics with dvc
```bash
dvc metrics show
```
4. check difference in metrics with dvc
```bash
dvc metrics diff
```

## move back to previous commit
1. copy the previous commit id from github.com/<user>/<repo>
2. move back with following command
```bash 
git checkout <commit id>
git checkout 2fc38c2ec265b4b8b4f51284ffe4f8bebbe1a27d
```
3. to discard previous checkout and to go back to current commit
```bash
git switch -
```

## using `pytest`
1. install pytest package with pip
2. create `tests` directory 
```bash
pip install pytest
mkdir tests
```
3. create test files in `tests` dir
> Note: All test files start with `test_` prefix
```bash
touch tests/__init__.py
touch tests/test_config.py
```
4. to test with `pytest`
```bash
pytest -v
```

## using `tox`
1. install tox package with pip
2. create `tox.ini` file for configuration
```bash
touch tox.ini
```
3. Add following lines to tox.ini configuration
```bash
[tox]
envlist = py37 ; define environment 
skipsdist = True ; skip local package if setup.py not defined

[testenv]
deps = -rrequirements.txt ; create new venv and install packages
commands =
    pytest -v ; test command
```
4. run test with `tox`
```bash
tox
```
4. run test with `tox` with reinstalling dependencies
```bash
tox -r
```