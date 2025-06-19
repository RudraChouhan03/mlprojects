import os  # Import os for file and directory operations
import sys  # Import sys for system-specific parameters

import numpy as np  # Import numpy for numerical operations
import pandas as pd  # Import pandas for data manipulation
import dill  # Import dill for advanced object serialization (not used here)
import pickle  # Import pickle for saving and loading Python objects
from sklearn.metrics import r2_score  # Import r2_score for model evaluation
from sklearn.model_selection import GridSearchCV  # Import GridSearchCV for hyperparameter tuning

from src.exception import CustomException  # Import custom exception for error handling

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)  # Get the directory path from the file path

        os.makedirs(dir_path, exist_ok=True)  # Create the directory if it doesn't exist

        with open(file_path, "wb") as file_obj:  # Open the file in write-binary mode
            pickle.dump(obj, file_obj)  # Save the object using pickle

    except Exception as e:
        raise CustomException(e, sys)  # Raise custom exception if error occurs
    
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}  # Dictionary to store model scores

        for i in range(len(list(models))):  # Loop through each model
            model = list(models.values())[i]  # Get the model
            para = param[list(models.keys())[i]]  # Get the parameters for the model

            gs = GridSearchCV(model, para, cv=3)  # Create GridSearchCV object
            gs.fit(X_train, y_train)  # Fit GridSearchCV to training data

            model.set_params(**gs.best_params_)  # Set the best parameters to the model
            model.fit(X_train, y_train)  # Train the model with best parameters

            y_train_pred = model.predict(X_train)  # Predict on training data

            y_test_pred = model.predict(X_test)  # Predict on test data

            train_model_score = r2_score(y_train, y_train_pred)  # Calculate R2 score for train data

            test_model_score = r2_score(y_test, y_test_pred)  # Calculate R2 score for test data

            report[list(models.keys())[i]] = test_model_score  # Store test score in report

        return report  # Return the report dictionary

    except Exception as e:
        raise CustomException(e, sys)  # Raise custom exception if error occurs
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:  # Open the file in read-binary mode
            return pickle.load(file_obj)  # Load and return the object

    except Exception as e:
        raise CustomException(e, sys)  # Raise custom exception if error occurs