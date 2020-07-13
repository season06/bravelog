import dataset
oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog')
newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog_new')
old_race = oldDB['event']
new_contest = newDB['race']

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

    query = {
            'id': id,
            'uid': col['RaceId'],
            'race_id': col['RaceName'],
            'number': col['url'],
            'name': '',
            'nation': col['Country'],
            'gender': '',
            'person_finish_time': '',
            'gun_finish_time': '',
            'group': '',
            'team': '',
            'team_sort': '',
            'total_place': '',
            'group_place': '',
            'gender_place': '',
            'cp_timing_json': '',
            'memo': '',
            'tags': '',
            'qrcode': '',
            'update_datetime': col['RaceTime'],
            'is_deleted': '',
            'is_disqualified': '',
            'is_passed': ''
        }