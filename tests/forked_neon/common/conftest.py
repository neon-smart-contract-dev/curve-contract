import json
import brownie
import pytest
from brownie import Contract
from brownie.project.main import get_loaded_projects

COMMIT_WAIT = 86400 * 3

@pytest.fixture(scope="module", autouse=True)
def update_pool_owner(chain, deployer, alice, swap):
    pool_proxy = Contract(swap.owner())
    pool_proxy.commit_transfer_ownership(swap, alice, {"from": deployer})
    chain.sleep(COMMIT_WAIT)
    pool_proxy.apply_transfer_ownership(swap, {"from": deployer})

@pytest.fixture(scope="module", autouse=True)
def remove_all_liquidity(pool_token, deployer, swap, n_coins):
    if pool_token.totalSupply() > 0:
        swap.remove_liquidity(
            pool_token.totalSupply(), [0] * n_coins, {"from": deployer}
        )

@pytest.fixture(scope="module", autouse=True)
def init_3pool_fees(chain, deployer):
    with get_loaded_projects()[0]._path.joinpath("contracts/pools/3pool/pooldata.json").open() as fp:
        swap = Contract(json.load(fp)["swap_address"])

    owner = swap.owner()
    swap.commit_new_fee(0, 0, {"from": owner})
    chain.sleep(COMMIT_WAIT)
    swap.apply_new_fee({"from": owner})
