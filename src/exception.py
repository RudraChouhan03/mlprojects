import sys  # Import the sys module to access system-specific parameters and functions
from src.logger import logging  # Import the logging object from the custom logger module

# Define a function to get detailed error message information
def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()  # Get exception type, value, and traceback object
    file_name = exc_tb.tb_frame.f_code.co_filename  # Get the filename where the error occurred
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))  # Format the error message with file name, line number, and error

    return error_message  # Return the formatted error message

# Define a custom exception class that inherits from the built-in Exception class
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)  # Call the base class constructor with the error message
        self.error_message = error_message_detail(error_message, error_detail=error_detail)  # Store the detailed error message

    def __str__(self):
        return self.error_message  # Return the detailed error message when the exception is printed


        