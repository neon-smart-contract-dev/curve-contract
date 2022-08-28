curl -i -X POST     -d '{"wallet": "0x25379d8c2fC2F9CCA4bD4d1CdBC3AA2702C58896", "amount": 50000}'     'http://localhost:3333/request_neon'
curl -i -X POST     -d '{"wallet": "0x25379d8c2fC2F9CCA4bD4d1CdBC3AA2702C58896", "amount": 50000}'     'http://localhost:3333/request_neon'

brownie networks add Neon neon_local host=http://localhost:9090/solana chainid=111 explorer=https://neonscan.org timeout=120

brownie test tests_local_neon/local_neon/ --pool 3pool --network neon_local -I -s



