import json
import requests
from _sha256 import sha256
from time import time
from typing import Optional
from urllib.parse import urlparse

FORGE_TRIGGER = 1


class Blockchain:
    def __init__(self):
        self.authority = None
        self.blocs = []
        self.peers = set()
        self.mempool = []

        self.forge(prev_hash='genesis', curr_hash=None)

    def forge(self, prev_hash: Optional[str], curr_hash: Optional[str]):
        # noinspection PyDictCreation
        if len(self.mempool) == 0:
            members = {
                'name': '',
                'firstname': '',
                'email': '',
                'rights': ''
            }
        else:
            members = {
                'name': self.mempool[0].get("content").get('name'),
                'firstname': self.mempool[0].get("content").get('firstname'),
                'email': self.mempool[0].get("content").get('email'),
                'rights': self.mempool[0].get("content").get('rights')
            }
        block = {
            'previous_hash': prev_hash or self.previous_block['current_hash'],
            'current_hash': '',
            'timestamp': int(time()),
            'members': members,
            'transactions': self.mempool[:]
        }
        print(block)
        block['current_hash'] = curr_hash or self.hash(block)

        self.blocs.append(block)
        print(self.blocs)

    def new_transaction(self, sender: str, content: dict):
        if self.authority is not None:
            requests.post(
                f'http://{self.authority}/transaction/create',
                json=content
            )
            return

        self.mempool.append({
            'sender': sender,
            'content': content
        })
        print(len(self.mempool))
        if len(self.mempool) == FORGE_TRIGGER:
            self.forge(prev_hash=None, curr_hash=None)
            self.mempool.clear()

    def register(self, address: str):
        parsed_url = urlparse(address)
        self.peers.add(parsed_url.path)

    def sync(self) -> bool:
        changed = False

        for peer in self.peers:
            r = requests.get(f'http://{peer}/')

            if r.status_code != 200:
                continue

            chain = r.json()['chain']
            if len(chain) > len(self.blocs):
                self.blocs = chain
                changed = True

        return changed

    def create_id(self, name, firstname, email):
        return self.forge(prev_hash=None, curr_hash=None)['members'].append({
            'lastname': name,
            'firstname': firstname,
            'email': email,
            'rights': []
        })

    def insert_rights(self, email, right):
        print(self.blocs)
        for p in range(len(self.blocs)):
            if self.blocs[p].get("members").get("email").lower() == email.lower():
                self.blocs[p].get("members").get("rights").append(right)
                break

    def delete_id(self, name, firstname, email):
        for p in self.forge(prev_hash=None, curr_hash=None)['members']:
            if self.forge(prev_hash=None, curr_hash=None)['members']['name'] == name & \
                    self.forge(prev_hash=None, curr_hash=None)['members']['firstname'] == firstname & \
                    self.forge(prev_hash=None, curr_hash=None)['members']['email'] == email:
                return self.forge(prev_hash=None, curr_hash=None)['members'].pop

    @property
    def previous_block(self) -> dict:
        return self.blocs[-1]

    @staticmethod
    def hash(block: dict):
        to_hash = json.dumps(block)
        return sha256(to_hash.encode()).hexdigest()

    def set_authority(self, address: str):
        self.authority = address
