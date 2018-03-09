import threading
import time
import logging
import random


def withdraw(fromAcc1, fromAcc2):
   for i in range(50):
       r = random.random()
       logging.debug('Sleeping %0.02f', r)
       time.sleep(r)
       fromAcc1.withdraw(r)
       fromAcc2.withdraw(r)
       print("account1 withdraw: {}".format(fromAcc1.value))
       print("account2 withdraw: {}".format(fromAcc2.value))
       print(fromAcc1.value - fromAcc2.value)


def deposit(toAcc1, toAcc2):
   for i in range(50):
       r = random.random()
       logging.debug('Sleeping %0.02f', r)
       time.sleep(r)
       toAcc1.deposit(r)
       toAcc2.deposit(r)
       print("account1 deposit: {}".format(toAcc1.value))
       print("account2 deposit: {}".format(toAcc2.value))
       print(toAcc1.value - toAcc2.value)


class bankAcc(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start  # initial account value

    def withdraw(self, value):
        logging.debug('Waiting for a lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired a lock')
            self.value = self.value - value
        except:
            logging.debug('Error')
        finally:
            logging.debug('Released a lock')
            self.lock.release()

    def deposit(self,value):
        logging.debug('Waiting for a lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired a lock')
            self.value = self.value + value
        except:
            logging.debug('Error')
        finally:
            logging.debug('Released a lock')
            self.lock.release()

if __name__ == '__main__':
    A = bankAcc(10)
    B = bankAcc(3)

    for i in range(3):
        t = threading.Thread(target=deposit, args=(A,B))
        t.start()
    for i in range(3):
        t = threading.Thread(target=withdraw, args=(A,B))
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    logging.debug('A: %d B %d', A.value,B.value)
