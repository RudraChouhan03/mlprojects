import sys  # Import sys for system-specific parameters and functions
import pandas as pd  # Import pandas for data manipulation
from src.exception import CustomException  # Import custom exception for error handling
from src.utils import load_object  # Import function to load saved objects


class PredictPipeline:
    def __init__(self):
        pass  # No initialization needed

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")  # Path to the saved model
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')  # Path to the saved preprocessor
            print("Before Loading")  # Print before loading objects
            model = load_object(file_path=model_path)  # Load the trained model
            preprocessor = load_object(file_path=preprocessor_path)  # Load the preprocessor
            print("After Loading")  # Print after loading objects
            data_scaled = preprocessor.transform(features)  # Transform input features
            preds = model.predict(data_scaled)  # Make predictions
            return preds  # Return predictions
        
        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if error occurs



class CustomData:
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender  # Store gender

        self.race_ethnicity = race_ethnicity  # Store race/ethnicity

        self.parental_level_of_education = parental_level_of_education  # Store parental education

        self.lunch = lunch  # Store lunch info

        self.test_preparation_course = test_preparation_course  # Store test prep info

        self.reading_score = reading_score  # Store reading score

        self.writing_score = writing_score  # Store writing score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],  # Add gender to dict
                "race_ethnicity": [self.race_ethnicity],  # Add race/ethnicity to dict
                "parental_level_of_education": [self.parental_level_of_education],  # Add parental education
                "lunch": [self.lunch],  # Add lunch info
                "test_preparation_course": [self.test_preparation_course],  # Add test prep info
                "reading_score": [self.reading_score],  # Add reading score
                "writing_score": [self.writing_score],  # Add writing score
            }

            return pd.DataFrame(custom_data_input_dict)  # Convert dict to DataFrame

        except Exception as e:
            raise CustomException(e, sys)  # Raise custom exception if error occurs