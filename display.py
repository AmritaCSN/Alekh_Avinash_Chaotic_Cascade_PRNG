#!/bin/python

import time
import os

from sharedManager import SharedDataManager

def display(data):
	os.system("clear")
	headers = []
	values = []

	for tid in sorted(data.keys()):
		headers.append(tid.center(22))
		values.append(str(data[tid]).center(22))

	print("".join(headers))
	print("".join(values))
	print("\nPress Ctrl+C to quit.")

if __name__ == "__main__":
	SharedDataManager.register('get_data')
	manager = SharedDataManager(address=('localhost', 50000), authkey=b'secret')
	manager.connect()
	shared_data = manager.get_data()

	try:
		while True:
			display(shared_data.copy())
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("Exiting dashboard.")
