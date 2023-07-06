#!/usr/bin/env python3
""" Complex type module """
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Takes a str and an int/float and returns a tuple"""
    return (k, v * v)
