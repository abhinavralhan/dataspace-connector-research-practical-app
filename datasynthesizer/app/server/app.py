from fastapi import FastAPI, Request
from datetime import datetime, timedelta
from .constants import DATE_FORMAT, DATE_AND_TIME_FORMAT
from .synthesise_data_v1 import synthesise_data_for_ui, synthesise_data_for_training, synthesise_data_auto_call

app = FastAPI()

# Request Data
# {
#   "start_time": "31/01/2022 12:23:31",
#   "end_time": "01/02/2022"
# }

# Sample Request:
# curl -X POST "http://0.0.0.0:8000/synthesise_data_for_ui/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"start_time\":\"31/01/2022\", \"end_time\":\"01/02/2022\"}"
# curl -X POST "http://0.0.0.0:8000/synthesise_data_auto_call/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"start_time\":\"31/01/2022 12:23:31\"}"


# Response Data
# {
# 	"eventId": "244ca386-89a5-4b7e-8ac4-4b7dd4fee74e",
# 	"eventTimestamp": "1/12/2022 08:20:43",
# 	"dataSource": "app",
# 	"healthState": "good",
# 	"generalHealthStats": {
# 		"stepCount": 4000,
# 		"stress": 3,
# 		"bloodOxygen": 95,
# 		"sleepHours": 8,
# 		"REMsleepHours": 4,
# 		"caloriesBurnt": 2000
# 	},
# 	"user": {
# 		"user_id": "fdde5bd5-1146-48df-94ef-d56532290901",
# 		"firstname": "john",
# 		"lastname": "doe",
# 		"gender": "male",
# 		"age": 23,
# 		"weight": 88,
# 		"height": 176
# 	},
# 	"vitals": {
# 		"heartRate": 72,
# 		"systolicBloodPressure": 130,
# 		"diastolicBloodPressure": 70,
# 		"bodyTemperature": 98.6,
# 		"breathingFrequency": 15
# 	}
# }


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello World"}


@app.post("/synthesise_data_for_ui/")
async def call_from_ui(request_data: Request):
    request_data = await request_data.json()
    start_time = datetime.strptime(request_data.get("start_time"), DATE_FORMAT) or datetime.now() - timedelta(minutes=10)
    end_time = datetime.strptime(request_data.get("end_time"), DATE_FORMAT) or datetime.now()
    return synthesise_data_for_ui(start_time=start_time, end_time=end_time)


@app.post("/synthesise_data_for_training/")
async def call_from_training(request_data: Request):
    request_data = await request_data.json()
    start_time = datetime.strptime(request_data.get("start_time"), DATE_FORMAT) or datetime.now() - timedelta(minutes=10)
    end_time = datetime.strptime(request_data.get("end_time"), DATE_FORMAT) or datetime.now()
    return synthesise_data_for_training(start_time=start_time, end_time=end_time)


@app.post("/synthesise_data_auto_call/")
async def call_from_auto_call(request_data: Request):
    request_data = await request_data.json()
    start_time = datetime.strptime(request_data.get("start_time"), DATE_AND_TIME_FORMAT) or datetime.now() - timedelta(minutes=10)
    return synthesise_data_auto_call(start_time=start_time)
