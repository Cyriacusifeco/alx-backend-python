#!/usr/bin/env python3
""" Duck type an iterable object """
from typing import Tuple, List, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Takes an interable and returns a list of tuple """
    return [(i, len(i)) for i in lst]
