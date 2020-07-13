import dataset
# oldDB = dataset.connect('mysql+pymysql://root:season1006@localhost/bravelog')
# newDB = dataset.connect('mysql+pymysql://root:season1006@localhost/bravelog_new')
oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@172.105.206.159/bravelog')
newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@172.105.206.159/bravelog_new')
old_race = oldDB['race']
new_contest = newDB['contest']

oldDB.begin()
newDB.begin()

try:
    id = 0
    for col in old_race:
        id += 1
        query = {
            'id': id,
            'uid': col['RaceId'],
            'title': col['RaceName'],
            'banner': col['url'],
            'location': col['Country'],
            'start_date': col['RaceTime'],
        }
        new_contest.insert(query)
    newDB.commit()
    print("success")
except Exception as err:
    newDB.rollback()
    print(err)

    # query = {
    #         'id': id,
    #         'uid': col['RaceId'],
    #         'title': col['RaceName'],
    #         'banner': col['url'],
    #         'host': '',
    #         'location': col['Country'],
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
    #         'start_date': col['RaceTime'],
    #         'end_date': '',
    #         'create_user_id': '',
    #         'update_datetime': '',
    #         'is_deleted': '',
    #         'is_passed': ''
    #     }