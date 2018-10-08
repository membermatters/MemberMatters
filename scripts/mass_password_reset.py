import csv
import requests
import json

with open('/home/jabelone/Downloads/to_reset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    counter = 0
    for row in csv_reader:
        counter += 1
        payload = {
            "email": row[0]
        }

        r = requests.post("https://portal.hsbne.org/profile/password/reset", data=payload)
        print(str(r.status_code) + row[0])

    print("Reset {} passwords.".format(counter))