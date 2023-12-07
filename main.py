import stateNum
import math
import finalStates
import numpy
diccionario = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')'
]
def generateDfa(dfaNumber,alphabetSize):
    print(f"Generating the dfa number {dfaNumber} with Sigma Size of {alphabetSize}")
    startingValues = stateNum.determine_number_of_states(dfaNumber,alphabetSize)
    Qlen = startingValues[0]
    # print(rangeQlen1)
    topInd = 0
    botInd = None
    Flen = None
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
    dfaNumber -= botInd + 1
    fStates = finalStates.estados_finales_posibles(Qlen,Flen)[fStateIndex]
    print(f"The states of the DFA are {finalStates.estados_finales_posibles(Qlen,Qlen)[-1]}")
    print(f"The final states are {fStates}")
    dfaNumber = numpy.base_repr(dfaNumber,Qlen+1)
    dfaNumber = dfaNumber.zfill(Qlen*alphabetSize)
    print(dfaNumber)
    count = 0
    for i in range(Qlen):
        for j in range(alphabetSize):
            if dfaNumber[count%len(dfaNumber)] == '0':
                print(f"∂(q{i},{diccionario[j]}) = ind")
            else:
                #print(dfaNumber[count%len(dfaNumber)])
                print(f"∂(q{i},{diccionario[j]}) = q{int(dfaNumber[count%len(dfaNumber)])-1}")
            count += 1
if "__main__" == __name__:
    generateDfa(2933,3)