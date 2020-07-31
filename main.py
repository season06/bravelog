import dataset
from getDictionary import *
from utils.log_utils import Logger

oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog')
newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog_new')
# oldDB = dataset.connect('mysql+pymysql://user:password@172.105.206.159/bravelog')
# newDB = dataset.connect('mysql+pymysql://user:password@172.105.206.159/bravelog_new')

new_contest = newDB['contest']
new_race = newDB['race']
new_record = newDB['record']

oldDB.begin()
newDB.begin()

def insertToContest(host):
    table = oldDB['race']
    for row in table:
        contest_data = getContestData(row, host)
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

def insertToRecord(host):
    table = f'{host}_result'
    record_statement = getRecordStatement(table)
    table = oldDB.query(record_statement)

    for row in table:
        cp_timing_dict = getRecordCpTiming(row, host)
        record_data = getRecordData(row, cp_timing_dict, host)
        new_record.insert(record_data)

    newDB.commit()
    mylog.info("record insert success")

def main():
    try:
        host = 'di'
        insertToContest(host)
        insertToRace(host)
        insertToRecord(host)

    except Exception as err:
        newDB.rollback()
        mylog.error("Transaction error -> " + str(err))

if __name__ == "__main__":
    mylog = Logger(logger="admin")
    main()