# Thompson's Construction
# Kevin Niland

""" References """
# Videos
# Shunting Yard Algorithm: https://web.microsoftstream.com/video/cfc9f4a2-d34f-4cde-afba-063797493a90
# Thompson's Construction: https://web.microsoftstream.com/video/5e2a482a-b1c9-48a3-b183-19eb8362abc9

""" Shunting Yard Algorithm for converting infix regular expressions to postfix """
def shunt(infix):
    # Curly braces = dictionary
    # *, +, and ? are repetition operators. They take precedence over concatenation and alternation operators
    # * = Zero or more
    # + = One or more
    # ? = Zero or one
    # . = 
    # | =  
    specials = {'?': 70, '+': 60, '*': 50, '.': 40, '|': 30}

    pofix = ""
    stack = ""

    # Loop through the string one character at a time
    for c in infix:
        if c == '(':
            stack = stack + c
        elif c == ')':
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1], stack[:-1]
            # Remove '(' from stack
            stack = stack[:-1]
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        else:
            pofix = pofix + c

    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]
        
    return pofix

""" Thompson's Construction """
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
def compile(pofix):
    nfaStack = []

    for c in pofix:
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
            nfa1.accept.edge1 = nfa1.initial
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

# print(compile("ab.cd.|"))
# print(compile("aa.*"))

""" Return the set of states that can be reached from a state following
    'e' arrows """
def followArrowE(state):
    # Create a new set, with each state as it's only member
    states = set()
    states.add(state)

    # Check if state has arrows labelled 'e' from it
    if state.label is None:
        # Check if edge1 is a state
        if state.edge1 is not None:
            # If there's an edge1, follow it 
            states |= followArrowE(state.edge1)
        # Check if edge2 is a state
        if state.edge2 is not None:
            # If there's an edge2, follow it
            states |= followArrowE(state.edge2)

    # Return the set of states.
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
                # Add edge1 state to the next set of states
                nextState |= followArrowE(c.edge1)

        # Set currentState to next and clear out nextState
        currentState = nextState
        nextState = set()
    
    # Check if the accept state is in the current set of states
    return(nfa.accept in currentState)

# Test cases
infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

# Test cases
for i in infixes:
    for s in strings:
       print('Match: ' + str(match(i, s)), "Infix: " + i, "String: " + s)

def userInput():
    counter = int(input("Define the amount of infixes and strings you wish to enter: "))
    print(counter)

    infixes = {""}
    strings = {""}

    for i in range(counter):
        infix = input("Enter an infix: ")
        infixes.add(infix)

    for i in range(counter):
        string = input("Enter a string: ")
        strings.add(string)

    print(infixes)
    print(strings)

userInput()