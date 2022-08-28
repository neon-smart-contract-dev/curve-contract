import pytest


def test_fallback_reverts(swap, bob):
    with pytest.raises(ValueError):
        bob.transfer(swap, "1 ether", gas_limit=100000000, allow_revert=True)
