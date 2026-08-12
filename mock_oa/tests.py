"""Grader. Run: python tests.py            (scores scheduler.py, max 800)
        or: python tests.py --solution     (scores the reference solution)
"""
import sys
import traceback

if "--solution" in sys.argv:
    sys.path.insert(0, "solution")
    import scheduler_solution as scheduler
    import level4_solution
    scheduler.run_preemptive = level4_solution.run_preemptive
else:
    import scheduler

from engine import EngineConfig, Request

CFG = EngineConfig(prefill_rate=4, memory_limit=100)

TESTS = []


def test(level, points):
    def deco(fn):
        TESTS.append((level, points, fn))
        return fn
    return deco


# ---------------------------------------------------------------- Level 1
@test(1, 50)
def t01_prefill_ticks():
    assert scheduler.prefill_ticks(8, 4) == 2
    assert scheduler.prefill_ticks(9, 4) == 3
    assert scheduler.prefill_ticks(1, 10) == 1
    assert scheduler.prefill_ticks(100, 7) == 15


@test(1, 50)
def t02_fifo_basic():
    got = scheduler.run_fifo([Request(1, 0, 8, 3), Request(2, 1, 4, 2)], CFG)
    assert list(got) == [(1, 5), (2, 8)], got


@test(1, 50)
def t03_fifo_idle_gap():
    got = scheduler.run_fifo([Request(3, 10, 4, 1), Request(1, 0, 16, 4)], CFG)
    assert list(got) == [(1, 8), (3, 12)], got


@test(1, 50)
def t04_fifo_tiebreak():
    got = scheduler.run_fifo(
        [Request(2, 0, 4, 2), Request(1, 0, 4, 1), Request(3, 0, 1, 1)], CFG)
    assert list(got) == [(1, 2), (2, 5), (3, 7)], got


# ---------------------------------------------------------------- Level 2
@test(2, 50)
def t05_batched_single():
    got = scheduler.run_batched([Request(1, 0, 8, 3)], CFG)
    assert got == {1: (3, 5)}, got


@test(2, 50)
def t06_batched_concurrent():
    got = scheduler.run_batched([Request(1, 0, 8, 3), Request(2, 0, 4, 2)], CFG)
    assert got == {1: (3, 5), 2: (2, 3)}, got


@test(2, 50)
def t07_batched_memory_blocking():
    cfg = EngineConfig(prefill_rate=4, memory_limit=12)
    got = scheduler.run_batched(
        [Request(1, 0, 8, 3), Request(2, 0, 4, 2), Request(3, 0, 2, 1)], cfg)
    assert got == {1: (3, 5), 2: (7, 8), 3: (7, 7)}, got


@test(2, 50)
def t08_batched_arrivals_and_freeing():
    cfg = EngineConfig(prefill_rate=2, memory_limit=10)
    got = scheduler.run_batched(
        [Request(1, 0, 6, 4), Request(2, 1, 4, 2), Request(3, 3, 2, 2)], cfg)
    assert got == {1: (4, 7), 2: (10, 11), 3: (9, 10)}, got


# ---------------------------------------------------------------- Level 3
@test(3, 50)
def t09_pick_worker():
    assert scheduler.pick_worker([3, 1, 2]) == 1
    assert scheduler.pick_worker([2, 2, 5]) == 0
    assert scheduler.pick_worker([0]) == 0
    assert scheduler.pick_worker([5, 4, 4]) == 1


@test(3, 50)
def t10_route_basic():
    asg, res = scheduler.route(
        [Request(1, 0, 8, 2), Request(2, 0, 8, 2), Request(3, 1, 4, 1)],
        CFG, 2)
    assert asg == {1: 0, 2: 1, 3: 0}, asg
    assert res == {1: (3, 4), 2: (3, 4), 3: (3, 3)}, res


@test(3, 50)
def t11_route_memory_pressure():
    cfg = EngineConfig(prefill_rate=4, memory_limit=20)
    asg, res = scheduler.route(
        [Request(1, 0, 10, 5), Request(2, 0, 8, 4), Request(3, 2, 6, 2),
         Request(4, 2, 4, 4), Request(5, 4, 2, 2)], cfg, 2)
    assert asg == {1: 0, 2: 1, 3: 1, 4: 0, 5: 1}, asg
    assert res == {1: (4, 8), 2: (3, 6), 3: (5, 6), 4: (10, 13),
                   5: (8, 9)}, res


@test(3, 50)
def t12_route_three_workers():
    cfg = EngineConfig(prefill_rate=4, memory_limit=20)
    reqs = [Request(i, i % 3, 4 + i, 2) for i in range(1, 7)]
    asg, res = scheduler.route(reqs, cfg, 3)
    assert asg == {1: 2, 2: 0, 3: 0, 4: 2, 5: 1, 6: 1}, asg
    assert res == {1: (4, 5), 2: (5, 6), 3: (3, 4), 4: (4, 5),
                   5: (9, 10), 6: (4, 5)}, res


# ---------------------------------------------------------------- Level 4
@test(4, 50)
def t13_priority_order_no_preemption():
    cfg = EngineConfig(prefill_rate=4, memory_limit=20)
    res, ev = scheduler.run_preemptive(
        [Request(1, 0, 4, 2), Request(2, 0, 4, 2)], {1: 0, 2: 5}, cfg)
    assert ev == 0, ev
    assert res == {1: (2, 3), 2: (2, 3)}, res


@test(4, 50)
def t14_preemption_basic():
    cfg = EngineConfig(prefill_rate=4, memory_limit=12)
    res, ev = scheduler.run_preemptive(
        [Request(1, 0, 8, 4), Request(2, 2, 4, 2)], {1: 1, 2: 9}, cfg)
    assert ev == 1, ev
    assert res == {1: (8, 11), 2: (4, 5)}, res


@test(4, 50)
def t15_no_victim_equal_priority():
    cfg = EngineConfig(prefill_rate=4, memory_limit=12)
    res, ev = scheduler.run_preemptive(
        [Request(1, 0, 8, 4), Request(2, 2, 4, 2)], {1: 5, 2: 5}, cfg)
    assert ev == 0, ev
    assert res == {1: (3, 6), 2: (8, 9)}, res


@test(4, 50)
def t16_preemption_mixed():
    cfg = EngineConfig(prefill_rate=2, memory_limit=16)
    reqs = [Request(1, 0, 6, 4), Request(2, 0, 4, 2),
            Request(3, 3, 8, 4), Request(4, 5, 2, 2)]
    res, ev = scheduler.run_preemptive(reqs, {1: 1, 2: 2, 3: 9, 4: 3}, cfg)
    assert ev == 2, ev
    assert res == {1: (15, 18), 2: (14, 15), 3: (8, 11), 4: (7, 8)}, res


def main():
    score = 0
    by_level = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0]}
    for level, points, fn in TESTS:
        by_level[level][1] += points
        try:
            fn()
        except NotImplementedError:
            print(f"  SKIP {fn.__name__} (not implemented)")
            continue
        except Exception:
            print(f"  FAIL {fn.__name__}")
            traceback.print_exc(limit=1)
            continue
        print(f"  PASS {fn.__name__} (+{points})")
        score += points
        by_level[level][0] += points
    print()
    for lvl, (got, total) in by_level.items():
        print(f"Level {lvl}: {got}/{total}")
    print(f"\nSCORE: {score}/800")


if __name__ == "__main__":
    main()
