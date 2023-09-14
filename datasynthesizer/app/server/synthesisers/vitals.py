import random
import secrets
from ..constants import *


def synthesise_vitals():
    vitals = {}

    heartRate = synthesise_heart_rate()
    vitals['heartRate'] = heartRate

    systolicBloodPressure = synthesise_systolic_blood_pressure()
    vitals['systolicBloodPressure'] = systolicBloodPressure

    diastolicBloodPressure = synthesise_diastolic_blood_pressure()
    vitals['diastolicBloodPressure'] = diastolicBloodPressure

    bodyTemperature = synthesise_body_temperature()
    vitals['bodyTemperature'] = bodyTemperature

    breathingFrequency = synthesise_breathing_frequency()
    vitals['breathingFrequency'] = breathingFrequency

    return vitals


def synthesise_breathing_frequency():
    breathingFrequency = MIN_BREATH_FREQUENCY + secrets.randbelow(12)
    return breathingFrequency


def synthesise_body_temperature():
    bodyTemperature = BASE_TEMPERATURE + secrets.randbelow(3)
    random_sign = secrets.randbelow(2)
    random_sign = random_sign if random_sign == 1 else -1
    bodyTemperature += random_sign * round(random.random(), 2)
    bodyTemperature = round(bodyTemperature, 2)
    if bodyTemperature <= MIN_TEMPERATURE:
        bodyTemperature = MIN_TEMPERATURE
    elif bodyTemperature >= MAX_TEMPERATURE:
        bodyTemperature = MAX_TEMPERATURE
    return bodyTemperature


def synthesise_diastolic_blood_pressure():
    return MIN_DIA_BP + secrets.randbelow(40)


def synthesise_systolic_blood_pressure():
    return MIN_SYS_BP + secrets.randbelow(40)


def synthesise_heart_rate():
    return MIN_HEART_RATE + secrets.randbelow(100)