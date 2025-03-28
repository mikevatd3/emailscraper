# emailscraper

What does this thing do?

- Goes to my email and downloads all the mischooldata files and names them appropriately
extract.py

- Places the files in the correct year folder in the vault
load.py

## Setting up your gmail account to use tool

[tutorial](https://developers.google.com/gmail/api/quickstart/python)

- Enable API
    - Create a new project on google cloud console
    - Configure OAuth consent screen (follow tutorial on this)
    - Add scopes
      - This isn't covered very well in the tutorial, but there are several gmail scopes that you can add, so select which seems the most appropriate
      - I chose 'gmail read-only' on the current round
    - Authorize credentials for a desktop application
      - From the Google Cloud Dashboard, choose hamburger icon > APIs & Services > Credentials
      - choose + CREATE CREDENTIALS at the top, then OAuth client ID
      - choose Desktop app for Application type
      - provide the name
      - when the popup appears with the credentials, choose download json at the bottom and save in the top level of this repo and rename to credentials.json.

- Install google client library

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Google Cloud questions

- Can the application be made to look at internal emails without setting up a new application on google cloud?