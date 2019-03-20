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
          # Pop two NFAs off the stack
            nfa2 = nfaStack.pop() 
            nfa1 = nfaStack.pop()

            # Create a new initial state, connect it to initial states
            # of the two NFAs popped from the stack
            initial = state()
            accept = state()

            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            # Create a new accept state, connecting the accept states
            # of the two NFAs popped from the stack to the new state
            accept = state()

            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        elif c == '*':
            # Pop a single NFA from the stack
            nfa1 = nfaStack.pop() 

            # Create new initial and accept states
            initial = state()
            accept = state()

            # Join the new initial state to nfa1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            # Join the old accept state to the new accept state and nfa1's initial state
            nfa1.accept.edge1 = nfa.initial
            nfa1.accept.edge2 = accept

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        else:
            


