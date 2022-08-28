import pytest
from brownie import ETH_ADDRESS, WETH, accounts

# shared logic for pool and base_pool setup fixtures


def _add_liquidity(acct, swap, coins, amounts):
    eth_value = 0
    if ETH_ADDRESS in coins:
        eth_value = amounts[coins.index(ETH_ADDRESS)]
    swap.add_liquidity(amounts, 0, {"from": acct, "value": eth_value})


def _mint(acct, wrapped_coins, wrapped_amounts, underlying_coins, underlying_amounts, is_forked, acc_deployer):
    for coin, amount in zip(wrapped_coins, wrapped_amounts):
        if coin == ETH_ADDRESS:
            if is_forked:
                # in fork mode, we steal ETH from the wETH contract
                weth = WETH.at("0x0071e2E38A52BbE86455Db84FaA9E0736cE038fd")
                weth.deposit({"from": acc_deployer, "value": amount})
                weth.transfer(acct, amount, {"from": acc_deployer})
            continue

        coin._mint_for_testing(acct, amount, {"from": acct})

    for coin, amount in zip(underlying_coins, underlying_amounts):
        if coin == ETH_ADDRESS or coin in wrapped_coins:
            if is_forked:
                weth = WETH.at("0x0071e2E38A52BbE86455Db84FaA9E0736cE038fd")
                weth.deposit({"from": acc_deployer, "value": amount})
                weth.transfer(acct, amount, {"from": acc_deployer})
            continue

        coin._mint_for_testing(acct, amount, {"from": acct})

def _approve(owner, spender, *coins):
    for coin in set(x for i in coins for x in i):
        if coin == ETH_ADDRESS:
            continue

        if coin.name() == "USDT" and coin.allowance(owner, spender) != 0:
            coin.approve(spender, 0, {"from": owner})

        coin.approve(spender, 2 ** 256 - 1, {"from": owner})


# pool setup fixtures


@pytest.fixture
def add_initial_liquidity(
    alice, mint_alice, approve_alice, underlying_coins, swap, initial_amounts
):
    # mint (10**7 * precision) of each coin in the pool
    _add_liquidity(alice, swap, underlying_coins, initial_amounts)


@pytest.fixture
def mint_bob(
    bob, underlying_coins, wrapped_coins, initial_amounts, initial_amounts_underlying, is_forked, acc_deployer
):
    _mint(
        bob, wrapped_coins, initial_amounts, underlying_coins, initial_amounts_underlying, is_forked, acc_deployer
    )


@pytest.fixture
def approve_bob(bob, swap, underlying_coins, wrapped_coins):
    _approve(bob, swap, underlying_coins, wrapped_coins)

@pytest.fixture
def mint_alice(
    alice, underlying_coins, wrapped_coins, initial_amounts, initial_amounts_underlying, is_forked, acc_deployer
):
    _mint(
        alice,
        wrapped_coins,
        initial_amounts,
        underlying_coins,
        initial_amounts_underlying,
        is_forked,
        acc_deployer
    )


@pytest.fixture
def approve_alice(alice, swap, underlying_coins, wrapped_coins):
    _approve(alice, swap, underlying_coins, wrapped_coins)

@pytest.fixture
def approve_deployer(acc_deployer, swap, underlying_coins, wrapped_coins):
    _approve(acc_deployer, swap, underlying_coins, wrapped_coins)

@pytest.fixture
def approve_zap(alice, bob, zap, pool_token, underlying_coins):
    for underlying in underlying_coins:
        if underlying == "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":
            continue
        underlying.approve(zap, 2 ** 256 - 1, {"from": alice})
        underlying.approve(zap, 2 ** 256 - 1, {"from": bob})

    pool_token.approve(zap, 2 ** 256 - 1, {"from": alice})
    pool_token.approve(zap, 2 ** 256 - 1, {"from": bob})


@pytest.fixture
def _add_base_pool_liquidity(
    charlie, base_swap, _base_coins, base_pool_data, base_amount, is_forked, acc_deployer
):
    # private fixture to add liquidity to the metapool
    if base_pool_data is None:
        return

    decimals = [i.get("decimals", i.get("wrapped_decimals")) for i in base_pool_data["coins"]]
    initial_amounts = [10 ** i * base_amount * 2 for i in decimals]
    _mint(charlie, _base_coins, initial_amounts, [], [], is_forked, acc_deployer)
    _approve(charlie, base_swap, _base_coins)
    _add_liquidity(charlie, base_swap, _base_coins, initial_amounts)
