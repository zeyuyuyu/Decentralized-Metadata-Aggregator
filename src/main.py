import os
import json
from web3 import Web3
from typing import Dict, List

class MetadataAggregator:
    def __init__(self, ethereum_node_url: str):
        self.w3 = Web3(Web3.HTTPProvider(ethereum_node_url))
        self.contract_address = os.environ['METADATA_CONTRACT_ADDRESS']
        self.contract_abi = json.load(open('abi.json'))
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.contract_abi)

    def get_metadata(self, entity_id: str) -> Dict[str, str]:
        metadata = self.contract.functions.getMetadata(entity_id).call()
        return {
            'name': metadata[0],
            'description': metadata[1],
            'image': metadata[2],
            'attributes': metadata[3]
        }

    def set_metadata(self, entity_id: str, metadata: Dict[str, str]) -> None:
        tx = self.contract.functions.setMetadata(
            entity_id,
            metadata['name'],
            metadata['description'],
            metadata['image'],
            metadata['attributes']
        ).build_transaction({
            'from': self.w3.eth.account.from_key(os.environ['PRIVATE_KEY']).address,
            'gas': 200000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'nonce': self.w3.eth.getTransactionCount(
                self.w3.eth.account.from_key(os.environ['PRIVATE_KEY']).address)
        })
        signed_tx = self.w3.eth.account.signTransaction(tx)
        self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)

if __name__ == '__main__':
    aggregator = MetadataAggregator('https://mainnet.infura.io/v3/YOUR_PROJECT_ID')
    print(aggregator.get_metadata('0x123456789abcdef'))
    aggregator.set_metadata('0x123456789abcdef', {
        'name': 'My NFT',
        'description': 'This is my NFT',
        'image': 'ipfs://QmWWQSuPMS6aXCbZKpEjPHPUZN2NjB3YrhJTHsV4X3vb2t',
        'attributes': ['rare', 'unique']
    })