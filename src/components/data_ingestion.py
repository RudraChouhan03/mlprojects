# components folder means modules which we are going to use it in our project
# data_ingestion.py file is created to read the data from the source (which can be database or any other source) and split it into train and test data

import os  # Import os module for file and directory operations
import sys  # it is used to interact with the Python system and control your program's behavior more directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.exception import CustomException  # Import custom exception class for better error handling
from src.logger import logging  # Import logging for logging messages
import pandas as pd  # Import pandas for data manipulation

from sklearn.model_selection import train_test_split  # Import function to split data into train and test sets
from dataclasses import dataclass  # Import dataclass for easy class creation

from src.components.data_transformation import DataTransformation  # Import data transformation class
from src.components.data_transformation import DataTransformationConfig  # Import data transformation config

from src.components.model_trainer import ModelTrainerConfig  # Import model trainer config
from src.components.model_trainer import ModelTrainer  # Import model trainer class

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")  # Path to save train data
    test_data_path: str = os.path.join('artifacts', "test.csv")  # Path to save test data
    raw_data_path: str = os.path.join('artifacts', "data.csv")  # Path to save raw data

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()  # Initialize config with file paths

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")  # Log start of ingestion
        try:
            df = pd.read_csv(r'D:\Data Science\Complete-Data-Science-With-Machine-Learning-And-NLP-2024-main\24-End To End ML Project With Deployment\Student Performance Project\notebook\data\stud.csv')  # Read the dataset into a DataFrame
            logging.info('Read the dataset as dataframe')  # Log successful read

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)  # Create artifacts directory if it doesn't exist

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)  # Save raw data to CSV

            logging.info("Train test split initiated")  # Log start of train-test split
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)  # Split data into train and test sets

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)  # Save train set to CSV

            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)  # Save test set to CSV

            logging.info("Ingestion of the data is completed")  # Log completion of ingestion

            return (
                self.ingestion_config.train_data_path,  # Return train data path
                self.ingestion_config.test_data_path    # Return test data path
            )
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if error occurs
        
if __name__ == "__main__":
    obj = DataIngestion()  # Create DataIngestion object
    train_data, test_data = obj.initiate_data_ingestion()  # Start data ingestion and get file paths

    data_transformation = DataTransformation()  # Create DataTransformation object
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)  # Transform data

    modeltrainer = ModelTrainer()  # Create ModelTrainer object
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))  # Train model and print result