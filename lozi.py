lozi_next = lambda x, y, a=1.7, b=0.3: (1 - a * abs(x) + y, b * x)
genXY 	  = lambda key: (float(f"0.{key:020}"[:12]), float(f"0.{key:020}"[10:]))

def genKey(x, y, x_t, y_t):
	l = lambda x: int(f"{f"{x:.12f}".split('.')[-1][:10]:010}")
	return str(l(x)^l(x_t)) + str(l(y)^l(y_t))

def lozi_gen(key, delta = 1000):
	l = lambda x: str(x).split('.')[-1][0:10]
	while True:
		x, y = genXY(key)
		for i in range(delta//10):
			x, y = lozi_next(x, y)

		for i in range(delta):
			x, y = lozi_next(x, y)
			if i == delta//2:
				x_t, y_t = x, y
			yield int(l(x) + l(y))%2**64

		key = genKey(x, y, x_t, y_t)

	return None