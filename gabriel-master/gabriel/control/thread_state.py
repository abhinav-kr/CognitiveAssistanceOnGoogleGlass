

class Thread_State:

   def __init__(self, thread_name):
      self.thread_name = thread_name
      self.last_odt = 0;

   def displayEmployee(self):
      print "Name : ", self.thread_name,  ", Last ODT: ", self.last_odt