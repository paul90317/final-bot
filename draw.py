import json
from utils import check_get

from transitions.extensions.diagrams import GraphMachine

with open("FSM.json","r") as f:
    m=json.load(f)

m2={}
m2['states']=[]
m2['transitions']=[]
for state in m:
    m2['states']+=[state]
    
    for word in check_get(m[state],'advance',{}):
        tmp={}
        tmp['trigger']='advance'
        tmp['source']=state
        tmp['dest']=m[state]['advance'][word]
        tmp['conditions']=word
        m2['transitions']+=[tmp]
    
    if 'any' in m[state]:
        tmp={}
        tmp['trigger']='any'
        tmp['source']=state
        tmp['dest']=m[state]['any']
        m2['transitions']+=[tmp]

    if 'back' in m[state]:
        tmp={}
        tmp['trigger']='go_back'
        tmp['source']=state
        tmp['dest']=m[state]['back']
        m2['transitions']+=[tmp]

machine = GraphMachine(
    states=m2['states'],
    transitions=m2['transitions'],
    initial="menu",
    auto_transitions=False,
    show_conditions=True,
)

machine.get_graph().draw("fsm.png", prog="dot", format="png")