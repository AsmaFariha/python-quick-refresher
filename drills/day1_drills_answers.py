"""Answers to day1_drills.py — attempt the drills first."""
from collections import deque, defaultdict, Counter
from dataclasses import dataclass, field
import heapq


def ceil_div(a, b):
    return -(-a // b)


def sort_requests(reqs):
    return sorted(reqs, key=lambda r: (-r[2], r[1], r[0]))


def least_loaded(loads):
    return min(range(len(loads)), key=lambda i: (loads[i], i))


def worst_victim(items):
    return min(items, key=lambda it: (it[1], -it[0]))[0]


def drain_finished(running):
    n = sum(1 for r in running if r["done"])
    running[:] = [r for r in running if not r["done"]]   # slice-assign = in place
    return n


def group_by_worker(assignments):
    d = defaultdict(list)
    for req_id, w in assignments:
        d[w].append(req_id)
    return dict(d)


def top_k_frequent(xs, k):
    return [x for x, _ in Counter(xs).most_common(k)]


def next_to_finish(heap):
    return heapq.heappop(heap)[1]


@dataclass
class Task:
    id: int
    arrival: int
    size: int
    progress: int = 0
    log: list = field(default_factory=list)

    @property
    def remaining(self):
        return self.size - self.progress

    def fresh(self):
        return Task(self.id, self.arrival, self.size)


class Pipeline:
    def __init__(self, capacity):
        self.capacity = capacity
        self.waiting = deque()
        self.active = []
        self.done = []

    def submit(self, task):
        self.waiting.append(task)

    def admit(self):
        n = 0
        while self.waiting and len(self.active) < self.capacity:
            self.active.append(self.waiting.popleft())
            n += 1
        return n

    def tick(self):
        finished = []
        for t in self.active:
            t.progress += 1
            if t.remaining <= 0:
                finished.append(t)
        for t in finished:
            self.active.remove(t)
            self.done.append(t)
        return sorted(t.id for t in finished)
