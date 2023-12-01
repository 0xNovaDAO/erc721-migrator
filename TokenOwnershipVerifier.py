from web3 import Web3
import json
import concurrent.futures


class TokenOwnershipVerifier:
    polygon_rpc_url = ""
    polygon_contract_address = Web3.to_checksum_address("0xc6D960E677f9081dD78009E4973c49BBd1dAAC75")
    ethereum_json_path = 'token_owners.json'

    abi = [
        {
            "constant": True,
            "inputs": [{"name": "_tokenId", "type": "uint256"}],
            "name": "ownerOf",
            "outputs": [{"name": "", "type": "address"}],
            "payable": False,
            "type": "function",
        }
    ]

    def __init__(self, polygon_rpc_url, polygon_contract_address, ethereum_json_path, abi):
        self.polygon_web3 = Web3(Web3.HTTPProvider(polygon_rpc_url))
        self.polygon_contract = self.polygon_web3.eth.contract(address=Web3.to_checksum_address(polygon_contract_address), abi=abi)
        self.ethereum_json_path = ethereum_json_path

    def get_max_supply(self):
        return self.polygon_contract.functions.maxSupply().call()

    def get_owner(self, token_id):
        print(f"grabbing token at ID {token_id}")
        return token_id, self.polygon_contract.functions.ownerOf(token_id).call()

    def get_owners_from_polygon(self, max_supply):
        owners_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            futures = [executor.submit(self.get_owner, token_id) for token_id in range(max_supply)]
            for future in concurrent.futures.as_completed(futures):
                owners_list.append(future.result())
        owners_list.sort(key=lambda x: x[0])
        return {str(token_id): owner for token_id, owner in owners_list}

    def compare_ownerships(self):
        with open(self.ethereum_json_path, 'r') as file:
            ethereum_owners = json.load(file)

        max_supply = 6765
        polygon_owners = self.get_owners_from_polygon(max_supply)
        matched = 0
        for token_id, eth_owner in ethereum_owners.items():
            if polygon_owners.get(token_id) != eth_owner:
                print(f"Mismatch found for token {token_id}: Ethereum owner {eth_owner}, Polygon owner {polygon_owners.get(token_id)}")
            else:
                matched += 1
                print(f"Token {token_id} matches across networks.")

        print(f"Matched: {matched}/{max_supply}")


verifier = TokenOwnershipVerifier(polygon_rpc_url, polygon_contract_address, ethereum_json_path, abi)
verifier.compare_ownerships()