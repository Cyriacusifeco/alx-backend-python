#!/usr/bin/env python3
""" Executing multiple coroutines """
from typing import List
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """ execute multiple coroutines at the same time """

    routines = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]

    # as_completed method returns an asynchronous iterator that yields
    # coroutines as they are completed
    return [await routine for routine in asyncio.as_completed(routines)]
