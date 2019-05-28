#!/usr/bin/env python3

import time
import json
import requests
import logging
import argparse
import base64
from random import randint, choice
from faker import Faker
from faker_schema.faker_schema import FakerSchema
from faker_schema.schema_loader import load_json_from_file

LOGMSG_TSFMT = '%a %b %d %H:%M:%S UTC %Y'
LOGMSG_FORMAT = '%(asctime)s %(levelname)5s:%(filename)s:%(funcName)s:%(lineno)s: %(message)s'

logmsg_formatter = logging.Formatter(fmt=LOGMSG_FORMAT, datefmt=LOGMSG_TSFMT)
stderr_handler = logging.StreamHandler()
stderr_handler.setFormatter(logmsg_formatter)

# set up logging
logger = logging.getLogger("machinable-tests")
logger.addHandler(stderr_handler)
logger.setLevel(logging.INFO)
logger.disabled = False

ACCESS_TOKEN = ""
REFRESH_TOKEN = ""

HOST = "https://{project}.machinable.io{path}"
PATHS = {
    "people": "/api/detailPeople",
    "count": "/api/count",
    "countLookup": "/api/count?peopleId={id}",
    "metrics": "/collections/metrics",
    "login": "/sessions/",
    "refresh": "/sessions/refresh/",
}

SLEEP_TIME = 2

fakerSchema = FakerSchema()
fake = Faker()
humanSchema = load_json_from_file('./scripts/schemas/people.details.json')

class TokenExpired(Exception):
  pass

def login(project, username, password):
  global ACCESS_TOKEN
  global REFRESH_TOKEN
  logger.info("logging in")

  encoded = base64.b64encode(bytes("{username}:{password}".format(username=username, password=password), 'utf8'))
  headers = {"Authorization": "Basic " + encoded.decode()}
  url = HOST.format(project=project, path=PATHS["login"])
  r = requests.post(url, headers=headers)

  response = r.json()
  ACCESS_TOKEN = response["access_token"]
  REFRESH_TOKEN = response["refresh_token"]

def refresh():
  global ACCESS_TOKEN
  
  headers = {"Authorization": "Bearer " + REFRESH_TOKEN}
  url = HOST.format(project=project, path=PATHS["refresh"])
  r = requests.post(url, headers=headers)

  if r.status_code == requests.codes.ok:
    logger.info("refreshed token")
    response = r.json()
    ACCESS_TOKEN = response["access_token"]

  return r.status_code

def create_person(headers):
  data = generatePerson()
  url = HOST.format(project=project, path=PATHS["people"])
  r = requests.post(url, json = data, headers = headers)

  # TODO: be more specific with exceptions
  if r.status_code != requests.codes.created:
    logger.info("unexpected status code from create_person: {code}".format(code=r.status_code))
    raise TokenExpired
  
  logger.info("created new person")

def get_people(headers, limit, offset):
  url = HOST.format(project=project, path=PATHS["people"])
  r = requests.get(url, headers = headers)

  # TODO: be more specific with exceptions
  if r.status_code != requests.codes.ok:
    logger.info("unexpected status code from get_people: {code}".format(code=r.status_code))
    raise TokenExpired

  logger.info("retrieved {limit} people offset by {offset}".format(limit=limit, offset=offset))

  people = r.json()["items"]
  return people

def generatePerson():
  person = fakerSchema.generate_fake(humanSchema)
  friends = []

  lenFriends = randint(0, 4)
  for x in range(lenFriends) :
      friends.append(fake.name())

  person["friends"] = friends
  person["profession"]["responsibilites"] = [fake.text()]
  person["birthDate"] = person["birthDate"].isoformat()+"Z"

  return person

def countPerson(person):
  url = HOST.format(project=project, path=PATHS["countLookup"].format(id=person["id"]))
  r = requests.get(url, headers = headers)

  # TODO: be more specific with exceptions
  if r.status_code == requests.codes.unauthorized:
    logger.info("unauthorized status code from countPerson: {code}".format(code=r.status_code))
    raise TokenExpired
  
  # TODO

def runForUser(project, username, password):
  limit = 100
  offset = 0
  try:
    # create a new person (record metrics)
    create_person({"Authorization": "Bearer " + ACCESS_TOKEN})

    # get the first page of people (record metrics)
    people = get_people({"Authorization": "Bearer " + ACCESS_TOKEN}, limit, offset)

    # select a person
    if len(people) > 0:
      person = choice(people)

    # lookup person in /api/count
    #   * does not exist: create
    #   * exists: increment count and update

    # 1/10 chance to delete person
    #   * delete person (record metrics)
    #   * find and delete count record (if exists)
  except TokenExpired as e:
    sc = refresh()
    if sc != requests.codes.ok:
      login(project, username, password)
    

def runForKey(project, apikey):
  pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Create project usage (tests)")
  parser.add_argument('project', help='The name of the project to use.')
  parser.add_argument('--apikey', help='API Key to make authenticated requests, assumes read/write permissions.')
  parser.add_argument('--username', help='Valid project username to login and make requests. Requires password.')
  parser.add_argument('--password', help='Valid project password to login and make requests. Requires username.')

  args = parser.parse_args()

  project = args.project
  username = args.username
  password = args.password

  # login, if needed
  if args.username and args.password:
    login(project, username, password)

    while True:
      try:
          runForUser(project, username, password)
      except Exception as ex:
          logger.error("exception creating usage: %s", str(ex))
          traceback.print_tb(ex.__traceback__)

      logger.info("sleeping %s seconds\n", SLEEP_TIME)
      time.sleep(SLEEP_TIME)
  logger.info("Done.")
