from decimal import Decimal, getcontext
from typing import Tuple, Dict, List

import math

getcontext().prec = 28 # Increase precision for financial calculations


class ArbitrageMathEngine:
"""Ultra-optimized mathematics engine for high-frequency arbitrage operations."""


def __init__(self, min_profit_threshold: Decimal = Decimal('0.001')):
self.min_profit_threshold = min_profit_threshold


def calculate_price_impact(self, amount_in: Decimal, reserve_in: Decimal, reserve_out: Decimal) -> Decimal:
if reserve_in <= 0 or reserve_out <= 0 or amount_in <= 0:
return Decimal('0')


k = reserve_in * reserve_out
new_reserve_in = reserve_in + amount_in
new_reserve_out = k / new_reserve_in
amount_out = reserve_out - new_reserve_out


expected_price = amount_in * reserve_in / reserve_out
actual_price = amount_in / amount_out if amount_out > 0 else Decimal('0')


return abs(actual_price - expected_price) / expected_price * 100 if expected_price > 0 else Decimal('0')


def calculate_output_amount(self, amount_in: Decimal, reserve_in: Decimal, reserve_out: Decimal, fee: Decimal = Decimal('0.003')) -> Decimal:
if reserve_in <= 0 or reserve_out <= 0 or amount_in <= 0:
return Decimal('0')


amount_in_with_fee = amount_in * (Decimal('1') - fee)
numerator = amount_in_with_fee * reserve_out
denominator = reserve_in + amount_in_with_fee
return numerator / denominator if denominator > 0 else Decimal('0')


def calculate_arbitrage_profit(self, amount_in: Decimal, dex_path: List[Tuple[Decimal, Decimal]], gas_cost: Decimal = Decimal('0')) -> Dict:
current_amount = amount_in
path_details = []


for i in range(len(dex_path) - 1):
reserve_in, reserve_out = dex_path[i]
next_reserve_in, next_reserve_out = dex_path[i + 1]


amount_out = self.calculate_output_amount(current_amount, reserve_in, reserve_out)
path_details.append({
'dex_index': i,
'input': current_amount,
'output': amount_out,
'price_impact': self.calculate_price_impact(current_amount, reserve_in, reserve_out)
})
current_amount = self.calculate_output_amount(amount_out, next_reserve_out, next_reserve_in) # reverse swap for selling


gross_profit = current_amount - amount_in
net_profit = gross_profit - gas_cost
profit_percentage = (net_profit / amount_in * 100) if amount_in > 0 else Decimal('0')


return {
'input_amount': amount_in,
'final_output': current_amount,
'gross_profit': gross_profit,
'net_profit': net_profit,
'profit_percentage': profit_percentage,
'gas_cost': gas_cost,
'is_profitable': net_profit > self.min_profit_threshold * amount_in,
'path_details': path_details
}


def optimize_input_amount(self, dex_path: List[Tuple[Decimal, Decimal]], max_input: Decimal, gas_cost: Decimal = Decimal('0')) -> Dict:
low = Decimal('0.001')
high = max_input
best_result = {'net_profit': Decimal('-inf'), 'input_amount': low}


for _ in range(30):
mid = (low + high) / 2
result = self.calculate_arbitrage_profit(mid, dex_path, gas_cost)
higher = self.calculate_arbitrage_profit(mid * Decimal('1.1'), dex_path, gas_cost)


if result['net_profit'] > best_result['net_profit']:
best_result = result
return max(min(dynamic_slippage, Decimal('0.05')), Decimal('0.001'))
