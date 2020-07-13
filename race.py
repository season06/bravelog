import dataset
oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog')
newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog_new')
old_race = oldDB['race']
old_event = oldDB['event']
old_event_ck = oldDB['event_ckeckpoint']
new_race = newDB['race']

oldDB.begin()
newDB.begin()

try:
    statement = 'SELECT r.RaceId, eck.EventName, eck.EventId, eck.CPId, eck.CPName, eck.CPDistance \
                 FROM `race` r, \
                    (SELECT e.EventName, e.RaceId, ck.EventId, ck.CPId, ck.CPName, ck.CPDistance \
                     FROM `event_checkpoint` ck, `event` e \
                     WHERE ck.`EventId`=e.`EventId`) eck \
                 WHERE r.RaceId=eck.RaceId'

    id = 0
    event = ''
    query = {}
    for row in oldDB_query(statement):
        if event != row['EventName']:
            if event != '':
                new_race.insert(query)
            event = row['EventName']
            id += 1
            cp_config = {
                'CPId': row['CPId'],
                'CPName': row['CPName'],
                'CPDistance': row['CPDistance']
            }
            query = {
                'id': id,
                'contest_id': row['RaceId'],
                'title': row['EventName'],
                'cp_json': cp_config
            }

        else:
            cp_config = {
                'CPId': row['CPId'],
                'CPName': row['CPName'],
                'CPDistance': row['CPDistance']
            }
            query["CP"].append(cp_config)
        new_race.insert(query)

    newDB.commit()
    print("success")
except Exception as err:
    newDB.rollback()
    print(err)

    # query = {
    #         'id': id,
    #         'uid': 
    #         'contest_id': ow['RaceId'],
    #         'sort': '',
    #         'title': row['EventName'],
    #         'start_time': '',
    #         'banner': '',
    #         'race_type': '',
    #         'race_status': '',
    #         'cp_json': cp_config,
    #         'cp_code': '',
    #         'memo': '',
    #         'memo2': '',
    #         'tags': '',
    #         'qrcode': '',
    #         'create_user_id': '',
    #         'update_datetime': '',
    #         'is_deleted': '',
    #         'is_passed': ''
    #     }