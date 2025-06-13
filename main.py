#!/bin/python3

import time
import threading
import random
import os
import multiprocessing

from sharedManager import SharedDataManager
from pthread import ThreadWorker
from mthread import MasterWorker

class ThreadManager:
	def __init__(self, states, secret):
		self.state_lock = threading.Lock()

		self.threads = {}
		self.states  = states
		self.master  = MasterWorker(secret)

	def spawn(self):
		# Get state value for new thread
		tid = f"T{len(self.threads)}"
		self.states[tid] = next(self.master)

		# Spin up thread
		worker = ThreadWorker(tid, self.states, self.state_lock)
		self.threads[tid] = worker
		worker.start()

		print(f"[+] Spawned Worker thread {tid}")
		return tid

	def sync(self, tid1, tid2):
		self.threads[tid2].gen = self.threads[tid1].gen
		print(f"[-] Sync threads {tid1} and {tid2}")

	def switch(self, tid1, tid2):
		self.threads[tid1].gen, self.threads[tid2].gen = self.threads[tid2].gen, self.threads[tid1].gen
		print(f"[-] Switched threads {tid1} and {tid2}")

	def kill(self, tid):
		if tid in self.threads:
			self.threads[tid].pause()
			self.threads[tid].join()
			with self.state_lock:
				del self.states[tid]
			del self.threads[tid]
			print(f"[-] Killed thread {tid}")

	def list_states(self):
		print(f"[-] {', '.join(self.threads.keys())}")

def cli_loop(manager):
	while True:
		cmd = input("cmd> ").strip().split()
		if not cmd:
			continue
		if cmd[0] == "spawn":
			manager.spawn()
		elif cmd[0] == "sync" and len(cmd) == 3:
			manager.sync(cmd[1], cmd[2])
		elif cmd[0] == "switch" and len(cmd) == 3:
			manager.switch(cmd[1], cmd[2])
		elif cmd[0] == "kill" and len(cmd) == 2:
			manager.kill(cmd[1])
		elif cmd[0] == "list":
			manager.list_states()
		elif cmd[0] == "exit":
			for tid in list(manager.threads.keys()):
				manager.kill(tid)
			break
		else:
			print("Commands: spawn | kill <id> | sync <id1> <id2> | switch <id1> <id2> | list | help | exit")

if __name__ == "__main__":
	with multiprocessing.Manager() as manager:

		# Init manager
		shared_data = manager.dict()
		secret 		= random.getrandbits(64)
		tmanager 	= ThreadManager(shared_data, secret)

		# Shared_data passing on to display.py
		SharedDataManager.register('get_data', callable=lambda: shared_data)
		m = SharedDataManager(address=('localhost', 50000), authkey=b'secret')
		server = m.get_server()

		threading.Thread(target=server.serve_forever, daemon=True).start()
		cli_loop(tmanager)

	server.shutdown()
	server.server_close()
