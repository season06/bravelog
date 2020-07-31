from datetime import datetime, timedelta

### Contest ###
def getContestData(row, host):
    timing_com = {
        'di': 9
    }
    timing_type = {
        'sportsnet': 8,
        'di': 13
    }
    contest_data = {
        'uid': row['RaceId'],
        'title': row['RaceName'],
        'banner': row['url'],
        'leading_id': 0,
        'timing_com': timing_com[host],
        'timing_type': timing_type[host],
        'service': 13,
        'start_date': row['RaceTime'],
        'create_user_id': 'season',
        'is_deleted': 0,
        'is_passed': 0
    }
    return contest_data

### Race ###
def getRaceStatement(host):
    foreign_column = {
        'sportsman': 'EventId',
        'di': 'RaceId'
    }
        
    race_statement = f'SELECT r.RaceId, r.bannerFile, eck.EventName, eck.EventId, eck.CPId, eck.CPName, eck.CPDistance \
                        FROM `race` r, \
                            (SELECT e.EventName, e.RaceId, ck.EventId, ck.CPId, ck.CPName, ck.CPDistance \
                            FROM `event_checkpoint` ck, `event` e \
                            WHERE ck.`EventId`=e.`EventId`) eck \
                        WHERE r.RaceId=eck.{foreign_column[host]}'
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

### Record ###
def getDate(contest_date, t):
    hour = t // 3600
    minute = (t - hour * 3600) // 60 
    second = t % 60
    date = contest_date + timedelta(hours=hour, minutes=minute, seconds=second)
    return str(date)

def getRecordStatement(table):
    record_statement = f'SELECT * \
            FROM `event` e, \
                    (SELECT * \
                    FROM `athlete` a, {table} r  \
                    WHERE a.`AthleteDataId`=r.`DataId`) ar \
            WHERE e.EventId=ar.AthleteEventId'
    return record_statement

def getRecordCpTiming(row, host):
    TimeCheck_num = {
        'sportsnet': 12,
        'di': 9
    }
    time_unit = {
        'sportsnet': 1,
        'di': 1000
    }
    unit = time_unit[host]
    # get contest date
    contest_date_str = row['EventCode']
    contest_date = datetime.strptime(contest_date_str, '%Y%m%d%H')

    record_cp_dict = [{
        "CP_Mode": "Gun",
        "CP_Time": getDate(contest_date, int(row['TimeGun'])/unit)
    },{
        "CP_Mode": "Start",
        "CP_Time": getDate(contest_date, int(row['TimeStart'])/unit)
    }]
    # TimeCheck根據賽事有所不同
    for i in range(1,TimeCheck_num[host]+1):
        col = f"TimeCheck0{i}" if i<10 else f"TimeCheck{i}"
        # 若"CP_time"為0 則不insert
        if int(row[col]) == 0:
            break
        temp = {
            "CP_Mode": f"CP{i}",
            "CP_Time": getDate(contest_date, int(row[col])/unit)
        }
        record_cp_dict.append(temp)
    # insert finish time
    finish_cp = {
        "CP_Mode": "End",
        "CP_Time": getDate(contest_date, int(row['finishTime'])/unit)
    }
    record_cp_dict.append(finish_cp)

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