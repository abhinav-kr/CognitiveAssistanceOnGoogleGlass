



class Soft_State:

   def __init__(self):
      self.vm_state_list = list();
      

   def displayEmployee(self):
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
   
   def updateODT(self,thread_name,odt) :
   	for ele in soft_state.vm_state_list :
   		if ele.thread_name == thread_name :
   			ele.odt = odt






soft_state = Soft_State()