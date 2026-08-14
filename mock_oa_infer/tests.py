"""Grader. Run: python tests.py           (scores engine.py)
        or: python tests.py --solution    (scores the reference solution)

Scoring follows CodeSignal's ICA scale: 200 baseline, 600 maximum.
"""
import sys
import traceback

if "--solution" in sys.argv:
    sys.path.insert(0, "solution")
    from engine_solution import InferenceEngine
else:
    from engine import InferenceEngine

TESTS = []


def test(level, points):
    def deco(fn):
        TESTS.append((level, points, fn))
        return fn
    return deco


# ------------------------------------------------------------ Level 1
@test(1, 20)
def t01_cost_formula():
    e = InferenceEngine()
    e.submit("r1", 8, 3)        # ceil(8/4)=2 + 3 = 5
    e.submit("r2", 9, 2)        # ceil(9/4)=3 + 2 = 5
    e.submit("r3", 1, 0)        # ceil(1/4)=1 + 0 = 1
    assert e.get_cost("r1") == 5
    assert e.get_cost("r2") == 5
    assert e.get_cost("r3") == 1


@test(1, 20)
def t02_missing_request():
    e = InferenceEngine()
    assert e.get_cost("nope") is None


@test(1, 20)
def t03_duplicate_submit_rejected():
    e = InferenceEngine()
    assert e.submit("r1", 8, 3) is True
    assert e.submit("r1", 4, 1) is False
    assert e.get_cost("r1") == 5          # unchanged


@test(1, 20)
def t04_cancel():
    e = InferenceEngine()
    e.submit("r1", 8, 3)
    assert e.cancel("r1") is True
    assert e.cancel("r1") is False
    assert e.get_cost("r1") is None


# ------------------------------------------------------------ Level 2
@test(2, 20)
def t05_total_cost():
    e = InferenceEngine()
    for i, (p, m) in enumerate([(8, 3), (4, 1), (16, 0), (1, 4)], 1):
        e.submit(f"r{i}", p, m)           # 5, 2, 4, 5
    assert e.total_cost() == 16


@test(2, 20)
def t06_total_cost_empty():
    assert InferenceEngine().total_cost() == 0


@test(2, 20)
def t07_top_n_ties_by_id():
    e = InferenceEngine()
    for i, (p, m) in enumerate([(8, 3), (4, 1), (16, 0), (1, 4)], 1):
        e.submit(f"r{i}", p, m)           # r1=5 r2=2 r3=4 r4=5
    assert e.top_n_costly(2) == ["r1(5)", "r4(5)"], e.top_n_costly(2)


@test(2, 20)
def t08_top_n_over_length():
    e = InferenceEngine()
    for i, (p, m) in enumerate([(8, 3), (4, 1), (16, 0), (1, 4)], 1):
        e.submit(f"r{i}", p, m)
    assert e.top_n_costly(9) == ["r1(5)", "r4(5)", "r3(4)", "r2(2)"]


# ------------------------------------------------------------ Level 3
@test(3, 28)
def t09_ttl_window():
    e = InferenceEngine()
    e.submit_at(1, "a", 8, 3, 5)          # alive on [1, 6)
    assert e.get_cost_at(1, "a") == 5
    assert e.get_cost_at(5, "a") == 5
    assert e.get_cost_at(6, "a") is None


@test(3, 28)
def t10_no_ttl_is_forever():
    e = InferenceEngine()
    e.submit_at(2, "b", 4, 1)
    assert e.get_cost_at(10_000, "b") == 2


@test(3, 28)
def t11_aggregates_ignore_expired():
    e = InferenceEngine()
    e.submit_at(1, "a", 8, 3, 5)          # cost 5, dies at 6
    e.submit_at(2, "b", 4, 1)             # cost 2, forever
    assert e.total_cost_at(5) == 7
    assert e.total_cost_at(6) == 2
    assert e.top_n_costly_at(5, 5) == ["a(5)", "b(2)"]
    assert e.top_n_costly_at(6, 5) == ["b(2)"]


@test(3, 28)
def t12_cancel_respects_expiry():
    e = InferenceEngine()
    e.submit_at(1, "a", 8, 3, 5)
    assert e.cancel_at(6, "a") is False    # already expired
    e.submit_at(1, "b", 4, 1)
    assert e.cancel_at(3, "b") is True
    assert e.cancel_at(4, "b") is False


@test(3, 28)
def t13_expired_id_can_be_reused():
    e = InferenceEngine()
    e.submit_at(1, "a", 8, 3, 5)
    assert e.submit_at(3, "a", 4, 1) is False     # still alive -> rejected
    assert e.submit_at(7, "a", 4, 1) is True      # expired -> allowed
    assert e.get_cost_at(7, "a") == 2


# ------------------------------------------------------------ Level 4
@test(4, 25)
def t14_add_worker():
    e = InferenceEngine()
    assert e.add_worker("w1") is True
    assert e.add_worker("w1") is False
    assert e.add_worker("w2") is True


@test(4, 25)
def t15_least_loaded_assignment():
    e = InferenceEngine()
    e.add_worker("w1")
    e.add_worker("w2")
    e.submit_at(0, "r1", 16, 4)           # cost 8
    e.submit_at(0, "r2", 4, 1)            # cost 2
    e.submit_at(1, "r3", 8, 2)            # cost 4
    # r1 -> w1 (tie, lowest id). r2 -> w2 (0 < 8). r3 -> w2 (2 < 8).
    assert e.assign_at(5) == {"r1": "w1", "r2": "w2", "r3": "w2"}


@test(4, 25)
def t16_worker_load():
    e = InferenceEngine()
    e.add_worker("w1")
    e.add_worker("w2")
    e.submit_at(0, "r1", 16, 4)
    e.submit_at(0, "r2", 4, 1)
    e.submit_at(1, "r3", 8, 2)
    e.assign_at(5)
    assert e.worker_load_at(5, "w1") == 8
    assert e.worker_load_at(5, "w2") == 6
    assert e.worker_load_at(5, "ghost") is None


@test(4, 25)
def t17_assignment_skips_expired_and_no_workers():
    e = InferenceEngine()
    assert e.assign_at(0) == {}           # no workers registered
    e.add_worker("w1")
    e.submit_at(0, "gone", 8, 2, 3)       # dies at 3
    e.submit_at(0, "stay", 4, 1)
    assert e.assign_at(5) == {"stay": "w1"}
    assert e.worker_load_at(5, "w1") == 2


def main():
    earned = 0
    by_level = {1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0]}
    for level, points, fn in TESTS:
        by_level[level][1] += points
        try:
            fn()
        except NotImplementedError:
            print(f"  TODO {fn.__name__}")
            continue
        except Exception:
            print(f"  FAIL {fn.__name__}")
            traceback.print_exc(limit=1)
            continue
        print(f"  PASS {fn.__name__} (+{points})")
        earned += points
        by_level[level][0] += points
    print()
    for lvl, (got, total) in by_level.items():
        print(f"Level {lvl}: {got}/{total}")
    print(f"\nCODING SCORE: {200 + earned}/600")


if __name__ == "__main__":
    main()
