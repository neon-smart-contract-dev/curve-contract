import pytest
from pytest import approx

pytestmark = pytest.mark.usefixtures("add_initial_liquidity", "approve_bob")

ETH_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"


@pytest.mark.itercoins("sending", "receiving")
def test_min_dy(bob, swap, wrapped_coins, sending, receiving, wrapped_decimals, base_amount):
    amount = 10 ** wrapped_decimals[sending]
    if wrapped_coins[sending] == ETH_ADDRESS:
        value = amount
    else:
        wrapped_coins[sending]._mint_for_testing(bob, amount, {"from": bob})
        value = 0

    min_dy = swap.get_dy(sending, receiving, amount)
    swap.exchange(sending, receiving, amount, min_dy - 1, {"from": bob, "value": value})

    if wrapped_coins[receiving] == ETH_ADDRESS:
        received = bob.balance() - 10 ** 18 * base_amount
    else:
        received = wrapped_coins[receiving].balanceOf(bob)

    assert abs(received - min_dy) <= 1
