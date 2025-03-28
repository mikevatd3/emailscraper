import os
from logging import Logger
from dataclasses import dataclass
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource

from .dataset import Dataset

@dataclass
class Inbox:
    service: Resource
    logger: Logger


    def build_dataset(self):
        pass

    def find_valid_mischooldata_messages(self):
        """
        This looks at the account and finds all the messages.
        """

        after = datetime.date.today() - datetime.timedelta(days=3)
        q = f"mischooldata after:{after.strftime('%Y/%m/%d')}"

        messages = (
            self.service.users().messages().list(userId="me", q=q).execute()
            .get("messages", [])
        )

        if not messages:
            self.logger.warning("No messages found.")
            return []

        self.logger.info("Extracting messages.")
        return [
            self.service.users()
            .messages()
            .get(userId="me", id=message["id"], format="full")
            .execute()
            for message in messages
        ]


def setup_inbox(logger):
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("credentials/token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        return Inbox(service, logger)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

        return None