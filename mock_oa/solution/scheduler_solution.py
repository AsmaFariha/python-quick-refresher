"""Reference solution. DO NOT OPEN until you've attempted the mock OA."""
import math

from engine import EngineConfig, Request


# ---------------------------------------------------------------- Level 1
def prefill_ticks(prompt_tokens: int, prefill_rate: int) -> int:
    return math.ceil(prompt_tokens / prefill_rate)


def run_fifo(requests, config):
    out = []
    t = 0
    for r in sorted(requests, key=lambda r: (r.arrival, r.id)):
        start = max(t, r.arrival)
        p = prefill_ticks(r.prompt_tokens, config.prefill_rate)
        finish = start + p + r.max_new_tokens
        out.append((r.id, finish))
        t = finish
    return out


# ---------------------------------------------------------------- Level 2
def run_batched(requests, config):
    queue = sorted((r.fresh() for r in requests),
                   key=lambda r: (r.arrival, r.id))
    running: list[Request] = []
    reserved = 0
    results = {}
    t = 0
    while queue or running:
        # 1. Free requests that finished at end of previous tick.
        still = []
        for r in running:
            if r.finished_at is not None:
                reserved -= r.reserved
            else:
                still.append(r)
        running = still
        # 2. Admit (head-of-line blocking).
        while queue and queue[0].arrival <= t and \
                reserved + queue[0].reserved <= config.memory_limit:
            r = queue.pop(0)
            r.started_at = t
            reserved += r.reserved
            running.append(r)
        # 3. Work.
        for r in running:
            if r.prefill_done < r.prompt_tokens:
                r.prefill_done += config.prefill_rate
            else:
                r.tokens_generated += 1
                if r.tokens_generated == 1:
                    r.first_token_at = t + 1
                if r.tokens_generated == r.max_new_tokens:
                    r.finished_at = t + 1
                    results[r.id] = (r.first_token_at, r.finished_at)
        t += 1
    return results


# ---------------------------------------------------------------- Level 3
def pick_worker(loads):
    return min(range(len(loads)), key=lambda i: (loads[i], i))


def route(requests, config, num_workers):
    loads = [0] * num_workers
    buckets = [[] for _ in range(num_workers)]
    assignment = {}
    for r in sorted(requests, key=lambda r: (r.arrival, r.id)):
        w = pick_worker(loads)
        assignment[r.id] = w
        loads[w] += r.reserved
        buckets[w].append(r)
    results = {}
    for bucket in buckets:
        results.update(run_batched(bucket, config))
    return assignment, results
