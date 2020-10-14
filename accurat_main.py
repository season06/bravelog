import dataset
from accurat_getDictionary import *
from utils.log_utils import Logger

oldDB = dataset.connect('mysql+pymysql://BraveLogAdmin@bravelog-mysql-basic:!BL@5270$4888*B@bravelog-mysql-basic.mysql.database.azure.com/bravelog')
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
        
        # return primary_key after insert, store in dictionary.
        primary_id = new_contest.insert(contest_data) 
        contest_id_dict[contest_data['uid']] = primary_id

    newDB.commit()
    mylog.info(f"contest insert success -- ID {RACEID}")

def insertToRace(RACEID):
    raceSQL = f'select * from `event` where RaceId = {RACEID}'
    table = oldDB.query(raceSQL)

    ### insert to race
    data = []
    for row in table:
        resultSQL = f"select resultData from accurat_result where Race='{row['EventId']}'"
        t_result = oldDB.query(resultSQL)
        
        cp_arr = accuratdef_to_cpjson(row['EventId'], row['accurat_def'], list(t_result)[0]['resultData'])
        cp_json_dict = {
            'Event': row['EventName'],
            'CP': cp_arr
        }
        # data.append(cp_json_dict)
    
        race_cp_config = {
            'RaceID': RACEID,
            'data': cp_json_dict,
            'exec_start': 'float', # ?
            'exec_time': 'float', # ?
            'activity': 'str' # ?
        }
        race_data = getRaceData(row, race_cp_config)
        ### return primary_key after insert, store in dictionary.
        primary_id = new_race.insert(race_data)
        race_id_dict[race_data['uid']] = primary_id

    newDB.commit()
    mylog.info(f"race insert success -- ID {RACEID}")

def insertRecord(RACEID):
    recordSQL = f"""SELECT *
                    FROM `event` e, `accurat_result` r 
                    WHERE e.`EventId`=r.`Race` and r.`EventCode`='{RACEID}'"""
    table = oldDB.query(recordSQL)

    for row in table:
        cp_timing = getRecordCpTiming(row)
        record_data = getRecordData(row, cp_timing)
        new_record.insert(record_data)

    newDB.commit()
    mylog.info(f"record insert success -- ID {RACEID}")

def findEventCode():
    table = f'{host}_result'
    arr = []
    stat = f'SELECT DISTINCT(EventCode), count(*) FROM `{table}` group by EventCode'
    table = oldDB.query(stat)
    for row in table:
        arr.append(row['EventCode'])
    print(arr)

def main():
    try:
        for _race in RACEID_arr:
            insertToContest(_race)
            insertToRace(_race)
            insertRecord(_race)
            print('\n')

    except Exception as err:
        newDB.rollback()
        mylog.error("Transaction error -> " + str(err))

if __name__ == "__main__":
    mylog = Logger(logger="admin")
    main()