"""Reference solution for Level 4 (preemption + priorities)."""
from scheduler_solution import prefill_ticks  # noqa: F401


def run_preemptive(requests, priorities, config):
    queue = [r.fresh() for r in requests]
    queue.sort(key=lambda r: (-priorities[r.id], r.arrival, r.id))
    running = []
    reserved = 0
    results = {}
    evictions = 0
    t = 0
    while queue or running:
        # 1. Free finished.
        still = []
        for r in running:
            if r.finished_at is not None:
                reserved -= r.reserved
            else:
                still.append(r)
        running = still
        # 2. Admit, in (-priority, arrival, id) order, with preemption.
        evicted_this_tick = set()
        progress = True
        while progress:
            progress = False
            for cand in list(queue):
                if cand.arrival > t or cand.id in evicted_this_tick:
                    continue
                while reserved + cand.reserved > config.memory_limit:
                    victims = [r for r in running
                               if priorities[r.id] < priorities[cand.id]]
                    if not victims:
                        break
                    victim = max(victims,
                                 key=lambda r: (-priorities[r.id], r.id))
                    running.remove(victim)
                    reserved -= victim.reserved
                    evictions += 1
                    evicted_this_tick.add(victim.id)
                    fresh = victim.fresh()
                    queue.append(fresh)
                    queue.sort(key=lambda r: (-priorities[r.id],
                                              r.arrival, r.id))
                if reserved + cand.reserved <= config.memory_limit:
                    queue.remove(cand)
                    cand.started_at = t
                    reserved += cand.reserved
                    running.append(cand)
                    progress = True
                    break
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
        if t > 10000:
            raise RuntimeError("livelock")
    return results, evictions
