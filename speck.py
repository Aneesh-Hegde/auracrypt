class Speck32:
    def __init__(self, key=0x1918111009080100):
        self.mask, self.word_size = 0xFFFF, 16
        self._expand_key(key)

    def _rr(self, x, r): return ((x >> r) | (x << (16 - r))) & 0xFFFF
    def _rl(self, x, r): return ((x << r) | (x >> (16 - r))) & 0xFFFF

    def _expand_key(self, key):
        k = [(key >> (i * 16)) & 0xFFFF for i in range(4)]
        self.round_keys, l = [k[0]], k[1:]
        for i in range(21):
            l_i = ((self._rr(l[i], 7) + self.round_keys[i]) & 0xFFFF) ^ i
            k_i = self._rl(self.round_keys[i], 2) ^ l_i
            l.append(l_i); self.round_keys.append(k_i)

    def encrypt(self, pt, rounds=22):
        x, y = pt
        for i in range(rounds):
            x = ((self._rr(x, 7) + y) & 0xFFFF) ^ self.round_keys[i]
            y = self._rl(y, 2) ^ x
        return x, y
