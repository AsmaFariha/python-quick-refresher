"""Reference solution — do not open until you've attempted the mock.

Demonstrates the playbook skeleton: a Field record, timestamp-aware
internals, thin public wrappers, and an append-only operation log that makes
Level 4 rollback a replay rather than an undo.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Field:
    value: int
    created_at: int = 0
    ttl: Optional[int] = None

    def alive_at(self, t: int) -> bool:
        return self.ttl is None or t < self.created_at + self.ttl


class Database:
    def __init__(self):
        self.store: dict[str, dict[str, Field]] = {}
        self.log: list[tuple] = []          # (timestamp, op, args)

    # ------------------------------------------------ Level 1 (public)
    def set(self, key, field, value):
        return self._set(0, key, field, value, None)

    def get(self, key, field):
        return self._get(0, key, field)

    def delete(self, key, field):
        return self._delete(0, key, field)

    def compare_and_set(self, key, field, expected, new_value):
        return self._compare_and_set(0, key, field, expected, new_value)

    # ------------------------------------------------ Level 2 (public)
    def scan(self, key):
        return self._scan(0, key, "")

    def scan_by_prefix(self, key, prefix):
        return self._scan(0, key, prefix)

    def top_n_keys(self, n):
        return self._top_n_keys(0, n)

    # ------------------------------------------------ Level 3 (public)
    def set_at(self, timestamp, key, field, value, ttl=None):
        return self._set(timestamp, key, field, value, ttl)

    def get_at(self, timestamp, key, field):
        return self._get(timestamp, key, field)

    def delete_at(self, timestamp, key, field):
        return self._delete(timestamp, key, field)

    def scan_at(self, timestamp, key):
        return self._scan(timestamp, key, "")

    def scan_by_prefix_at(self, timestamp, key, prefix):
        return self._scan(timestamp, key, prefix)

    # ------------------------------------------------ Level 4 (public)
    def rollback(self, timestamp):
        kept = [entry for entry in self.log if entry[0] <= timestamp]
        self.store = {}
        self.log = []
        for t, op, args in kept:
            getattr(self, f"_{op}")(t, *args)

    # ------------------------------------------------ internals
    def _live_fields(self, t, key):
        """Field dict for `key`, expired entries filtered out."""
        return {name: f for name, f in self.store.get(key, {}).items()
                if f.alive_at(t)}

    def _set(self, t, key, field, value, ttl=None):
        self.log.append((t, "set", (key, field, value, ttl)))
        self.store.setdefault(key, {})[field] = Field(value, t, ttl)

    def _get(self, t, key, field):
        f = self._live_fields(t, key).get(field)
        return None if f is None else f.value

    def _delete(self, t, key, field):
        if field not in self._live_fields(t, key):
            return False
        self.log.append((t, "delete", (key, field)))
        del self.store[key][field]
        return True

    def _compare_and_set(self, t, key, field, expected, new_value):
        f = self._live_fields(t, key).get(field)
        if f is None or f.value != expected:
            return False
        self._set(t, key, field, new_value, f.ttl)
        return True

    def _scan(self, t, key, prefix):
        fields = self._live_fields(t, key)
        return [f"{name}({fields[name].value})"
                for name in sorted(fields) if name.startswith(prefix)]

    def _top_n_keys(self, t, n):
        counts = [(k, len(self._live_fields(t, k))) for k in self.store]
        counts = [(k, c) for k, c in counts if c > 0]
        counts.sort(key=lambda kc: (-kc[1], kc[0]))
        return [f"{k}({c})" for k, c in counts[:n]]
