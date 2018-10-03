import csv

with open('/home/jabelone/access.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    kept_people = []
    kept_people_phone = []

    for row in csv_reader:
        if int(row[6]):
            if len(row[5]) == 10:
                kept_people_phone.append({"active": "active", "name": row[1], "email": row[3], "nickname": row[2], "rfid": row[5]})
            else:
                kept_people.append({"active": "active", "name": row[1], "email": row[3], "nickname": row[2], "rfid": row[5]})
        else:
            if len(row[5]) == 10:
                kept_people_phone.append({"active": "inactive", "name": row[1], "email": row[3], "nickname": row[2], "rfid": row[5]})
            else:
                kept_people.append({"active": "inactive", "name": row[1], "email": row[3], "nickname": row[2], "rfid": row[5]})

    print("with card {}:".format(len(kept_people)))
    for person in kept_people:
        print(f"{person['active']},{person['rfid']},{person['nickname']},{person['name']},{person['email']}")

    print("\nwithout card {}:".format(len(kept_people_phone)))
    for person in kept_people_phone:
        print(f"{person['active']},{person['rfid']},{person['nickname']},{person['name']},{person['email']}")

    print("total: " + str(len(kept_people) + len(kept_people_phone)))