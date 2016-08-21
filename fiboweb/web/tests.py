from itertools import izip
from unittest import TestCase

from fiboweb.web.utils import (NthFibonacci, get_redis_cursor,
                               get_from_redis)


class NthFibonacciTestCase(TestCase):
    def setUp(self):
        """
        Since we are using same redis database we need to back up our key
        values before running the tests, this is not a good idea though.
        XXX: Use different redis db
        """
        self.redis_cursor = get_redis_cursor()
        self.data = {}
        keys = self.redis_cursor.keys()
        values = self.redis_cursor.mget(keys)
        for k, v in izip(keys, values):
            self.data[k] = v
        self.redis_cursor.flushall()

    def test_nth_fibonacci(self):
        position = 6
        self.assertEqual(NthFibonacci(position)(), 8)
        self.redis_cursor.flushall()

    def test_negative_position(self):
        position = -10
        with self.assertRaises(AssertionError):
            NthFibonacci(position)()
        self.redis_cursor.flushall()

    def test_caching(self):
        position = 6
        self.redis_cursor.flushall()
        value = NthFibonacci(position)()
        self.assertEqual(get_from_redis(position), value)
        self.redis_cursor.flushall()

    def test_upto_nth_caching(self):
        position = 6
        value = NthFibonacci(position)()
        for pos in xrange(position):
            value_from_redis = get_from_redis(pos)
            value_generated = NthFibonacci(pos)()
            self.assertEqual(value_from_redis, value_generated)
        self.redis_cursor.flushall()

    def tearDown(self):
        """
        Restore all the key values
        """
        self.redis_cursor.mset(self.data)
