from globals import *

class Board():

	def __init__(self):
		self.board = []
		for i in xrange(BSIZE):
			self.board.append([None]*BSIZE)
		
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				self.board[i][j] = 0
		
		self.tetrimo = []
		self.eq = None
		self.spawn = (BSIZE - 4)/2
		self.lineclears = 0
		
	def __getitem__(self, idx):
		return self.board[idx]
		
	def add_tetrimo(self, tetrimo):
		self.tetrimo.append(tetrimo)
		
	def move(self, dirc = None):
		for t in self.tetrimo:
			dir = t.direction
			if dirc is not None:
				dir = dirc
			ni = t.topleft[0] + dir[0]
			nj = t.topleft[1] + dir[1]
			if(ni >= 0 and nj >= 0 and ni+t.h <= BSIZE and nj+t.w <= BSIZE):
				valid = True
				for i in xrange(t.h):
					for j in xrange(t.w):
						if(t[i][j] and self[ni+i][nj+j]):
							valid = False
					if not valid: break
				if valid:
					t.topleft = (ni, nj)
				else:
					if dirc is None:	
						self.place(t)
						self.tetrimo.remove(t)
			else:
				if dirc is None:
					self.place(t)
					self.tetrimo.remove(t)
	
	def rotate_tetrimo_L(self):
		for t in self.tetrimo:
			t.rotateL()
			i = t.topleft[0]
			j = t.topleft[1]
			if not (i >= 0 and j >= 0 and i+t.h <= BSIZE and j+t.w <= BSIZE):
				t.rotateR()
				continue
			valid = True
			for ii in xrange(t.h):
				for jj in xrange(t.w):
					if(t[ii][jj] and self[i+ii][j+jj]):
						valid = False
			if not valid:
				t.rotateR()
				continue

	def rotate_tetrimo_R(self):
		for t in self.tetrimo:
			t.rotateR()
			i = t.topleft[0]
			j = t.topleft[1]
			if not (i >= 0 and j >= 0 and i+t.h <= BSIZE and j+t.w <= BSIZE):
				t.rotateL()
				continue
			valid = True
			for ii in xrange(t.h):
				for jj in xrange(t.w):
					if(t[ii][jj] and self[i+ii][j+jj]):
						valid = False
			if not valid:
				t.rotateL()
				continue

	def remove(self, t):
		self.tetrimo.remove(t)

	def drop(self):
		tet = self.tetrimo[0]
		while(tet == self.tetrimo[0]):
			self.move()
			
	def place(self, t):
		for i in xrange(t.h):
			for j in xrange(t.w):
				if(t[i][j]):
					self[t.topleft[0]+i][t.topleft[1]+j] = 1
		self.eq.next_tetrimo()
		self.line_clear()
	
	def is_over(self):
		for i in xrange(4):
			for j in xrange(4):
				if(self[self.spawn+i][self.spawn+j]):
					return True
		return False
	
	def line_clear(self):
		for i in xrange(((BSIZE-4)/2) - 1, -1, -1):
			lc = True
			for j in xrange(BSIZE):
				if not self[i][j]:
					lc = False
					break
			if lc:
				self.lineclears += 1
				for j in xrange(i, ((BSIZE-4)/2) - 1):
					for k in xrange(BSIZE):
						self[j][k] = self[j+1][k]
				for j in xrange(BSIZE):
					self[((BSIZE-4)/2)-1][j] = 0

		for i in xrange(((BSIZE-4)/2) - 1, -1, -1):
			lc = True
			for j in xrange(BSIZE):
				if not self[j][i]:
					lc = False
					break
			if lc:
				self.lineclears += 1
				for j in xrange(i, ((BSIZE-4)/2) - 1):
					for k in xrange(BSIZE):
						self[k][j] = self[k][j+1]
				for j in xrange(BSIZE):
					self[j][((BSIZE-4)/2)-1] = 0

		for i in xrange(((BSIZE+4)/2) , BSIZE):
			lc = True
			for j in xrange(BSIZE):
				if not self[i][j]:
					lc = False
					break
			if lc:
				self.lineclears += 1
				for j in xrange(i, ((BSIZE+4)/2) + 1, -1):
					for k in xrange(BSIZE):
						self[j][k] = self[j-1][k]
				for j in xrange(BSIZE):
					self[((BSIZE+4)/2)][j] = 0

		for i in xrange(((BSIZE+4)/2) , BSIZE):
			lc = True
			for j in xrange(BSIZE):
				if not self[j][i]:
					lc = False
					break
			if lc:
				self.lineclears += 1
				for j in xrange(i, ((BSIZE+4)/2) + 1, -1):
					for k in xrange(BSIZE):
						self[k][j] = self[k][j-1]
				for j in xrange(BSIZE):
					self[j][((BSIZE+4)/2)] = 0

	def rotateL(self):
		narr = []
		for i in xrange(BSIZE):
			narr.append([None]*BSIZE)
			
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				narr[i][j] = 0
		
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				narr[BSIZE-1-j][i] = self[i][j]
				
		self.board = narr
		
	def rotateR(self):
		narr = []
		for i in xrange(BSIZE):
			narr.append([None]*BSIZE)
			
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				narr[i][j] = 0
		
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				narr[j][BSIZE-1-i] = self[i][j]
				
		self.board = narr
		
class Tetrimo():

	def __init__(self, type, topleft, direction):
		self.layout = []
		for i in xrange(4):
			self.layout.append([None]*4)
		
		for i in xrange(4):
			for j in xrange(4):
				self.layout[i][j] = 0
				
		for i in xrange(4):
			self.layout[type[i][0]][type[i][1]] = 1
		
		self.w = type[4]
		self.h = type[5]
		self.color = type[6]
		self.topleft = topleft
		self.direction = direction

		self.ttype = type
		
	def rotateL(self):	#checking
		narr = []
		for i in xrange(4):
			narr.append([None]*4)
			
		for i in xrange(4):
			for j in xrange(4):
				narr[i][j] = 0
		
		for i in xrange(self.h):
			for j in xrange(self.w):
				narr[self.w-1-j][i] = self[i][j]
				
		self.layout = narr
		self.w, self.h = self.h, self.w
		
	def rotateR(self):	#checking
		narr = []
		for i in xrange(4):
			narr.append([None]*4)
			
		for i in xrange(4):
			for j in xrange(4):
				narr[i][j] = 0
		
		for i in xrange(self.h):
			for j in xrange(self.w):
				narr[j][self.h-1-i] = self[i][j]
				
		self.layout = narr
		self.w, self.h = self.h, self.w
		
	def __getitem__(self, idx):
		return self.layout[idx]