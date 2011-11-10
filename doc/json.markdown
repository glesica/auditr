# Auditr JSON Schemas

The following are the JSON schemas for communication between clients 
and the server.

## Audit submission

The following format can be used to submit an audit.

    {
        "computer": {
            "name": "<string 1:15>"
        },
        "applications": [
            {
                "name": "<string 1:128>",
                "vendor": "<string 1:128>",
                "version": "<string 1:128>"
            },
            "..."
        ]
    }
