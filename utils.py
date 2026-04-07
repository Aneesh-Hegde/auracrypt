import numpy as np
from speck import Speck32

def _pair_to_bits(c0, c1):
    diff_x, diff_y = c0[0] ^ c1[0], c0[1] ^ c1[1]
    words = np.array([c0[0], c0[1], c1[0], c1[1], diff_x, diff_y], dtype=np.uint16)
    return np.unpackbits(words.view(np.uint8)).astype(np.float32)

def generate_dataset(n_samples, rounds, diff=(0x0040, 0x0000)):
    half = n_samples // 2
    X, Y = [], []
    for i in range(half):
        key = np.random.randint(0, 2**63)
        cipher = Speck32(key=key)
        p0 = (np.random.randint(0, 0xFFFF), np.random.randint(0, 0xFFFF))
        p1 = (p0[0] ^ diff[0], p0[1] ^ diff[1])
        c0, c1 = cipher.encrypt(p0, rounds=rounds), cipher.encrypt(p1, rounds=rounds)
        X.append(_pair_to_bits(c0, c1)); Y.append(1.0)
        rd = (np.random.randint(0, 0xFFFF), np.random.randint(0, 0xFFFF))
        while rd == diff: rd = (np.random.randint(0, 0xFFFF), np.random.randint(0, 0xFFFF))
        q0 = (np.random.randint(0, 0xFFFF), np.random.randint(0, 0xFFFF))
        q1 = (q0[0] ^ rd[0], q0[1] ^ rd[1])
        d0, d1 = cipher.encrypt(q0, rounds=rounds), cipher.encrypt(q1, rounds=rounds)
        X.append(_pair_to_bits(d0, d1)); Y.append(0.0)
    return np.array(X, dtype=np.float32), np.array(Y, dtype=np.float32)
