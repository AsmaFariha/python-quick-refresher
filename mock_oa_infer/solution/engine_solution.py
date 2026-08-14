"""Reference solution — ICF house style.

Note the shape: ONE class, methods added per level, public methods
delegating to timestamp-aware internals, nothing from Levels 1-2 rewritten.
"""
import math
from dataclasses import dataclass
from typing import Optional

PREFILL_RATE = 4


@dataclass
class Request:
    id: str
    prompt_tokens: int
    max_tokens: int
    submitted_at: int = 0
    ttl: Optional[int] = None
    worker: Optional[str] = None

    @property
    def cost(self) -> int:
        return math.ceil(self.prompt_tokens / PREFILL_RATE) + self.max_tokens

    def alive_at(self, t: int) -> bool:
        return self.ttl is None or t < self.submitted_at + self.ttl


class InferenceEngine:
    def __init__(self):
        self.requests: dict[str, Request] = {}
        self.workers: list[str] = []

    # ------------------------------------------------ Level 1
    def submit(self, request_id, prompt_tokens, max_tokens):
        return self._submit(0, request_id, prompt_tokens, max_tokens, None)

    def get_cost(self, request_id):
        return self._get_cost(0, request_id)

    def cancel(self, request_id):
        return self._cancel(0, request_id)

    # ------------------------------------------------ Level 2
    def total_cost(self):
        return self._total_cost(0)

    def top_n_costly(self, n):
        return self._top_n_costly(0, n)

    # ------------------------------------------------ Level 3
    def submit_at(self, timestamp, request_id, prompt_tokens, max_tokens,
                  ttl=None):
        return self._submit(timestamp, request_id, prompt_tokens, max_tokens,
                            ttl)

    def get_cost_at(self, timestamp, request_id):
        return self._get_cost(timestamp, request_id)

    def cancel_at(self, timestamp, request_id):
        return self._cancel(timestamp, request_id)

    def total_cost_at(self, timestamp):
        return self._total_cost(timestamp)

    def top_n_costly_at(self, timestamp, n):
        return self._top_n_costly(timestamp, n)

    # ------------------------------------------------ Level 4
    def add_worker(self, worker_id):
        if worker_id in self.workers:
            return False
        self.workers.append(worker_id)
        return True

    def assign_at(self, timestamp):
        if not self.workers:
            return {}
        load = {w: 0 for w in self.workers}
        result = {}
        pending = sorted(self._alive(timestamp),
                         key=lambda r: (r.submitted_at, r.id))
        for req in pending:
            w = min(self.workers, key=lambda w: (load[w], w))
            req.worker = w
            load[w] += req.cost
            result[req.id] = w
        return result

    def worker_load_at(self, timestamp, worker_id):
        if worker_id not in self.workers:
            return None
        return sum(r.cost for r in self._alive(timestamp)
                   if r.worker == worker_id)

    # ------------------------------------------------ internals
    def _alive(self, t):
        return [r for r in self.requests.values() if r.alive_at(t)]

    def _submit(self, t, request_id, prompt_tokens, max_tokens, ttl):
        existing = self.requests.get(request_id)
        if existing is not None and existing.alive_at(t):
            return False
        self.requests[request_id] = Request(request_id, prompt_tokens,
                                            max_tokens, t, ttl)
        return True

    def _get_cost(self, t, request_id):
        req = self.requests.get(request_id)
        if req is None or not req.alive_at(t):
            return None
        return req.cost

    def _cancel(self, t, request_id):
        req = self.requests.get(request_id)
        if req is None or not req.alive_at(t):
            return False
        del self.requests[request_id]
        return True

    def _total_cost(self, t):
        return sum(r.cost for r in self._alive(t))

    def _top_n_costly(self, t, n):
        rs = sorted(self._alive(t), key=lambda r: (-r.cost, r.id))
        return [f"{r.id}({r.cost})" for r in rs[:n]]
