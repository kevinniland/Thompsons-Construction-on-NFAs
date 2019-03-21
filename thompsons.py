# Thompson's Construction
# Kevin Niland

""" Shunting Yard Algorithm for converting infix regular expressions to postfix """
def shunt(infix):
    # Curly braces = dictionary
    specials = {'*': 50, '.': 40, '|': 30}
    
    postfix = "" # Output
    stack  = "" # Operator stack

    # Loop through the string one character at a time
    for c in infix:
        if c == '(':
            stack += c
        elif c == ')':
            while stack[-1] != '(':
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack[:-1]
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack += c
        else:
            postfix += c

    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]
            
    return postfix
    
print(shunt("(a.b)|(c*.d)"))

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

""" Compiles a postfix regular expression into an NFA """
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
            # Create new initial and accept states
            accept = state()
            initial = state()

            # Join the initial state and the accept state using an arrow labelled 'c'
            initial.label = c
            initial.edge1 = accept

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)

    # NFA stack should only have a single NFA on it at this point
    return nfaStack.pop()

## print(compile("ab.cd.|"))
## print(compile("aa.*"))

""" Return the set of states that can be reached from a state following
    'e' arrows """
def followArrowE(state):
    # Create a new set, with each state as it's only member
    states = set()
    states.add(state)

    # Check if state has arrows labelled 'e' from it
    if state.label is None:
        # Check if edg1 is a state
        if state.edge1 is not None:
            # If there's an edge1, follow it  
            states |= followArrowE(state.edge1)
        # Check if edg1 is a state
        if state.edge2 is not None:
            # If there's an edge2, follow it
            states |= followArrowE(state.edge2)

      # Return the set of states
    return states

""" Matches string to infix regular expression """
def match(infix, string):
    # Shunt and compile the regular expression 
    postfix = shunt(infix)
    nfa = compile(postfix)

    # The current set of states and the next set of states
    currentState = set()
    nextState = set()

    # Add the initial state to the current set of states
    currentState |= followArrowE(nfa.initial)

    # Loop through each character in the string
    for s in string:
        # Loop through current set of states
        for c in currentState:
            # Check if that state is labelled 's'
            if c.label == s:
                # Add edg1 state to the next set of states
                nextState |= followArrowE(c.edge1)
        # Set currentState to next and clear out nextState
        currentState = nextState
        nextState = set()

    # Check if the accept state is in the current set of states
    return (nfa.accept in currentState)

# Test cases
infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

for i in infixes:
    for s in strings:
        print(match(i, s), i, s)