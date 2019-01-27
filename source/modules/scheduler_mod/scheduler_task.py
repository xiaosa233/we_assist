
class schedule_task:
	def __init__(self, response_time, func, args, repeate_num = 1, delta_time = 0.0):
		self.func = func
		self.args = args
		self.response_time = response_time
		self.repeate_num = repeate_num
		self.delta_time = delta_time

	# True for end this task
	# False for continue to run rask
	def run(self):
		if self.args :
			self.func(self.args)
		else :
			self.func()
		b_end_this_task = False
		if self.repeate_num > 0 :
			self.repeate_num -= 1
			b_end_this_task =  self.repeate_num == 0
		elif self.repeate_num < 0 :
			b_end_this_task = False

		if not b_end_this_task :
			#update delta_time
			self.response_time += self.delta_time
		return b_end_this_task


	def tick(self, now_time):
		return self.response_time <= now_time