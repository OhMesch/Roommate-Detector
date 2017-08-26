class Roomates():
	def __init__(self,x):
		self.lastSeen = None
		self.mac = x

	def update(self,prevLine,currLine,currTime):
		self.justArr=False
		self.justLeft=False
		self.here = False

		if self.mac in prevLine and self.mac not in currLine:
			self.justLeft=True
		if self.mac in currLine:
			self.here=True
			self.lastSeen=currTime
			if self.mac not in prevLine:
				self.justArr=True

	def is_here(self):
		return(self.here)

	def last_seen(self):
		if self.lastSeen:
			return(self.lastSeen)

	def just_left(self):
		return(self.justLeft)

	def just_arrived(self):
		return(self.justArr)

	def get_mac(self):
		return(self.mac)