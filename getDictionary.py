from datetime import datetime, timedelta
import json
### eb '2019102706' '2019120105' 
### focusline '20180922', '20180923' 無eventcheckpoint / '2019042801' 無race
### sportsnet '2019102701': (1062, "Duplicate entry '612-04266' for key 'race_id_number'")

# check 'TimeCheckNum' 'api_type_dict' 'timing_com_dict'
host = 'sportsnet'
RACEID_arr = ['2019121501'] 

TimeCheckNum = {
    'di': 9,
    'eb': 16,
    'focusline': 12,
    'lohas': 16,
    'jchip': 9,
    'promos': 9,
    'sportsnet': 12,
    'eb2': 700
}

contest_id_dict = {}
race_id_dict = {}

### Contest ###
def getContestData(row):
    api_type_dict = {
        1: '', # accurat
        2: '', # focusline
        4: '', # sportsnet
        6: '', # promos
        7: 'read_EB_dropbox.php', # eb
        9: 'read_dropbox.php',  # di
        8: '', # jchip
        10: '', # eb2
        11: '' # lohas
    }
    timing_com_dict = {
        'focusline': 22,
        'di': 9,
        'eb': 8,
        'eb2': 8,
        'lohas': 26,
        'jchip': 28,
        'promos': 23,
        'sportsnet': 25,
        'accurat': 24
    }

    contest_data = {
        'uid': row['RaceId'],
        'title': row['RaceName'],
        'banner': row['url'],
        'timing_com': timing_com_dict[host],
        'sync_php_file': api_type_dict[row['ApiType']] if row['ApiType'] != None else '',
        'leading_id': 0,
        'service': 13,
        'start_date': row['RaceTime'],
        'create_user_id': 'season',
        'is_deleted': 0,
        'is_passed': 1
    }

    return contest_data

### Race ###
def getRaceStatement(RACEID):    
    race_statement = f"""SELECT r.RaceId, r.bannerFile, eck.EventName, eck.EventId, eck.event_type, eck.CPId, eck.CPName, eck.CPDistance
                        FROM `race` r,
                            (SELECT e.EventName, e.RaceId, ck.EventId, e.event_type, ck.CPId, ck.CPName, ck.CPDistance
                            FROM `event_checkpoint` ck, `event` e
                            WHERE ck.`EventId`=e.`EventId` and e.`RaceId`='{RACEID}') eck
                        WHERE r.RaceId=eck.RaceId"""

    return race_statement

def getRaceCpConfig(row, i):
    CPID = ''
    if row['CPName'] == 'Gun Start':
        CPID = '0'
    elif row['CPName'] == 'Start':
        CPID = '00'
    elif row['CPName'] == 'FINISH':
        CPID = '99'
    else:
        CPID = str(i).zfill(2)
        i += 1

    race_cp_dict = {
            'CPId': CPID,
            'CPName': row['CPName'],
            'CPDistance': row['CPDistance']
    }

    return race_cp_dict, i

def getRaceData(row):
    EventType = {
        1: 1, # run
        4: 2, # swim
        5: 3, # bike
    }

    race_data = {
        'uid': row['EventId'],
        'contest_id': contest_id_dict[row['RaceId']],
        'sort': 0,
        'title': row['EventName'],
        'race_unit_type': EventType[row['event_type']],
        'banner': row['bannerFile'],
        'race_status': 36,
        'cp_json': '',
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

def getRecordStatement(table, RACEID):
    record_statement = f"""SELECT *
            FROM `event` e,
                    (SELECT *
                    FROM `athlete` a, {table} r 
                    WHERE a.`AthleteDataId`=r.`DataId` and r.`EventCode`='{RACEID}') ar
            WHERE e.EventId=ar.AthleteEventId"""

    return record_statement

def getRecordCpTiming(row):
    check_num = TimeCheckNum[host]
    unit = 1000

    # get contest date
    contest_date_str = str(row['EventCode'])
    if len(contest_date_str) == 8:
        contest_date = datetime.strptime(contest_date_str, '%Y%m%d')
    elif len(contest_date_str) == 10:
        contest_date = datetime.strptime(contest_date_str, '%Y%m%d%H')

    record_cp_dict = [{
        "CP_Mode": "Gun",
        "CP_Time": getDate(contest_date, int(row['TimeGun'])//unit)
    },{
        "CP_Mode": "Start",
        "CP_Time": getDate(contest_date, int(row['TimeStart'])//unit)
    }]

    # TimeCheck 根據賽事有所不同
    for i in range(1, check_num+1):
        num = str(i).zfill(2)
        col = f"TimeCheck{num}"
        # 若"CP_time"為0 則不insert
        if row[col] == 0: # eb2 timecheck type is int
            break
        temp = {
            "CP_Mode": f"CP{num}",
            "CP_Time": getDate(contest_date, int(row[col])//unit)
        }
        record_cp_dict.append(temp)

    # insert finish time
    finish_cp = {
        "CP_Mode": "End",
        "CP_Time": getDate(contest_date, int(row['TimeFinish'])//unit)
    }
    record_cp_dict.append(finish_cp)

    record_cp_json = json.dumps(record_cp_dict)

    return record_cp_json

def getRecordData(row, record_cp):
    unit = 1000
    person_finish_time = float(row['personalFinishTime']) // unit
    gun_finish_time = float(row['finishTime']) // unit

    record_data = {
        'uid': row['AthleteDataId'],
        'race_id': race_id_dict[row['EventId']],
        'number': row['AthleteNo'],
        'name': row['AthleteName'],
        'nation': row['AthleteCountryCode'],
        'gender': 1 if row['AthleteGender'] == 'M' else 2,  # turn varchar into int
        'group': row['AthleteGroup'],
        'person_finish_time': person_finish_time if person_finish_time>=0 else 0,
        'gun_finish_time': gun_finish_time if gun_finish_time>=0 else 0,
        'team': row['AthleteTeam'],
        'team_sort': 0,
        'total_place': row['RankAll'],
        'group_place': row['RankCat'],
        'gender_place': row['RankSex'],
        'cp_timing_json': record_cp,
        'is_deleted': 0,
        'is_disqualified': 0,
        'is_passed': 0
    }
    
    return record_data