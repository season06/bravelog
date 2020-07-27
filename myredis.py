import redis
class redisDB():
    def connect(self):
        REDIS_CONFIG = {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'decode_responses': True
        }
        r = redis.Redis(**REDIS_CONFIG)
        return r

def main():
    r = redisDB().connect()
    p = r.pipeline()    # create a pipeline

    # insert user info
    for i in range(10):
        user = 'user' + chr(i+65)
        account = str(i*10)
        email = user + '@gmail.com'
        phone = '09123456' + str(i)

        p.hset(user, 'account', account)
        p.hset(user, 'email', email)
        p.hset(user, 'phone', phone)

        p.incr('user_number')
    
    p.execute()

    # search user
    username = 'userA'
    if r.exists(username) == None:
        print(username + ' is not exist')
    else:
        print(r.hgetall(username)) # O(N)

    print(r.keys())
    print('user number: ' + r['user_number'])

if __name__ == "__main__":
    main()