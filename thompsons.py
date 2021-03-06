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
    # . = Concatenation
    # | =  Alternation
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
        if c == '?':
            # Pop a single NFA from the stack
            nfa1 = nfaStack.pop()

            # Create new initial and accept states
            initial = state()
            accept = state()

            # Join the new initial state to nfa1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            # Make the accept state equal to the the NFA's accept state
            nfa1.accept.edge1 = accept

            # Push new NFA to the stack
            newNFA = nfa(initial, accept)
            nfaStack.append(newNFA)
        elif c == '+':
            # Pop a single NFA from the stack
            nfa1 = nfaStack.pop()

            # Create new initial and accept states
            initial = state()
            accept = state()

            # Make the accept edge 1 and edge 2 of the NFA equal to the initial state of the NFA
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept

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
        elif c == '.':
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
                # Add edge1 state to the next set of states
                nextState |= followArrowE(c.edge1)

        # Set currentState to next and clear out nextState
        currentState = nextState
        nextState = set()
    
    # Check if the accept state is in the current set of states
    return(nfa.accept in currentState)

""" Prints the results of the match function to a file and to the screen """    
def printMatch():
    # Open a file for reading and create it if it does not exist
    file = open("testCases.txt", "w+")
    fileInf = open("infixes.txt", "a+")
    fileStr = open("strings.txt", "a+")

    # Test cases
    infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c", "a.b?", "a+b.c"]
    strings = ["", "a", "ab", "abc", "abbc", "abcc", "abad", "abbbc", "abcd", "abbbb", "ac"]

    # Test cases
    for i in infixes:
        for s in strings:
            print("Match: " + str(match(i, s)), "Infix: " + i, "String: " + s)
            file.write("{} {} {}".format("Match: %s" % str(match(i, s)), "Infix: %s" % i, "String: %s\n" % s))
            fileInf.write("%s\n" % i)
            fileStr.write("%s\n" % s)

    # Close the file when done
    file.close()
    fileInf.close()
    fileStr.close()

""" Takes in the user entered infixes and strings and compares them """
def printUserInputMatch(userInfixes, userStrings):
    file = open("userInputs.txt", "a+")
    fileInf = open("infixes.txt", "a+")
    fileStr = open("strings.txt", "a+")

    for i in userInfixes:
        for s in userStrings:
            print("Match: " + str(match(i, s)), "Infix: " + i, "String: " + s)
            file.write("{} {} {}".format("Match: %s" % str(match(i, s)), "Infix: %s" % i, "String: %s\n" % s))
            fileInf.write("%s\n" % i)
            fileStr.write("%s\n" % s)

    # Close the file when done
    file.close()

# Allows user to read in a file and compare the infixes and strings in the file
# Problem with this function - can read in file successfuully and compare infixes. However function will continously get called
def readFile():
    infixesIn = []
    stringsIn = []

    fileInf = open("infixes.txt", "r")
    fileStr = open("strings.txt", "r")
    fileOut1 = open("testCases.txt", "w+")
    fileOut2 = open("userInputs.txt", "w+")
    
    for fInf in fileInf:
        infixesIn.append(fInf.strip()) # strip() returns a string after removing any leading/trailing whitespaces, tabs (\t), new lines (\n), etc.

    for fStr in fileStr:
        stringsIn.append(fStr.strip())
    

    for i in infixesIn:
        for s in stringsIn:
            print("Match: " + str(match(i, s)), "Infix: " + i, "String: " + s)
            lineOut1 = fileOut1.write("{} {} {}".format("Match: %s" % str(match(i, s)), "Infix: %s" % i, "String: %s\n" % s))
            lineOut2 = fileOut2.write("{} {} {}".format("Match: %s" % str(match(i, s)), "Infix: %s" % i, "String: %s\n" % s))

    fileInf.close()
    fileStr.close()
    fileOut1.close()
    fileOut2.close()

""" Takes in user's input """
def userInput():
    counter = int(input("Define the amount of infixes and strings you wish to enter: "))
    print(counter)

    userInfixes = []
    userStrings = []

    printInfixes = set()
    printStrings = set()

    for i in range(counter):
        userEntry = input("Enter an infix: ")
        userInfixes.append(userEntry)
    for i in range(counter):
        userEntry = input("Enter a string: ")
        userStrings.append(userEntry)

    printUserInputMatch(userInfixes, userStrings)

""" Menu interface """
def menu():
    isRunning = True

    while isRunning:
        userChoice = input("\nEnter '1' to print the view the matching results of the predetermined infixes and strings,\n" +
                            "Enter '2' to enter in your own infixes and strings (You must enclose your input with quotation marks),\n" + 
                            "Enter '3' to read and compare infixes and strings from a file or,\nEnter '-1' to exit the program: ")

        if userChoice == 1:
            printMatch()
        elif userChoice == 2:
            userInput()
        elif userChoice == 3:
            readFile()
        elif userChoice == -1:
            isRunning = False
            print("Bye")

menu()