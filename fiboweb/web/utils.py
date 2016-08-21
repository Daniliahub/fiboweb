""" web utils """
import json
import redis

from fiboweb.web.constants import (
    REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
)

POOL = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    db=0
)

def get_redis_cursor():
    r_cursor = redis.Redis(connection_pool=POOL)
    return r_cursor


def store_to_redis(key, value):
    r_cursor = get_redis_cursor()
    r_cursor.set(key, json.dumps(value))


def get_from_redis(key):
    r_cursor = get_redis_cursor()
    value = r_cursor.get(key)
    if value:
        return json.loads(value)


def set_latest_position(key):
    store_to_redis('latest', key)


def get_latest_position():
    return get_from_redis('latest')


class NthFibonacci(object):
    """ ddd """
    def __init__(self, number):
        self._number = number

    def __call__(self):
        return self.get_fibonacci(self._number)

    def get_fibonacci(self, number):
        value = get_from_redis(number)
        latest = get_latest_position()
        if value is not None:
            return value
        elif number in (0, 1):
            if latest is None or latest < number:
                set_latest_position(number)
                store_to_redis(number, number)
            return number
        elif number == 2:
            if latest is None or latest < number:
                set_latest_position(number)
                store_to_redis(number, 1)
            return 1
        else:
            return self._calculate_fibonacci(number, latest)

    def _calculate_fibonacci(self, number, latest):
        """
        function to calculate fibonacci sequence
        """
        if latest is None:
            store_to_redis(0, 0)
            store_to_redis(1, 1)
            store_to_redis(2, 1)
            latest = 2
            set_latest_position(latest)
        first, second = get_from_redis(latest-1), get_from_redis(latest)
        iterations = number - latest + 1
        for offset in xrange(1, iterations):
            first, second = second, first + second
            store_to_redis(offset+latest, second)
        set_latest_position(number)
        return second
