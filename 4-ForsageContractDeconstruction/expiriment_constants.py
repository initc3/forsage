#!/usr/bin/env python3

from typing import List, Optional, TypedDict
from web3.types import Wei

__author__ = 'tyler'


# Convenience to work with both normal and mutable numbers
def _get_value(obj):
    try:
        return obj.value[0]
    except:
        return obj

# necessary to make ids work like pointers
# each object needs a separate memory location
class MutableObj(object):
    def __init__(self, value):
        self.value = [value]

    def __eq__(self, other):
        return _get_value(self) == _get_value(other)

    def __ne__(self, other):
        return _get_value(self) != _get_value(other)

    def __copy__(self):
        new = MutableObj(None)
        new.value = self.value
        return new

    def __repr__(self):
        return repr(self.value[0])

    def get(self):
        return self.value[0]

class MutableString(MutableObj):
    def __copy__(self):
        new = MutableString('')
        new.value = self.value
        return new

class MutableBool(MutableObj):
    def __copy__(self):
        new = MutableString(False)
        new.value = self.value
        return new

class MutableInt(MutableObj):
    def __copy__(self):
        new = MutableString(0)
        new.value = self.value
        return new

class Address(TypedDict):
    human_name: str
    private_key: str
    addr: str
    balance: int
    balance_start: int

class X3(TypedDict):
    currentReferrer: MutableString
    referrals: List[MutableString]
    blocked: MutableBool
    #reinvestCount: MutableInt

class X6(TypedDict):
    currentReferrer: MutableString
    firstLevelReferrals: List[MutableString]
    secondLevelReferrals: List[MutableString]
    blocked: MutableBool
    #reinvestCount: MutableInt
    closedPart: MutableString

class User(TypedDict):
    name: MutableString
    id: MutableInt
    referrer: MutableString
    partnersCount: MutableInt
    activeX3Levels: List[bool] # note: indexed [0-11] instead of [1-12] like in the solidity
    activeX6Levels: List[bool]
    x3Matrix: List[Optional[X3]]
    x6Matrix: List[Optional[X6]]
    balanceDelta: MutableInt
    balanceLastChange: int

ONE_GWEI = Wei(1000000000)
GAS_MAX =     Wei(8000000)
WEI_TO_ETH = Wei(1000000000000000000)

def wei_to_eth(wei_in: int) -> float:
    return wei_in / WEI_TO_ETH

def eth_to_wei(amount: float) -> int:
    return int(amount * WEI_TO_ETH)

def eth_to_Wei(amount: float) -> Wei:
    return Wei(int(amount * WEI_TO_ETH))

