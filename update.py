import dataset
from getDictionary import *
from utils.log_utils import Logger

# oldDB = dataset.connect('mysql+pymysql://user:password@172.105.206.159/bravelog')
oldDB = dataset.connect('mysql+pymysql://BraveLogAdmin@bravelog-mysql-basic:!BL@5270$4888*B@bravelog-mysql-basic.mysql.database.azure.com/bravelog')
# newDB = dataset.connect('mysql+pymysql://user:password@172.105.206.159/bravelog_new')
newDB = dataset.connect('mysql+pymysql://BraveLogAdmin@bravelog-mysql-basic:!BL@5270$4888*B@bravelog-mysql-basic.mysql.database.azure.com/bravelog2020')

oldDB.begin()
newDB.begin()

host = 'sportsnet'
RACEID_arr = ['2020011901']

def updateRace(RACEID):
    race_sql = f"""SELECT r.RaceId, eck.EventName, eck.EventId, eck.CPId, eck.CPName, eck.CPDistance
                    FROM `race` r,
                        (SELECT e.EventName, e.RaceId, ck.EventId, ck.CPId, ck.CPName, ck.CPDistance
                        FROM `event_checkpoint` ck, `event` e
                        WHERE ck.`EventId`=e.`EventId` and e.`RaceId`='{RACEID}') eck
                    WHERE r.RaceId=eck.RaceId"""
    table = oldDB.query(race_sql)

    event_id = ''
    race_data = {}
    cp_json_dict = {
        'Event': '',
        'CP': []
    }
    i = 1
    for row in table:
        cp_dict, i = getRaceCpConfig(row, i)
        
        # 若上一row與這一row的EventName不一樣,代表此賽事的cp_json新增完畢 -> insert到db
        if event_id != row['EventId']:
            if event_id != '': # 第一次不update
                cp_json = json.dumps(cp_json_dict, ensure_ascii=False)
                update_sql = f"""UPDATE race SET cp_json='{cp_json}' WHERE uid='{event_id}';"""
                newDB.query(update_sql)
                i = 1

            event_id = row['EventId']
            cp_json_dict['Event'] = row['EventName']
            cp_json_dict['CP'] = [cp_dict]
        else:
            cp_json_dict['CP'].append(cp_dict)

    cp_json = json.dumps(cp_json_dict, ensure_ascii=False)
    update_sql = f"""UPDATE race SET cp_json='{cp_json}' WHERE uid='{event_id}';"""
    newDB.query(update_sql)

    newDB.commit()
    mylog.info(f"event update success -- ID {RACEID}")

def for_sportsnet_getRecordSQL(RACEID, DataId, AthleteNo):
    forign_sql = f"and r.`EventCode`='{RACEID}' and a.`AthleteRaceId`='{RACEID}'"

    record_sql = f"SELECT * \
            FROM `event` e, \
                    (SELECT * \
                    FROM `athlete` a, `sportsnet_result` r  \
                    WHERE a.`AthleteNo`='{AthleteNo}' and r.`DataId`='{DataId}' {forign_sql}) ar \
            WHERE e.EventId=ar.AthleteEventId"
    return record_sql

def for_sportsnet_getParameter(RACEID):
    _statement = f'SELECT * FROM `sportsnet_result` WHERE `EventCode` LIKE {RACEID}'
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

def updateRecord(RACEID):
    result_athlete_mapping_dict = for_sportsnet_getParameter(RACEID)
    for _key, _val in result_athlete_mapping_dict.items():
        record_SQL = for_sportsnet_getRecordSQL(RACEID, _key, _val)
        table = oldDB.query(record_SQL)
        for row in table:
            cp_timing = getRecordCpTiming(row)
            update_sql = f"""UPDATE record SET cp_timing_json='{cp_timing}' WHERE uid='{row['AthleteDataId']}';"""
            newDB.query(update_sql)

    newDB.commit()
    mylog.info(f"record update success -- ID {RACEID}")

def main():
    try:
        for RACEID in RACEID_arr:
            updateRace(RACEID)
            updateRecord(RACEID)
            print('\n')

    except Exception as err:
        newDB.rollback()
        mylog.error("Transaction error -> " + str(err))

if __name__ == "__main__":
    mylog = Logger(logger="admin")
    main()