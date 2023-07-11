#!/usr/bin/env python3
""" Measure run time """
from time import time
import asyncio
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Runtime for 4 parallel comprehensions """
    start = time()

    results = [async_comprehension() for _ in range(4)]
    await asyncio.gather(*results)

    end = time()
    total_time = end - start

    return total_time
