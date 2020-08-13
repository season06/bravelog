import dataset

def getStatement(race_id, event_id):
    statement = f"""SELECT e.`RaceId`, eck.`EventId`, COUNT(*) as num
                    FROM `event` e, `event_checkpoint` eck
                    WHERE e.`RaceId` = '{race_id}' and eck.`EventId` = '{event_id}' and e.`EventId` = eck.`EventId`
                    GROUP BY eck.EventId
                    ORDER BY eck.EventId"""
    return statement


def main():
    event_table = 0
    check_table = 0

    NOtable = {}

    with dataset.connect('mysql+pymysql://BraveLogAdminR:!BL@5270$4888*local@52.230.126.251/bravelog') as db:
        raceDB = db['race']
        for race in raceDB:
            race_id = race['RaceId']

            NOevent = []
            eventDB = db['event'].find(RaceId=race_id)
            for event in eventDB:
                event_id = event['EventId']

                checkDB = db['event_checkpoint'].find(EventId=event_id)
                n = 0
                for check in checkDB:
                    n += 1
                _print = f"{race_id}, {event_id}, {n}"
                print(_print)

                
                event_table += 1
                check_table += n
                NOevent.append(event_id)

            if n==0:
                _key = f"""{race['RaceName']}, {race_id}"""
                NOtable[_key] = NOevent

        print('event_table: ', event_table)
        print('check_table: ', check_table)
        print(NOtable)

if __name__ == "__main__":
    main()