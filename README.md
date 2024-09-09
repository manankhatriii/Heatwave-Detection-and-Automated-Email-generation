# Heatwave-Detection-and-Automated-Email-generation

This project focuses on predicting heatwave events based on historical weather data and sending timely alerts via email. It uses machine learning models to analyze weather patterns and provides a prediction if a heatwave is expected the next day.

Features:
Data Preprocessing: Includes lag features and rolling averages of weather parameters (temperature, humidity, etc.) for prediction.
Heatwave Prediction: Predicts the likelihood of a heatwave using a trained machine learning model.
Email Alerts: Sends automated email alerts to a list of recipients if a heatwave is predicted.
Files:
final_app.py: Main script to make predictions on weather data and send email alerts.
Algorithms/MODEL.pkl: Pretrained machine learning model for heatwave prediction.
Algorithms/scaler.pkl: Scaler to standardize input data before prediction.
How to Use:
Ensure the MODEL.pkl and scaler.pkl are placed in the Algorithms/ directory.
Run the script final_app.py and provide the path to the weather data file when prompted.
If a heatwave is predicted, the system will automatically send an email to the specified recipients.
Email Settings:
Set your Gmail address and an app-specific password in the script.
Update the mail_id list with the email addresses of the recipients.
Requirements:
Python 3.x
Required libraries: pandas, numpy, joblib, smtplib, sklearn
