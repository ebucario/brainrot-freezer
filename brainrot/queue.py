"""contains task queue and tools to enqueue and consume"""

import queue
from dataclasses import dataclass, field
from typing import Any

# convention: items are (priority, callable)
# p0 is critical
# p100 is UI (e.g. button actions)
# p200 is background (e.g. loading sounds)
def enqueue(priority, task):
	_queue.put(Task(priority, task))

@dataclass(order=True)
class Task:
	priority: int
	task: Any=field(compare=False)
	
_queue = queue.PriorityQueue()

def spin():
	while True:
		t = _queue.get()
		t.task()
		_queue.task_done()