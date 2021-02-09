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
		self.minPinCount = -1
		pass

	def findMinPinCount(self,buffer) :
		min = 0
		for idx in range(len(buffer)) : 
			if (buffer[idx].pinCount < min) :
				min = buffer[idx].pinCount
		return min

	def pickVictim(self,buffer):
		victim = -1
		signal = 1
		self.minPinCount = self.findMinPinCount(buffer)
		for idx in range(len(buffer)) :
			
			if (buffer[idx].pinCount == self.minPinCount) :
				buffer[idx].referenced = 0
				if(signal == 1 ) :
					victim = buffer[idx].frameNumber
					self.current = idx
					signal = 0
			
		if(victim == -1 ) :
			# if all pages in the buffer pool are pinned, raise the exception BufferPoolFullError
			raise BufferPoolFullError('Buffer Pool Full')
		else :
			# find a victim page using the clock algorithm and return the frame number
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
		# page number = 101, new true
		if (new == True) :
			# if new = True, the page is new so no need to read it from disk
			#find a victim
			victim = self.clk.pickVictim(self.buffer)
			current = self.clk.current
			self.buffer[current].pinCount += 1
			self.buffer[current].referenced = 1
			self.buffer[current].currentPage.pageNo = pageNumber
			self.dm.writePageToDisk(self.buffer[current].currentPage)
			return self.buffer[current].currentPage
		#else :
			# if new = False, the page already exists. So read it from disk if it is not already in the pool. 
			
		#pass
    
	#------------------------------------------------------------
	def unpin(self,pageNumber, dirty):
		for i in range(len(self.buffer)) :
			if(self.buffer[i].currentPage.pageNo == pageNumber) :
				self.buffer[i].pinCount -= 1
				self.buffer[i].referenced = 0
				self.buffer[i].dirtyBit = dirty
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
