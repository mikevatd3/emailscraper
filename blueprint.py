import time

from returns.result import Success, Failure
import requests

from inbox import setup_inbox

# 1. grab relevant emails
# 2. relevant emails -> tasks = [(topic, year, download link),]
# 3. for each task in tasks:
#   - download csv from link
#   - compile filename from topic and year
#   - save csv as filename

# Grab relevant emails
inbox = setup_inbox()
datasets = inbox.find_mischooldata_datasets()

start = time.time()

for dataset in datasets:
    match dataset:
        case Success(dataset):
            file = requests.get(dataset.dl_link)

            with open(f"raw/{dataset.raw_name}_{dataset.year}.csv", "wb") as f:
                f.write(file.content)

            print(f"Finished downloading and saving {dataset.name}")


        case Failure(error):
            print(error)

    time.sleep(5)

end = time.time()
total_seconds = start - end

minutes, seconds = divmod(int(total_seconds), 60)
hours, minutes = divmod(minutes, 60)

print(f"Total running time {hours:02}:{minutes:02}:{seconds:02}")

