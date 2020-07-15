import dataset
oldDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog')
newDB = dataset.connect('mysql+pymysql://root:tNMW9ksfylH1oosQ@localhost/bravelog_new')

new_contest = newDB['contest']
new_race = newDB['race']
new_record = newDB['record']

oldDB.begin()
newDB.begin()

def contest(id):
    for row in oldDB['race']:
        id += 1
        data = {
            'id': id,
            'uid': row['RaceId'],
            'title': row['RaceName'],
            'banner': row['url'],
            'leading_id': 0,
            'service': 13,
            'start_date': row['RaceTime'],
            'create_user_id': 'season',
            'is_deleted': 0,
            'is_passed': 0
        }
        new_contest.insert(data)
    newDB.commit()
    print("contest insert success")

def race(id, statement):
    event = ''
    data = {}

    for row in oldDB.query(statement):
        cp_config = {
                'CPId': row['CPId'],
                'CPName': row['CPName'],
                'CPDistance': row['CPDistance']
        }
        
        # 若上一row與這一row的EventName不一樣
        # 代表此賽事的cp_json新增完畢 -> insert到db
        if event != row['EventName']:
            if event != '': # 第一次不insert
                data['cp_json'] = str(data['cp_json'])
                new_race.insert(data)

            event = row['EventName']
            id += 1
            
            data = {
                'id': id,
                'uid': id,
                'contest_id': row['RaceId'],
                'sort': id,
                'title': row['EventName'],
                'banner': row['bannerFile'],
                'race_status': 36,
                'cp_json': [cp_config],
                'create_user_id': 'season',
                'is_deleted': 0,
                'is_passed': 0
            }
        else:
            data['cp_json'].append(cp_config)
            
    data['cp_json'] = str(data['cp_json'])
    new_race.insert(data)

    newDB.commit()
    print("race insert success")

def record(id, table, TimeCheck_num):
    statement = f'SELECT * \
                FROM `event` e, \
                      (SELECT * \
                       FROM `athlete` a, {table} r  \
                       WHERE a.`AthleteDataId`=r.`DataId`) ar \
                WHERE e.EventId=ar.AthleteEventId'

    for row in oldDB.query(statement):
        id += 1
        
        # for cp_config, TimeCheck根據賽事有所不同
        cp_config = [{
                        'CP_Mode': 'Gun',
                        'CP_Time': row['TimeGun']
                    },{
                        'CP_Mode': 'Start',
                        'CP_Time': row['TimeStart']
                    },{
                        'CP_Mode': 'End',
                        'CP_Time': row['finishTime']
                    }]
        for i in range(1,TimeCheck_num+1):
            col = f'TimeCheck0{i}' if i<10 else f'TimeCheck{i}'
            temp = {
                'CP_Mode': f'CP{i}',
                'CP_Time': row[col]
            }
            cp_config.append(temp)
        
        data = {
            'id': id,
            'uid': id,
            'race_id': row['RaceId'],
            'number': row['AthleteNo'],
            'name': row['AthleteName'],
            'nation': row['AthleteCountryCode'],
            'gender': 0 if row['AthleteGender'] == 'M' else 1,  # turn varchar into int
            'group': row['AthleteGroup'],
            'person_finish_time': float(row['personalFinishTime']),
            'gun_finish_time': float(row['finishTime']),
            'team': row['AthleteTeam'],
            'team_sort': id,
            'total_place': row['RankAll'],
            'group_place': row['RankCat'],
            'gender_place': row['RankSex'],
            'cp_timing_json': str(cp_config),
            'is_deleted': 0,
            'is_disqualified': 0,
            'is_passed': 0
        }
        new_record.insert(data)
    newDB.commit()
    print("record insert success")

def find_max_id(table):
    statement = f'SELECT MAX(x.id) AS max_id FROM {table} x'
    id = [row for row in newDB.query(statement)]
    if id[0]['max_id'] == None:
        return 0
    else:
        return id[0]['max_id']

def main():
    try:
        contest(find_max_id('contest'))

        stmt_sportsman = 'SELECT r.RaceId, r.bannerFile, eck.EventName, eck.EventId, eck.CPId, eck.CPName, eck.CPDistance \
                                FROM `race` r, \
                                    (SELECT e.EventName, e.RaceId, ck.EventId, ck.CPId, ck.CPName, ck.CPDistance \
                                    FROM `event_checkpoint` ck, `event` e \
                                    WHERE ck.`EventId`=e.`EventId`) eck \
                                WHERE r.RaceId=eck.EventId'
        race(find_max_id('race'), stmt_sportsman)

        stmt_di = 'SELECT r.RaceId, r.bannerFile, eck.EventName, eck.EventId, eck.CPId, eck.CPName, eck.CPDistance \
                        FROM `race` r, \
                            (SELECT e.EventName, e.RaceId, ck.EventId, ck.CPId, ck.CPName, ck.CPDistance \
                            FROM `event_checkpoint` ck, `event` e \
                            WHERE ck.`EventId`=e.`EventId`) eck \
                        WHERE r.RaceId=eck.RaceId'
        race(find_max_id('race'), stmt_di)

        record(find_max_id('record'), 'sportsnet_result', 12)
        record(find_max_id('record'), 'di_result', 9)

    except Exception as err:
        newDB.rollback()
        print(err)

if __name__ == "__main__":
    main()