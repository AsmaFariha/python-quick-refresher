"""YOUR CODE GOES HERE. Implement the functions below.

Note: docstrings here are authoritative where they conflict with README
prose — just like a real messy codebase. When in doubt, the tests are the
ground truth.
"""
from engine import EngineConfig, Request, Worker  # noqa: F401


# ---------------------------------------------------------------- Level 1
def prefill_ticks(prompt_tokens: int, prefill_rate: int) -> int:
    """Number of ticks needed to prefill a prompt."""
    raise NotImplementedError


def run_fifo(requests: list[Request], config: EngineConfig):
    """Serve requests one at a time on a single worker.

    Returns a LIST of (id, finished_at) tuples in completion order.
    (Yes, the README example shows a dict. The tests import this file.)
    """
    raise NotImplementedError


# ---------------------------------------------------------------- Level 2
def run_batched(requests: list[Request], config: EngineConfig) -> dict:
    """Continuous batching on one worker under a memory limit.

    Returns {id: (first_token_at, finished_at)}.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- Level 3
def pick_worker(loads: list[int]) -> int:
    """Index of least-loaded worker; ties -> lowest index."""
    raise NotImplementedError


def route(requests: list[Request], config: EngineConfig, num_workers: int):
    """Assign requests to workers (least reserved-token load at assignment
    time, ties -> lowest index), then run each worker as in Level 2.

    Returns (assignment: {id: worker_index},
             results: {id: (first_token_at, finished_at)}).
    """
    raise NotImplementedError


# ---------------------------------------------------------------- Level 4
def run_preemptive(requests: list[Request], priorities: dict,
                   config: EngineConfig):
    """Single worker, priority-aware admission with preemption.

    Returns ({id: (first_token_at, finished_at)}, eviction_count).
    """
    raise NotImplementedError

