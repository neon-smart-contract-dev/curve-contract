# curve-contract

Vyper contracts used in [Curve](https://www.curve.fi/) exchange pools.

## Overview

Curve is an exchange liquidity pool on Ethereum designed for extremely efficient stablecoin trading and low risk, supplemental fee income for liquidity providers, without an opportunity cost.

Curve allows users to trade between correlated cryptocurrencies with a bespoke low slippage, low fee algorithm. The liquidity pool is also supplied to lending protocol where it generates additional income for liquidity providers.

## Testing and Development

### Dependencies

* [python3](https://www.python.org/downloads/release/python-368/) from version 3.6 to 3.8, python3-dev
* [brownie](https://github.com/iamdefinitelyahuman/brownie) - tested with version [1.13.2](https://github.com/eth-brownie/brownie/releases/tag/v1.13.2)
* [ganache-cli](https://github.com/trufflesuite/ganache-cli) - tested with version [6.12.1](https://github.com/trufflesuite/ganache-cli/releases/tag/v6.12.1)
* [brownie-token-tester](https://github.com/iamdefinitelyahuman/brownie-token-tester) - tested with version [0.1.0](https://github.com/iamdefinitelyahuman/brownie-token-tester/releases/tag/v0.1.0)

Curve contracts are compiled using [Vyper](https://github.com/vyperlang/vyper), however installation of the required Vyper versions is handled by Brownie.

### Setup

To get started, first create and initialize a Python [virtual environment](https://docs.python.org/3/library/venv.html). Next, clone the repo and install the developer dependencies:

```bash
git clone https://github.com/curvefi/curve-contract.git
cd curve-contract
pip install -r requirements.txt
```

### Organization and Workflow

* New Curve pools are built from the contract templates at [`contracts/pool-templates`](contracts/pool-templates)
* Once deployed, the contracts for a pool are added to [`contracts/pools`](contracts/pools)

See the documentation within [`contracts`](contracts) and it's subdirectories for more detailed information on how to get started developing on Curve.

### Add Neon networks to brownie

```bash
brownie networks add Neon neon host=https://proxy.devnet.neonlabs.org/solana chainid=245022926 explorer=https://neonscan.org timeout=120
brownie networks add Neon neon_mainnet host=https://proxy.mainnet.neonlabs.org/solana chainid=245022934 explorer=https://neonscan.org timeout=120
brownie networks add Neon neon_testnet host=https://proxy.testnet.neonlabs.org/solana chainid=245022940 explorer=https://neonscan.org timeout=120
brownie networks add Neon neon_local host=http://localhost:9090/solana chainid=111 explorer=https://neonscan.org timeout=120
```

### Add forked devnet Neon network to brownie

```bash
brownie networks add Development neon-devnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=neon port=8545 evm_version=istanbul accounts=10 timeout=120
```

### Running the Tests

The [test suite](tests) contains common tests for all Curve pools, as well as unique per-pool tests. To run the entire suite:

```bash
brownie test
```

To run tests on a specific pool:

```bash
brownie test tests/ --pool <POOL NAME> -I -s
```

Running tests in forked devnet Neon network for 3pool:

```bash
brownie test tests/forked/ --network neon-devnet-fork --pool 3pool -I -s
brownie test tests/forked_neon/ --network neon-devnet-fork --pool 3pool -I -s
```

Running tests in forked devnet Neon network for HUSD metapool:

```bash
brownie test tests/forked/ --network neon-devnet-fork --pool husd -I -s
brownie test tests/forked_neon/ --network neon-devnet-fork --pool husd -I -s
```

Running tests in local neon network for 3pool:

```bash
brownie test tests_local_neon/local_neon --pool 3pool --network neon_local -I -s
```

Valid pool names are the names of the subdirectories within [`contracts/pools`](contracts/pools). For templates, prepend `template-` to the subdirectory names within [`contracts/pool-templates`](../contracts/pool-templates). For example, the base template is `template-base`.

You can optionally include the `--coverage` flag to view a coverage report upon completion of the tests.

## Deployment

To deploy a new pool:

1. Ensure the `pooldata.json` for the pool you are deploying contains all the necessary fields.
2. Edit the configuration settings within [`scripts/deploy.py`](scripts/deploy.py).
3. Test the deployment locally against a forked Neon Devnet.

    ```bash
    brownie run deploy --network neon-devnet-fork -I
    ```
    
    When the script completes it will open a console. You should call the various getter methods on the deployed contracts to ensure the pool has been configured correctly.

4. Deploy the pool to the Neon.

    ```bash
    brownie run deploy --network neon
    ```

    Be sure to open a pull request that adds the deployment addresses to the pool `README.md`.

## Deployment to Neon

Deploy `CurveTokenV2 3Crv` and `StableSwap3Pool`:

```bash
brownie run scripts/deploy_3pool.py --network neon -I
```

Deploy `CurveTokenV2 husd3CRV` and `StableSwapHUSD`:

```bash
brownie run scripts/deploy_husd.py --network neon -I
```

## Run tests in local neon network by docker

Local neon node must be running beforehand by [proxy-model.py](https://github.com/neonlabsorg/proxy-model.py).

Next, we need to build the image:

```bash
sudo docker build --tag tests_local_neon:1.0.5 .
```

And run container:

```bash
sudo docker run -it --net=host tests_local_neon:1.0.5
```

or so

```bash
sudo docker run -it --net=host tests_local_neon:1.0.5 sh

# ./start.sh
```

## Audits and Security

Curve smart contracts have been audited by Trail of Bits. These audit reports are made available on the [Curve website](https://www.curve.fi/audits).

There is also an active [bug bounty](https://www.curve.fi/bugbounty) for issues which can lead to substantial loss of money, critical bugs such as a broken live-ness condition, or irreversible loss of funds.

## License

(c) Curve.Fi, 2020 - [All rights reserved](LICENSE).
