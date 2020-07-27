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

    # def getAllKey(self):
    #     all_key = self.r.keys()
    #     print(all_key)

    # def setKey(self, key, value):
    #     self.r.set('food', 'beef')
    
    # def getKey(self, key):
    #     value = self.r.get(key)
    #     print(value)

    # def getList(self): # O(N)

    # def getHash(self): # O(1)

    # def getSet(self):

    # def getSortSet(self):

def main():
    r = redisDB().connect()
    p = r.pipeline()

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

    username = 'userA'
    if r.exists(username) == None:
        print(username + ' is not exist')
    else:
        print(r.hgetall(username)) # O(N)

    print(r.keys())
    
    print('user number: ' + r['user_number'])

if __name__ == "__main__":
    main()