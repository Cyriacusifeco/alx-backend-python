#!/usr/bin/env python3
""" Using TypeVar """
from typing import TypeVar, Mapping, Union, Any


T = TypeVar('T')


def safely_get_value(
        dct: Mapping, key: Any, default: Union[T, None]) -> Union[Any, T]:
    """ using TypeVar annotation """
    if key in dict:
        return dct[key]
    else:
        return default
