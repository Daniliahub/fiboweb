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
    """
    """
    r_cursor = redis.Redis(connection_pool=POOL)
    return r_cursor


def store_to_redis(key, value):
    """
    Stores `value` to redis
    """
    r_cursor = get_redis_cursor()
    r_cursor.set(key, json.dumps(value))


def get_from_redis(key):
    """
    Return value from key if found else return None
    """
    r_cursor = get_redis_cursor()
    value = r_cursor.get(key)
    if value:
        return json.loads(value)
    else:
        return None

def set_latest_position(key):
    """
    Store the latest calcualtion of position n
    """
    store_to_redis('latest', key)


def get_latest_position():
    """
    Return the latest position upto which fibonacci numbers are calculated
    """
    return get_from_redis('latest')


class NthFibonacci(object):
    """ Returns nth fibonacci number, expects n.

    >>> NthFibonacci(6)()
    8
    """
    def __init__(self, number):
        self._number = number

    def __call__(self):
        return self.get_fibonacci(self._number)

    def get_fibonacci(self, number):
        """
        Returns the fibonacci number `number`th position from the sequence

        `number` variable should be a positive integer and here it defines
        position of a number in fibonacci sequence.
        """
        assert number >= 0
        value = get_from_redis(number)
        latest = get_latest_position()

        # If fibonacci number was previously calculated return it
        if value is not None:
            return value
        # If position is in 0, 1, 2 set latest position, save to redis and return
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
        Function to calculate fibonacci sequence

        `number` is the position of a number in fibonacci sequence
        `latest` is the position till which fibonacci sequence was already
        generated and available in cache
        """
        # `latest` shall be None once in a lifetime when we setup the project
        # and never tried to retrive any fibonacci number from this app
        if latest is None:
            store_to_redis(0, 0)
            store_to_redis(1, 1)
            store_to_redis(2, 1)
            latest = 2
            set_latest_position(latest)

        # The general formula to calculate fibonacci sequence is:
        # a, b = b, a + b. Here we have tweaked it a little. For example:
        # We want 10th fibonacci number. So, `number` is 10 and `latest` is 2 now.
        # Here, We are getting the values upto which the fibonacci numbers were
        # already calculated, in this case 1 and 2
        first, second = get_from_redis(latest-1), get_from_redis(latest)

        # iterations will be then 9 and we will have the the 10th fibonacci
        # number.
        # (Important point to note: here we save some iteration, ex: next time
        # if we need 100th fibonacci number we only need 100 - 10 + 1 = 91
        # iterations.)
        iterations = number - latest + 1
        # Basically optimization happens here. During calcualtion of 10th
        # fibonacci number we store all (3rd, 4th, ...) the fibonacci which
        # comes in between our calcualtion, so that next time some user tries
        # to get we return directly from redis.
        for offset in xrange(1, iterations):
            first, second = second, first + second
            store_to_redis(offset+latest, second)
        # Set the latest position so that we know till which position we have
        # calculated the sequence. So one position gets calculated once in a
        # lifetime if no natural calamities happen.
        set_latest_position(number)
        return second
