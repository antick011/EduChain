import hashlib
import json
import os
from datetime import datetime

# Path to store the chain
CHAIN_FILE = os.path.join(os.path.dirname(__file__), "cert_chain.json")

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Certificate info
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data, sort_keys=True)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

def load_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE, 'r') as f:
        return json.load(f)

def save_chain(chain):
    with open(CHAIN_FILE, 'w') as f:
        json.dump(chain, f, indent=2)

def get_last_block(chain):
    return chain[-1] if chain else None

def add_certificate(student_name, course_name, issue_date):
    chain = load_chain()
    index = len(chain)
    previous_hash = chain[-1]['hash'] if chain else "0"
    data = {
        "student": student_name,
        "course": course_name,
        "issued": issue_date
    }
    block = Block(index, str(datetime.now()), data, previous_hash)
    chain.append(block.to_dict())
    save_chain(chain)
    return block.hash  # return hash to be saved/shown to student

def verify_certificate(cert_hash):
    chain = load_chain()
    for block in chain:
        if block['hash'] == cert_hash:
            return True
    return False
