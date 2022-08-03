from brownie import (
    StableSwap3Pool,
    CurveTokenV2,
    config,
    accounts,
)

DEPLOYER = accounts.add(config["wallets"]["from_key"])
POOL_OWNER = "0xA8c546358EAEE194A7B5F693AF5DB51da7125D42"  # PoolProxy

def main():
    token = CurveTokenV2.deploy(
        "Curve.fi DAI/USDC/USDT", # _name: String[64]
        "3Crv", # _symbol: String[32]
        18, # _decimals: uint256
        0, # _supply: uint256
        {"from": DEPLOYER}
    )

    coins = [
        "0x1d9af6e77650ffc67c15a50fb9d8f0d2ba345c52", # DAI
        "0x1a5a01a2adbe256e994c0f3a894ceb70a78a191c", # USDC
        "0xC046E84dA78E3d35F15c5F97438b72048D687479" # USDT
    ]

    swap = StableSwap3Pool.deploy(
        POOL_OWNER, # _owner: address,
        coins, # _coins: address[N_COINS],
        token, # _pool_token: address,
        2000, # _A: uint256,
        1000000, # _fee: uint256,
        5000000000, # _admin_fee: uint256
        {"from": DEPLOYER}
    )

    token.set_minter(swap, {"from": DEPLOYER})
