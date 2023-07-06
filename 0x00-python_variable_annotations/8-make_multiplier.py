#!/usr/bin/env python3
""" complex typing: function """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Takes a float and returns a function that multiplies
    a float by multiplier """
    def mul(x: float) -> float:
        return x * multiplier
    return mul
