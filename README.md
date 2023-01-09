# Wadhwani AI - WIAI_Farmer_App

Problem Statement: ***We are provided a list of farmer names and other relevant details in a csv file that needs to be translated into multiple languages for display in the application.***

### Basic Details about the project:
Framework and Database: **FastAPI and SQLite (Default)**

External APIs Used: **Google Translate APIs** [Link](https://cloud.google.com/translate/docs/basic/translate-text-basic)

### Assumption:
**Keeping the default password as "temp@123" for users in csv and the phone number is used as the username for the model**

Note: To get a idea about the project please go through the API Documentation.pdf file for better understanding.

### To use the project in your local machine

## Create a folder for the project and get to the folder
```
mkdir WIAI
cd WIAI
```

## Clone the project
```
(HTTPS)
git clone https://github.com/ankurRangi/wiai_farmer_app.git
```

```
(SSH)
git clone git@github.com:ankurRangi/wiai_farmer_app.git
```

## Create your virtual environment to intall the libraries
```
python -m venv wai-env
```

## Start the virtual env
```
(Windows)
wai-env\Scripts\activate.dat
```

```
(Linux)
source wai-env\scripts\activate
```

## After the virtual environment is active and running, install the requirements

```
(wai-env) D:\WIAI> pip install -r requirements.tx
```

## Before you start with the project, add the necessary files including,
```
farmerdb.db
data.csv
translateKey.json
keys.py
```

## Now you are ready to start with the project, use the following command,
```
uvicorn WIAI_Farmer.main:app --reload
```

## Now head over to your browser to play with the APIs,
```
http://127.0.0.1:8000/docs
```

## To test the project, Add the following files in the top directory,
```
test_data.csv
test_db.db
```

## And now to finally run the tests,
```
Press 'ctrl + c'
pytest
```

Note: To ignore the deprecation warning, use the command below,
```
(wai-env) D:\Work\WIAI>pytest -W ignore::DeprecationWarning
```





