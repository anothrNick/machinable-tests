#!/usr/bin/env python3

"""
This script creates usage for a project. It assumes the project has the following 2 API Resources configured:

## /api/count

Stores a count per person accessed by this script. The count is incremented each time that person is retrieved (meta data).

```
{
    "peopleId": {
        "type": "string",
        "description": "The ID of the person stored in 'people'"
    },
    "count": {
        "type": "integer",
        "description": "A counter. Keeps track of how many times this person has been accessed."
    }    
}
```

## /api/people

Stores a list of people.

```
{
  "age": {
    "description": "Age in years which must be equal to or greater than zero.",
    "minimum": 0,
    "type": "integer"
  },
  "birthDate": {
    "description": "The date of this person's birth, represented by a RFC3339 formated date-time string",
    "format": "date-time",
    "type": "string"
  },
  "firstName": {
    "description": "The person's first name.",
    "type": "string"
  },
  "friends": {
    "description": "A list of this person's friends",
    "items": {
      "type": "string"
    },
    "type": "array"
  },
  "lastName": {
    "description": "The person's last name.",
    "type": "string"
  },
  "profession": {
    "description": "The profession of this person. What they do for a career or their lifestyle.",
    "properties": {
      "responsibilites": {
        "description": "A list of this profession's responsibilities",
        "items": {
          "type": "string"
        },
        "type": "array"
      },
      "title": {
        "type": "string"
      },
      "years": {
        "description": "The number of years this person has spent with this profession",
        "type": "number"
      }
    },
    "type": "object"
  }
}
```

A collection will also be managed by this script:

## /collections/metrics

Keeps track of request metrics for visualization later.

```
{
    "status_code": {
        "type": "integer",
        "description": "The HTTP Status code returned by the request."
    },
    "response_time": {
        "type": "number",
        "description": "The response time, in milliseconds, of the HTTP request."
    },
    "verb": {
        "type": "string",
        "description": "The HTTP Verb of the measured request."
    },
    "path": {
        "type": "string",
        "description": "The URL path of the request made."
    }
}
```



"""

import time
import json
import requests
import logging
import argparse
import base64

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

accessToken = ""
refreshToken = ""

HOST = "https://{project}.machinable.io{path}"
PATHS = {
    "people": "/api/people",
    "count": "/api/count",
    "metrics": "/api/metrics",
    "login": "/sessions/",
    "refresh": "/sessions/refresh/",
}

def login(project, username, password):
    encoded = base64.b64encode(bytes("{username}:{password}".format(username=username, password=password), 'utf8'))
    headers = {"Authorization": "Basic " + encoded.decode()}
    url = HOST.format(project=project, path=PATHS["login"])
    r = requests.post(url, headers=headers)

    response = r.json()
    accessToken = response["access_token"]
    refreshToken = response["refresh_token"]

def refresh(token):
    pass

def create_person(headers):
    data = generatePerson()
    url = HOST.format(project=project, path=PATHS["login"])
    r = requests.post(PROJECT_HOST + PATHS["API"], json = data, headers = {"Authorization": "apikey " + API_KEY})

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



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create project usage (tests)")
    parser.add_argument('project', help='The name of the project to use.')
    parser.add_argument('--apikey', help='API Key to make authenticated requests, assumes read/write permissions.')
    parser.add_argument('--username', help='Valid project username to login and make requests. Requires password.')
    parser.add_argument('--password', help='Valid project password to login and make requests. Requires username.')

    args = parser.parse_args()

    # login, if needed
    if args.username and args.password:
        login(args.project, args.username, args.password)

    # create a new person (record metrics)

    # get the first page of people (record metrics)

    # select a person

    # lookup person in /api/count
    #   * does not exist: create
    #   * exists: increment count and update

    # 1/10 chance to delete person
    #   * delete person (record metrics)
    #   * find and delete count record (if exists)

    logger.info("done")
