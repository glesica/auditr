# Auditr API and JSON Schemas

The following are the JSON schemas for communication between clients 
and the server.

## Audits Endpoint

This endpoint is used to store and retrieve the results of 
software audits. The URL is `/audits`.

### GET

#### Request

There are a few valid parameters for GET requests.

  * computer_name
  * latest

#### Response

The return data format is as follows:

    {
        "audits": [
            {
                "computer": {
                    "computer_name": "<string 1:15>"
                },
                "audit_date": "<string %yyyy-mm-dd%>",
                "audit_id": "<int>",
                "applications": [
                    {
                        "application_name": "<string 1:128>",
                        "application_vendor": "<string 1:128>",
                        "application_version": "<string 1:128>"
                    },
                    ...
                ]
            },
            ...
        ],
        "status": "success"
    }

### POST

#### Request

This will create a new audit entry in the database. The request 
body should be formatted as follows:

    {
        "computer": {
            "computer_name": "<string 1:15>"
        },
        "audit_date": "<string %yyyy-mm-dd%>",
        "applications": [
            {
                "application_name": "<string 1:128>",
                "application_vendor": "<string 1:128>",
                "application_version": "<string 1:128>"
            },
            ...
        ]
    }

#### Response

    {
        "status": "success"
    }

## Computers Endpoint

Used for manipulating computer object. URL is `/computers`.

### GET

#### Request

Valid parameters are given below.

  * computer_name

#### Response

    {
        "computers": [
            {
                "computer_id": "<int>",
                "computer_name": "<string 1:15>"
            },
            ...
        ],
        "status": "success"
    }

### POST

#### Request

Computers can be created by submitting a JSON document according to the following pattern:

    {
        "computer_name": "<string 1:15>"
    }

#### Response

    {
        "computer": {
            "computer_id": "<int>",
            "computer_name": "<string 1:15>"
        },
        "status": "success"
    }