BASE_DIR = 'app/model'
DATA_SOURCE = '/machinelearningmodel/data'

CURRENT_MODEL_VERSION = "0.1.3"
DEFAULT_MODEL = "LATEST_MODEL"  # All new trained models will be saved here

FEATURES_IN_USE = ['stepCount', 'bloodOxygenAvg', 'stress', 'sleepHours', 'REMsleepHours',
                   'caloriesBurnt', 'heartRate', 'systolicBloodPressure',
                   'diastolicBloodPressure', 'bodyTemperature', 'breathingFrequency', 'healthState']

DEFAULT_HYPERPARAMETERS = {
    'max_depth': 9,
    'random_state': 15,
    'min_samples_split': 2
}
