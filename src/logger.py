import logging  # Import the logging module to enable logging in the application
import os  # Import the os module to interact with the operating system
from datetime import datetime  # Import datetime to get the current date and time

# Create a log file name with the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the path for the logs directory and the log file
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Create the logs directory if it doesn't exist
os.makedirs(logs_path, exist_ok=True)

# Set the full path for the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure the logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Set the log file path
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Set the log message format
    level=logging.INFO,  # Set the logging level to INFO
)
'''
This code is created to set up a logging system for your project. Logging helps you:

Track events and errors that happen when your code runs.
Save detailed information (like time, file, line number, and error message) to a log file.
Make debugging and monitoring easier by keeping a record of what happened and when.
The code automatically creates a new log file with a timestamp in its name, stores it in a logs folder, 
and formats each log entry for clarity. This is useful for troubleshooting and maintaining your project.
'''