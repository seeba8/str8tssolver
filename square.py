class Square:	
	def __init__(self, i, b=False, value="123456789"):
		self.val = value
		self.x = i % 9
		self.y = i // 9
		self.black = b
			
	def is_number(self):
		return len(self.val) == 1
	
	def getx(self):
		return self.x
	
	def gety(self):
		return self.y
	
	def set_value(self, v):
		self.val = v
	
	def get_value(self):
		return self.val if len(self.val) == 1 else "0"
	
	def get_options(self):
		return self.val if len(self.val) > 1 else "0"
		
	def set_black(self):
		self.black = True
		
	def is_black(self):
		return self.black
		
	def remove_option(self, v):
		v = str(v)
		if len(self.val) == 1: 
			return False # Don't remove the last option as it would be an error
		b = (v in self.val)
		self.val = self.val.replace(v,"")
		return b
		
	def __str__(self):
		return "({}: {},{})".format(self.get_value() if self.is_number() else "", 
									self.getx(), self.gety())
