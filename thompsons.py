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

    # 'self' represents current instance of the class -- similar to 'this'
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

