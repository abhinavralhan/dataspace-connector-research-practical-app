import pandas as pd
from ..constants import *


def generate_labels_for_data(event_data, generate_user):
    df_records = pd.DataFrame(event_data).T.reset_index(drop=True)

    if generate_user:
        df_records = pd.concat([df_records,
                                df_records['generalHealthStats'].apply(lambda x: pd.Series(x)),
                                df_records['user'].apply(lambda x: pd.Series(x)),
                                df_records['vitals'].apply(lambda x: pd.Series(x))
                                ], axis=1)
        columns_to_retain = ['user', 'vitals', 'generalHealthStats', 'dataSource', 'eventId', 'eventTimestamp', 'healthState']
    else:
        df_records = pd.concat([df_records,
                                df_records['generalHealthStats'].apply(lambda x: pd.Series(x)),
                                df_records['vitals'].apply(lambda x: pd.Series(x))
                                ], axis=1)
        columns_to_retain = ['vitals', 'generalHealthStats', 'dataSource', 'eventId', 'eventTimestamp', 'healthState']

    df_records['healthState'] = ''
    df_records.loc[(df_records['heartRate'] <= HEART_RATE_LB) |
                   (df_records['heartRate'] >= HEART_RATE_UB) |

                   (df_records['systolicBloodPressure'] <= SYS_BP_LB) |
                   (df_records['systolicBloodPressure'] >= SYS_BP_UB) |

                   (df_records['diastolicBloodPressure'] <= DIA_BP_LB) |
                   (df_records['diastolicBloodPressure'] >= DIA_BP_UB) |

                   (df_records['bodyTemperature'] < BODY_TEMP_LB) |
                   (df_records['bodyTemperature'] > BODY_TEMP_UB) |

                   (df_records['breathingFrequency'] <= BF_LB) |
                   (df_records['breathingFrequency'] >= BF_UB)
        , 'healthState'] = 'bad'
    df_records.loc[df_records['healthState'] == '', 'healthState'] = 'good'

    return df_records[columns_to_retain].to_dict('records')
