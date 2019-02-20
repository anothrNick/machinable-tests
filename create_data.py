import time
import json
import requests
import logging
import base64
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

APP_USERNAME = "test_account"
APP_PASSWORD = "raPI1nqZT83N9UZYggWXwvuc"

TEST_PROJECT_ONE = "test_account_project_one"
TEST_PROJECT_TWO = "test_account_project_two"

APP_PROJECTS = [
    {"name": TEST_PROJECT_ONE, "slug": TEST_PROJECT_ONE, "description": "First test project for end-to-end testing.", "authn": True, "icon": "rocket"},
    {"name": TEST_PROJECT_TWO, "slug": TEST_PROJECT_TWO, "description": "Second test project for end-to-end testing.", "authn": False, "icon": "rocket"},
]

MANAGE_HOST = "https://manage.machinable.io"
PROJECT_HOST = "https://%s.machinable.io"

PATHS = {
    "APP_SESSIONS": "/users/sessions",
    "PROJECTS": "/projects"
}

humanSchema = load_json_from_file('./schemas/humans.json')
faker = FakerSchema()

def get_session():
    """
    Retrieve a new session with the test user credentials. The session will be used for all tests.
    """
    authBytes = base64.b64encode(bytes(APP_USERNAME + ":" + APP_PASSWORD, 'utf8'))
    r = requests.post(MANAGE_HOST + PATHS["APP_SESSIONS"], headers = {"Authorization": "Basic " + authBytes.decode()})
    
    logger.info("sessions response code: " + str(r.status_code))
    if r.status_code == requests.codes.created:
        return r.json()["access_token"]

def create_projects(accessToken):
    """
    Create machinable projects to use for testing.
    """
    for prj in APP_PROJECTS:
        r = requests.post(MANAGE_HOST + PATHS["PROJECTS"], headers = {"Authorization": "Bearer " + accessToken}, json = prj)
        logger.info("project create response code: " + str(r.status_code))
        if r.status_code != requests.codes.created:
            logger.error(r.text)

def create_apikeys(accessToken):
    pass

def create_projectusers(accessToken):
    pass

def generateJSON():
    return faker.generate_fake(humanSchema)

if __name__ == "__main__":
    logger.info("Running Machinable end-to-end tests...")
    # do something
    accessToken = get_session()

    if accessToken is None:
        raise Exception("error creating session")
    logger.info("access token: " + accessToken)

    create_projects(accessToken)
    # humanJson = generateJSON()
    # logger.info(humanJson)

    logger.info("Done.")