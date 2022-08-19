from brownie import (
    StableSwapHUSD,
    DepositHUSD,
    CurveTokenV2,
    config,
    accounts,
)

DEPLOYER = accounts.add(config["wallets"]["from_key"])
POOL_OWNER = "0xA8c546358EAEE194A7B5F693AF5DB51da7125D42"  # PoolProxy
BASE_POOL = "0xE5248B3de946901cC6A288263190B24Bff33c025" # 3pool

def main():
    token = CurveTokenV2.deploy(
        "Curve.fi HUSD/3Crv", # _name: String[64]
        "husd3CRV", # _symbol: String[32]
        18, # _decimals: uint256
        0, # _supply: uint256
        {"from": DEPLOYER}
    )
    #token = CurveTokenV2.at("0xfcdeD598B8fA83F7a48e9ffdBE8f6b8f8d394743")

    coins = [
        "0x7011306db3dc8f3f7d954f9dd46bf8b20af75a11", # HUSD
        "0x776879aBDe87Eb540faCBF44c13aaef445796cCe" # 3CRV
    ]

    swap = StableSwapHUSD.deploy(
        POOL_OWNER, # _owner: address,
        coins, # _coins: address[N_COINS],
        token, # _pool_token: address,
        BASE_POOL, # _base_pool: address,
        200, # _A: uint256,
        4000000, # _fee: uint256,
        0, # _admin_fee: uint256
        {"from": DEPLOYER}
    )
    #swap = StableSwapHUSD.at("0x147405e9A8AA2aFFDCE8C3D0e13A560c3cFcf53B")

    token.set_minter(swap, {"from": DEPLOYER})

    zap = DepositHUSD.deploy(
        swap, # _pool: address,
        token, # _token: address
        {"from": DEPLOYER}
    )
