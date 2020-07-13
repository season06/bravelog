import dataset
# tNMW9ksfylH1oosQ
oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog')
newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog_new')
old_race = oldDB['race']
old_athlete = oldDB['athlete']
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
        
        # for cp_config
        cp_config = [{
                        'CP_Mode': 'Gun',
                        'CP_Time': row['TimeGun']
                    },{
                        'CP_Mode': 'Start',
                        'CP_Time': row['TimeStart']
                    },{
                        'CP_Mode': 'End',
                        'CP_Time': row['finishTime']
                    }]
        for i in range(1,10):
            col = f'TimeCheck0{i}' if i<10 else f'TimeCheck{i}'
            temp = {
                'CP_Mode': f'CP{i}',
                'CP_Time': row[col]
            }
            cp_config.append(temp)
        
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
        new_record.insert(query)
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