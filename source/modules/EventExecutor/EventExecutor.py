
class EventExecutor:
	dispatch_funcs = []
	is_inited = False
	def __init__(self):
		EventExecutor.init_class()
		self.funcs = []
		self.result = None

	def add(self, func_obj):
		self.funcs.append(func_obj)

	def add_unique(self, func_obj):
		if( func_obj not in self.funcs) :
			self.funcs.append(func_obj)

	def get_result(self):
		return self.result

	def broadcast(self, *args):
		args_len = len(args)
		if args_len > 6 :
			args_len = 0
		return EventExecutor.dispatch_funcs[args_len](self.funcs, args)

	@staticmethod
	def dispatch_para0(funcs, args):
		result = None
		for func_obj in funcs :
			result = func_obj()
		return result

	@staticmethod
	def dispatch_para1(funcs, args):
		result = None
		for func_obj in funcs :
			result = func_obj(args[0])
		return result

	@staticmethod
	def dispatch_para2(funcs, args):
		result = None
		for func_obj in funcs :
			result = func_obj(args[0], args[1])
		return result

	@staticmethod
	def dispatch_para3(funcs, args):
		result = None
		for func_obj in funcs :
			result = func_obj(args[0], args[1], args[2])
		return result

	@staticmethod
	def dispatch_para4(funcs, args):
		result = None
		for func_obj in funcs :
			result = func_obj(args[0], args[1], args[2], args[3])
		return result

	@staticmethod
	def dispatch_para5(funcs, args):
		result = None
		for func_obj in funcs :
			result = func_obj(args[0], args[1], args[2], args[3], args[4])

		return result

	@staticmethod
	def dispatch_para6(funcs, args):
		result = None
		for func_obj in funcs :
			result = func_obj(args[0], args[1], args[2], args[3], args[4], args[5])
		return result

	@staticmethod
	def init_class():
		if not EventExecutor.is_inited :
			EventExecutor.is_inited = True
			EventExecutor.dispatch_funcs.append(EventExecutor.dispatch_para0)
			EventExecutor.dispatch_funcs.append(EventExecutor.dispatch_para1)
			EventExecutor.dispatch_funcs.append(EventExecutor.dispatch_para2)
			EventExecutor.dispatch_funcs.append(EventExecutor.dispatch_para3)
			EventExecutor.dispatch_funcs.append(EventExecutor.dispatch_para4)
			EventExecutor.dispatch_funcs.append(EventExecutor.dispatch_para5)
			EventExecutor.dispatch_funcs.append(EventExecutor.dispatch_para6)