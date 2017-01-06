from square import Square
class Street:
	def __init__(self, square):
		self.street = set()
		self.street.add(square)
	
	def add(self,square):
		self.street.add(square)
	
	def get_length(self):
		return len(self.street)
		
	def get_squares(self):
		for s in self.street:
			yield s
	
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
		