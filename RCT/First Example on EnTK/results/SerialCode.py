#!/usr/bin/env python

import time

def basic_func(x):
    if x == 0:
        return 'zero'
    elif x%2 == 0:
        return 'even'
    else:
        return 'odd'

def main():
    for i in range(0,16):
        y = i*i
        time.sleep(2) #seconds
        print('{} squared results in a/an {} number'.format(i, basic_func(y)))

if __name__ == '__main__':
    start_time = time.time()
    main()
    print('That took {} seconds'.format(time.time() - start_time))