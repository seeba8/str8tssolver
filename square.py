class Square:
    def __init__(self, i, b=False, value="123456789"):
        self.val = value
        self._x = i % 9
        self._y = i // 9
        self.black = b
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def is_number(self):
        return len(self.val) == 1

    #def getx(self):
        #return self.x

    #def gety(self):
        #return self.y

    def set_value(self, v):
        if self.is_black():
            raise Exception
        self.val = v

    def get_value(self):
        return self.val if len(self.val) == 1 else "0"

    def get_options(self):
        return self.val

    def iter_options(self):
        for o in self.val:
            yield o

    def set_black(self):
        self.black = True

    def is_black(self):
        return self.black

    def remove_option(self, v):
        if self.is_black():
            return False
        v = str(v)
        if len(self.val) == 1:
            return False  # Don't remove the last option as it would be an error
        b = (v in self.val)
        self.val = self.val.replace(v, "")
        return b

    def __str__(self):
        return "({}: {},{})".format(self.get_value() if self.is_number() else " ",
                                    self.x, self.y)
