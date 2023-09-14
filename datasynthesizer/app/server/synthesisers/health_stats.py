import random
import secrets
from ..constants import *


def synthesise_health_stats(hour_of_the_day):
    generalHealthStats = {}

    stepCount = synthesise_step_count(hour_of_the_day)
    min_increment = secrets.randbelow(10)
    additional_steps = (min_increment + secrets.randbelow(100))
    stepCount = stepCount + additional_steps
    generalHealthStats['stepCount'] = stepCount

    bloodOxygenAvg = synthesise_blood_oxygen_level()
    generalHealthStats['bloodOxygenAvg'] = bloodOxygenAvg

    stress = synthesise_stress_score()
    generalHealthStats['stress'] = stress

    sleepHours = synthesise_sleep_hours()
    generalHealthStats['sleepHours'] = sleepHours

    REMsleepHours = synthesise_rem_sleep_hours()
    generalHealthStats['REMsleepHours'] = REMsleepHours

    caloriesBurnt = synthesise_calories_count(hour_of_the_day)
    min_increment = secrets.randbelow(20)
    decimal_increment = 0
    random_sign = secrets.randbelow(2)
    random_sign = random_sign if random_sign == 1 else -1
    decimal_increment += random_sign * random.random()
    additional_calories = (round(decimal_increment, 2) + min_increment + secrets.randbelow(200))
    caloriesBurnt = caloriesBurnt + additional_calories

    generalHealthStats['caloriesBurnt'] = caloriesBurnt

    return generalHealthStats


def synthesise_step_count(hour_of_the_day):
    if hour_of_the_day <= MORNING_HOUR:
        return secrets.randbelow(500)

    elif (hour_of_the_day > MORNING_HOUR) and (hour_of_the_day <= NOON_HOUR):
        return secrets.randbelow(8000)

    elif (hour_of_the_day > NOON_HOUR) and (hour_of_the_day <= EVENING_HOUR):
        return secrets.randbelow(15_000)

    elif hour_of_the_day > EVENING_HOUR:
        return secrets.randbelow(MAX_STEP_COUNT)


def synthesise_calories_count(hour_of_the_day):
    if hour_of_the_day <= MORNING_HOUR:
        return secrets.randbelow(200)

    elif (hour_of_the_day > MORNING_HOUR) and (hour_of_the_day <= NOON_HOUR):
        return secrets.randbelow(800)

    elif (hour_of_the_day > NOON_HOUR) and (hour_of_the_day <= EVENING_HOUR):
        return secrets.randbelow(1500)

    elif hour_of_the_day > EVENING_HOUR:
        return secrets.randbelow(MAX_CALORIES_BURNT)


def synthesise_blood_oxygen_level():
    bloodOxygenAvg = MIN_O2_AVG + secrets.randbelow(10)
    return bloodOxygenAvg


def synthesise_stress_score():
    stress = secrets.randbelow(5)
    return stress


def synthesise_sleep_hours():
    sleepHours = 4 + secrets.randbelow(6)
    minutes = 0
    random_sign = secrets.randbelow(2)
    random_sign = random_sign if random_sign == 1 else -1
    minutes += random_sign * round(random.random(), 2)
    sleepHours = sleepHours + minutes
    return sleepHours


def synthesise_rem_sleep_hours():
    REMsleepHours = secrets.randbelow(4)
    minutes = 0
    random_sign = secrets.randbelow(2)
    random_sign = random_sign if random_sign == 1 else -1
    minutes += random_sign * round(random.random(), 2)
    REMsleepHours += minutes
    if REMsleepHours <= MIN_REM_SLEEP_HOURS:
        REMsleepHours = MIN_REM_SLEEP_HOURS
    return REMsleepHours
