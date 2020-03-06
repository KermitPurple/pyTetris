from coord import coord

class peice:
    peices = [
	[
		".I..",
		".I..",
		".I..",
		".I..",
	],
	[
		".S..",
		".SS.",
		"..S.",
		"....",
	],
	[
		"..Z.",
		".ZZ.",
		".Z..",
		"....",
	],
	[
		"..T.",
		".TT.",
		"..T.",
		"....",
	],
	[
		"....",
		".OO.",
		".OO.",
		"....",
	],
	[
		".L..",
		".L..",
		".LL.",
		"....",
	],
	[
		"..J.",
		"..J.",
		".JJ.",
		"....",
	],
        ]
    def __init__(self, pos=coord(0,0), scl=10):
        self.pos = pos
        self.peice = [
                "....",
                "....",
                "....",
                "....",
                ]

    def realpos(self):
        return coord(pos.x*scl, pos.y*scl)
