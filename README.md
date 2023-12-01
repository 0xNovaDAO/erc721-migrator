# ERC721 Migration Validator

Simple script for snapshotting erc721 contracts, and validating any migrations against them.

Contains logic for overwriting snapshotted data for manual token moves or DAO re-distribution.

Note that while this script snapshots/verifies migrations, it does not execute any write transactions on-chain.

Used for validating the DeFi Girls airdrop from Ethereum to Polygon, sample outputs included under `token_owners.json` and `token_owners.txt`.