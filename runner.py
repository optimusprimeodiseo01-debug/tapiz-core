import math
from web3 import Web3
import json
import time

# ===== CONFIG =====
RPC_URL = "https://sepolia.infura.io/v3/TU_API_KEY"
PRIVATE_KEY = "TU_PRIVATE_KEY"
ADDRESS = "TU_DIRECCION"

CONTRACT_ADDRESS = "0x..."
ABI_PATH = "TapizABI.json"

# ===== PRIMOS =====
def primes(n):
    ps = []
    x = 2
    while len(ps) < n:
        for p in ps:
            if x % p == 0:
                break
        else:
            ps.append(x)
        x += 1
    return ps

# ===== MATRICES =====
def build_T(n):
    p = primes(n)
    return [[math.log(p[i]) + math.log(p[j]) for j in range(n)] for i in range(n)]

def transpose(M):
    return list(map(list, zip(*M)))

def subtract(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def multiply_i(M):
    n = len(M)
    return [[1j * M[i][j] for j in range(n)] for i in range(n)]

def norm(M):
    return sum(abs(x)**2 for row in M for x in row) ** 0.5

# ===== BLOCKCHAIN =====
def load_contract(w3):
    with open(ABI_PATH) as f:
        abi = json.load(f)
    return w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def send_norm(w3, contract, value):
    nonce = w3.eth.get_transaction_count(ADDRESS)

    tx = contract.functions.update(int(value)).build_transaction({
        "from": ADDRESS,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei")
    })

    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)

    print("TX:", tx_hash.hex())

# ===== LOOP PRINCIPAL =====
def main():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = load_contract(w3)

    n = 6

    while True:
        T = build_T(n)
        H = T
        K = subtract(H, transpose(H))
        L = multiply_i(K)

        k_norm = norm(K)

        print("\n--- TAPIZ ---")
        print("||K|| =", k_norm)

        if k_norm != 0:
            send_norm(w3, contract, k_norm)

        time.sleep(30)

if __name__ == "__main__":
    main()
