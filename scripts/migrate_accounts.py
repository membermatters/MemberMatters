import csv
import requests
import json

with open('/home/jabelone/Downloads/access_parsed.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    counter = 0
    for row in csv_reader:
        counter += 1
        payload = {
            "secret": "cookiemonster",
            "screen_name": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "email": row[4],
            "phone": row[3],
            "rfid_code": row[5],
            "created": row[6],
            "state": row[7]
        }
        payload = json.dumps(payload)
        r = requests.post("https://portal.hsbne.org/api/member/create", data=payload)
        print(r.status_code)
