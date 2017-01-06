from square import Square
from street import Street
from colours import Colours

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
		if x < 0 or x >= 9 or y < 0 or y >= 9:
			raise NameError("OutOfBounds")
		try:
			return self.get_square(y*9+x)
		except:
			raise
		
	def get_square(self,i):
		if i >= 81 or i < 0:
			raise NameError("OutOfBounds") 
		else:
			return self.field[i]
	
	def get_squares(self):
		for f in self.field:
			yield f
	
	def get_filled_squares(self):
		for s in self.get_squares():
			if s.is_number():
				yield s
				
	def get_row(self, square):
		for i in range(9):
			yield self.get_squarexy(i, square.gety())
		
	def get_column(self, square):
		for i in range(9):
			yield self.get_squarexy(square.getx(),i)
			
	def get_hstreet(self,square):
		x = square.getx()
		y = square.gety()
		rfinished = lfinished = False
		street = Street(square)
		for i in range(1,10):
			if lfinished and rfinished: 
				break
			if not lfinished:
				try:
					if not self.get_squarexy(x-i,y).is_black():
						street.add(self.get_squarexy(x-i,y))
					else:
						lfinished = True
				except:
						lfinished = True
			if not rfinished:
				try:
					if not self.get_squarexy(x+i,y).is_black():
						street.add(self.get_squarexy(x+i,y))
					else:
						rfinished = True
				except:
					rfinished = True
		print("Square {} is in street of length {}".format(str(square),street.get_length()))
		return street
		
	def get_vstreet(self,square):
		x = square.getx()
		y = square.gety()
		ufinished = dfinished = False
		street = Street(square)
		for i in range(1,10):
			if ufinished and dfinished: 
				break
			if not ufinished:
				try:
					if not self.get_squarexy(x,y-1).is_black():
						street.add(self.get_squarexy(x,y-1))
					else:
						ufinished = True
				except:
						ufinished = True
			if not dfinished:
				try:
					if not self.get_squarexy(x,y+i).is_black():
						street.add(self.get_squarexy(x,y+i))
					else:
						dfinished = True
				except:
					dfinished = True
		print("Square {} is in street of length {}".format(str(square),street.get_length()))
		return street
	
	def eliminate_possibilities(self):
		for square in self.get_filled_squares():
			self.eliminate_rowcol(square)
			if not square.is_black():
				self.eliminate_streets(square) # redundancy because we check every street length(street) times
			
		#eliminate_vstreet(self, square)
	
	def eliminate_street(self,street, square):
		for s in street.get_squares():
			if s != square:
				for i in range(1,street.get_min_possible()):
					s.remove_option(i)
				for i in range(9,street.get_max_possible(), -1):
					s.remove_option(i)
	
	def eliminate_streets(self, square):
		v = square.get_value()
		self.eliminate_street(self.get_hstreet(square),square)
		self.eliminate_street(self.get_vstreet(square),square)
	
	def eliminate_rowcol(self,square):
		v = square.get_value()
		for s in self.get_row(square):
			if s != square:
				s.remove_option(v)
		for s in self.get_column(square):
			if s != square:
				s.remove_option(v)
				
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
