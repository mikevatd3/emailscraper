from dataclasses import dataclass
import re
import os
import datetime

from urllib.parse import urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

from base64 import urlsafe_b64decode
from googleapiclient.discovery import Resource
from returns.result import Success, Failure


@dataclass
class Dataset:
    name: str
    subject_name: str  # The name parsed from the email subject line
    raw_name: str
    year: int
    dl_link: str
    filename: str

    def save_filename(self):
        return f"{self.raw_name}_{self.year}.csv"


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = name.replace(" ", "")
    name = name.replace("(", "")
    name = name.replace(")", "")
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

name_convention_lookup = {
    "Student Count": ("Student counts", "student_count"),
}


def extract_subject_name(subject: str) -> str | None:
    result = re.search(
        r"Your requested ([\w ()-/]+) data file is ready for download.", subject
    )
    if not result:
        return None
    return result.groups()[0]


def extract_year(first_paragraph: str) -> str | None:
    make_full_year = lambda x: "20" + x[-2:]
    result = re.search(r"[\w ,']+([0-9]{4}-[0-9]{2}):", first_paragraph)

    if not result:
        return None
    return make_full_year(result.groups()[0])


def extract_dl_link(soup):
    links = soup.find_all("a")
    return links[0]["href"]


def extract_filename(href):
    parsed = urlparse(href)
    query = parsed.query

    _, filename = query.split("=")

    return filename


@dataclass
class Inbox:
    service: Resource

    def search(self, q: str):
        results = (
            self.service.users().messages().list(userId="me", q=q).execute()
        )
        messages = results.get("messages", [])

        if not messages:
            print("No messages found.")
            []

        result = []
        for message in messages:
            full_msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=message["id"], format="full")
                .execute()
            )

            result.append(self.build_dataset(full_msg))
        return result

    def build_dataset(self, message):
        try:
            payload = message["payload"]

            # find subject in headers
            subject_name = None  # Hate this
            for header in payload.get("headers", []):
                if header.get("name", "").lower() == "subject":
                    print(header.get("value"))
                    subject_name = extract_subject_name(header.get("value", ""))
                    break

            print(subject_name)
            name, raw_name = name_convention_lookup.get(
                subject_name, (subject_name, camel_to_snake(subject_name))
            )

            soup = BeautifulSoup(
                urlsafe_b64decode(payload["body"]["data"]).decode(),
                "html.parser",
            )

            dl_link = extract_dl_link(soup)
            filename = extract_filename(dl_link)

            year = extract_year(soup.find_all("p")[0].contents[0])

            return Success(
                Dataset(
                    name,
                    subject_name,
                    raw_name,
                    year,
                    dl_link,
                    filename,
                )
            )

        except TypeError as e:
            return Failure(e)

    def find_mischooldata_datasets(self):
        after = datetime.date.today() - datetime.timedelta(days=3)
        return self.search(
            f"mischooldata after:{after.strftime('%Y/%m/%d')}"
        )

        


def setup_inbox():
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        return Inbox(service)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

        return None
