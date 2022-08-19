import pytest

from brownie import (
    config,
    Contract
)

@pytest.fixture(scope="session")
def alice(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def bob(accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def charlie(accounts):
    yield accounts[2]


@pytest.fixture(scope="module")
def deployer(accounts):
    yield accounts.add(config["wallets"]["from_key"])
