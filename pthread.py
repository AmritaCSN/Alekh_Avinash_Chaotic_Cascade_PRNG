from threading import Thread
import time, tqdm

from lozi import lozi_gen

class ThreadWorker(Thread):
	def __init__(self, tid, state, lock, tk = 0.1):
		super().__init__()
		self.tid 	= tid
		self.state 	= state
		self.gen = lozi_gen(state[tid])
		self.tk = tk
		self.running = True

	def run(self):
		while self.running:
			self.state[self.tid] = next(self.gen)

			# Simulated delay
			time.sleep(self.tk)

	def pause(self):
		self.running = False

	def unpause(self):
		self.running = True