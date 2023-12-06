diccionario = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')'
]
#xD
import stateNum
import numpy
import math
import finalStates
import biyeccion

def generateDfa(dfaNumber,alphabetSize):
    dataBase = stateNum.determine_number_of_states(dfaNumber,alphabetSize)
    stateAmount = dataBase[0]
    cotaInf = dataBase[2]
    amountDfaWStateN = dataBase[3]
    cotaSup = cotaInf +  amountDfaWStateN
    cotaInf += 1
    ranges = []
    print(f"Cota inferior {cotaInf} Cota superior: {cotaSup} ")
    print(dataBase)

    # for i in (range(stateAmount+1)):
    #     print(i,math.comb(stateAmount,i))

    a = stateNum.determine_amount_of_dfas_without_final(stateAmount,alphabetSize)
    rangenum = a
    cumSum = dataBase[2] + 1
    print(a)

    # for i in (range(stateAmount+1)):
    #     print(f"Amount of states with {stateAmount} states and {i} final states ",math.comb(stateAmount,i)*stateNum.determine_amount_of_dfas_without_final(stateAmount,alphabetSize))

    #Creo los rangos de los estados finales posibles
    for i in range(stateAmount+1):
        print(cumSum)
        ranges.append(cumSum)
        cumSum += math.comb(3,i)*stateNum.determine_amount_of_dfas_without_final(stateAmount,alphabetSize)
    ranges.append(cotaSup)
    print(ranges)

    """"
    Bueno, ahora tenemos la cantidad de estados, y los rangos de los estados finales posibles, tenemos que generar los conjuntos de estados finales
    en el orden correcto y luego determinar cual de ellos le corresponde a nuestro dfa.
    """
    #Generamos los estados
    states = [f"q{i}" for i in range(stateAmount)]
    print(f"Conjunto q =<{states}>")

    #Ahora verificaremos el conjunto de estados finales perteneciente a nuestro automata
    a=None
    newCotaInf = None
    newCotaSup = None

    for i in range(len(ranges)-1):
        if dfaNumber in range(ranges[i],ranges[i+1]+1):
            print(f"{dfaNumber} esta entre {ranges[i]} y {ranges[i+1]}")
            a=i
            newCotaInf = ranges[i]
            newCotaSup = ranges[i+1]
    """"
    Me colgue, recien sabemos la cantidad de estados finales, aun no sabemos el conjunto, para eso tenemos que partir aun mas los rangos
    xd. Esto para 3 estados se veia facil, pero si quiero hacer para mas la combinatoria se va honestamente mas a la puta, que me pise un tren por favor
    """
    print(a)

    finalStateAmount = a
    cotaDist = newCotaSup - newCotaInf
    dfaNumberSpec = dfaNumber - newCotaInf #Esta es la posicion relativa del numero del dfa
    print("cantidad de estados finales: ", finalStateAmount)
    print("posicion relativa: ",dfaNumberSpec)
    print(cotaDist)
    ranges2 = [0]
    cumSum=0
    indexForFinalState = None
    """"
    Tuve una pequeña segunda iluminacion, la verdad soy medio bobito
    """
    for i in range(math.comb(stateAmount,finalStateAmount)):
        cumSum += ranges2[i]
        ranges2.append(cumSum + stateNum.determine_amount_of_dfas_without_final(stateAmount,alphabetSize)*math.comb(stateAmount,i))
        # cumSum += ranges2[i]
    #Bug fix xD
    # if dfaNumber == dataBase[1]+1:
    #     ranges2.append()
    print(ranges2)
    for i in range(len(ranges2)-1):
        if dfaNumberSpec in range(ranges2[i],ranges2[i+1]):
            print(f"{dfaNumberSpec} esta entre {ranges2[i]} y {ranges2[i+1]}")
            indexForFinalState = i
    #Bugfix
    # if dfaNumberSpec == ranges2[-1]:
    #     indexForFinalState = len(ranges2)-1
    #ESTO HICE PARA QUE ME QUEDE COMO A ALAIN PERO NO ENTIENDO BIEN PORQUE??
    #TIENE SENTIDO PORQUE EL NUMERO DE GODEL PARA EL AUTOMATA CON ESE ESTADO FINAL
    #NO TIENE QUE SER MAYOR A LA CANTIDAD DE DFAS QUE HAY SI NO CONTAS LOS ESTADOS FINALES (YA QUE SUPERA LA CANTIDAD POSIBLE DE AUTOMATAS CON ESE CONJUNTO DE ESTADOS FINALES)
    #PERO PORQUE ASI ES LA FORMA???
    #Edit 06-12-2013 7:30AM al parecer Alain esta haciendo esto de manera inconsistente en su cuaderno, habria que analizar bien lq pasa acá
    #Edit 06-12-2023 Creo que esta mal lo que hizo alain, puesto que mi ultimo dfa de 3 estados no lleva a q2 en todos los casos, comentare la linea de abajo
    # dfaNumberSpec = dfaNumberSpec -  ranges2[indexForFinalState]*2 
    """"
    AWANTE CERROOOOO POR FIN KRAJOOOO
    """
    print("Index: ",indexForFinalState)
    #Bugfix ni idea porque pasa
    if stateAmount == finalStateAmount:
        finalStateSet = finalStates.estados_finales_posibles(stateAmount,finalStateAmount)[0]
    else:
        finalStateSet = finalStates.estados_finales_posibles(stateAmount,finalStateAmount)[indexForFinalState]
    print(f"El conjunto de estados finales del automata es : {finalStateSet}")
    print(f"El conjunto de estados del automata es: {states}")
    nbaseTransitions =numpy.base_repr(dfaNumberSpec,stateAmount+1)
    print(f"{dfaNumberSpec} es en base {stateAmount+1} {nbaseTransitions}")
    transitionsModified = nbaseTransitions
    if len(nbaseTransitions) < (stateAmount)*alphabetSize:
        for i in (range((stateAmount)*alphabetSize-len(nbaseTransitions))):
            transitionsModified = f"0{transitionsModified}"
    elif len(nbaseTransitions) > (stateAmount)*alphabetSize:
        for i in (range(len(nbaseTransitions)-(stateAmount)*alphabetSize)):
            transitionsModified = transitionsModified[1:]
    print(transitionsModified)
    transitions = []

    alphabet = diccionario[:alphabetSize]
    # for i in range(alphabetSize*(stateAmount)):
    #     if transitionsModified[i] == '0':
    #         transitions.append(f"∂({states[i%stateAmount]},{alphabet[i%alphabetSize]}) = ⊥")
    #     else:
    #         transitions.append(f"∂({states[i%stateAmount]},{alphabet[i%alphabetSize]}) = q{int(transitionsModified[i])-1}")
    transIndex = 0
    for i in states:
        for j in alphabet:
            if transIndex >= len(transitionsModified):
                break #LEGALMENTE NO ME PUEDO NIO CAER TANTO A PEDAZOS XD
            if transitionsModified[transIndex] == '0':
                transitions.append(f"∂({i},{j}) = ⊥")
            else:
                transitions.append(f"∂({i},{j}) = q{int(transitionsModified[transIndex])-1}")
            transIndex += 1
    for i in transitions:
        print("trans",i)
    return True
# for i in range(1,8888888888888888):
#     print(f"dfa({i},1)")
#     try:
#         generateDfa(i,3)
#     except:
#         print(print(f"dfa({i},3) se rompe"))
#         break

# for i in range(8888888888):
#     a = biyeccion.g_inv(i)
#     print(f"dfa({a[0]},{a[1]})")
#     generateDfa(a[0],a[1])
generateDfa(1180591620717411303424,3)
# generateDfa(2097150,3)