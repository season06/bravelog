def getContestData(row):
    contest_data = {
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
    return contest_data

def getRaceStatement(host):
    if host == 'sportsman':
        foreign_column = 'EventId'
    elif host == 'di':
        foreign_column = 'RaceId'
        
    race_statement = f'SELECT r.RaceId, r.bannerFile, eck.EventName, eck.EventId, eck.CPId, eck.CPName, eck.CPDistance \
                        FROM `race` r, \
                            (SELECT e.EventName, e.RaceId, ck.EventId, ck.CPId, ck.CPName, ck.CPDistance \
                            FROM `event_checkpoint` ck, `event` e \
                            WHERE ck.`EventId`=e.`EventId`) eck \
                        WHERE r.RaceId=eck.{foreign_column}'
    return race_statement

def getRaceCpConfig(row):
    race_cp_dict = {
            'CPId': row['CPId'],
            'CPName': row['CPName'],
            'CPDistance': row['CPDistance']
    }
    return race_cp_dict

def getRaceData(row, race_cp_dict):
    race_data = {
        'uid': row['EventId'],
        'contest_id': row['RaceId'],
        'sort': 0,
        'title': row['EventName'],
        'banner': row['bannerFile'],
        'race_status': 36,
        'cp_json': [race_cp_dict],
        'create_user_id': 'season',
        'is_deleted': 0,
        'is_passed': 0
    }
    return race_data

def getRecordStatement(table):
    record_statement = f'SELECT * \
            FROM `event` e, \
                    (SELECT * \
                    FROM `athlete` a, {table} r  \
                    WHERE a.`AthleteDataId`=r.`DataId`) ar \
            WHERE e.EventId=ar.AthleteEventId'
    return record_statement

def getRecordCpTiming(row, TimeCheck_num):
    record_cp_dict = [{
        'CP_Mode': 'Gun',
        'CP_Time': row['TimeGun']
    },{
        'CP_Mode': 'Start',
        'CP_Time': row['TimeStart']
    },{
        'CP_Mode': 'End',
        'CP_Time': row['finishTime']
    }]
    # TimeCheck根據賽事有所不同
    for i in range(1,TimeCheck_num+1):
        col = f'TimeCheck0{i}' if i<10 else f'TimeCheck{i}'
        temp = {
            'CP_Mode': f'CP{i}',
            'CP_Time': row[col]
        }
        record_cp_dict.append(temp)
    return record_cp_dict

def getRecordData(row, record_cp_dict):
    record_data = {
        'uid': row['AthleteDataId'],
        'race_id': row['RaceId'],
        'race_id_temp': row['EventId'],  # temp
        'number': row['AthleteNo'],
        'name': row['AthleteName'],
        'nation': row['AthleteCountryCode'],
        'gender': 0 if row['AthleteGender'] == 'M' else 1,  # turn varchar into int
        'group': row['AthleteGroup'],
        'person_finish_time': float(row['personalFinishTime']),
        'gun_finish_time': float(row['finishTime']),
        'team': row['AthleteTeam'],
        'team_sort': 0,
        'total_place': row['RankAll'],
        'group_place': row['RankCat'],
        'gender_place': row['RankSex'],
        'cp_timing_json': str(record_cp_dict),
        'is_deleted': 0,
        'is_disqualified': 0,
        'is_passed': 0
    }
    return record_data