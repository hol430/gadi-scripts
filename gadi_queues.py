
QUEUE_NORMAL = "normal"

class Queue:
	"""
	Queue properties.

	@param name: Name of the queue.
	@param cpus_per_node: Number of CPUs per node in the queue.
	@param mem_per_node: Amount of memory (GiB) per node in the queue.
	@param charge_rate: Charge rate per resource hour.
	@param walltime_limits: List of pairs of (walltime limit in hours, ncpu) which gives a walltime limit for the given number of CPUs.
	"""
	def __init__(self, name: str, charge_rate: float, cpus_per_node: int
	      , mem_per_node: int, walltime_limits: list[tuple[int, int]]):
		self.name = name
		self.cpus_per_node = cpus_per_node
		self.mem_per_node = mem_per_node
		self._walltime_limits = walltime_limits
		self.charge_rate = charge_rate

	def get_walltime_limit(self, ncpu: int):
		"""
		Get the maximum walltime allowed for a job in this queue with the given
		number of CPUs.

		@param ncpu: Number of CPUs used by the hypothetical job.
		"""
		max: int = 0
		for (walltime_limit, cpu_count) in self._walltime_limits:
			if ncpu <= cpu_count:
				return walltime_limit
			max = cpu_count
		raise ValueError(f"CPU count of {ncpu} exceeds the maximum {max} in queue {self.name}")

_queues = [
	Queue(QUEUE_NORMAL, 2, 48, 192, [(48, 672), (24, 1440), (10, 2976), (5, 20736)]),
	Queue("express", 6, 48, 192, [(24, 48), (5, 3168)]),
	Queue("hugemem", 3, 48, 1470, [(48, 48), (24, 96), (5, 192)]),
	Queue("megamem", 5, 48, 2990, [(48, 48), (24, 96)]),
	Queue("gpuvolta", 3, 12, 382, [(48, 96), (24, 192), (5, 960)]),
	Queue("normalbw", 1.25, 28, 256, [(48, 336), (24, 840), (10, 1736), (5, 10080)]),
	Queue("expressbw", 3.75, 28, 256, [(24, 280), (5, 1848)]),
	Queue("normalsl", 1.5, 32, 192, [(48, 288), (24, 608), (10, 1984), (5, 3200)]),
	Queue("hugemembw", 1.25, 28, 1020, [(48, 28), (12, 140)]),
	Queue("megamembw", 1.25, 64, 3000, [(48, 32), (12, 64)]),
	Queue("copyq", 2, 1, 192, [(1, 10)]),
	Queue("dgxa100", 4.5, 16, 2000, [(48, 128), (5, 256)]),
	Queue("normalsr", 2, 104, 500, [(48, 1040), (24, 2080), (10, 4160), (5, 10400)]),
	Queue("expresssr", 6, 104, 500, [(24, 1040), (5, 2080)]),
]

def get_queue(name: str) -> Queue:
	"""
	Get the queue with the given name. Throw if not found.
	"""
	for queue in _queues:
		if queue.name == name:
			return queue
	raise ValueError(f"Unknown queue: '{name}'")
