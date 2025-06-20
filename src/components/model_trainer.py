import os  # Import os for file and directory operations
import sys  # Import sys for system-specific parameters
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from dataclasses import dataclass  # Import dataclass for easy class creation

from catboost import CatBoostRegressor  # Import CatBoostRegressor model
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)  # Import ensemble models
from sklearn.linear_model import LinearRegression  # Import linear regression model
from sklearn.metrics import r2_score  # Import r2_score for model evaluation
from sklearn.neighbors import KNeighborsRegressor  # Import KNN regressor (not used here)
from sklearn.tree import DecisionTreeRegressor  # Import decision tree regressor
from xgboost import XGBRegressor  # Import XGBoost regressor

from src.exception import CustomException  # Import custom exception for error handling
from src.logger import logging  # Import logging for logging messages

from src.utils import save_object, evaluate_models  # Import utility functions

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")  # Path to save the trained model

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()  # Initialize config

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")  # Log data splitting
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],  # Features from train data
                train_array[:, -1],   # Target from train data
                test_array[:, :-1],   # Features from test data
                test_array[:, -1]     # Target from test data
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False), # CatBoostRegressor is unique because it can handle categorical features automatically. It uses ordered boosting to reduce overfitting and often works well
                "AdaBoost Regressor": AdaBoostRegressor(),
            }  # Dictionary of models to train
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }  # Hyperparameters for each model

            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
                models=models, param=params
            )  # Evaluate all models and get their scores

            # Get the best model score from the report
            best_model_score = max(sorted(model_report.values()))

            # Get the name of the best model
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]  # Get the best model object

            if best_model_score < 0.6:
                raise CustomException("No best model found")  # Raise error if no good model found
            logging.info(f"Best found model on both training and testing dataset")  # Log best model found

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )  # Save the best model to file

            predicted = best_model.predict(X_test)  # Predict on test data

            r2_square = r2_score(y_test, predicted)  # Calculate R2 score for predictions
            return r2_square  # Return the R2 score

        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if error occurs