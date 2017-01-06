class Colours:
	'''
	For colours, see e.g. http://ascii-table.com/ansi-escape-sequences.php
	'''
	BB = '\033[40m'
	WB = '\033[47m'
	GB = '\033[42m'
	WHITE = '\033[37m'
	BLACK = '\033[30m'
	GREEN = '\033[32m'

class Field:
	def __init__(self, preset=0):
		if preset == 1:
			# The Daily Str8ts, #2971, by Andrew Stuart (http://www.str8ts.com)
			blacks = "100110001000100000001001100100010000100000001000010001001100100000001000100011001"
			values = "600070010007000003780000100000000021000090000100480500009000006000040000000000005"
			self.field = [Square(i, blacks[i] == "1", "123456789" if values[i] == "0" else values[i]) for i in range(81)]
		else:
			self.field = [Square(i) for i in range(81)]
	
	def get_squarexy(self, x, y):
		return self.get_square(y*9+x)
		
	def get_square(self,i):
		return self.field[i]
	
	def eliminate_possibilities(self):
		for square in self.field:
			eliminate_row(self, square)
			eliminate_column(self, square)
			eliminate_hstreet(self, square)
			eliminate_vstreet(self, square)
				
	def oldprint(self):
		s = Colours.GREEN
		for i in range(81):
			if i % 9 == 0:
				s += "\n"
			if self.get_square(i).is_black():
				if not self.get_square(i).is_number():
					s += "\u2588"
				else: 
					s += (Colours.GB + Colours.BLACK + self.get_square(i).get_value() 
							+ Colours.BB + Colours.GREEN)
			else:
				if self.get_square(i).is_number():
					s += self.get_square(i).get_value()
				else:
					s += " "
			s += "|"
		return s
	
	def show(self):
		s = Colours.GREEN
		sa = []
		for i in range(81):
			if i % 9 == 0:
				s += "\n".join(sa) + "\n"
				s += "+-------"*9 + "+\n"
				sa = ["|  ","|  ","|  "]
			if self.get_square(i).is_black():
				if not self.get_square(i).is_number():
					sa = [sa[i] + "\u2588\u2588\u2588" for i in range(3)]
				else: 
					sa[0] += "\u2588\u2588\u2588"
					sa[1] += ("\u2588" + Colours.GB + Colours.BLACK + self.get_square(i).get_value() 
							+ Colours.BB + Colours.GREEN+ "\u2588")
					sa[2] += "\u2588\u2588\u2588"
			else:
				if self.get_square(i).is_number():
					sa[0] += "   "
					sa[1] += " " + self.get_square(i).get_value() + " "
					sa[2] += "   "
				else:
					sa = [sa[i] + "   " for i in range(3)]
			sa = [sa[i] + "  |  " for i in range(3)]
		s += "\n".join(sa) +"\n" + "+-------"*9 + "+"
		print(s)
		return s
		
	def __str__(self):
		s = Colours.GREEN
		sa = []
		for i in range(81):
			if i % 9 == 0:
				s += "\n".join(sa) + "\n"
				s += "+-------"*9 + "+\n"
				sa = ["|  ","|  ","|  "]
			if self.get_square(i).is_black():
				if not self.get_square(i).is_number():
					sa = [sa[i] + "\u2588\u2588\u2588" for i in range(3)]
				else: 
					sa[0] += "\u2588\u2588\u2588"
					sa[1] += ("\u2588" + Colours.GB + Colours.BLACK + self.get_square(i).get_value() 
							+ Colours.BB + Colours.GREEN+ "\u2588")
					sa[2] += "\u2588\u2588\u2588"
			else:
				if self.get_square(i).is_number():
					sa[0] += "   "
					sa[1] += " " + self.get_square(i).get_value() + " "
					sa[2] += "   "
				else:
					sa = [sa[i] + "   " for i in range(3)]
			sa = [sa[i] + "  |  " for i in range(3)]
		s += "\n".join(sa) +"\n" + "+-------"*9 + "+"
		return s
	
	def show_hints(self):
		s = Colours.GREEN
		sa = []
		for i in range(81):
			if i % 9 == 0:
				s += "\n".join(sa) + "\n"
				s += "+-------"*9 + "+\n"
				sa = ["|  ","|  ","|  "]
			if self.get_square(i).is_black():
				if not self.get_square(i).is_number():
					sa = [sa[i] + "\u2588\u2588\u2588" for i in range(3)]
				else: 
					sa[0] += "\u2588\u2588\u2588"
					sa[1] += ("\u2588" + Colours.GB + Colours.BLACK + self.get_square(i).get_value() 
							+ Colours.BB + Colours.GREEN+ "\u2588")
					sa[2] += "\u2588\u2588\u2588"
			else:
				if self.get_square(i).is_number():
					sa[0] += "   "
					sa[1] += " " + self.get_square(i).get_value() + " "
					sa[2] += "   "
				else:
					o = self.get_square(i).get_options()
					options = "".join([str(i) if str(i) in o else " " for i in range(1,10) ])
					sa = [sa[i] + options[3*i:3*(i+1)] for i in range(3)]
			sa = [sa[i] + "  |  " for i in range(3)]
		s += "\n".join(sa) +"\n" + "+-------"*9 + "+"
		print(s)
		return s
				
			
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
		if len(self.val) == 1: 
			return False # Don't remove the last option as it would be an error
		b = (v in self.val)
		self.val = self.val.replace(v,"")
		return b
	
def main():
	f = Field(1)
	f.show()
	f.show_hints()


if __name__ == "__main__":
	main()