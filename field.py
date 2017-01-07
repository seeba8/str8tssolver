from square import Square
from street import Street
from colours import Colours


class Field:
    def __init__(self, test=None):
        self.streets = set()
        if test != None:
            blacks = test["blacks"]
            values = test["values"]
            self.field = [Square(i, blacks[i] == "1", "123456789" if values[i] == "0" else values[i]) for i in
                          range(81)]
        else:
            self.field = [Square(i) for i in range(81)]

    def collect_streets(self):
        for square in self.get_squares():
            if not square.is_black():
                s = self.get_hstreet(square)
                if s != None:
                    self.streets.add(s)
                s = self.get_vstreet(square)
                if s != None:
                    self.streets.add(s)

    def iter_streets(self):
        for s in self.streets:
            yield s

    def get_squarexy(self, x, y):
        if x < 0 or x >= 9 or y < 0 or y >= 9:
            raise NameError("OutOfBounds")
        try:
            return self.get_square(y * 9 + x)
        except:
            raise

    def get_square(self, i):
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

    def get_row(self, square, without_square=False):
        for i in range(9):
            s = self.get_squarexy(i, square.y)
            if not without_square or s != square:
                yield s

    def get_column(self, square, without_square=False):
        for i in range(9):
            s = self.get_squarexy(square.x, i)
            if not without_square or s != square:
                yield s

    def get_hstreet(self, square):
        x = square.x
        y = square.y
        street = {square}
        if x - 1 >= 0 and not self.get_squarexy(x - 1, y).is_black():
            return None
        for i in range(1, 10):
            try:
                if not self.get_squarexy(x + i, y).is_black():
                    street.add(self.get_squarexy(x + i, y))
                else:
                    return Street(street)
            except:
                return Street(street)
        # print("Square {} is in street of length {}".format(str(square),len(street)))
        return Street(street)

    def get_vstreet(self, square):
        x = square.x
        y = square.y
        street = {square}
        if y - 1 >= 0 and not self.get_squarexy(x, y - 1).is_black():
            return None
        for i in range(1, 10):
            try:
                if not self.get_squarexy(x, y + i).is_black():
                    street.add(self.get_squarexy(x, y + i))
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
                if not self.get_squarexy(x, y) in street:
                    yield self.get_squarexy(x, y)
        else:
            x = street.x
            for y in range(9):
                if not self.get_squarexy(x, y) in street:
                    yield self.get_squarexy(x, y)

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
        for square in self.get_filled_squares():
            self.eliminate_rowcol(square)
        for street in self.iter_streets():
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
  
    def construct_output(self, show_hints=False):
        s = ""
        sa = []
        for i in range(81):
            if i % 9 == 0:
                s += "\n".join(sa) + "\n"
                s += "+-------" * 9 + "+\n"
                sa = ["|  ", "|  ", "|  "]
            if self.get_square(i).is_black():
                if not self.get_square(i).is_number():
                    sa = [sa[i] + "\u2588\u2588\u2588" for i in range(3)]
                else:
                    sa[0] += "\u2588\u2588\u2588"
                    sa[1] += ("\u2588" + self.get_square(i).get_value() + "\u2588")
                    sa[2] += "\u2588\u2588\u2588"
            else:
                if self.get_square(i).is_number():
                    sa[0] += "   "
                    sa[1] += " " + self.get_square(i).get_value() + " "
                    sa[2] += "   "
                else:
                    if show_hints:
                        o = self.get_square(i).get_options()
                        options = "".join([str(i) if str(i) in o else " " for i in range(1, 10)])
                        sa = [sa[i] + options[3 * i:3 * (i + 1)] for i in range(3)]
                    else:
                        sa = [sa[i] + "   " for i in range(3)]
            sa = [sa[i] + "  |  " for i in range(3)]
        s += "\n".join(sa) + "\n" + "+-------" * 9 + "+"
        return s

    def __str__(self):
        return self.construct_output()

    def show(self):
        print(str(self))
        return str(self)    
    
    def show_hints(self):
        s = self.construct_output(True)
        print(s)
        return s

    def get_total_length(self):
        return len("".join(s.get_options() for s in self.get_squares()))
