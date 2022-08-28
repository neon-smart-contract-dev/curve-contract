import brownie
import pytest
import time

from brownie import (
    web3
)

pytestmark = pytest.mark.target_pool("3pool", "hbtc", "pax", "sbtc")


MIN_RAMP_TIME = 86400


def test_ramp_A(chain, alice, swap):
    initial_A = swap.initial_A()
    future_time = web3.eth.get_block(web3.eth.block_number).timestamp + MIN_RAMP_TIME + 5

    tx = swap.ramp_A(initial_A * 2, future_time, {"from": alice})

    assert swap.initial_A() == initial_A
    assert swap.future_A() == initial_A * 2
    assert swap.initial_A_time() == tx.timestamp
    assert swap.future_A_time() == future_time


def test_ramp_A_final(chain, alice, swap):
    initial_A = swap.initial_A()
    future_time = web3.eth.get_block(web3.eth.block_number).timestamp + 20

    swap.ramp_A(initial_A * 2, future_time, {"from": alice})

    time.sleep(20)

    assert swap.A() == initial_A * 2


def test_ramp_A_value_up(chain, alice, swap):
    initial_A = swap.initial_A()
    future_time = web3.eth.get_block(web3.eth.block_number).timestamp + 60
    tx = swap.ramp_A(initial_A * 2, future_time, {"from": alice})

    initial_time = tx.timestamp
    duration = future_time - tx.timestamp

    while web3.eth.get_block(web3.eth.block_number).timestamp < future_time:
        time.sleep(1)

        block_number = web3.eth.block_number
        timestamp = web3.eth.get_block(block_number).timestamp
        current_A = swap.A()
        time.sleep(2)
        timestamp_next_block = web3.eth.get_block(block_number + 1).timestamp

        expected = int(initial_A + ((timestamp - initial_time) / duration) * initial_A)
        expected_next_block = int(initial_A + ((timestamp_next_block - initial_time) / duration) * initial_A)

        if timestamp_next_block < future_time:
            assert expected <= current_A <= expected_next_block


def test_ramp_A_value_down(chain, alice, swap):
    initial_A = swap.initial_A()
    future_time = web3.eth.get_block(web3.eth.block_number).timestamp + 60
    tx = swap.ramp_A(initial_A // 10, future_time, {"from": alice})

    initial_time = tx.timestamp
    duration = future_time - tx.timestamp

    while web3.eth.get_block(web3.eth.block_number).timestamp < future_time:
        time.sleep(1)

        block_number = web3.eth.block_number
        timestamp = web3.eth.get_block(block_number).timestamp
        current_A = swap.A()
        time.sleep(2)
        timestamp_next_block = web3.eth.get_block(block_number + 1).timestamp

        expected = int(initial_A - ((timestamp - initial_time) / duration) * (initial_A // 10 * 9))
        expected_next_block = int(initial_A - ((timestamp_next_block - initial_time) / duration) * (initial_A // 10 * 9))

        if timestamp_next_block < future_time:
            assert expected >= current_A >= expected_next_block


def test_stop_ramp_A(chain, alice, swap):
    initial_A = swap.initial_A()
    future_time = web3.eth.get_block(web3.eth.block_number).timestamp + 1000000
    swap.ramp_A(initial_A * 2, future_time, {"from": alice})

    time.sleep(10)

    current_A = swap.A()

    tx = swap.stop_ramp_A({"from": alice})

    assert swap.initial_A() == current_A
    assert swap.future_A() == current_A
    assert swap.initial_A_time() == tx.timestamp
    assert swap.future_A_time() == tx.timestamp


def test_ramp_A_only_owner(chain, bob, swap):
    with pytest.raises(ValueError):
        swap.ramp_A(0, web3.eth.get_block(web3.eth.block_number).timestamp + 1000000, {"from": bob})


def test_ramp_A_insufficient_time(chain, alice, swap):
    with pytest.raises(ValueError):
        swap.ramp_A(0, web3.eth.get_block(web3.eth.block_number).timestamp + MIN_RAMP_TIME - 1, {"from": alice})


def test_stop_ramp_A_only_owner(chain, bob, swap):
    with pytest.raises(ValueError):
        swap.stop_ramp_A({"from": bob})
