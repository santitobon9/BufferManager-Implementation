from page import page
from frame import frame
from dm import diskManager

class BufferPoolFullError(Exception):
	#exception used in the Clock class
	def __init__(self, message):
		self.message = message

class clock:
	def __init__(self):
		# do the required initializations
		self.current = 0
		pass

	def pickVictim(self,buffer):
		victim = -1
		lock = False
		current = self.current
		while(current < len(buffer)) : 
			if (buffer[current].pinCount == 0) : 
				if (lock == False) :
					# pickup the first victim then lock it.
					victim = buffer[current].frameNumber
					lock = True
					self.current = current
				buffer[current].referenced = 0
			current += 1
		return victim
		

		
		
		
#==================================================================================================
		
class bufferManager:
	
	def __init__(self,size):
		self.buffer = []
		self.clk = clock()
		self.dm = diskManager()
		for i in range(size):
			self.buffer.append(frame()) # creating buffer frames (i.e., allocating memory)
			self.buffer[i].frameNumber = i
	#------------------------------------------------------------

	def pin(self,pageNumber, new = False): 
		# given a page number, pin the page in the buffer
		if (new == True) : 
			# if new = True, the page is new so no need to read it from disk
			victim = self.clk.pickVictim(self.buffer)
			if(victim == -1) :
				#buffer pool full, reset a current to 0 
				self.clk.current = 0
			current = self.clk.current
			if(self.buffer[current].dirtyBit == True) :
				# write to disk
				self.dm.writePageToDisk(self.buffer[current].currentPage)
			self.buffer[current].pinCount += 1
			self.buffer[current].referenced = 1
			self.buffer[current].currentPage.pageNo = pageNumber
			self.buffer[current].dirtyBit = False
			return self.buffer[current].currentPage			
		else : 
			# if new = False, the page already exists. So read it from disk if it is not already in the pool. 
			for ind in range(len(self.buffer)):
				if (self.buffer[ind].currentPage.pageNo == pageNumber):
					# page is in the buffer
					return self.buffer[ind].currentPage
			# page not in buffer so read from disk
			return self.dm.readPageFromDisk(pageNumber)
		#pass

	#------------------------------------------------------------
	def unpin(self,pageNumber, dirty):
		for i in range(len(self.buffer)) :
			if(self.buffer[i].currentPage.pageNo == pageNumber) :
				self.buffer[i].pinCount -= 1
				self.buffer[i].referenced = 0
				self.clk.current += 1
				if (dirty == True):
					self.buffer[i].dirtyBit = True
				return
		
	def flushPage(self,pageNumber): 
		# Ignore this function, it is not needed for this homework.
		# flushPage forces a page in the buffer pool to be written to disk
		for i in range(len(self.buffer)):
			if self.buffer[i].currentPage.pageNo == pageNumber:
				self.dm.writePageToDisk(self.buffer[i].currentPage) # flush writes a page to disk 
				self.buffer[i].dirtyBit = False

	def printBufferContent(self): # helper function to display buffer content on the screen (helpful for debugging)
		print("---------------------------------------------------")
		for i in range(len(self.buffer)):
			print("frame#={} pinCount={} dirtyBit={} referenced={} pageNo={} pageContent={} ".format(self.buffer[i].frameNumber, self.buffer[i].pinCount, self.buffer[i].dirtyBit, self.buffer[i].referenced,  self.buffer[i].currentPage.pageNo, self.buffer[i].currentPage.content))	
		print("---------------------------------------------------")
