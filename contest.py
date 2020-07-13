import dataset
oldDB = dataset.connect('mysql+pymysql://root:season1006@localhost/bravelog')
newDB = dataset.connect('mysql+pymysql://root:season1006@localhost/bravelog_new')
old_race = oldDB['race']
old_event = oldDB['event']
old_athlete = oldDB['event']
old_event_ck = oldDB['event_ckeckpoint']
old_result = oldDB['di_result']

new_contest = newDB['contest']
new_race = newDB['race']
new_record = newDB['record']

oldDB.begin()
newDB.begin()

try:
    id = 0
    for row in old_race:
        id += 1
        query = {
            'id': id,
            'uid': row['RaceId'],
            'title': row['RaceName'],
            'banner': row['url'],
            'leading_id': 0,
            'service': 13,
            'start_date': row['RaceTime'],
            'create_user_id': 'season',
            'is_deleted': 0,
            'is_passed': 0
        }
        new_contest.insert(query)
    newDB.commit()
    print("success")
except Exception as err:
    newDB.rollback()
    print(err)

    # query = {
    #         'id': id,
    #         'uid': row['RaceId'],
    #         'title': row['RaceName'],
    #         'banner': row['url'],
    #         'host': '',
    #         'location': row['Country'],
    #         'leading_id': '',
    #         'timing_com': '',
    #         'timing_chip': '',
    #         'timing_type': '',
    #         'contest_status': '',
    #         'contract_status': '',
    #         'attendance': '',
    #         'extra_service': '',
    #         'memo': '',
    #         'contact_memo': '',
    #         'tags': '',
    #         'qrcode': '',
    #         'service': '',
    #         'contact_date': '',
    #         'start_date': row['RaceTime'],
    #         'end_date': '',
    #         'create_user_id': '',
    #         'update_datetime': '',
    #         'is_deleted': '',
    #         'is_passed': ''
    #     }