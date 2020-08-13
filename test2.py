import os
import time
from 

last_time = ''

if __name__ == '__main__':
    file_name = 'test.py'
    while(1):
        modify_time = time.ctime(os.path.getmtime(file_name))
        if modify_time != last_time:
            last_time = modify_time
            print('Last modified:', modify_time)
            
