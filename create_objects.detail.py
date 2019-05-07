import time
import json
import requests
import logging
import base64
import traceback
from random import randint
from faker import Faker
from faker_schema.faker_schema import FakerSchema
from faker_schema.schema_loader import load_json_from_file

LOGMSG_TSFMT = '%a %b %d %H:%M:%S UTC %Y'
LOGMSG_FORMAT = '%(asctime)s %(levelname)5s:%(filename)s:%(funcName)s:%(lineno)s: %(message)s'

logmsg_formatter = logging.Formatter(fmt=LOGMSG_FORMAT, datefmt=LOGMSG_TSFMT)
stderr_handler = logging.StreamHandler()
stderr_handler.setFormatter(logmsg_formatter)

# set up logging
logger = logging.getLogger("machinable")
logger.addHandler(stderr_handler)
logger.setLevel(logging.INFO)
logger.disabled = False

PROJECT_HOST = "https://one.machinable.io"
API_KEY = "2a3e5add-a0ca-4493-a0ab-474c6b1aad45"
PATHS = {
    "API": "/api/detailPeople"
}

SLEEP_TIME = .5

humanSchema = load_json_from_file('./schemas/people.details.json')
fakerSchema = FakerSchema()
fake = Faker()

def create_object(data):
    logger.info("creating new object...")
    r = requests.post(PROJECT_HOST + PATHS["API"], json = data, headers = {"Authorization": "apikey " + API_KEY})
    logger.info("create response code: " + str(r.status_code))
    logger.info("create response text: " + str(r.text))
    logger.info("done.")

def generateJSON():
    person = fakerSchema.generate_fake(humanSchema)
    friends = []

    lenFriends = randint(0, 4)
    for x in range(lenFriends) :
        friends.append(fake.name())

    person["friends"] = friends
    person["profession"]["responsibilites"] = [fake.text()]
    person["birthDate"] = person["birthDate"].isoformat()+"Z"

    return person

if __name__ == "__main__":
    logger.info("Creating machinable objects...")
    while True:
        try:
            personJson = generateJSON()
            create_object(personJson)
        except Exception as ex:
            logger.error("exception creating objects: %s", str(ex))
            traceback.print_tb(ex.__traceback__)

        logger.info("sleeping %s seconds\n", SLEEP_TIME)
        time.sleep(SLEEP_TIME)
    logger.info("Done.")