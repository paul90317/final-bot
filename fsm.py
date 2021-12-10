from transitions.extensions import GraphMachine

from utils import check_get

class myFSM():
    def __init__(self, mjson):
        self.machine = mjson

    def advance(self,state,msg):
        if 'any' in self.machine[state]:
            return self.machine[state]['any']

        return check_get(self.machine[state]['advance'],msg,None)
        
    def go_back(self,state):
        return check_get(self.machine[state],'back',None)
        
        
