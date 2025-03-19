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
    

def factor_to_forward(factors: Iterable) -> list[float]:
    """
    Converts a list of spot discount factors to forward discount factors within the same time intervals.
    These forward factors are forward looking for the TTM interval of the discount factors
        (for instance, the 3 yr forward discount factor would be for the period between 3 and 3 + TTM interval)

    Params:
        factors (Iterable): any list of discount factors

    Returns:
        (list[float]): a list of forward discount factors at the same TTMs
    """
    forward_factors = [factors[i+1] / factors[i] for i in range(len(factors) - 1)]
    forward_factors.append(None)
    return forward_factors


def rate_factor_converter(input_type: str, input_values: Iterable, input_ttms: Iterable, dr_compounding_freq: int = 2, fr_compounding_freq: int = 2) -> pd.DataFrame:
    ''' 
    Given any of discount rates, discount factors, forward rates, forward factors, can produce information on the other three in a dataframe
    Note: forward looking time window is always going to be difference between TTM values

    Params:
        input (str): string of which input metrics is given (DR: discount rate, DF: discount factor, FR: forward rate, FF: forward factor)
        input_values (Iterable): list of input rates/factors
        input_ttms (Iterable): list of input time to maturity
        dr_compounding_freq (int): the number of compounding periods in a year for the discount rate. "continuous" if continuous compounding. 
        fr_compounding_freq (int): the number of compounding periods in a year for the forward rate. "continuous" if continuous compounding. 
    
    Returns:
        pd.DataFarme: A dataframe with all four metrics returned
    '''
    input_set = {'DR', 'DF', 'FR', 'FF'}

    if input_type not in input_set:
        raise ValueError(f"Input type must be one of these: {input_set}")

    data = pd.DataFrame({'TTM': input_ttms, input_type: input_values})

    if input_type == 'DR':
        data['DF'] = rate_to_factor(data['DR'], data['TTM'], dr_compounding_freq)
        data['FF'] = factor_to_forward(data['DF'])
        data['FR'] = factor_to_rate(data['FF'], data['TTM'], fr_compounding_freq)
    
    

    

    # if input == 'DR':
    #     output = output.rename(columns = {'Metric': 'Discount Rates'})
    #     output['Discount Factors'] = convert_discount_rate_to_discount_factor(output['Discount Rates'], output['Time'], dr_compounding_freq)
    #     w = spot_forward_factors_conversion(output)
    #     output['Forward Discount Factors'] = w['Forward Discount Factors']
    #     output['Forward Discount Rates'] = convert_discount_factor_to_discount_rate(output['Forward Discount Factors'], forward_time_length, fr_compounding_freq)
    #     output['Forward Discount Rates'] = output['Forward Discount Rates'].shift(-1)
    #     output['Forward Discount Factors'] = output['Forward Discount Factors'].shift(-1)
    
    # elif input == 'DF':
    #     output = output.rename(columns = {'Metric': 'Discount Factors'})
    #     output['Discount Rates'] = convert_discount_factor_to_discount_rate(output['Discount Factors'], output['Time'], dr_compounding_freq)
    #     w = spot_forward_factors_conversion(output)
    #     output['Forward Discount Factors'] = w['Forward Discount Factors']
    #     output['Forward Discount Rates'] = convert_discount_factor_to_discount_rate(output['Forward Discount Factors'], forward_time_length, fr_compounding_freq)
    #     output['Forward Discount Rates'] = output['Forward Discount Rates'].shift(-1)
    #     output['Forward Discount Factors'] = output['Forward Discount Factors'].shift(-1)

    # elif input == 'FR':
    #     output = output.rename(columns = {'Metric': 'Forward Discount Rates'})
    #     output['Forward Discount Factors'] = convert_discount_rate_to_discount_factor(output['Forward Discount Rates'], forward_time_length, fr_compounding_freq)
    #     output['Discount Factors'] = output['Forward Discount Factors'].cumprod()
    #     output['Discount Rates'] = convert_discount_factor_to_discount_rate(output['Discount Factors'], output['Time'], dr_compounding_freq)

    # elif input == 'FF':
    #     output = output.rename(columns = {'Metric': 'Forward Discount Factors'})
    #     output['Discount Factors'] = output['Forward Discount Factors'].cumprod()
    #     output['Forward Discount Rates'] = convert_discount_factor_to_discount_rate(output['Forward Discount Factors'], forward_time_length, fr_compounding_freq)
    #     output['Discount Rates'] = convert_discount_factor_to_discount_rate(output['Discount Factors'], output['Time'], dr_compounding_freq)
    
    # return output
