import time
from z3 import BitVec, BitVecVal, RotateRight, RotateLeft, Solver, sat

def recover_key_with_z3(pairs, rounds):
    s = Solver()
    k = [BitVec(f"k_{i}", 16) for i in range(4)]
    rk, l = [k[0]], [k[1], k[2], k[3]]
    for i in range(rounds - 1):
        nl = (RotateRight(l[i], 7) + rk[i]) ^ i
        nk = RotateLeft(rk[-1], 2) ^ nl
        l.append(nl); rk.append(nk)

    for pt, ct in pairs:
        x, y = BitVecVal(pt[0], 16), BitVecVal(pt[1], 16)
        for i in range(rounds):
            x = (RotateRight(x, 7) + y) ^ rk[i]
            y = RotateLeft(y, 2) ^ x
        s.add(x == BitVecVal(ct[0], 16), y == BitVecVal(ct[1], 16))

    t0 = time.time()
    if s.check() == sat:
        m = s.model()
        words = [m.evaluate(k[i], model_completion=True).as_long() & 0xFFFF for i in range(4)]
        return hex(sum(words[i] << (i * 16) for i in range(4))), time.time() - t0
    return None, time.time() - t0
