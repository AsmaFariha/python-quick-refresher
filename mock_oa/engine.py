"""Pre-built engine classes. DO NOT MODIFY THIS FILE.

You will implement the functions in scheduler.py, which operate on these
classes. Read carefully — not every field is set for you; the scheduler is
responsible for updating runtime state.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class EngineConfig:
    """Static engine parameters.

    prefill_rate: prompt tokens processed per tick during prefill.
    memory_limit: KV-cache capacity of ONE worker, in tokens. A request
        reserves its full potential footprint (prompt_tokens + max_new_tokens)
        for its entire lifetime on the worker.
    """
    prefill_rate: int = 4
    memory_limit: int = 100


@dataclass
class Request:
    """A single inference request.

    Immutable inputs: id, arrival, prompt_tokens, max_new_tokens.
    Runtime state (managed by YOUR scheduler code): everything else.
    """
    id: int
    arrival: int
    prompt_tokens: int
    max_new_tokens: int

    prefill_done: int = 0
    tokens_generated: int = 0
    started_at: Optional[int] = None
    first_token_at: Optional[int] = None
    finished_at: Optional[int] = None

    @property
    def reserved(self) -> int:
        """KV-cache tokens this request reserves while on a worker."""
        return self.prompt_tokens + self.max_new_tokens

    def fresh(self) -> "Request":
        """A copy with runtime state reset."""
        return Request(self.id, self.arrival, self.prompt_tokens,
                       self.max_new_tokens)


class Worker:
    """A single GPU worker. The scheduler may use this or manage its own
    bookkeeping — tests only check the return values of scheduler functions.
    """

    def __init__(self, index: int, config: EngineConfig):
        self.index = index
        self.config = config
        self.running: list[Request] = []
        self.reserved_tokens: int = 0

    def has_room_for(self, req: Request) -> bool:
        return self.reserved_tokens + req.reserved <= self.config.memory_limit
