import uuid
import secrets
from faker import Faker
from ..constants import *

fake = Faker()
fake.seed_instance(8)


def synthesise_user_data(user):
    user['user_id'] = str(uuid.uuid4())

    name = fake.name()
    user['firstname'] = name.split(' ')[0]
    user['lastname'] = name.split(' ')[1]

    random_no = secrets.randbelow(2)
    gender = 'male' if random_no == 1 else 'female'
    user['gender'] = gender

    age = MIN_AGE + secrets.randbelow(65)
    user['age'] = age

    height = 0
    weight = 0

    if age < NEW_BORN_AGE:
        weight = MIN_WEIGHT + secrets.randbelow(10)
        height = MIN_HEIGHT + secrets.randbelow(40)

    elif NEW_BORN_AGE <= age <= ADOLESCENT_AGE:
        weight = 20 + secrets.randbelow(20)
        height = 70 + secrets.randbelow(60)

    elif age > ADOLESCENT_AGE:
        weight = 40 + secrets.randbelow(80)
        height = 140 + secrets.randbelow(60)

    user['weight'] = weight
    user['height'] = height
    return user
