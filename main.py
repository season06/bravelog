import dataset
from getDictionary import *
from utils.log_utils import Logger

oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@172.105.206.159/bravelog')
newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@172.105.206.159/bravelog_new')

new_contest = newDB['contest']
new_race = newDB['race']
new_record = newDB['record']

oldDB.begin()
newDB.begin()

def insertToContest():
    table = oldDB['race']
    for row in table:
        contest_data = getContestData(row)
        new_contest.insert(contest_data)
    newDB.commit()
    mylog.info("contest insert success")

def insertToRace(host):
    race_statement = getRaceStatement(host)
    table = oldDB.query(race_statement)

    event = ''
    race_data = {}

    for row in table:
        cp_dict = getRaceCpConfig(row)
        
        # 若上一row與這一row的EventName不一樣,代表此賽事的cp_json新增完畢 -> insert到db
        if event != row['EventName']:
            if event != '': # 第一次不insert
                race_data['cp_json'] = str(race_data['cp_json'])
                new_race.insert(race_data)

            event = row['EventName']
            race_data = getRaceData(row, cp_dict)
            
        else:
            race_data['cp_json'].append(cp_dict)
            
    race_data['cp_json'] = str(race_data['cp_json'])
    new_race.insert(race_data)

    newDB.commit()
    mylog.info("race insert success")

def insertToRecord(table, TimeCheck_num):
    record_statement = getRecordStatement(table)
    table = oldDB.query(record_statement)

    for row in table:
        
        cp_timing_dict = getRecordCpTiming(row, TimeCheck_num)
        record_data = getRecordData(row, cp_timing_dict)
        new_record.insert(record_data)

    newDB.commit()
    mylog.info("record insert success")

def findMaxId(table):
    statement = f'SELECT MAX(x.id) AS max_id FROM {table} x'
    id = [row for row in newDB.query(statement)]
    if id[0]['max_id'] == None:
        return 0
    else:
        return id[0]['max_id']

def main():
    try:
        insertToContest()

        # insertToRace(findMaxId('race'), 'sportsman')
        insertToRace('di')

        # insertToRecord(findMaxId('record'), 'sportsnet_result', 12)
        insertToRecord('di_result', 9)

    except Exception as err:
        newDB.rollback()
        mylog.error("Transaction error -> " + str(err))

if __name__ == "__main__":
    mylog = Logger(logger="admin")
    main()