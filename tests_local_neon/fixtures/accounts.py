import pytest

from brownie import (
    config,
    Contract,
    web3
)

@pytest.fixture(scope="session")
def add_accounts(accounts):
    accounts.add(web3.eth.account.create().key)
    accounts.add(web3.eth.account.create().key)
    accounts.add(web3.eth.account.create().key)
    accounts.add(config["wallets"]["from_key"])
    accounts[3].transfer(accounts[0], "20000 ether", allow_revert=True)
    accounts[3].transfer(accounts[1], "20000 ether", allow_revert=True)
    accounts[3].transfer(accounts[2], "20000 ether", allow_revert=True)
    yield accounts


@pytest.fixture(scope="session")
def alice(add_accounts, accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def bob(add_accounts, accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def charlie(add_accounts, accounts):
    yield accounts[2]


@pytest.fixture(scope="session")
def acc_deployer(add_accounts, accounts):
    yield accounts[3]

