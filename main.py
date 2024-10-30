from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import dfaMermaid
import os

app = FastAPI()

# Mount static directory to serve generated DFA graphs
app.mount("/static", StaticFiles(directory="generatedDFAGraphs"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = f"""
    <html>
        <head>
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
            <script type="module" src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"></script>
            <script>
                mermaid.initialize(\u007b startOnLoad: true, theme: 'neutral' \u007d);
            </script>
            <style>
                body \u007b
                    background-color: #1e1e1e;
                    color: #c98f20;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding-top: 40px;
                    font-family: 'Roboto', sans-serif;
                    margin: 0;
                \u007d
                h1 \u007b
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    color: #ffa500;
                \u007d
                a \u007b
                    text-decoration: none;
                    color: #c98f20;
                    font-weight: bold;
                    margin-top: 20px;
                    padding: 10px 20px;
                    border: 2px solid #c98f20;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                \u007d
                a:hover \u007b
                    background-color: #c98f20;
                    color: #1e1e1e;
                \u007d
                .content-container \u007b
                    background-color: #2e2e2e;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
                    max-width: 90%;
                    overflow-x: auto;
                \u007d
                form \u007b
                    background-color: #2e2e2e;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
                    max-width: 400px;
                    margin-top: 20px;
                    color: #c98f20;
                    text-align: center;
                \u007d
                label, input \u007b
                    display: block;
                    margin-bottom: 10px;
                    font-size: 1.2em;
                \u007d
                input[type="number"] \u007b
                    padding: 10px;
                    border: 2px solid #c98f20;
                    border-radius: 5px;
                    background-color: #1e1e1e;
                    color: #ffa500;
                \u007d
                button[type="submit"] \u007b
                    background-color: #c98f20;
                    color: #1e1e1e;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 8px;
                    font-size: 1.2em;
                    cursor: pointer;
                    transition: all 0.3s ease;
                \u007d
                button[type="submit"]:hover \u007b
                    background-color: #ffa500;
                    color: #1e1e1e;
                \u007d
            </style>
        </head>
        <body>
            <h1>Generador de DFAs por enumeración</h1>
            <div class="content-container">
                Hecho por Carlos Troya
            </div>
            <form action="/generate" method="post">
                <label for="dfaNumber">DFA Number:</label>
                <input type="number" id="dfaNumber" name="dfaNumber" required>
                <label for="alphabetSize">Alphabet Size:</label>
                <input type="number" id="alphabetSize" name="alphabetSize" required>
                <button type="submit">Generate DFA</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/generate", response_class=HTMLResponse)
async def generate_dfa(request: Request):
    form_data = await request.form()
    dfaNumber = int(form_data["dfaNumber"])
    alphabetSize = int(form_data["alphabetSize"])

    # Generate DFA using the provided inputs
    dfa = generateDfa(dfaNumber, alphabetSize)
    div_content = dfaMermaid.createMermaidDiv(dfaNumber, dfa[0], dfa[1], dfa[2])

    html_content = f"""
<html>
    <head>
        <link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap\">
        <script type=\"module\" src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs\"></script>
        <script>
            mermaid.initialize(\u007b startOnLoad: true, theme: 'neutral' \u007d);
        </script>
        <style>
            body \u007b
                background-color: #1e1e1e;
                color: #c98f20;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding-top: 40px;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                position: relative;
            \u007d
            h1 \u007b
                font-size: 2.5em;
                margin-bottom: 20px;
                color: #ffa500;
                display: flex;
                align-items: center;
            \u007d
            a \u007b
                text-decoration: none;
                color: #c98f20;
                font-weight: bold;
                padding: 2px 5px;
                border: 1px solid #c98f20;
                border-radius: 3px;
                transition: all 0.3s ease;
                font-size: 0.9em;
                position: absolute;
                top: 20px;
                right: 20px;
            \u007d
            a:hover \u007b
                background-color: #c98f20;
                color: #1e1e1e;
            \u007d
            .content-container \u007b
                background-color: #2e2e2e;
                padding: 50px;
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
                width: auto;
                height: auto;
                max-width: 100%;
                max-height: 100%;
                overflow-x: auto;
                display: inline-block;
            \u007d
        </style>
    </head>
    <body>
        <h1>Visualizacion del DFA</h1>
        <a href=\"/\">Back to Home</a>

            {div_content}

    </body>
</html>
    """
    return HTMLResponse(content=html_content)

import stateNum
import math
import finalStates
import numpy
import convert
import dict
import dfaMermaid
import os
import json
import jsonify

def generateDfa(dfaNumber,alphabetSize):
    diccionario = dict.get_unicode_letters(alphabetSize)
    print(f"Generating the dfa number {dfaNumber} with Sigma Size of {alphabetSize}")
    startingValues = stateNum.determine_number_of_states(dfaNumber,alphabetSize)
    Qlen = startingValues[0]
    # print(rangeQlen1)
    topInd = 0
    botInd = None
    Flen = None
    print(startingValues)
    dfaNumber -= startingValues[2]
    for i in (range(Qlen+1)):
        topInd += math.comb(Qlen,i)*(Qlen+1)**(alphabetSize*Qlen)
        # print(topInd)
        if topInd >= dfaNumber:
            botInd = topInd - math.comb(Qlen,i)*(Qlen+1)**(alphabetSize*Qlen)
            print(f"{dfaNumber} in between {botInd} and {topInd}")
            print(f"Therefore the dfa has {i} final states")
            Flen = i
            break
    dfaNumber -= botInd
    topInd = 0
    botInd = 0
    rangeLen = stateNum.determine_amount_of_dfas_without_final(Qlen,alphabetSize)
    fStateIndex = None
    for i in range(math.comb(Qlen,Flen)):
        topInd += rangeLen
        if topInd >= dfaNumber:
            botInd = topInd - rangeLen
            print(f"{dfaNumber} in between {botInd} and {topInd}")
            print(f"Therefore the final state index is {i}")
            fStateIndex = i
            break #XD
    dfaNumber -= botInd + 1
    fStates = finalStates.estados_finales_tamano_n(Qlen,Flen)[fStateIndex]
    allStates = finalStates.estados_finales_tamano_n(Qlen,Qlen)[-1]
    print(f"The states of the DFA are {allStates}")
    print(f"The final states are {fStates}")
    # dfaNumber = numpy.base_repr(dfaNumber,Qlen+1)
    # print(dfaNumber)
    dfaNumber = convert.int_to_base(dfaNumber,Qlen+1)
    dfaNumber = dfaNumber.zfill(Qlen*alphabetSize)
    # print(dfaNumber)
    count = 0
    transitions = []
    for i in range(Qlen):
        for j in range(alphabetSize):
            if dfaNumber[count%len(dfaNumber)] == '0':
                print(f"∂(q{i},{diccionario[j]}) = ⟂")
                #transitions.append([f"q{i}",diccionario[j],'ind'])
            else:
                #print(dfaNumber[count%len(dfaNumber)])
                print(f"∂(q{i},{diccionario[j]}) = q{int(dfaNumber[count%len(dfaNumber)],base=Qlen+1)-1}")
                transitions.append([f"q{i}",diccionario[j],f"q{int(dfaNumber[count%len(dfaNumber)],base=Qlen+1)-1}"])
            count += 1
    return [fStates,transitions,allStates]

# if "__main__" == __name__:
#     dfaN = int(input("Inserte el numero del dfa:"))
#     alphSize = int(input("Inserte el tamaño del alfabeto"))
#     dfa = generateDfa(dfaN,alphSize)
#     if os.path.exists("generatedDFAGraphs") != True:
#         os.makedirs("generatedDFAGraphs")
#     if os.path.exists("jsonDfa")!= True:
#         os.makedirs("jsonDfa")
#     dfaMermaid.write_to_file(f"generatedDFAGraphs/dfa{dfaN}Sigma{alphSize}.html",dfaMermaid.createMermaidFile(dfaN,dfa[0],dfa[1],dfa[2]))
#     dfaJson = jsonify.DFA(dfa[1],dfa[2],dfa[0])
#     print(dfaJson)
#     dfaMermaid.write_to_file(f"jsonDfa/dfa{dfaN}Sigma{alphSize}.json",json.dumps(dfaJson.to_dict()))
#     print(f"Graph for the file can be found in",f"generatedDFAGraphs/dfa{dfaN}Sigma{alphSize}.html")