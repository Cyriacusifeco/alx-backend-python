#!/usr/bin/env python3
""" Creating instances of asyncio.Task """
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """ creates asyncio.Task object """
    task = asyncio.create_task(wait_random())
    return task
