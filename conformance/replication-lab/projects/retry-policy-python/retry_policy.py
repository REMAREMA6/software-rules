from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class RetryDecision:
    retry: bool
    delay_ms: int
    state: str


Backoff = Callable[[int], int]


def decide_retry(
    attempts: int,
    attempts_made: int,
    attempts_started: int = 0,
    max_started_attempts: Optional[int] = None,
    unrecoverable: bool = False,
    backoff: Optional[Backoff] = None,
) -> RetryDecision:
    """Independent model of the bounded retry decision rule.

    attempts_made is the number of failed attempts already recorded.
    The backoff receives a one-based failed-attempt number.
    """
    max_started_reached = (
        bool(max_started_attempts)
        and max_started_attempts <= attempts_started
    )
    if attempts_made + 1 >= attempts or unrecoverable or max_started_reached:
        return RetryDecision(False, 0, "failed")

    delay = backoff(attempts_made + 1) if backoff else 0
    if delay == -1:
        return RetryDecision(False, 0, "failed")

    if delay > 0:
        return RetryDecision(True, delay, "delayed")
    return RetryDecision(True, 0, "waiting")


def fixed(delay_ms: int) -> Backoff:
    return lambda _attempt: delay_ms


def exponential(seed_ms: int) -> Backoff:
    return lambda attempt: round((2 ** (attempt - 1)) * seed_ms)
