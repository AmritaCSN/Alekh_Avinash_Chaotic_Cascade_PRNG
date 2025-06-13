from lozi import lozi_gen

splitter = lambda s: [s[i:i+20] for i in range(0, len(s), 20)]

def joiner(parts):
    result = 0
    for part in parts:
        result ^= part
    return f"{result:020}"

def MasterWorker(secret):
    gen = [lozi_gen(i) for i in splitter(str(secret))]

    while True:
    	yield joiner([next(g) for g in gen])

    return None