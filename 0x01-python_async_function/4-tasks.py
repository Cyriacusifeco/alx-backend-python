#!/usr/bin/env python3
""" Executing multiple coroutines """
from typing import List
import asyncio
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """ execute multiple coroutines at the same time """

    routines = [task_wait_random(max_delay) for _ in range(n)]

    # as_completed method returns an asynchronous iterator that yields
    # coroutines as they are completed
    return [await routine for routine in asyncio.as_completed(routines)]
