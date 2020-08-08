import redis
import time
import schedule
from datetime import datetime, timedelta
import dataset
import random

class redisDB():
    def __init__(self):
        REDIS_CONFIG = {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'decode_responses': True
        }
        pool = redis.ConnectionPool(**REDIS_CONFIG)
        self.r = redis.StrictRedis(connection_pool = pool)
        
    def connect(self):
        return self.r

    # def find_user_hash(self):
    #     username = 'userA'
    #     if self.r.exists(username) == None:
    #         print(username + ' is not exist')
    #     else:
    #         print(self.r.hgetall(username)) # O(N)

    def insert_user_info(self, contest_date):
        pipe = self.r.pipeline()

        contest_id_hash = f'{contest_date}_userid_result_1212'
        contest_id_zsort = f'{contest_date}_order_by_gun_finish_time_1212'
        for i in range(10):
            user_id = f'member_{i}'
            json_str_value = i
            pipe.hset(contest_id_hash,  user_id, json_str_value)

            score_dict = {
                user_id: i
            }
            pipe.zadd(contest_id_zsort, score_dict)
        
        pipe.execute()

        print(self.r.zrange(contest_id_zsort, 0, -1))

    def check_time_expire(self):
        redis_keys_arr = self.r.keys()
        for key in redis_keys_arr:
            key_arr = key.split('_')

            now_time_str = time.strftime('%Y%m%d')
            now_time = datetime.strptime(now_time_str, '%Y%m%d')
            contest_time = datetime.strptime(key_arr[0], "%Y%m%d")

            minus_day = now_time - contest_time
            if minus_day > timedelta(days=2):
                self.r.delete(key)
    
    def insert_user_random_time(self):
        pipe = self.r.pipeline()

        hash_table_name = '2020080932_user_result'
        with dataset.connect('mysql+pymysql://user:password@172.105.206.159/test') as db:
            for row in db['marathon']:
                hash_key = f"3_{row['number']}"
                hash_value = {
                    'race_id': 3,
                    'number': row['number'],
                    'group': row['group'],
                    'name': row['name'],
                    'gender': row['gender'],
                    'person_finish_time': get_random_time()
                }
                pipe.hset(hash_table_name, hash_key, str(hash_value))
            pipe.execute()

def get_random_time():
    # time range
    a1=(2020,7,7,1,45,0,0,0,0)
    a2=(2020,7,7,2,15,59,0,0,0)
    start=time.mktime(a1)
    end=time.mktime(a2)

    # random time
    t = random.randint(start,end)
    date_touple = time.localtime(t)
    date_str = time.strftime("%H:%M:%S",date_touple)
    return date_str

def main():
    Redis = redisDB()
    r = Redis.connect()

    # Redis.insert_user_info('20200803')
    # Redis.insert_user_info('20200629')
    # schedule.every().wednesday.at('11:00').do(Redis.check_time_expire)

    Redis.insert_user_random_time()
    
    hash_table_name = '2020080932_user_result'
    key_list = list(r.hgetall(hash_table_name))
    value_list = list(r.hgetall(hash_table_name).values())
    for i in range(len(key_list)):
        print(key_list[i], ':: ', value_list[i])

if __name__ == "__main__":
    main()

# cd /usr/local/opt/redis/bin open redis-cli

# 3 min 6 9