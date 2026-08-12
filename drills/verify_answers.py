"""CI check: the reference answers satisfy every drill assertion."""
import importlib.util
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

spec = importlib.util.spec_from_file_location("drills", HERE / "day1_drills.py")
drills = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drills)

import day1_drills_answers as answers  # noqa: E402

for name in ["ceil_div", "sort_requests", "least_loaded", "worst_victim",
             "drain_finished", "group_by_worker", "top_k_frequent",
             "next_to_finish", "Task", "Pipeline"]:
    setattr(drills, name, getattr(answers, name))

failed = 0
for fn in drills.CHECKS:
    try:
        fn()
        print(f"PASS {fn.__name__}")
    except Exception as e:                     # noqa: BLE001
        print(f"FAIL {fn.__name__}: {type(e).__name__}: {e}")
        failed += 1

print(f"\n{len(drills.CHECKS) - failed}/{len(drills.CHECKS)} passing")
sys.exit(1 if failed else 0)
