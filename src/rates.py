"""
Module Name: Rates
Description: Implements methods of generating discount (and forward) factors and rates accounting for compounding conversions
Date: [2025-03-19]
"""

# Imports
import numpy as np
import pandas as pd
from typing import Iterable

# =============================================================================
#  1. Rate Conversion
# =============================================================================

def rate_to_factor(discount_rate: float, ttm: float, compounding_freq: str | int) -> float:
    ''' 
    Given an annualized discount rate, a time to maturity, and a compounding frequency for the initial discount rate, convert the discount rate into a discount factor.

    Params:
        discount_rate (float): the discount rate in decimal form (0.0x for x percent).
        ttm (float): time to maturity in years.
        compounding_freq (str | int): the number of compounding periods in a year. "continuous" if continuous compounding. 
    
    Returns:
        (float): the discount factor calculated
    '''
    if compounding_freq=='continuous':
        return np.exp(-discount_rate * ttm)
    else:
        return (1 + discount_rate/compounding_freq)**(-compounding_freq * ttm)

def factor_to_rate(discount_factor: float, ttm: float, compounding_freq: str| int) -> float:
    ''' 
    Given an discount factor, a time to maturity, and a compounding frequency, convert the discount factor to an annualized discount rate.

    Params:
        discount_factor (float): the number f such that cash flow * f = present value.
        ttm (float): time to maturity in years.
        compounding_freq (str | int): the number of compounding periods in a year. "continuous" if continuous compounding. 
    
    Returns:
        (float): the discount rate calculated at that speciifc compounding frequency
    '''
    if compounding_freq=='continuous':
        return np.log(1/discount_factor)/ttm
    else:
        return ((1/discount_factor)**(1/compounding_freq/ttm) - 1) * compounding_freq
    

def spot_forward_factors_conversion(factors: Iterable) -> list[float]:
    """
    Converts a list of spot discount factors to forward discount factors within the same time intervals

    Params:
        factors (Iterable): any list of discount factors

    Returns:
        (list[float]): a list of forward discount factors at the same TTMs
    """
    forward_factors = [factors[i+1] / factors[i] for i in range(len(factors) - 1)]
    forward_factors.append(None)
    return forward_factors


