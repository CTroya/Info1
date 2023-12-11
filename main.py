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
if "__main__" == __name__:
    dfaN = int(input("Inserte el numero del dfa:"))
    alphSize = 3
    dfa = generateDfa(dfaN,alphSize)
    if os.path.exists("generatedDFAGraphs") != True:
        os.makedirs("generatedDFAGraphs")
    if os.path.exists("jsonDfa")!= True:
        os.makedirs("jsonDfa")
    dfaMermaid.write_to_file(f"generatedDFAGraphs/dfa{dfaN}Sigma{alphSize}.html",dfaMermaid.createMermaidFile(dfaN,dfa[0],dfa[1],dfa[2]))
    dfaJson = jsonify.DFA(dfa[1],dfa[2],dfa[0])
    dfaMermaid.write_to_file(f"jsonDfa/dfa{dfaN}Sigma{alphSize}.json",json.dumps(dfaJson.to_dict()))
    print(f"Graph for the file can be found in",f"generatedDFAGraphs/dfa{dfaN}Sigma{alphSize}.html")