import sys  # Import sys module for system-specific parameters and functions
from dataclasses import dataclass  # Import dataclass for easy class creation

import numpy as np  # Import numpy for numerical operations
import pandas as pd  # Import pandas for data manipulation
from sklearn.compose import ColumnTransformer  # Import ColumnTransformer for preprocessing columns
from sklearn.impute import SimpleImputer  # Import SimpleImputer to handle missing values
from sklearn.pipeline import Pipeline  # Import Pipeline to chain preprocessing steps
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # Import encoders and scalers

from src.exception import CustomException  # Import custom exception for error handling
from src.logger import logging  # Import logging for logging messages
import os  # Import os for file and directory operations

from src.utils import save_object  # Import save_object utility to save objects

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "proprocessor.pkl")  # Path to save the preprocessor object

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()  # Initialize config

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]  # List of numerical columns
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]  # List of categorical columns

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # Fill missing values with median
                    ("scaler", StandardScaler())  # Scale numerical features
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),  # Fill missing values with most frequent value
                    ("one_hot_encoder", OneHotEncoder()),  # Convert categorical columns to one-hot encoding
                    ("scaler", StandardScaler(with_mean=False))  # Scale encoded features
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")  # Log categorical columns
            logging.info(f"Numerical columns: {numerical_columns}")  # Log numerical columns

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),  # Apply num_pipeline to numerical columns
                    ("cat_pipelines", cat_pipeline, categorical_columns)  # Apply cat_pipeline to categorical columns
                ]
            )

            return preprocessor  # Return the preprocessor object
        
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if error occurs
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)  # Read training data from CSV
            test_df = pd.read_csv(test_path)  # Read testing data from CSV

            logging.info("Read train and test data completed")  # Log data read completion

            logging.info("Obtaining preprocessing object")  # Log preprocessing object creation

            preprocessing_obj = self.get_data_transformer_object()  # Get the preprocessor object

            target_column_name = "math_score"  # Name of the target column
            numerical_columns = ["writing_score", "reading_score"]  # List of numerical columns

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)  # Drop target column from train data
            target_feature_train_df = train_df[target_column_name]  # Get target column from train data

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)  # Drop target column from test data
            target_feature_test_df = test_df[target_column_name]  # Get target column from test data

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )  # Log preprocessing application

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)  # Fit and transform train features
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)  # Transform test features

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]  # Combine processed train features and target
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]  # Combine processed test features and target

            logging.info(f"Saved preprocessing object.")  # Log saving of preprocessor

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,  # Path to save preprocessor
                obj=preprocessing_obj  # Preprocessor object to save
            )

            return (
                train_arr,  # Return processed train array
                test_arr,  # Return processed test array
                self.data_transformation_config.preprocessor_obj_file_path,  # Return path to preprocessor object
            )
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if error occurs