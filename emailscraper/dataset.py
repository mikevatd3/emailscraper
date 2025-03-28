from dataclasses import dataclass
from base64 import urlsafe_b64decode
from urllib.parse import urlparse
import re

from bs4 import BeautifulSoup


NAME_CONVENTION_LOOKUP = {
    "Student Count": ("Student counts", "student_count"),
    "Graduation/Dropout": ("Graduation/Dropout", "graduation_dropout"),
    "Top 30 / Bottom 30 Analysis": ("Top 30 / Bottom 30 Analysis", "top_30_btm_30"),
}


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



def extract_subject_name(subject: str) -> str | None:
    result = re.search(
        r"Your requested ([\w ()-/&]+) data file is ready for download.", subject
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


def build_dataset(message):
    payload = message["payload"]

    # find subject in headers
    subject_name = None  # Hate this
    for header in payload.get("headers", []):
        if header.get("name", "").lower() == "subject":
            subject_name = extract_subject_name(header.get("value", ""))
            break

    name, raw_name = NAME_CONVENTION_LOOKUP.get(
        subject_name, (subject_name, camel_to_snake(subject_name))
    )

    soup = BeautifulSoup(
        urlsafe_b64decode(payload["body"]["data"]).decode(),
        "html.parser",
    )

    dl_link = extract_dl_link(soup)
    filename = extract_filename(dl_link)

    year = extract_year(soup.find_all("p")[0].contents[0])

    return Dataset(
        name,
        subject_name,
        raw_name,
        year,
        dl_link,
        filename,
    )

