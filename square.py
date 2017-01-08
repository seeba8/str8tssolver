class Square:
    def __init__(self, i, b=False, value="123456789"):
        self.val = value
        self._x = i % 9
        self._y = i // 9
        self._is_black = b
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def is_black(self):
        return self._is_black
    
    def is_number(self):
        return len(self.val) == 1

    # def __int__(self):
        # if self.is_number(): 
            # return int(self.val)
        # else:
            # raise NameError("Not found yet")
    
    def get_value(self):
        if len(self.val) == 1:
            return self.val
        raise NameError("NotAValue")

    def get_options(self):
        return self.val

    def iter_options(self):
        for o in self.val:
            yield o

    def remove_option(self, v):
        if self.is_black:
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
