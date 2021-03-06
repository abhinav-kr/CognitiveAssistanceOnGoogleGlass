from gabriel.control.thread_state import Thread_State
from gabriel.common import log as logging


import threading

LOG = logging.getLogger(__name__)

class VM_Schedule :

	def __init__(self,thread_name,offset,slice_perc):
		self.thread_name = thread_name
		self.slice_perc = slice_perc
		self.offset_perc = offset

	def displayVMSchedule(self):
   		print "Thread name : ", self.thread_name

class Schedule:

	def __init__(self):
		self.schedule_id = 0
		self.vm_schedule_list = list()

	def displaySchedule(self):
		print "Thread schedule list : ", self.vm_schedule_list

	def addScheduleForThread(self,thread_name,offset,slice_perc):
		thread_schedule = VM_Schedule(thread_name,offset,slice_perc)
		self.vm_schedule_list.append(thread_schedule);

	def getScheduleForName(self,vm_name):
		for ele in self.vm_schedule_list:	
			if ele.thread_name == vm_name:
				return ele

		return None


	def getScheduleForId(self,vm_id):
		if vm_id > len(self.vm_schedule_list) :
			return None
		else:
			return self.vm_schedule_list[vm_id]

	def addVMSchedule(self,vm_schedule):
		self.vm_schedule_list.append(vm_schedule)


	def printSchedule(self):
		message = "( "
		for ele in self.vm_schedule_list :
			message = message + str(ele.slice_perc)+ " "

		return message;
