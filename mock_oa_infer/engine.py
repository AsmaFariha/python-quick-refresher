"""Implement the InferenceEngine class.

Do not change existing method signatures. Read README.md, then read tests.py
— the tests are part of the spec.
"""

PREFILL_RATE = 4


class InferenceEngine:
    def __init__(self):
        raise NotImplementedError

    # ------------------------------------------------ Level 1
    def submit(self, request_id, prompt_tokens, max_tokens):
        raise NotImplementedError

    def get_cost(self, request_id):
        raise NotImplementedError

    def cancel(self, request_id):
        raise NotImplementedError

    # ------------------------------------------------ Level 2
    def total_cost(self):
        raise NotImplementedError

    def top_n_costly(self, n):
        raise NotImplementedError

    # ------------------------------------------------ Level 3
    def submit_at(self, timestamp, request_id, prompt_tokens, max_tokens,
                  ttl=None):
        raise NotImplementedError

    def get_cost_at(self, timestamp, request_id):
        raise NotImplementedError

    def cancel_at(self, timestamp, request_id):
        raise NotImplementedError

    def total_cost_at(self, timestamp):
        raise NotImplementedError

    def top_n_costly_at(self, timestamp, n):
        raise NotImplementedError

    # ------------------------------------------------ Level 4
    def add_worker(self, worker_id):
        raise NotImplementedError

    def assign_at(self, timestamp):
        raise NotImplementedError

    def worker_load_at(self, timestamp, worker_id):
        raise NotImplementedError
