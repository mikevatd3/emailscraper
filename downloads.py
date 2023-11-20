import requests

dl = requests.get(
    "https://downloads.mischooldata.org/GeneratedDataFile?filename=37e67b5c-b0e0-4bc2-aa9c-db5dbad60acd.csv"
)

with open("at_rist_student_2017.csv", "w") as f:
    f.write(dl.content.decode())
