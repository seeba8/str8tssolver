from square import Square
from street import Street
from colours import Colours


class Field:
    def __init__(self, test=None):
        self.streets = set()
        if test != None:
            blacks = test["blacks"]
            values = test["values"]
            self.squares = [Square(i, blacks[i] == "1", "123456789" if values[i] == "0" else values[i]) for i in
                          range(81)]
            self.collect_streets()
        else:
            self.squares = [Square(i) for i in range(81)]
    
    def solve(self):
        last_perf = 0
        current_perf = 1
        while (last_perf != current_perf):
            last_perf = self.get_total_length()
            self.eliminate_possibilities()
            current_perf = self.get_total_length()
            if self.is_solved():
                return True
        return False
    
    def is_solved(self):
        for s in self:
            if not s.is_number() and not s.is_black:
                return False
        return True
    
    def collect_streets(self):
        for square in self:
            if not square.is_black:
                s = self.get_hstreet(square)
                if s != None:
                    self.streets.add(s)
                s = self.get_vstreet(square)
                if s != None:
                    self.streets.add(s)

    def __getitem__(self,i):
        if isinstance(i,tuple):
            x,y = i
            if x < 0 or x >= 9 or y < 0 or y >= 9:
                raise IndexError
            i = y * 9 + x
        try:
            return self.squares[i]
        except:
            raise
    
    def __iter__(self):
        for s in self.squares:
            yield s

    def get_row(self, square, without_square=False):
        for i in range(9):
            s = self[i, square.y]
            if not without_square or s != square:
                yield s

    def get_column(self, square, without_square=False):
        for i in range(9):
            s = self[square.x, i]
            if not without_square or s != square:
                yield s

    def get_hstreet(self, square):
        x = square.x
        y = square.y
        street = {square}
        if x - 1 >= 0 and not self[x - 1, y].is_black:
            return None
        for i in range(1, 10):
            try:
                if not self[x + i, y].is_black:
                    street.add(self[x + i, y])
                else:
                    return Street(street)
            except IndexError:
                return Street(street)
        # print("Square {} is in street of length {}".format(str(square),len(street)))
        return Street(street)

    def get_vstreet(self, square):
        x = square.x
        y = square.y
        street = {square}
        if y - 1 >= 0 and not self[x, y - 1].is_black:
            return None
        for i in range(1, 10):
            try:
                if not self[x, y + i].is_black:
                    street.add(self[x, y + i])
                else:
                    return Street(street)
            except:
                return Street(street)
        # print("Square {} is in street of length {}".format(str(square),len(street)))
        return Street(street)

    def get_rest_without_street(self, street):
        if street.is_horizontal:
            y = street.y
            for x in range(9):
                if not self[x, y] in street:
                    yield self[x, y]
        else:
            x = street.x
            for y in range(9):
                if not self[x, y] in street:
                    yield self[x, y]

    def remove_street_options_from_rest(self, street):
        street_options = street.get_options()
        if len(street_options) < 9 and len(street_options) < len(street) * 2:
            removables = ("".join(sorted(street_options))[len(street_options) -
                                                          len(street):len(street)])
            streetsum = ""
            for o in removables:
                streetsum = ""
                for s in self.get_rest_without_street(street):
                    streetsum += str(s)
                    s.remove_option(o)

    def eliminate_possibilities(self):
        for square in self:
            if square.is_number():
                self.eliminate_rowcol(square)
        for street in self.streets:
            street.eliminate_nonconsec()
            self.remove_street_options_from_rest(street)
            for square in street:
                if square.is_number():
                    street.eliminate_out_of_range(square)

    def eliminate_rowcol(self, square):
        v = square.get_value()
        for s in self.get_row(square,True):
            s.remove_option(v)
        for s in self.get_column(square,True):
            s.remove_option(v)
  
    def _construct_output(self, show_hints=False):
        rowsep = "+-------" * 9 + "+\n"
        rowstart = ["|  "]*3
        output = rowsep
        sa = rowstart
        for i in range(81):
            s = self[i]
            placeholder = "\u2588" if s.is_black else " " 
            if s.is_number():
                sa = [sa[r] + placeholder + (s.get_value() if r == 1 else placeholder) 
                        + placeholder for r in range(3)]
            else:
                if show_hints and not s.is_black:
                    o = self[i].get_options()
                    options = "".join([str(r) if str(r) in o else placeholder for r in range(1, 10)])
                    sa = [sa[r] + options[3 * r:3 * (r + 1)] for r in range(3)]
                else:
                    sa = [sa[r] + placeholder*3 for r in range(3)]
            
            sa = [sa[r] + "  |  " for r in range(3)]
            if (i+1) % 9 == 0:
                output += "\n".join(sa) + "\n"
                output += rowsep
                sa = rowstart
        return output[:-1]

    def __str__(self):
        return self._construct_output()

    def show(self):
        print(str(self))
        return str(self)    
    
    def show_hints(self):
        s = self._construct_output(True)
        print(s)
        return s

    def get_total_length(self):
        return len("".join(s.get_options() for s in self))
