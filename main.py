import dataset
from getDictionary import *

oldDB = dataset.connect('mysql+pymysql://user:password@172.105.206.159/bravelog')
newDB = dataset.connect('mysql+pymysql://user:password@172.105.206.159/bravelog_new')

new_contest = newDB['contest']
new_race = newDB['race']
new_record = newDB['record']

oldDB.begin()
newDB.begin()

def insertToContest(id):
    for row in oldDB['race']:
        id += 1
        contest_data = getContestData(row, id)
        new_contest.insert(contest_data)
    newDB.commit()
    print("contest insert success")

def insertToRace(id, host):
    race_statement = getRaceStatement(host)
    event = ''
    race_data = {}

    for row in oldDB.query(race_statement):
        cp_dict = getRaceCpConfig(row)
        
        # 若上一row與這一row的EventName不一樣,代表此賽事的cp_json新增完畢 -> insert到db
        if event != row['EventName']:
            if event != '': # 第一次不insert
                race_data['cp_json'] = str(race_data['cp_json'])
                new_race.insert(race_data)

            event = row['EventName']
            id += 1
            race_data = getRaceData(row, id, cp_dict)
            
        else:
            race_data['cp_json'].append(cp_dict)
            
    race_data['cp_json'] = str(race_data['cp_json'])
    new_race.insert(race_data)

    newDB.commit()
    print("race insert success")

def insertToRecord(id, table, TimeCheck_num):
    record_statement = getRecordStatement(table)
    
    for row in oldDB.query(record_statement):
        id += 1
        
        cp_timing_dict = getRecordCpTiming(row, TimeCheck_num)
        record_data = getRecordData(row, id, cp_timing_dict)
        new_record.insert(record_data)

    newDB.commit()
    print("record insert success")

def findMaxId(table):
    statement = f'SELECT MAX(x.id) AS max_id FROM {table} x'
    id = [row for row in newDB.query(statement)]
    if id[0]['max_id'] == None:
        return 0
    else:
        return id[0]['max_id']

def main():
    try:
        # insertToContest(findMaxId('contest'))

        insertToRace(findMaxId('race'), 'sportsman')
        insertToRace(findMaxId('race'), 'di')

        # insertToRecord(findMaxId('record'), 'sportsnet_result', 12)
        # insertToRecord(findMaxId('record'), 'di_result', 9)

    except Exception as err:
        newDB.rollback()
        print(err)

if __name__ == "__main__":
    main()