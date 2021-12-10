import json
from utils import check_get
from fsm import machine

from transitions.extensions.diagrams import GraphMachine

m2={}
m2['states']=[]
m2['transitions']=[]
for state in machine:
    m2['states']+=[state]
    
    for node in check_get(machine[state],'advance',[]):
        tmp={}
        tmp['trigger']='advance'
        tmp['source']=state
        tmp['dest']=node['next']
        tmp['conditions']=node['condition']
        m2['transitions']+=[tmp]
    
    if 'else' in machine[state]:
        tmp={}
        tmp['trigger']='else'
        tmp['source']=state
        tmp['dest']=machine[state]['else']
        m2['transitions']+=[tmp]

machine = GraphMachine(
    states=m2['states'],
    transitions=m2['transitions'],
    initial="menu",
    auto_transitions=False,
    show_conditions=True,
)

machine.get_graph().draw("fsm.png", prog="dot", format="png")