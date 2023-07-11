#!/usr/bin/env python3
""" This is an Async generator """
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """The asycn generator function """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
