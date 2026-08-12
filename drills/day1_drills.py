"""Day 1 drills — fill in the TODOs, then run: python day1_drills.py

Each drill takes 1-3 minutes. If one takes longer than 5, that's exactly the
gap worth closing before the OA. Answers in day1_drills_answers.py.
"""
import math  # noqa: F401
from collections import deque, defaultdict, Counter  # noqa: F401
from dataclasses import dataclass, field  # noqa: F401
import heapq  # noqa: F401

CHECKS = []


def check(fn):
    CHECKS.append(fn)
    return fn


# ------------------------------------------------ Idioms
def ceil_div(a, b):
    """Ceiling division using integer math only (no float, no math.ceil)."""
    # TODO
    raise NotImplementedError


def sort_requests(reqs):
    """reqs: list of (id, arrival, priority) tuples.
    Return them sorted by priority DESCENDING, then arrival ascending,
    then id ascending."""
    # TODO
    raise NotImplementedError


def least_loaded(loads):
    """Index of the smallest value; ties -> lowest index. One line."""
    # TODO
    raise NotImplementedError


def worst_victim(items):
    """items: list of (id, priority). Return the id of the lowest-priority
    item, breaking ties toward the HIGHEST id."""
    # TODO
    raise NotImplementedError


def drain_finished(running):
    """running: list of dicts with a 'done' bool. Remove finished entries
    IN PLACE (the caller holds a reference to this same list) and return
    how many were removed."""
    # TODO
    raise NotImplementedError


def group_by_worker(assignments):
    """assignments: list of (req_id, worker_idx). Return
    {worker_idx: [req_id, ...]} preserving input order within each worker."""
    # TODO
    raise NotImplementedError


def top_k_frequent(xs, k):
    """The k most common elements, most frequent first."""
    # TODO
    raise NotImplementedError


def next_to_finish(heap):
    """heap: list of (finish_time, req_id) already heapified.
    Pop and return the req_id finishing soonest; ties -> lowest req_id."""
    # TODO
    raise NotImplementedError


# ------------------------------------------------ OOP
@dataclass
class Task:
    """TODO: give this class
    - fields: id (int), arrival (int), size (int), progress (int, default 0)
    - a field `log` that is a list defaulting to empty (mutable-default trap!)
    - a @property `remaining` returning size - progress
    - a method `fresh()` returning a NEW Task with the same id/arrival/size
      and progress reset to 0
    """
    id: int
    # TODO: the rest


class Pipeline:
    """TODO: a tiny class exercising the OOP mechanics.

    __init__(self, capacity): store capacity, an empty deque `waiting`,
        an empty list `active`.
    submit(task): append to waiting.
    admit(): move tasks from the FRONT of waiting into active while
        len(active) < capacity. Return the number admitted.
    tick(): add 1 to every active task's progress; move any task whose
        remaining <= 0 out of active into self.done (a list). Return the
        list of ids completed this tick, sorted ascending.
    """


# ------------------------------------------------ Checks
@check
def c1():
    assert ceil_div(8, 4) == 2
    assert ceil_div(9, 4) == 3
    assert ceil_div(1, 10) == 1
    assert ceil_div(100, 7) == 15


@check
def c2():
    reqs = [(1, 5, 2), (2, 0, 2), (3, 0, 9), (4, 0, 2)]
    assert sort_requests(reqs) == [(3, 0, 9), (2, 0, 2), (4, 0, 2), (1, 5, 2)]


@check
def c3():
    assert least_loaded([3, 1, 2]) == 1
    assert least_loaded([2, 2, 5]) == 0
    assert least_loaded([5, 4, 4]) == 1


@check
def c4():
    assert worst_victim([(1, 5), (2, 1), (7, 1), (3, 9)]) == 7
    assert worst_victim([(4, 2)]) == 4


@check
def c5():
    running = [{"id": 1, "done": True}, {"id": 2, "done": False},
               {"id": 3, "done": True}]
    alias = running
    n = drain_finished(running)
    assert n == 2, n
    assert alias == [{"id": 2, "done": False}], "must mutate in place"


@check
def c6():
    got = group_by_worker([(1, 0), (2, 1), (3, 0), (4, 1), (5, 0)])
    assert got == {0: [1, 3, 5], 1: [2, 4]}, got


@check
def c7():
    assert top_k_frequent(["a", "b", "a", "c", "b", "a"], 2) == ["a", "b"]


@check
def c8():
    h = [(5, 2), (5, 1), (3, 9)]
    heapq.heapify(h)
    assert next_to_finish(h) == 9
    assert next_to_finish(h) == 1


@check
def c9():
    t = Task(id=1, arrival=0, size=5)
    assert t.progress == 0 and t.log == []
    t.log.append("x")
    assert Task(id=2, arrival=0, size=5).log == [], "mutable default leaked!"
    assert t.remaining == 5, "remaining must be a @property, not a method"
    t.progress = 2
    assert t.remaining == 3
    f = t.fresh()
    assert f.progress == 0 and t.progress == 2 and f is not t


@check
def c10():
    p = Pipeline(capacity=2)
    for i in (1, 2, 3):
        p.submit(Task(id=i, arrival=0, size=i))
    assert p.admit() == 2
    assert p.tick() == [1]
    assert p.admit() == 1
    assert p.tick() == [2]
    assert sorted(t.id for t in p.done) == [1, 2]


if __name__ == "__main__":
    passed = 0
    for fn in CHECKS:
        try:
            fn()
        except NotImplementedError:
            print(f"  TODO {fn.__name__}")
            continue
        except Exception as e:
            print(f"  FAIL {fn.__name__}: {type(e).__name__}: {e}")
            continue
        print(f"  PASS {fn.__name__}")
        passed += 1
    print(f"\n{passed}/{len(CHECKS)} drills passing")
