from flask import Flask, request, render_template  # Import Flask and related modules for web app
import numpy as np  # Import numpy for numerical operations
import pandas as pd  # Import pandas for data manipulation

from sklearn.preprocessing import StandardScaler  # Import scaler (not used here)
from src.pipeline.predict_pipeline import CustomData, PredictPipeline  # Import custom data and prediction pipeline

application = Flask(__name__)  # Create a Flask web application

app = application  # Assign the app variable

## Route for a home page

@app.route('/')  # Define the route for the main page
def index():
    return render_template('index.html')  # Render the index.html template

@app.route('/predictdata', methods=['GET', 'POST'])  # Route for prediction page
def predict_datapoint():
    if request.method == 'GET':  # If the request is GET, show the form
        return render_template('home.html')  # Render the home.html template
    else:  # If the request is POST, process the form data
        data = CustomData(
            gender=request.form.get('gender'),  # Get gender from form
            race_ethnicity=request.form.get('ethnicity'),  # Get ethnicity from form
            parental_level_of_education=request.form.get('parental_level_of_education'),  # Get education level
            lunch=request.form.get('lunch'),  # Get lunch info
            test_preparation_course=request.form.get('test_preparation_course'),  # Get test prep info
            reading_score=float(request.form.get('writing_score')),  # Get writing score (note: swapped)
            writing_score=float(request.form.get('reading_score'))  # Get reading score (note: swapped)
        )
        
        pred_df = data.get_data_as_data_frame()  # Convert input data to DataFrame
        print(pred_df)  # Print the DataFrame for debugging

        predict_pipeline = PredictPipeline()  # Create prediction pipeline object
        results = predict_pipeline.predict(pred_df)  # Make prediction
        return render_template('home.html', results=results[0])  # Show result on the page
    

if __name__ == "__main__":      
    app.run(host="0.0.0.0", port=80)  # Run the Flask app on port 80