import dataset
from getDictionary import *
from utils.log_utils import Logger

oldDB = dataset.connect('mysql+pymysql://user:password@172.105.206.159/bravelog')
# oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog')
# newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog_new')
# oldDB = dataset.connect('mysql+pymysql://BraveLogAdmin@bravelog-mysql-basic:!BL@5270$4888*B@bravelog-mysql-basic.mysql.database.azure.com/bravelog')
newDB = dataset.connect('mysql+pymysql://user:password@172.105.206.159/bravelog_new')
# newDB = dataset.connect('mysql+pymysql://BraveLogAdmin@bravelog-mysql-basic:!BL@5270$4888*B@bravelog-mysql-basic.mysql.database.azure.com/bravelog2020')

new_contest = newDB['contest']
new_race = newDB['race']
new_record = newDB['record']

oldDB.begin()
newDB.begin()

def insertToContest(RACEID):
    table = oldDB['race']
    for row in table:
        if row['RaceId'] != RACEID: # select
            continue
        contest_data = getContestData(row)
        primary_id = new_contest.insert(contest_data) # return primary_key after insert
        contest_id_dict[contest_data['uid']] = primary_id

    newDB.commit()
    mylog.info(f"contest insert success -- ID {RACEID}")

def insertToRace(RACEID):
    race_statement = getRaceStatement(RACEID)
    table = oldDB.query(race_statement)

    event = ''
    race_data = {}
    cp_json_dict = {
        'Event': '',
        'CP': []
    }
    i = 1

    for row in table:
        cp_dict, i = getRaceCpConfig(row, i)
        
        # 若上一row與這一row的EventName不一樣,代表此賽事的cp_json新增完畢 -> insert到db
        if event != row['EventName']:
            if event != '': # 第一次不insert
                cp_json = json.dumps(cp_json_dict, ensure_ascii=False).encode('utf8')
                race_data['cp_json'] = cp_json
                primary_id = new_race.insert(race_data) # return primary_key after insert
                race_id_dict[race_data['uid']] = primary_id
                i = 1

            race_data = getRaceData(row)
            event = row['EventName']
            cp_json_dict['Event'] = row['EventName']
            cp_json_dict['CP'] = [cp_dict]
        else:
            cp_json_dict['CP'].append(cp_dict)

    cp_json = json.dumps(cp_json_dict, ensure_ascii=False).encode('utf8')
    race_data['cp_json'] = cp_json
    primary_id = new_race.insert(race_data) # return primary_key after insert
    race_id_dict[race_data['uid']] = primary_id

    newDB.commit()
    mylog.info(f"race insert success -- ID {RACEID}")

def for_sportsnet_getParameter(_race):
    _statement = f"""SELECT * FROM `sportsnet_result` WHERE `EventCode` LIKE {_race}"""
    table = oldDB.query(_statement)
    result_athlete_mapping_dict = {} # 'DataId': 'AthleteNo'

    for row in table:
        DataId = row['DataId']

        AthleteNo = DataId.split('_')[1]
        if len(AthleteNo) < 5:
            AthleteNo = AthleteNo.zfill(5)

        result_athlete_mapping_dict[DataId] = AthleteNo
    
    # del result_athlete_mapping_dict['20181028_0000_DW1H8BD']
    return result_athlete_mapping_dict

def for_sportsnet_getRecordStatement(RACEID, DataId, AthleteNo):
    RECORD_STET = f"""and r.`EventCode`='{RACEID}' and a.`AthleteRaceId`='{RACEID}'"""

    record_statement = f"""SELECT *
            FROM `event` e,
                    (SELECT *
                    FROM `athlete` a, `sportsnet_result` r 
                    WHERE a.`AthleteNo`='{AthleteNo}' and r.`DataId`='{DataId}' {RECORD_STET}) ar
            WHERE e.EventId=ar.AthleteEventId"""
    return record_statement

def for_sportsnet_insertToRecord(RACEID):
    result_athlete_mapping_dict = for_sportsnet_getParameter(RACEID) ##

    for _key, _val in result_athlete_mapping_dict.items():
        record_statement = for_sportsnet_getRecordStatement(RACEID, _key, _val)
        table = oldDB.query(record_statement)
        for row in table:
            cp_timing = getRecordCpTiming(row)
            record_data = getRecordData(row, cp_timing)
            new_record.insert(record_data)

    newDB.commit()
    mylog.info(f"record insert success -- ID {RACEID}")

def insertToRecord(RACEID):
    table_name = f'{host}_result'
    record_statement = getRecordStatement(table_name, RACEID)
    table = oldDB.query(record_statement)

    for row in table:
        cp_timing = getRecordCpTiming(row)
        record_data = getRecordData(row, cp_timing)
        new_record.insert(record_data)

    newDB.commit()
    mylog.info(f"record insert success -- ID {RACEID}")

def findEventCode(): # return IDs
    table = f'accurat_result'
    arr = []
    stat = f"""SELECT DISTINCT(EventCode), count(*) FROM `{table}` group by EventCode"""
    table = oldDB.query(stat)
    for row in table:
        arr.append(row['EventCode'])
    print(arr)

def main():
    try:
        # findEventCode()
        for _race in RACEID_arr:
            insertToContest(_race)
            insertToRace(_race)
            # insertToRecord(_race)
            for_sportsnet_insertToRecord(_race)
            print('\n')

    except Exception as err:
        newDB.rollback()
        mylog.error("Transaction error -> " + str(err))

if __name__ == "__main__":
    mylog = Logger(logger="admin")
    main()