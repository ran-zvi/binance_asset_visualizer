from dataclasses import dataclass
from typing import NamedTuple, Optional

from data.constants import ComparisonResult
from data.settings import TokenBalances, TokenBalance


@dataclass
class TokenComparisonResult(NamedTuple):
    result: ComparisonResult
    diff: TokenBalance

    @classmethod
    def compare(cls, left: TokenBalance, right: TokenBalance) -> 'TokenComparisonResult':
        diff = left - right
        if left == right:
            result = ComparisonResult.Equal
        else:
            if diff.balance() < 0:
                result = ComparisonResult.Smaller
            else:
                result = ComparisonResult.Greater
        return cls(result, diff)

TokenComparisonResults = dict[str, TokenComparisonResult]


@dataclass
class TokenBalanceCorrectionData(NamedTuple):
    left: TokenBalance
    right: TokenBalance
    comparison_result: TokenComparisonResult

    @classmethod
    def create_from_dicts(cls, token_name: str, left: TokenBalances, right: TokenBalances,
                          comparison_result: TokenComparisonResult) -> 'TokenBalanceCorrectionData':
        return cls(
            left.get(token_name, TokenBalance()),
            right.get(token_name, TokenBalance()),
            comparison_result
        )

    def correct_staking_data(self) -> TokenBalance:
        if self.comparison_result == ComparisonResult.Smaller:
            return self.right
        else:
            return self.right + self.left.flipped()


TokenBalanceCorrectionDataset = dict[str, TokenBalanceCorrectionData]


def in_price_range(old_price: float, new_price: float, acceptable_percentage_error: float = 0) -> bool:
    percentage_of_price = (old_price / 100) * acceptable_percentage_error
    low_price_end = old_price - percentage_of_price
    high_price_end = old_price + percentage_of_price
    return high_price_end >= new_price >= low_price_end


def compare_token_balances(left: TokenBalances, right: TokenBalances) -> dict[str, TokenComparisonResult]:
    all_tokens = list(set(left.keys()).union(right.keys()))
    default = TokenBalance()
    comparison_result = {}
    for token in all_tokens:
        result = TokenComparisonResult.compare(
            left.get(token, default),
            right.get(token, default)
        )
        comparison_result[token] = result
    return comparison_result


def _get_balance_correction_data(left: TokenBalances, right: TokenBalances,
                                 comparison_results: TokenComparisonResults) -> TokenBalanceCorrectionDataset:
    return {
        token: TokenBalanceCorrectionData.create_from_dicts(token, left, right, comparison_results) for token in
        comparison_results
    }


def correct_token_balances(left: TokenBalances, right: TokenBalances, timestamp: float):
    comparison_results = compare_token_balances(left, right)
    non_equal_results = {token: result for token, result in comparison_results.items() if
                         result.result != ComparisonResult.Equal}
    balance_correction_data = _get_balance_correction_data(left, right, non_equal_results)


def _correct_non_equal_tokens(balance_correction_data: TokenBalanceCorrectionDataset, timestamp: float) -> TokenBalances:
    if len(balance_correction_data) == 1:
        token = list(balance_correction_data.keys())[0]
        corrected_balance = balance_correction_data[token].correct_staking_data()
        return {token: corrected_balance}
    else:
        return _correct_skewed_balances_by_price(balance_correction_data, timestamp)


def _correct_skewed_balances_by_price(balance_correction_data, timestamp):
    pass
