shapes = [ [(0, 0), (0, 1), (1, 0), (1, 1)],
           [(0, 0), (0, 1), (0, 2), (1, 1)],
           [(0, 0), (1, 0), (2, 0), (1, 1)],
           [(1, 0), (0, 1), (1, 1), (1, 2)],
           [(1, 0), (0, 1), (1, 1), (2, 1)],
#           #   ###  #   #
#           ##   #  ##  ###
#           #        #
           [(0, 0), (1, 0), (1, 1), (2, 1)],
           [(1, 0), (2, 0), (0, 1), (1, 1)],
           [(1, 0), (0, 1), (1, 1), (0, 2)],
           [(0, 0), (0, 1), (1, 1), (1, 2)],
#           ##   ##  #  # 
#            ## ##  ##  ##
#                   #    #
           [(0, 0), (1, 0), (1, 1), (1, 2)],
           [(2, 0), (0, 1), (1, 1), (2, 1)],
           [(0, 0), (0, 1), (0, 2), (1, 2)],
           [(0, 0), (1, 0), (2, 0), (0, 1)],
#           ##    # #   ###
#            #  ### #   # 
#            #      ##    
           [(0, 0), (1, 0), (0, 1), (0, 2)],
           [(0, 0), (1, 0), (2, 0), (2, 1)],
           [(1, 0), (1, 1), (0, 2), (1, 2)],
           [(0, 0), (0, 1), (1, 1), (2, 1)],
#           ##  ###  #  #  
#           #     #  #  ###
#           #       ##   
           [(0, 0), (0, 1), (0, 2), (0, 3)],
           [(0, 0), (1, 0), (2, 0), (3, 0)]
         ]

WIDTH = 10
HEIGHT = 5

blocks = []
for shape in shapes:
    maxi = max(i for i, j in shape)
    maxj = max(j for i, j in shape)
    for x in range(WIDTH-maxi):
        for y in range(HEIGHT-maxj):
            blocks.append([(x+i, y+j) for i, j in shape])

def prune(bloc, pos):
    return [shape for shape in bloc if pos in shape]

def colourmatch(cols):
    if "empty" in cols: return False
    if4 = ifr = ifg = ifb = ify = True
    if "red" in cols: ifg = ifb = ify = False
    if "green" in cols: ifr = ifb = ify = False
    if "blue" in cols: ifg = ifr = ify = False
    if "yellow" in cols: ifg = ifb = ifr = False
    if len(set(cols)-{"black"}) + cols.count("black") != 4: if4 = False
    return if4 or ifr or ifg or ifb or ify

class defaultlist(list):
    def __init__(self, *args, **kwargs):
        if "default" in kwargs:
            self.default = kwargs.pop("default")
        else:
            self.default = 0
        list.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        if key >= len(self):
            self.extend([self.default]*(key-len(self)+1))
        return list.__getitem__(self, key)

    def __setitem__(self, key, value):
        if key >= len(self):
            self.extend([self.default]*(key-len(self)+1))
        return list.__setitem__(self, key, value)
