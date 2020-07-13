import dataset
oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog')
newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog_new')
old_race = oldDB['race']
old_race - oldDB['athlete']
old_result = oldDB['di_result']
new_record = newDB['record']

oldDB.begin()
newDB.begin()


try:
    statement = 'SELECT * \
                FROM `event` e, \
                      (SELECT * \
                       FROM `athlete` a, `di_result` r  \
                       WHERE a.`AthleteDataId`=r.`DataId`) ar \
                WHERE e.EventId=ar.AthleteEventId'

    id = 0

    for row in oldDB.query(statement):
        id += 1
        
        cp_config = [
            {
                'CP_Mode': 'Gun',
                'CP_Time': row['TimeGun']
            },
            {
                'CP_Mode': 'Start',
                'CP_Time': row['TimeStart']
            }
            {
                'CP_Mode': 'CP1',
                'CP_Time': row['TimeCheck01']
            },
            {
                'CP_Mode': 'CP2',
                'CP_Time': row['TimeCheck02']
            },
            {
                'CP_Mode': 'CP3',
                'CP_Time': row['TimeCheck03']
            },
            {
                'CP_Mode': 'CP4',
                'CP_Time': row['TimeCheck04']
            },
            {
                'CP_Mode': 'CP5',
                'CP_Time': row['TimeCheck05']
            },
            {
                'CP_Mode': 'CP6',
                'CP_Time': row['TimeCheck06']
            },
            {
                'CP_Mode': 'CP7',
                'CP_Time': row['TimeCheck07']
            },
            {
                'CP_Mode': 'CP8',
                'CP_Time': row['TimeCheck08']
            },
            {
                'CP_Mode': 'CP9',
                'CP_Time': row['TimeCheck09']
            },
            {
                'CP_Mode': 'End',
                'CP_Time': row['finishTime']
            }
        ]
        query = {
            'id': id,
            'uid': id,
            'race_id': row['RaceId'],
            'number': row['AthleteNo'],
            'name': row['AthleteName'],
            'nation': row['AthleteCountryCode'],
            'gender': row['AthleteGender'],
            'group': row['AthleteGroup'],
            'person_finish_time': float(row['personalFinishTime']),
            'gun_finish_time': float(row['finishTime']),
            'team': row['AthleteTeam'],
            'team_sort': id,
            'total_place': row['RankAll'],
            'group_place': row['RandCat'],
            'gender_place': row['RandSex'],
            'cp_timing_json': str(cp_config),
            'is_deleted': 0,
            'is_disqualified': 0,
            'is_passed': 0
        }
    
    new_race.insert(query)
    newDB.commit()
    print("success")
except Exception as err:
    newDB.rollback()
    print(err)

    # query = {
    #         'id': id,
    #         'uid':
    #         'race_id': row['RaceId'],
    #         'number': row['AthleteNo'],
    #         'name': row['AthleteName'],
    #         'nation': row['AthleteCountryCode'],
    #         'gender': row['AthleteGender'],
    #         'person_finish_time': 
    #         'gun_finish_time': 
    #         'group': row['AthleteGroup'],
    #         'team': row['AthleteTeam'],
    #         'team_sort': 
    #         'total_place': row['RankAll'],
    #         'group_place': row['RandCat'],
    #         'gender_place': row['RandSex'],
    #         'cp_timing_json': 
    #         'memo': 
    #         'tags': 
    #         'qrcode': 
    #         'update_datetime': 
    #         'is_deleted':
    #         'is_disqualified': 
    #         'is_passed':
    #     }