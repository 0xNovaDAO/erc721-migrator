from web3 import Web3
import json
import concurrent.futures

rpc_url = ""
contract_address = Web3.to_checksum_address("0x3B14d194c8CF46402beB9820dc218A15e7B0A38f")

abi = [
    {
        "constant": True,
        "inputs": [{"name": "_tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "payable": False,
        "type": "function",
    },
]

web3 = Web3(Web3.HTTPProvider(rpc_url))
contract = web3.eth.contract(address=contract_address, abi=abi)
max_supply = 6765

def get_owner(token_id):
    print(f"grabbing token at ID {token_id}")
    return token_id, contract.functions.ownerOf(token_id).call()

owners_list = []
with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    futures = [executor.submit(get_owner, token_id) for token_id in range(max_supply)]
    for future in concurrent.futures.as_completed(futures):
        owners_list.append(future.result())

owners_list.sort(key=lambda x: x[0])

address_to_replace = "0x754bbb703EEada12A6988c0e548306299A263a08"
new_address1 = "0xa9cC3AE2618B3a2Ec779FF288D87afaB3dc20A5A"
new_address2 = "0x123D26A886b4080e3b5B43d6f1025AB39F1C5414"

replace_count1 = 700
replace_count2 = 600

for i in range(len(owners_list)):
    token_id, owner = owners_list[i]
    if owner.lower() == address_to_replace.lower():
        if replace_count1 > 0:
            owners_list[i] = (token_id, new_address1)
            replace_count1 -= 1
        elif replace_count2 > 0:
            owners_list[i] = (token_id, new_address2)
            replace_count2 -= 1

token_owners = {str(token_id): owner for token_id, owner in owners_list}

with open('token_owners.json', 'w') as json_file:
    json.dump(token_owners, json_file, indent=4)

with open('token_owners.txt', 'w') as txt_file:
    for i in range(0, len(owners_list), 200):
        chunk = [owner for _, owner in owners_list[i:i + 200]]
        txt_file.write(json.dumps(chunk) + "\n\n")
