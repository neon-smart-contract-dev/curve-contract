# curve-contract/contracts/pools/husd

[Curve HUSD metapool](https://www.curve.fi/husd), allowing swaps via the Curve [tri-pool](../3pool).

## Contracts

* [`DepositHUSD`](DepositHUSD.vy): Depositor contract, used to wrap underlying tokens prior to depositing them into the pool
* [`StableSwapHUSD`](StableSwapHUSD.vy): Curve stablecoin AMM contract

## Deployments

* [`CurveContractV2`](../../tokens/CurveTokenV2.vy): [0xfcdeD598B8fA83F7a48e9ffdBE8f6b8f8d394743](https://neonscan.org/address/0xfcdeD598B8fA83F7a48e9ffdBE8f6b8f8d394743)
* [`DepositHUSD`](DepositHUSD.vy): [0x2aA3f593C96D3dFeec87864ee5C8F421366d181c](https://neonscan.org/address/0x2aA3f593C96D3dFeec87864ee5C8F421366d181c)
* [`LiquidityGauge`](../../gauges/LiquidityGauge.vy): [0xF5cc2115B6d6864eBeBaD690e588fE8E5c01946b](https://neonscan.org/address/0xF5cc2115B6d6864eBeBaD690e588fE8E5c01946b)
* [`StableSwapHUSD`](StableSwapHUSD.vy): [0x147405e9A8AA2aFFDCE8C3D0e13A560c3cFcf53B](https://neonscan.org/address/0x147405e9A8AA2aFFDCE8C3D0e13A560c3cFcf53B)

## Stablecoins

Curve HUSD metapool utilizes the supports swaps between the following assets:

## Direct swaps

Direct swaps are possible between HUSD and the Curve tri-pool LP token.

* `HUSD`: [0x7011306db3dc8f3f7d954f9dd46bf8b20af75a11](https://neonscan.org/address/0x7011306db3dc8f3f7d954f9dd46bf8b20af75a11)
* `3CRV`: [0x776879aBDe87Eb540faCBF44c13aaef445796cCe](https://neonscan.org/address/0x776879aBDe87Eb540faCBF44c13aaef445796cCe)

## Base Pool coins

The tri-pool LP token may be wrapped or unwrapped to provide swaps between HUSD and the following stablecoins:

* `DAI`: [0x1d9af6e77650ffc67c15a50fb9d8f0d2ba345c52](https://neonscan.org/address/0x1d9af6e77650ffc67c15a50fb9d8f0d2ba345c52)
* `USDC`: [0x1a5a01a2adbe256e994c0f3a894ceb70a78a191c](https://neonscan.org/address/0x1a5a01a2adbe256e994c0f3a894ceb70a78a191c)
* `USDT`: [0xC046E84dA78E3d35F15c5F97438b72048D687479](https://neonscan.org/address/0xC046E84dA78E3d35F15c5F97438b72048D687479)
