from datetime import datetime, timedelta
import json
#### 無event_checkpoint table
# check 'TimeCheckNum' 'api_type_dict' 'timing_com_dict'
host = 'accurat'
RACEID_arr = [''] #

contest_id_dict = {}
race_id_dict = {}
mainFields = []

### Contest ###
def getContestData(row):
    contest_data = {
        'uid': row['RaceId'],
        'title': row['RaceName'],
        'banner': row['url'],
        'timing_com': 24, # accurat
        'sync_php_file': '',
        'leading_id': 0,
        'service': 13,
        'start_date': row['RaceTime'],
        'create_user_id': 'season',
        'is_deleted': 0,
        'is_passed': 1
    }
    return contest_data

### Race ###
def getRaceCpConfig(row):
    race_cp_config = {
        'RaceID': '',
        'data': [],
        'exec_start': 1600391943.037,
        'exec_time': 0.051820993423462,
        'activity': '4396'
    }
    return race_cp_config

def accuratdef_to_cpjson(row_acc):
    acc_dict = json.loads(row_acc)

    type_dict = {
        '': 'Gun',
        '': 'Run',
        '': 'Bike',
        '': 'T1',
        '': 'T2',
        '': 'FINISH'
    }
    unit_dict = {
        'Run': 'min/km',
        'Bike': 'km/hr'
    }

    cp_arr = []
    i = 0
    mainFields = acc_dict['mainFields'] # restore for record use
    for field in mainFields:
        CPID = str(i).zfill(2)
        CPName = f'{field}_ENAME'
        CPDistance = f'{field}_DIST'

        race_cp_dict = {
            'CPId': CPID,
            'CPName': acc_dict[CPName],
            'CPShow': '', # for front-end?
            'CPTYPE': type_dict[], # check type?
            'CPACTION': ['', ''],
            'CPUNIT': unit_dict[], # check swim unit?
            'CPMemo': '',
            'CPDistance': acc_dict[CPDistance]
        }
        cp_arr.append(race_cp_dict)
        i += 1

    return cp_arr

def getRaceData(row, cp_json):
    EventType = {
        1: 1, # run
        4: 2, # swim
        5: 3, # bike
    }

    race_data = {
        'uid': row['EventId'],
        'contest_id': contest_id_dict[row['RaceId']],
        'sort': 0,
        'title': row['EventName'], # check all event in a json, or seperate into many row?
        'race_unit_type': EventType[row['event_type']], # check ironman type?
        'banner': '',
        'race_status': 36,
        'cp_json': cp_json,
        'create_user_id': 'season',
        'is_deleted': 0,
        'is_passed': 0
    }
    return race_data

### Record ###
def getRecordStatement(table, RACEID):
    record_statement = f"SELECT * \
            FROM `event` e, \
                    (SELECT * \
                    FROM `athlete` a, {table} r  \
                    WHERE a.`AthleteRaceId`='{RACEID}' and r.`EventCode`='{RACEID}' ar \
            WHERE e.`RaceId`=ar.`EventCode`"
    return record_statement

def get_cp_timeing_json(mode, date, time_str): # ('Gun', 20191117, '00:20:39')
    time = time_str.split(':')
    date = date + timedelta(hours=int(time[0]), minutes=int(time[1]), seconds=int(time[2]))

    cp_timing_json = {
        "CP_Mode": mode,
        "CP_Time": str(date)
    }
    return cp_timing_json

def getRecordCpTiming(row):
    result_dict = json.loads(row['resultData'])

    # get contest date
    contest_date_str = str(row['EventCode'])
    if len(contest_date_str) == 8:
        contest_date = datetime.strptime(contest_date_str, '%Y%m%d')
    elif len(contest_date_str) == 10:
        contest_date = datetime.strptime(contest_date_str, '%Y%m%d%H')

    # insert field
    fields = ['Gun', 'Start']
    fields.append(mainFields)
    fields.append('FINISH')

    cp_timeing_json_arr = []
    next_date = contest_date
    for field in fields:
        _cp = get_cp_timeing_json(field, next_date, result_dict[field])
        cp_timeing_json_arr.append(_cp)
        next_date = _cp['CP_Time']

    record_cp_json = json.dumps(cp_timeing_json_arr)

    return record_cp_json

def getRecordData(row, record_cp): #### 大改 = =
    result_dict = json.loads(row['resultData'])

    t = result_dict['FinishedNodeTotalValue'].split(':')
    person_finish_time = int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2])

    record_data = {
        'uid': row['AthleteDataId'],
        'race_id': race_id_dict[row['EventId']],
        'number': result_dict['PlayerNo'],
        'name': result_dict['PlayerName'],
        'nation': result_dict['Group4'], # ??
        'gender': 0, # ???
        'group': result_dict['Group2'], # ??
        'person_finish_time': person_finish_time,
        'gun_finish_time': 0, # ???
        'team': result_dict['Group2'], # ??
        'team_sort': 0,
        'total_place': row['placerder'], 
        'group_place': 0, # ???
        'gender_place': 0, # ???
        'cp_timing_json': record_cp,
        'is_deleted': 0,
        'is_disqualified': 0,
        'is_passed': 0
    }
    return record_data