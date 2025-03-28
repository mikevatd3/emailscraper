from emailscraper import setup_logging
from email_extract import extract_mischooldata_from_email
from load import load_mischooldata_to_valut


logger = setup_logging()


extract_mischooldata_from_email(logger)
load_mischooldata_to_valut(logger)
