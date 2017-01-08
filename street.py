class Street:
    def __init__(self, street):
        self.street = street
        self._y = self._gety()
        self._x = self._getx()
        self._h = self._is_horizontal()
        self._v = self._is_vertical()

    def __contains__(self,s):
        return s in self.street

    def __len__(self):
        return len(self.street)
    
    def __iter__(self):
        for s in self.street:
            yield s

    def get_options(self):
        o = set()
        for s in self:
            o = o | set(s.get_options())
        return o

    @property
    def y(self):
        return self._y
        
    @property
    def x(self):
        return self._x
    
    @property
    def is_horizontal(self):
        return self._h
    
    @property
    def is_vertical(self):
        return self._v
        
    def _gety(self):
        if len(self) == 1:
            return next(iter(self)).y
        topleft = None
        for s in self:
            if topleft == None:
                topleft = s
            else:
                if topleft.y == s.y:
                    return topleft.y
                else:
                    if topleft.y > s.y:
                        topleft = s
                   
    def _getx(self):
        if len(self) == 1:
            return next(iter(self)).x
        topleft = None
        for s in self:
            if topleft == None:
                topleft = s
            else:
                if topleft.x == s.x:
                    return topleft.x
                else:
                    if topleft.x > s.x:
                        topleft = s

    def _is_vertical(self):
        if len(self) == 1:
            return True
        topleft = None
        for s in self:
            if topleft == None:
                topleft = s
            else:
                return topleft.x == s.x
        return False

    def _is_horizontal(self):
        if len(self) == 1:
            return True
        topleft = None
        for s in self:
            if topleft == None:
                topleft = s
            else:
                return topleft.y == s.y
        return False

    def get_min(self):
        m = min(int(s.get_value()) if s.is_number() else 10 for s in self.street)
        return 0 if m == 10 else m

    def get_min_possible(self):
        if self.get_max() == 0:
            return 1
        else:
            return max(1, self.get_max() - len(self) + 1)

    def get_max(self):
        m = max(int(s.get_value()) if s.is_number() else 0 for s in self.street)
        return 10 if m == 0 else m

    def get_max_possible(self):
        if self.get_min() == 0:
            return 9
        else:
            return min(9, self.get_min() + len(self) - 1)

    def has_option(self, o, nothere):
        for s in self:
            if s != nothere and str(o) in s.get_options():
                return True
        return False

    def can_be_consecutive(self, s, o):
        minval = max(1, int(o) - len(self) + 1)
        maxval = min(9, int(o) + len(self) - 1)
        l = 1
        for i in range(1, len(self)):
            if not int(o) - i < minval and self.has_option(int(o) - i, s):
                l += 1
            if not int(o) + i > maxval and self.has_option(int(o) + i, s):
                l += 1
        return l >= len(self)

    def eliminate_nonconsec(self):
        if len(self) == 1:
            return
        for s in self:
            for o in s.iter_options():
                if not self.can_be_consecutive(s, o):
                    s.remove_option(o)
                # eliminate nonconsecutives
                # max/min also for options

    def eliminate_out_of_range(self, square):
        for s in self:
            if s != square:
                for i in range(1, self.get_min_possible()):
                    s.remove_option(i)
                for i in range(9, self.get_max_possible(), -1):
                    s.remove_option(i)
                   

    def __str__(self):
        topleft = None
        horizontal = False
        for s in self:
            if topleft == None or s.x < topleft.x or s.y < topleft.y:
                topleft = s
            if topleft != None and s.x > topleft.x:
                horizontal = True
        return "pos=({},{}), len={},{}".format(topleft.x, topleft.y,
                                               len(self.street), "h" if horizontal else "v")
