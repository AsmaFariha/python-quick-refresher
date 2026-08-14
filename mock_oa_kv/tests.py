"""Grader. Run: python tests.py           (scores database.py)
        or: python tests.py --solution    (scores the reference solution)

Scoring follows CodeSignal's ICA scale: 200 baseline, 600 maximum.
Higher levels are weighted more heavily.
"""
import sys
import traceback

if "--solution" in sys.argv:
    sys.path.insert(0, "solution")
    from database_solution import Database
else:
    from database import Database

TESTS = []


def test(level, points):
    def deco(fn):
        TESTS.append((level, points, fn))
        return fn
    return deco


# ------------------------------------------------------------ Level 1
@test(1, 20)
def t01_set_and_get():
    d = Database()
    d.set("u1", "name", 1)
    d.set("u1", "age", 30)
    assert d.get("u1", "age") == 30
    assert d.get("u1", "name") == 1


@test(1, 20)
def t02_missing_returns_none():
    d = Database()
    d.set("u1", "name", 1)
    assert d.get("u1", "missing") is None
    assert d.get("nokey", "name") is None


@test(1, 20)
def t03_delete():
    d = Database()
    d.set("u1", "age", 30)
    assert d.delete("u1", "age") is True
    assert d.delete("u1", "age") is False
    assert d.get("u1", "age") is None
    assert d.delete("nokey", "f") is False


@test(1, 20)
def t04_compare_and_set():
    d = Database()
    d.set("u1", "name", 1)
    assert d.compare_and_set("u1", "name", 1, 9) is True
    assert d.get("u1", "name") == 9
    assert d.compare_and_set("u1", "name", 1, 5) is False
    assert d.get("u1", "name") == 9
    assert d.compare_and_set("u1", "absent", 1, 5) is False


# ------------------------------------------------------------ Level 2
@test(2, 20)
def t05_scan_sorted():
    d = Database()
    for f, v in [("z", 1), ("b", 2), ("bc", 3)]:
        d.set("a", f, v)
    assert d.scan("a") == ["b(2)", "bc(3)", "z(1)"], d.scan("a")


@test(2, 20)
def t06_scan_missing_key():
    d = Database()
    assert d.scan("nothing") == []


@test(2, 20)
def t07_scan_by_prefix():
    d = Database()
    for f, v in [("z", 1), ("b", 2), ("bc", 3)]:
        d.set("a", f, v)
    assert d.scan_by_prefix("a", "b") == ["b(2)", "bc(3)"]
    assert d.scan_by_prefix("a", "q") == []


@test(2, 20)
def t08_top_n_keys():
    d = Database()
    for k, f in [("a", "1"), ("a", "2"), ("a", "3"),
                 ("c", "1"), ("c", "2"), ("b", "1"), ("b", "2")]:
        d.set(k, f, 1)
    # b and c tie at 2 fields -> b first (lexicographic)
    assert d.top_n_keys(2) == ["a(3)", "b(2)"], d.top_n_keys(2)
    assert d.top_n_keys(10) == ["a(3)", "b(2)", "c(2)"]


# ------------------------------------------------------------ Level 3
@test(3, 28)
def t09_ttl_window():
    d = Database()
    d.set_at(1, "k", "f", 10, 5)          # alive on [1, 6)
    assert d.get_at(1, "k", "f") == 10
    assert d.get_at(5, "k", "f") == 10
    assert d.get_at(6, "k", "f") is None


@test(3, 28)
def t10_no_ttl_is_forever():
    d = Database()
    d.set_at(3, "k", "g", 7)
    assert d.get_at(1000, "k", "g") == 7


@test(3, 28)
def t11_scan_hides_expired():
    d = Database()
    d.set_at(1, "k", "f", 10, 5)
    d.set_at(3, "k", "g", 7)
    assert d.scan_at(5, "k") == ["f(10)", "g(7)"], d.scan_at(5, "k")
    assert d.scan_at(6, "k") == ["g(7)"]
    assert d.scan_by_prefix_at(5, "k", "f") == ["f(10)"]


@test(3, 28)
def t12_reset_extends_lifespan():
    d = Database()
    d.set_at(1, "k", "f", 10, 5)
    d.set_at(4, "k", "f", 11, 5)          # now alive on [4, 9)
    assert d.get_at(8, "k", "f") == 11
    assert d.get_at(9, "k", "f") is None


@test(3, 28)
def t13_delete_at_respects_expiry():
    d = Database()
    d.set_at(1, "k", "f", 10, 5)
    assert d.delete_at(6, "k", "f") is False     # already expired
    d.set_at(1, "k", "g", 1)
    assert d.delete_at(2, "k", "g") is True
    assert d.delete_at(3, "k", "g") is False


# ------------------------------------------------------------ Level 4
@test(4, 25)
def t14_rollback_discards_later_ops():
    d = Database()
    d.set_at(5, "k", "f", 1)
    d.set_at(8, "k", "g", 2)
    d.set_at(12, "k", "h", 3)
    d.rollback(8)
    assert d.get_at(8, "k", "f") == 1
    assert d.get_at(8, "k", "g") == 2
    assert d.get_at(12, "k", "h") is None


@test(4, 25)
def t15_rollback_preserves_original_ttl():
    d = Database()
    d.set_at(5, "k", "f", 1, 10)          # alive on [5, 15)
    d.set_at(12, "k", "h", 3)
    d.rollback(8)
    assert d.get_at(14, "k", "f") == 1
    assert d.get_at(15, "k", "f") is None


@test(4, 25)
def t16_rollback_undoes_deletes():
    d = Database()
    d.set_at(1, "k", "f", 1)
    d.delete_at(5, "k", "f")
    d.rollback(3)
    assert d.get_at(4, "k", "f") == 1


@test(4, 25)
def t17_rollback_then_continue():
    d = Database()
    d.set_at(1, "k", "a", 1)
    d.set_at(9, "k", "b", 2)
    d.rollback(5)
    d.set_at(6, "k", "c", 3)
    assert d.scan_at(7, "k") == ["a(1)", "c(3)"], d.scan_at(7, "k")


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
