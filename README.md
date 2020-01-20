<h3><b>Author:</b></h3> <i>Kevin Niland</i>
<h3><b>Build version:</b></h3> <i>1.0.0</i>

<h2>Project Statement</h2>
You must write a program in the Python programming language that can build a Non-Deterministic Finite Automaton (NFA) from a regular expression,  
and can use the NFA to check if the regular expression matches any given string of text. You must write the program from scratch and cannot use 
the re package from the Python standard library nor any other external library.

<h2>Aim</h2>
The aim of this project is write a program in Python that can check if a given string matches a regular expression built through a Non-Deterministic Automation (NFA). The re package, which provides regular expression matching operations, may not be used.

<h2>Tech/Framework?Language(s) used:</h2>
Python

<h2>What it does</h2>
There are several functions contained in the program, however the five main functions are: shunt, compile, followArrowE, match, and printMatch:

<ul>
    <li>The shunt function has one parameter, 'infix'. In it, a set of the special characters is defined, each with it's own precedence. Below this, there is a for loop that loops through the infix looking for any brackets, special characters, or regular characters. If a bracket is encountered, it pops everything from the stack and adds all characters to the postfix in order of their precedence. The functions then returns the postfix.</li>
    <li>The compile function has one parameter, 'pofix'. In it, an NFA stack is declared. Below this, there is a for loop that performs different operations depending on the special character (Refer to the comments in the program to see what happens when a specific special character is encountered). Once the if statement has exited, the remaining item on the NFA stack is popped off.</li>
    <li>The followArrowE function has one parameter, 'state'. In it, a new set called 'states' is declared and the parameter is add to this set. Below this, there is a nested if statement. The first if statement checks if the state has a arrow labelled 'e' coming from it. The second one checks if edge1 is a state. If it is, follow it. The third one checks if edge2 is a state. If it is, follow it. After the if statement has exited, the set of states is returned.</li>
    <li>The match function has two parameters, 'infix' and 'string'. In it, 'postfix' and 'nfa' shunt and compile the regular expression, respectively. Sets containing the currentState and nextState are defined. Below this, the initial state is added to the current set of states. Using a nested for loop, each character in the string and the current set of states is looped through. If the state is labelled as 's', add the state of edge1 to the next set of states. Following this, the currentState is set to the nextState and then intialise a new set of nextState. The accept state of the currentState is returned.</li>
    <li>The printMatch function takes in no parameters. In it, a file is opened. A set of infixes and strings is declared. Using a nested if statement, 'True' or 'False' is printed depending on whether the infix and string match. The results of this are printed to the file simultaneously.</li>
 </ul>

<h2>How To Use</h2>
<b>IMPORTANT: In order for the user to enter in their own infix/string, they must surrond their input with quotation marks i.e 'Enter an infix: "a.b"'. Attempting to enter an infix/string <i>without</i> quotation marks will result in an error.</b>
    
<br>
<br>

<ol>
    <li>Download/clone project to a desired location.</li>
    <li>Navigate to the directory in which the project is located.</li>
    <li>Assuming everything necessary to run a Python program is installed, type 'python thompsons.py' into the command prompt and press enter.</li>
    <li>The user will then be greeted with the menu.</li>
</ol>

<h2>Tests</h2>
Infixes:
["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c", "a.b?", "a+b.c"]

Strings:
["", "a", "ab", "abc", "abbc", "abcc", "abad", "abbbc", "abcd", "abbbb", "ac"]

<h2>Extras</h2>
<ul>
    <li>'+' operator</li>
    <li>'?' operator</li>
    <li>Menu/User Interface - <b>Please note that due to a problem with the 'readFile()' function, the program will read in files but the function won't exit - files will be continuosly be read in until user manually exits the operation.</b></li> 
</ul>

<h2>Research/Additional Information</h2>
Please refer to the wiki of this repository to view the research conducted in relation to this project.
      

