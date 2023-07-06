#!/usr/bin/env python3
""" Mixed list typing """
from typing import Union, List


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Takes a mixed list of integers and float and
    returns their sum as float"""
    return sum(mxd_lst)
