import csv
import dataset

# with open('reference/20200119_sc.csv', newline='') as csvfile:
#     rows = csv.reader(csvfile)
#     id = 0
#     for row in rows:
#         print(row)
#         id +=1
#         if id == 5:
#             break

with dataset.connect('mysql+pymysql://user:password@172.105.206.159/test') as db:
    with open('/Users/season/Downloads/marathon.csv', newline='', encoding='utf-8') as csvfile:
        db_table = db['marathon']
        for row in db_table:
        rows = csv.reader(csvfile)
        id = 0
        for row in rows:
            id += 1
            if id == 1:
                continue
            data = {
                'race_id': 3,
                'number': row[1],
                'group': row[2],
                'name': row[3],
                'qrcode': row[5],
                'gender': row[6]
            }
            db['marathon'].insert(data)
            print(data)