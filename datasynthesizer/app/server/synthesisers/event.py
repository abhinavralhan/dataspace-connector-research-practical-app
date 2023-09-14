import uuid
import secrets
from datetime import timedelta


def synthesise_event_details(event, start_time, end_time, event_ts):
    min_increment = 1
    additional_mins = (min_increment + secrets.randbelow(5))
    additional_sec = secrets.randbelow(30)
    event_ts = event_ts + timedelta(minutes=additional_mins, seconds=additional_sec)

    if event_ts > end_time:
        event_ts = end_time
    elif event_ts < start_time:
        event_ts = start_time

    event['eventTimestamp'] = event_ts

    random_no = secrets.randbelow(2)
    source = 'app' if random_no == 1 else 'manual'
    event['dataSource'] = source

    event_id = str(uuid.uuid4())
    event['eventId'] = event_id

    return event
