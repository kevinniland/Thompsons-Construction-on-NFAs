# Thompson's Construction
# Kevin Niland

# Represents a state with two arrows, labelled by 'label'
# Use 'None' for a label representing 'e' arrows
class state:
    label = None
    edge1 = None
    edge2 = None

# An NFA is represented by it's initial and accept states
class nfa:
    initial = None
    accept = None

    # 'self' represents current instance of the class - similar to 'this'
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(postfix):
    nfaStack = []

    for c in postfix:
        if c == '.':
           # Pop two NFAs off the stack
            nfa2 = nfaStack.pop() 
            nfa1 = nfaStack.pop()

            # Connect first NFA's accept state to the second's initial
            nfa1.accept.edge1 = nfa2.initial

            # Push new NFA to the stack
            newNFA = nfa(nfa1.initial, nfa2.accept)
            nfaStack.append(newNFA)
        elif c == '|':
          
        elif c == '*':
            
        else:
            


