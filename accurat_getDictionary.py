from datetime import datetime, timedelta
import json

host = 'accurat'
RACEID_arr = ['2019122803'] #

contest_id_dict = {}
race_id_dict = {}
mainField_dict = {}

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

def accuratdef_to_cpjson(eventid, row_acc, result_acc):
    acc_dict = json.loads(row_acc)
    result_dict = json.loads(result_acc)

    # type_dict = {
    #     '': 'Gun',
    #     '': 'Run',
    #     '': 'Bike',
    #     '': 'T1',
    #     '': 'T2',
    #     '': 'FINISH'
    # }
    unit_dict = {
        'run': 'min/km',
        'bike': 'km/hr',
        'swim': 'm/min'
    }

    cp_arr = []
    i = 1
    mainField_dict[eventid] = acc_dict['mainFields']
    for field in acc_dict['mainFields']:
        CPID = str(i).zfill(2)
        CPName = f'{field}_ENAME'
        CPDistance = f'{field}_DIST'
        CPType = f'{field}_TYPE'

        race_cp_dict = {
            'CPId': CPID,
            'CPName': acc_dict[CPName],
            'CPShow': acc_dict[CPName],
            'CPTYPE': result_dict[CPType], # check type?
            'CPACTION': ['', ''],
            'CPUNIT': unit_dict.get(result_dict[CPType].lower(), ''), # check swim unit?
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
        3: 3, # ironman
        5: 3, # bike
    }

    race_data = {
        'uid': row['EventId'],
        'contest_id': contest_id_dict[row['RaceId']],
        'sort': 0,
        'title': row['EventName'], # check all event in a json, or seperate into many row?
        'race_unit_type': EventType[row['event_type']],
        'banner': '',
        'race_status': 36,
        'cp_json': json.dumps(cp_json, ensure_ascii=False).encode('utf8'),
        'create_user_id': 'season',
        'is_deleted': 0,
        'is_passed': 0
    }
    return race_data

### Record ###
def get_cp_timeing_json(mode, date_str, time_str): # ('Gun', '20191117', '00:20:39')
    if time_str == '--:--:--':
        return 0

    date = ''
    if len(date_str) == 8:
        date = datetime.strptime(date_str, '%Y%m%d')
    elif len(date_str) == 10:
        date = datetime.strptime(date_str, '%Y%m%d%H')
    else:
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    
    time = time_str.split(':')
    time = [ t if t != '--' else '0' for t in time]
    date = date + timedelta(hours=int(time[0]), minutes=int(time[1]), seconds=int(time[2]))

    cp_timing_json = {
        "CP_Mode": mode,
        "CP_Time": str(date)
    }
    return cp_timing_json

def getRecordCpTiming(row):
    result_dict = json.loads(row['resultData'])

    # insert field
    # fields = ['Gun', 'Start']
    fields = mainField_dict[row['EventId']]
    # fields.append('FINISH')

    cp_timeing_json_arr = []
    next_date = str(row['EventCode']) # get contest date
    for field in fields:
        _cp = get_cp_timeing_json(field, next_date, result_dict[field])
        if _cp == 0:
            break
        cp_timeing_json_arr.append(_cp)
        next_date = _cp['CP_Time']

    record_cp_json = json.dumps(cp_timeing_json_arr)

    return record_cp_json

def getRecordData(row, record_cp): #### 大改 = =
    result_dict = json.loads(row['resultData'])

    person_finish_time = '00:00:00'
    if result_dict['FinishedNodeTotalValue'] != '--:--:--':
        t = result_dict['FinishedNodeTotalValue'].split(':')
        person_finish_time = int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2])

    record_data = {
        'uid': row['DataId'],
        'race_id': race_id_dict[row['EventId']],
        'number': row['Bib'],
        'name': row['Name'],
        'nation': result_dict['Group4'], # ??
        'gender': row['Gender'], # ???
        'group': result_dict['Group2'], # ??
        'person_finish_time': person_finish_time,
        'gun_finish_time': 0, # ???
        'team': result_dict['Group2'], # ??
        'team_sort': 0,
        'total_place': row['placeOrder'], 
        'group_place': 0, # ???
        'gender_place': 0, # ???
        'cp_timing_json': record_cp,
        'is_deleted': 0,
        'is_disqualified': 0,
        'is_passed': 0
    }
    return record_data