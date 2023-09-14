import random
import secrets
from .constants import *
from .helpers import fetch_random_date
from .synthesisers.event import synthesise_event_details
from .synthesisers.health_stats import synthesise_health_stats, synthesise_step_count, synthesise_calories_count, \
    synthesise_sleep_hours, synthesise_rem_sleep_hours, synthesise_blood_oxygen_level, synthesise_stress_score
from .synthesisers.label import generate_labels_for_data
from .synthesisers.user import synthesise_user_data
from .synthesisers.vitals import synthesise_vitals, synthesise_body_temperature, synthesise_heart_rate, \
    synthesise_systolic_blood_pressure, synthesise_diastolic_blood_pressure, synthesise_breathing_frequency

random.seed(8)


def synthesise_data_for_ui(start_time, end_time):
    return synthesise_core(start_time=start_time, end_time=end_time, generate_multiple_records=False,
                          generate_labels=True)


def synthesise_data_for_training(start_time, end_time):
    return synthesise_core(start_time=start_time, end_time=end_time, generate_multiple_records=True,
                          generate_labels=True, generate_user=True)


def synthesise_data_auto_call(start_time):
    return synthesise_core(start_time=start_time, generate_multiple_records=False, generate_labels=False)


def synthesise_bulk(event_data, start_time, end_time, generate_labels, generate_user, n_users=100):

    for _ in range(n_users):
        user = {}
        # generate user
        if generate_user:
            user = synthesise_user_data(user=user)

        # intervals: number of periods where data is captured
        # pick random number of time intervals (1,10)
        intervals = 1 + secrets.randbelow(10)
        for _ in range(intervals):

            interval_records = secrets.randbelow(30)

            start_date = start_time
            end_date = end_time

            first_ts = fetch_random_date(start_date, end_date)
            event_ts = first_ts
            hour_of_the_day = event_ts.hour

            # These health stats are monotonically increasing for the day, so they are generated outside the loop
            stepCount = synthesise_step_count(hour_of_the_day)
            caloriesBurnt = synthesise_calories_count(hour_of_the_day)

            # These health stats remain the same for the same day, so they are generated outside the loop
            sleepHours = synthesise_sleep_hours()
            REMsleepHours = synthesise_rem_sleep_hours()
            bodyTemperature = synthesise_body_temperature()

            # interval_records: number of records present in each period
            # pick random number of timestamps between start and end date for all intervals
            for _ in range(interval_records):
                event = {}
                vitals = {}
                generalHealthStats = {}

                if generate_user:
                    event['user'] = user

                # generate event details
                event = synthesise_event_details(event, start_time, end_time, event_ts)

                # generate vitals
                heartRate = synthesise_heart_rate()
                vitals['heartRate'] = heartRate

                systolicBloodPressure = synthesise_systolic_blood_pressure()
                vitals['systolicBloodPressure'] = systolicBloodPressure

                diastolicBloodPressure = synthesise_diastolic_blood_pressure()
                vitals['diastolicBloodPressure'] = diastolicBloodPressure

                random_sign = secrets.randbelow(2)
                random_sign = random_sign if random_sign == 1 else -1
                bodyTemperature += random_sign * round(random.random(), 2)
                bodyTemperature = round(bodyTemperature, 2)
                if bodyTemperature <= MIN_TEMPERATURE:
                    bodyTemperature = MIN_TEMPERATURE
                elif bodyTemperature >= MAX_TEMPERATURE:
                    bodyTemperature = MAX_TEMPERATURE
                vitals['bodyTemperature'] = bodyTemperature

                breathingFrequency = synthesise_breathing_frequency()
                vitals['breathingFrequency'] = breathingFrequency

                event['vitals'] = vitals

                # generate generalHealthStats
                min_increment = secrets.randbelow(10)
                additional_steps = (min_increment + secrets.randbelow(100))
                stepCount = stepCount + additional_steps
                generalHealthStats['stepCount'] = stepCount

                bloodOxygenAvg = synthesise_blood_oxygen_level()
                generalHealthStats['bloodOxygenAvg'] = bloodOxygenAvg

                stress = synthesise_stress_score()
                generalHealthStats['stress'] = stress

                generalHealthStats['sleepHours'] = sleepHours

                generalHealthStats['REMsleepHours'] = REMsleepHours

                min_increment = secrets.randbelow(20)
                additional_calories = (min_increment + secrets.randbelow(200))
                caloriesBurnt = caloriesBurnt + additional_calories
                generalHealthStats['caloriesBurnt'] = caloriesBurnt

                event['generalHealthStats'] = generalHealthStats
                eventId = event.get('eventId')
                event_data[f'{eventId}'] = event

    if generate_labels:
        event_data = generate_labels_for_data(event_data, generate_user=generate_user)
    return event_data


def synthesise_core(start_time, end_time=None, generate_multiple_records=False, generate_labels=False, generate_user=False, n_users=100):
    event_data = {}
    user = {}

    if generate_multiple_records:
        return synthesise_bulk(event_data=event_data, start_time=start_time, end_time=end_time,
                                       generate_labels=generate_labels, generate_user=generate_user, n_users=n_users)

    else:
        # generate random timestamp between (start, end)
        first_ts = fetch_random_date(start=start_time, end=end_time)
        event_ts = first_ts
        hour_of_the_day = event_ts.hour

        event = {}
        # generate event related details
        if end_time is None:
            end_time = start_time
        event = synthesise_event_details(event, start_time, end_time, event_ts)

        # generate user information
        if generate_user:
            user = synthesise_user_data(user)

        event['user'] = user
        # generate vitals
        event['vitals'] = synthesise_vitals()

        # generate health stats
        event['generalHealthStats'] = synthesise_health_stats(hour_of_the_day)

        eventId = event.get('eventId')
        event_data[f'{eventId}'] = event

        if generate_labels:
            return generate_labels_for_data(event_data, generate_user=generate_user)[0]

        return event_data[eventId]
