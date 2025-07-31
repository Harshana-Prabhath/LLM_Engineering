import asyncio
from typing import Coroutine, TypeVar, Any

T = TypeVar("T")

def run_async(coro: Coroutine[Any, Any, T]) -> T:
    """Run an async coroutine."""
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(coro)