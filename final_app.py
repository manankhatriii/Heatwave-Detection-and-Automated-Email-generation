import pandas as pd
import numpy as np
import joblib
import warnings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

model = joblib.load("Algorithms/MODEL.pkl")
scaler = joblib.load('Algorithms/scaler.pkl')

def preprocess_data(df):
    print("Preprocessing data.")

    for i in range(1, 8):
        df[f"MaxTemperature_lag_{i}"] = df["MaxTemperature"].shift(i)
        df[f"MinTemperature_lag_{i}"] = df["MinTemperature"].shift(i)
        df[f"RelHumidity_lag_{i}"] = df["RelHumidity"].shift(i)
        df[f"WindSpeed10_lag_{i}"] = df["WindSpeed10"].shift(i)
        df[f"SurfacePressure_lag_{i}"] = df["SurfacePressure"].shift(i)
        df[f"DewPoint_lag_{i}"] = df["DewPoint"].shift(i)
        df[f"WetBulbTemp_lag_{i}"] = df["WetBulbTemp"].shift(i)
        df[f"Precipitation_lag_{i}"] = df["Precipitation"].shift(i)

    for col in ['MaxTemperature', 'MinTemperature', 'RelHumidity', 'WindSpeed10', 'SurfacePressure', 'DewPoint', 'WetBulbTemp', 'Precipitation']:
        df[f"{col}_rolling_mean_7"] = df[col].rolling(window=7).mean()
    
    df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
    df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
    df['Day_sin'] = np.sin(2 * np.pi * df['Day'] / 31)
    df['Day_cos'] = np.cos(2 * np.pi * df['Day'] / 31)
    
    df.dropna(inplace=True)
    return df

def predict_heatwave(model, df):
    print("Predicting heatwave based on these 10 days")
    X = preprocess_data(df).tail(1)
    X_scaled = scaler.transform(X.drop(columns=['HEATWAVE', 'Year', 'Month', 'Day']))

    prediction = model.predict(X_scaled)
    probability = model.predict_proba(X_scaled)[:, 1]

    return prediction[0], probability[0]

filepath = input("Enter relative file path: ")
df = pd.read_csv(filepath)

heatwave_pred, heatwave_proba = predict_heatwave(model, df)
print(f"Heatwave Prediction: {heatwave_pred}, Probability: {heatwave_proba}")

mail_id = ["yiriva6008@polatrix.com"]
sender_id = "pythonwithmk@gmail.com"
sender_pass = "wnuelbqrqpylrwem"
subject = "Heatwave Alert!!!"
message = "A heatwave is predicted. Please take the necessary precautions for the same."

if heatwave_pred == 1:
    print("1")
    msg = MIMEMultipart()
    msg["From"] = sender_id
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        print("2")
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.starttls()
        print("3")
        smtpserver.login(sender_id, sender_pass)
        print("4")

        for email in mail_id:
            msg["To"] = email 
            text = msg.as_string()
            smtpserver.sendmail(sender_id, email, text)

        smtpserver.quit()
        print("Heatwave alert email sent successfully.")
    
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
    
else:
    print("No heatwave predicted.")
