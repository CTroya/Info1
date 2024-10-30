
def write_to_file(file_path, text):
    """
    This function creates a new file or overwrites an existing file with the specified text.

    :param file_path: The path of the file to be written to.
    :param text: The text to be written into the file.
    """
    with open(file_path, 'w') as file:
        file.write(text)


def createMermaidFile(dfaNumber,finalStates,transitions,states):
    Header = f"<script type=\"module\"> \n import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs'; \n mermaid.initialize({'{startOnLoad: true,theme: neutral}'});\n</script>\n<body style=\"background-color: rgb(0, 0, 0);color: rgb(202, 132, 2)\">\nHere is the dfa {dfaNumber}\n<pre class=\"mermaid\">\n   graph LR\n  classDef state font-style:italic,font-weight:bold,fill:yellow\n  classDef finalState font-style:italic,font-weight:bold,fill:green"
    for i in finalStates:
        Header = f"{Header}\n {i}:::finalState"
    for i in (list(set(states)-set(finalStates))):
        Header = f"{Header}\n {i}(({i})):::state"
    Header = f"{Header}\n  0(( ))\n 0-->q0((q0))"
    for i in transitions:
        Header = f"{Header}\n {i[0]}--\'{i[1]}\'-->{i[2]}(({i[2]}))"
    Header =f"{Header}\n   </pre>\n</body>"
    return Header
def createMermaidDiv(dfaNumber, finalStates, transitions, states):
    """
    This function creates a Mermaid diagram div element without including the full HTML structure.

    :param dfaNumber: The number of the DFA being represented.
    :param finalStates: A list of final states in the DFA.
    :param transitions: A list of transitions in the form of tuples (from_state, input, to_state).
    :param states: A list of all states in the DFA.
    :return: A string representing the div containing the Mermaid diagram.
    """
    div_content = f"<pre class=\"mermaid\">\n   graph LR\n  classDef state font-style:italic,font-weight:bold,fill:yellow\n  classDef finalState font-style:italic,font-weight:bold,fill:green"
    
    for i in finalStates:
        div_content = f"{div_content}\n {i}:::finalState"
    for i in (list(set(states) - set(finalStates))):
        div_content = f"{div_content}\n {i}(({i})):::state"
    
    div_content = f"{div_content}\n  0(( ))\n 0-->q0((q0))"
    
    for i in transitions:
        div_content = f"{div_content}\n {i[0]}--\'{i[1]}\'-->{i[2]}(({i[2]}))"
    
    div_content = f"{div_content}\n   </pre>"
    return div_content