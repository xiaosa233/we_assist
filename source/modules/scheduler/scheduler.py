
import threading
import time
import scheduler_task

class scheduler:
	def __init__(self):
		self.run_thread = None
		self.task_pool = []
		self.mutex = threading.Lock()
		self.is_exit = False

	def enqueue_impl(self, task):
		if threading.current_thread() != self.run_thread :
			self.mutex.acquire()

		index = len( self.task_pool)-1
		while index >= 0 :
			if self.task_pool[index].response_time <= task.response_time:
				index -= 1
			else :
				break

		self.task_pool.insert(index+1, task)

		if threading.current_thread() != self.run_thread :
			self.mutex.release()

	def enqueue(self, response_time, func, args, repeate_num = 1, delta_time = 0.0):
		self.enqueue_impl(scheduler_task.schedule_task(response_time, func, args, repeate_num, delta_time))

	def start(self):
		if not self.run_thread :
			self.run_thread = threading.Thread(target=self.run)
			self.run_thread.start()

	def stop(self):
		self.is_exit = True
		self.run_thread.join(3)


	def run(self):
		while not self.is_exit:
			if len(self.task_pool) > 0:
				self.mutex.acquire()
				now_time = time.time()
				index = len(self.task_pool)-1
				next_equeue = []
				while index >= 0 and self.task_pool[index].tick(now_time) :
					b_end_this_task = self.task_pool[index].run()
					if not b_end_this_task :
						next_equeue.append(self.task_pool[index])
					index -= 1
					self.task_pool.pop()

				for task in next_equeue :
					index = len(self.task_pool) - 1
					while index >= 0:
						if self.task_pool[index].response_time <= task.response_time:
							index -= 1
						else:
							break
					self.task_pool.insert(index + 1, task)
				self.mutex.release()
			time.sleep(1)

	def close(self):
		self.stop()