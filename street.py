from square import Square
class Street:
	def __init__(self, square):
		self.street = set()
		self.street.add(square)
	
	def add(self,square):
		self.street.add(square)
	
	def contains(self,square):
		return square in self.street
	
	def get_length(self):
		return len(self.street)
	
	def iter_filled(self):
		for s in self.iter_squares():
			if s.is_number():
				yield s
	
	def iter_squares(self):
		for s in self.street:
			yield s
			
	def get_options(self):
		o = set()
		for s in self.iter_squares():
			o = o | set(s.get_options())
		return o
	
	def gety(self):
		if self.get_length() == 1:
			for s in self.iter_squares():
				return s.gety()
		topleft = None
		for s in self.iter_squares():
			if topleft == None: 
				topleft = s
			else:
				if topleft.gety() == s.gety():
					return topleft.gety()
				else:
					raise NameError("NotHorizontal")
	
	def getx(self):
		if self.get_length() == 1:
			for s in self.iter_squares():
				return s.getx()
		topleft = None
		for s in self.iter_squares():
			if topleft == None: 
				topleft = s
			else:
				if topleft.getx() == s.getx():
					return topleft.getx()
				else:
					raise NameError("NotVertical")
	
	def is_vertical(self):
		if self.get_length() == 1:
			return True
		topleft = None
		for s in self.iter_squares():
			if topleft == None: 
				topleft = s
			else:
				return topleft.getx() == s.getx()
		return False
	
	def is_horizontal(self):
		if self.get_length() == 1:
			return True
		topleft = None
		for s in self.iter_squares():
			if topleft == None: 
				topleft = s
			else:
				return topleft.gety() == s.gety()
		return False
	
	def get_min(self):
		m = min(int(s.get_value()) if s.is_number() else 10 for s in self.street)
		return 0 if m == 10 else m
		
	def get_min_possible(self):
		if self.get_max() == 0:
			return 1
		else:
			return max(1,self.get_max()-self.get_length() + 1)
		
	def get_max(self):
		m = max(int(s.get_value()) if s.is_number() else 0 for s in self.street)
		return 10 if m == 0 else m
		
	def get_max_possible(self):
		if self.get_min() == 0:
			return 9
		else:
			return min(9,self.get_min() + self.get_length() - 1)
	
	def has_option(self, o, nothere):
		for s in self.iter_squares():
			if s != nothere and str(o) in s.get_options():
				return True
		return False
	
	
	def can_be_consecutive(self, s, o):
		minval = max(1, int(o)-self.get_length()+1)
		maxval = min(9,int(o)+self.get_length()-1)
		l = 1
		for i in range(1,self.get_length()):
			if not int(o)-i < minval and self.has_option(int(o)-i,s):
				l += 1
			if not int(o)+i > maxval and self.has_option(int(o)+i,s):
				l += 1
		return l >= self.get_length()
		
		
	def eliminate_nonconsec(self):
		if self.get_length() == 1:
			return
		for s in self.iter_squares():
			for o in s.iter_options():
				if not self.can_be_consecutive(s, o):
					s.remove_option(o)
			#eliminate nonconsecutives
			#max/min also for options
			
	def eliminate_street(self, square):
		for s in self.iter_squares():
			if s != square:
				for i in range(1,self.get_min_possible()):
					s.remove_option(i)
				for i in range(9,self.get_max_possible(), -1):
					try:
						s.remove_option(i)
					except:
						print(square)
						print("maxpos" + str(self.get_max_possible()))
						print("len" + str(self.get_length()))
						print("squares:")
						for s2 in self.iter_squares():
							print(str(s2))
						raise
			#eliminate nonconsecutives
			#max/min also for options		

	def __str__(self):
		topleft = None
		horizontal = False
		for s in self.iter_squares():
			if topleft == None or s.getx() < topleft.getx() or s.gety() < topleft.gety():
				topleft = s
			if topleft != None and s.getx() > topleft.getx():
				horizontal = True
		return "pos=({},{}), len={},{}".format(topleft.getx(), topleft.gety(), 
			len(self.street), "h" if horizontal else "v")
				