class Soft_State:

   def __init__(self):
      
      # vm states
      self.vm_state_list = list()

      # used for triggering schedule calculation
      self.countdown =dict()
      
      # Locks
      self.frame_lock = threading.RLock()
      self.handler_lock = threading.RLock()
      
      #used to check if a thread is first to process a frame
      self.last_frame_id =-1;

      #used to filter values going in countdown
      self.schedule_switch_frame =-1
      

      # curr value of exp odt, usually should be in 100s or 1000s 
      self.curr_expected_odt = 9999999

      #schedules
      self.new_schedule = None
      self.curr_schedule = None
      self.accepted_odt = 9999999
      
      #current vm under going optimization
      self.thread_under_opt =0

      # Is state stable
      self.state_stable = False

      #ESVM fidelity (10 is 100%)
      self.fidelity =6 

      #Indicates how many schedules have been offered since last accepted schedule
      self.schedule_ahead_by =1
      
   def displaySoftState(self):
      print "VM state list : ", self.vm_state_list

   def getIndexForHandler(self,thread_name) :
        index = -1
        found = False;
        for ele in self.vm_state_list :
            
            index=index+1
            if ele.thread_name == thread_name :
                found = True;
                break

        if found == True :
        	return index
        else :
        	return -1

   def calculateExpectedODT(self):
   	expected_odt = 0
   	
   	index =0;
   	for ele in self.vm_state_list :
   		vm_schedule = self.curr_schedule.getScheduleForId(index);
   		expected_odt = expected_odt + ( (vm_schedule.slice_perc/100.0)* ele.last_odt)
   		index+=1
   	
   	#LOG.info("Calculation is triggered %s" % str(expected_odt));
   	return expected_odt


   def revertToPrevSchedule(self, new_schedule):

   		vm_count = len(self.vm_state_list)

   		#loop over prev state and restore prev state
		offset = 0
                slice_perc =0
   		for x in xrange(0,vm_count):
   			vm_schedule = self.curr_schedule.getScheduleForId(x);
   			if x == self.thread_under_opt :

   				#getting slice_perc to the previous state
   				k = (2*self.schedule_ahead_by)*(vm_count - 1 - self.thread_under_opt)
   				slice_perc = vm_schedule.slice_perc + k
   				
   				vm_name = vm_schedule.thread_name
   				
   				#restored value
   				new_schedule.addVMSchedule( VM_Schedule(vm_name,offset,slice_perc) )
   			elif x > self.thread_under_opt :
   				#getting slice_perc to the previous state
   				slice_perc = vm_schedule.slice_perc - ((2)*self.schedule_ahead_by)
   				vm_name = vm_schedule.thread_name
   				
   				#restored value
   				new_schedule.addVMSchedule( VM_Schedule(vm_name,offset,slice_perc) )
   			else :

   				#getting slice_perc to the previous state
   				slice_perc = vm_schedule.slice_perc
   				vm_name = vm_schedule.thread_name
   				new_schedule.addVMSchedule( VM_Schedule(vm_name,offset,slice_perc) )

			offset +=slice_perc


   def createNewSchedule(self,new_schedule,curr_schedule):
   		
   		vm_count = len(self.vm_state_list)
   		offset = 0
   		slice_perc =0 
   		for x in xrange(0,vm_count) :
   			vm_schedule = self.curr_schedule.getScheduleForId(x)

   			if x == self.thread_under_opt :

   				#getting slice_perc to the previous state
   				k = 2*(vm_count - 1 - self.thread_under_opt)
   				slice_perc = vm_schedule.slice_perc - k
   				vm_name = vm_schedule.thread_name
   				#restored value
   				new_schedule.addVMSchedule( VM_Schedule(vm_name,offset,slice_perc) )

   			elif x > self.thread_under_opt :
   				#getting slice_perc to the previous state
   				slice_perc = vm_schedule.slice_perc + 2
   				vm_name = vm_schedule.thread_name

   				
   				#restored value
   				new_schedule.addVMSchedule( VM_Schedule(vm_name,offset,slice_perc) )
   			else :

   				#getting slice_perc to the previous state
   				slice_perc = vm_schedule.slice_perc
   				vm_name = vm_schedule.thread_name

   				new_schedule.addVMSchedule( VM_Schedule(vm_name,offset,slice_perc) )
   			
   			offset+=slice_perc

   		

   def changeThreadUnderOpt(self):
   		self.thread_under_opt = self.thread_under_opt +1
   		vm_count = len(self.vm_state_list)
   		if self.thread_under_opt == vm_count-1 :
   			self.state_stable = True


   def decreaseFidelity(self):
         if self.fidelity > 3 :
            self.fidelity-=1
	    LOG.info("Decreased scaling to %s", str(self.fidelity) );

   def increaseFidelity(self):
         if self.fidelity <= 10 :
            self.fidelity+=1
	    LOG.info("Increased scaling to %s", str(self.fidelity) );



   def adjustFidelity(self):
      #calculate the expected value based on current set of odt
	new_expected_odt =self.calculateExpectedODT();
	if new_expected_odt > 500 :
         self.decreaseFidelity()
	else:
         self.increaseFidelity()

   	

   def triggerScheduleCalculation(self, new_expected_odt):
   	self.countdown.clear()
   	#LOG.info("Calculation is triggered");
   	
   	#calculate the expected value based on current set of odt
   	#inew_expected_odt =self.calculateExpectedODT();
   	
   	new_schedule =  Schedule()
   	# if new schedule did not worked
        diff = self.accepted_odt - new_expected_odt

        perc_diff = 0

        if diff < 0 :
         perc_diff = ((-diff)/self.accepted_odt)*100
	

	LOG.info("Measured EODT:  %s, accepted EODT: %s , Diff: %s, Perc diff : %s",new_expected_odt, self.accepted_odt,diff, perc_diff)
        if (diff < 0) and (perc_diff < 10):
		 LOG.info("Not sure, Trying a different one accepted one  %s", self.accepted_odt)
	      	 self.createNewSchedule(new_schedule,self.curr_schedule);
        	 self.schedule_ahead_by+=1

   	elif (diff < 0) and (perc_diff > 10):
        	 #revert schdule back to last accepted
		 LOG.info("Reverting back to old schedule");
        	 self.revertToPrevSchedule(new_schedule)
	         self.schedule_ahead_by=1
   		 LOG.info("Reverted Schedule : " + new_schedule.printSchedule())	
   		 self.changeThreadUnderOpt()
   	else :
		self.accepted_odt = new_expected_odt
		LOG.info("Accepted Schedule : " + self.curr_schedule.printSchedule())
   		self.createNewSchedule(new_schedule,self.curr_schedule);
   		self.curr_expected_odt = new_expected_odt
         	self.schedule_ahead_by=1

   	self.new_schedule = new_schedule

   def updateODT(self,thread_name,frame_id,odt) :
   	if frame_id >= self.schedule_switch_frame :
	   	for ele in self.vm_state_list :
	   		if ele.thread_name == thread_name :
	   			ele.last_odt = odt
	   			self.countdown[thread_name]=1
				
	   			if len(self.countdown) == len(self.vm_state_list) :
					new_expected_odt =self.calculateExpectedODT();
					#if self.state_stable == True :
					LOG.info("Expected odt found %s" % new_expected_odt )
        		                #LOG.info("Count down expired" )
	   				if (self.state_stable == False) and (len(self.vm_state_list) >1 ):
		                                #LOG.info("Triggering schedule calculation" )
	   					self.triggerScheduleCalculation(new_expected_odt)
         	        		elif (self.state_stable == True) or (len(self.vm_state_list) == 1):
		        	          #self.adjustFidelity()
					  LOG.info('')
   			

   def getSchedule(self,vm_name,frame_id) :
   	#import pdb; pdb.set_trace()
   	self.frame_lock.acquire()
   	try:
   		if self.last_frame_id < frame_id :
   			#changing the frame id for latest id used
   			self.last_frame_id = frame_id
   			
   			if self.new_schedule is not None:
				self.curr_schedule = self.new_schedule
				self.new_schedule = None
   				self.schedule_switch_frame = frame_id

   		return self.curr_schedule.getScheduleForName(vm_name)
   	
   	finally:
   		self.frame_lock.release()

   def reinitializeState(self,vm_name):
   	vm_count = len(self.vm_state_list)
   	new_schedule = Schedule()

   	offset=0
   	slice_perc = 100/vm_count
	#slice_perc = 35
   	if vm_count == 1:
   		new_schedule.addVMSchedule( VM_Schedule(vm_name,0,100) )
   	else :
	   	
	   	for x in xrange(0,vm_count-1):
	   		vm_schedule = self.curr_schedule.getScheduleForId(x)
	   		cur_vm_name = vm_schedule.thread_name
			new_schedule.addVMSchedule( VM_Schedule(cur_vm_name,offset,slice_perc) )
			offset += slice_perc
			#slice_perc =65

		if slice_perc+offset <100:
			slice_perc += 1

		new_schedule.addVMSchedule( VM_Schedule(vm_name,offset,slice_perc) )

	self.curr_schedule = new_schedule


   def addHandler(self,thread_name) :
   	self.handler_lock.acquire()
   	try:
   		self.vm_state_list.append(Thread_State(thread_name));
   		self.reinitializeState(thread_name)
   	finally:
   		self.handler_lock.release()

   	def removehandler(self,thread_name) :
   	 self.handler_lock.acquire()
   	 try:
   		index = self.getIndexForHandler(thread_name)
   		self.vm_state_list.pop(index)
   		self.reinitializeState(thread_name)
   	 finally:
   		self.handler_lock.release()



soft_state = Soft_State()
