# machinable-tests

The `scripts/project_usage.py` file creates usage for a project. It assumes the project has the following 2 API Resources configured:

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
