"""Implement the Database class. Do not change existing method signatures.

Read README.md, then read tests.py — the tests are part of the spec.
"""


class Database:
    def __init__(self):
        raise NotImplementedError

    # ------------------------------------------------ Level 1
    def set(self, key, field, value):
        raise NotImplementedError

    def get(self, key, field):
        raise NotImplementedError

    def delete(self, key, field):
        raise NotImplementedError

    def compare_and_set(self, key, field, expected, new_value):
        raise NotImplementedError

    # ------------------------------------------------ Level 2
    def scan(self, key):
        raise NotImplementedError

    def scan_by_prefix(self, key, prefix):
        raise NotImplementedError

    def top_n_keys(self, n):
        raise NotImplementedError

    # ------------------------------------------------ Level 3
    def set_at(self, timestamp, key, field, value, ttl=None):
        raise NotImplementedError

    def get_at(self, timestamp, key, field):
        raise NotImplementedError

    def delete_at(self, timestamp, key, field):
        raise NotImplementedError

    def scan_at(self, timestamp, key):
        raise NotImplementedError

    def scan_by_prefix_at(self, timestamp, key, prefix):
        raise NotImplementedError

    # ------------------------------------------------ Level 4
    def rollback(self, timestamp):
        raise NotImplementedError
