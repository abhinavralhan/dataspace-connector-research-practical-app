import pandas as pd
from fastapi import FastAPI, Request
from .constants import FEATURES_IN_USE, DATA_SOURCE
from .model import DecisionTreeModel
import logging
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


app = FastAPI()
model = DecisionTreeModel()

# curl -X POST "http://0.0.0.0:8000/synthesise_data_for_ui/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"start_time\":\"31/01/2022\", \"end_time\":\"01/02/2022\"}"

# Sample Endpoint usage

# curl -X GET "http://0.0.0.0:8000/"
# curl -X GET "http://0.0.0.0:8000/get_hyperparameters/"
# curl -X GET "http://0.0.0.0:8000/train/"
# curl -X POST "http://0.0.0.0:8000/predict/" -H  "accept: application/json" -H  "Content-Type: application/json" -d @request_healthy_user.json
# curl -X POST "http://0.0.0.0:8000/set_hyperparameters/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"criterion\":\"entropy\", \"max_depth\":9, \"random_state\":15,\"min_samples_split\":5}"


# Request Data
# {
# 	"eventId": "244ca386-89a5-4b7e-8ac4-4b7dd4fee74e",
# 	"eventTimestamp": "1/12/2022 08:20:43",
# 	"dataSource": "app",
# 	"healthState": "good",
# 	"generalHealthStats": {
# 		"stepCount": 4070,
# 		"stress": 3,
# 		"bloodOxygenAvg": 95,
# 		"sleepHours": 8.4,
# 		"REMsleepHours": 4.1,
# 		"caloriesBurnt": 2006.8
# 	},
# 	"user": {
# 		"user_id": "fdde5bd5-1146-48df-94ef-d56532290901",
# 		"firstname": "john",
# 		"lastname": "doe",
# 		"gender": "male",
# 		"age": 33,
# 		"weight(kg)": 80,
# 		"height(cm)": 176
# 	},
# 	"vitals": {
# 		"heartRate": 71,
# 		"systolicBloodPressure": 135,
# 		"diastolicBloodPressure": 73,
# 		"bodyTemperature": 99.6,
# 		"breathingFrequency": 15
# 	}
# }

# Response Data
# {'healthState': "Healthy"}

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World"}


@app.get('/train/')
async def train_model():
    dataset = pd.read_csv(f"{DATA_SOURCE}/time_series_dump_v3.csv")
    dataset = dataset[FEATURES_IN_USE]
    model.train(dataset)
    return {"message": "Model successfully updated. Ready for prediction."}


@app.post('/predict/')
async def predict_label(request_data: Request):
    data = await request_data.json()

    stepCount = data.get('generalHealthStats').get('stepCount')
    bloodOxygenAvg = data.get('generalHealthStats').get('bloodOxygenAvg')
    stress = data.get('generalHealthStats').get('stress')
    sleepHours = data.get('generalHealthStats').get('sleepHours')
    REMsleepHours = data.get('generalHealthStats').get('REMsleepHours')
    caloriesBurnt = data.get('generalHealthStats').get('caloriesBurnt')
    heartRate = data.get('vitals').get('heartRate')
    systolicBloodPressure = data.get('vitals').get('systolicBloodPressure')
    diastolicBloodPressure = data.get('vitals').get('diastolicBloodPressure')
    bodyTemperature = data.get('vitals').get('bodyTemperature')
    breathingFrequency = data.get('vitals').get('breathingFrequency')

    prediction = model.predict([[stepCount, bloodOxygenAvg, stress, sleepHours, REMsleepHours,
                                 caloriesBurnt, heartRate, systolicBloodPressure, diastolicBloodPressure,
                                 bodyTemperature, breathingFrequency]])

    print(prediction)

    if prediction == "good":
        prediction = "Healthy"
    else:
        prediction = "Risky"

    prediction = {'healthState': prediction}
    data.update(prediction)
    logging.info(f"Prediction completed: {prediction}")
    return data


@app.get('/get_hyperparameters/')
async def get_hyperparameters():
    return model.hyperparameters


@app.post('/set_hyperparameters/')
async def set_hyperparameters(request_data: Request):
    data = await request_data.json()
    if type(data) is dict and data != {}:
        model.hyperparameters = data

    return {"message": "Succesfully set hyperparameters"}
