import dataset
from getDictionary_accurat import *
from utils.log_utils import Logger

# oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog')
# newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog_new')
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
    race_statement = f'select * from `event` where RaceId = {RACEID}'
    table = oldDB.query(race_statement)

    data = []
    for row in table:
        cp_arr = accuratdef_to_cpjson(row['accurat_def'])
        cp_json_dict = {
            'Event': row['EventName'],
            'CP': cp_arr
        }
        cp_json = json.dumps(cp_json_dict, ensure_ascii=False).encode('utf8')
        data.append(cp_json)
    
    race_cp_config = {
        'RaceID': RACEID,
        'data': data,
        'exec_start': 'float', # ?
        'exec_time': 'float', # ?
        'activity': 'str' # ?
    }
    race_data = getRaceData(row, race_cp_config)
    # return primary_key after insert, store in dictionary.
    primary_id = new_race.insert(race_data)
    race_id_dict[race_data['uid']] = primary_id

    newDB.commit()
    mylog.info(f"race insert success -- ID {RACEID}")

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

def findEventCode():
    table = 'focusline_result'
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
            # insertToRecord(_race)
            print('\n')

    except Exception as err:
        newDB.rollback()
        mylog.error("Transaction error -> " + str(err))

if __name__ == "__main__":
    mylog = Logger(logger="admin")
    main()