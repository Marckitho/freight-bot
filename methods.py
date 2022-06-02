# Imports
import config as cfg
from unicodedata import normalize

def package(qty, p, product):
    pack = []
    aux = []
    choice = 0

    # Brecar se nulo
    if (qty < 1): return

    # Definir alcance
    if (p > 1): r = p//2
    else: r = p
    
    for i in range(r):
        # Inteiro
        if (qty % (p - i) == 0):
            pack.append([product, qty//(p - i), p - i])
            return pack
        
        # Quebrado
        aux.append([qty//(p - i), p - i])
        aux.append([1, qty % (p - i)])

    for i in range(int(len(aux)/2)):
        if (aux[i * 2][1] - aux[i * 2 + 1][1] < aux[choice * 2][1] - aux[choice * 2 + 1][1]):
            choice = i
    aux[choice * 2].insert(0, product)
    aux[choice * 2 + 1].insert(0, product)
    return aux[choice * 2], aux[choice * 2 + 1]

def applyPackage(array, package):
    if (package != None):
        for i in range(len(package)):
            array.append(package[i])

def getPackages():
    # Imports
    import config as cfg
    import request as rq
    # Declara o array
    p = []

    # Pega as quantidades
    applyPackage(p, package(rq.alba, cfg.pack[0], 0)) # Alba
    applyPackage(p, package(rq.cervia, cfg.pack[1], 1)) # Cervia
    applyPackage(p, package(rq.novara, cfg.pack[2], 2)) # Novara
    applyPackage(p, package(rq.ravenna, cfg.pack[3], 3)) # Ravenna

    return p

def getTotalWeight():
    # Imports
    import config as cfg
    import request as rq
    # Declara o total
    t = 0

    # Pega os pesos por produto
    t += rq.alba * cfg.weight[0] # Alba
    t += rq.cervia * cfg.weight[1] # Cervia
    t += rq.novara * cfg.weight[2] # Novara
    t += rq.ravenna * cfg.weight[3] # Ravenna

    return t

def getTotalQty(packages):
    total = 0

    for i in range(len(packages)):
        total += packages[i][1]

    return total

def cleanStateAcronym(s):
    s = ''.join([i for i in s if not i.isdigit()]) # Retira números
    s = s[:2] # Pega até o segundo caractere
    s = s.upper() # Coloca em maiúsculo
    s = normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII') # Remove acentuação
    return s

def cleanStateName(s):
    s = ''.join([i for i in s if not i.isdigit()]) # Retira números
    s = s.upper() # Coloca em maiúsculo
    s = normalize('NFKD', s).encode('ASCII','ignore').decode('ASCII') # Remove acentuação
    return s

def toStateName(s):
    if (len(s) == 2):
        return cfg.stateName[cfg.stateAcronym.index(cleanStateAcronym(s))]
    else:
        return s

def toStateAcronym(s):
    s = cleanStateName(s)

    if (len(s) > 2):
        return cfg.stateAcronym[cfg.stateName.index(cleanStateName(s))]
    else:
        return s

def convertToMeters(v):
    v = str(v) # Converte pra string
    while (len(v) < 3): # Adiciona zeros no inicio
        v = "0" +v
    v = v[:(len(v) - 2)] +"," +v[(len(v) - 2):] # Adiciona a vírgula
    return v

# DEBUG
# print(package(98, 3, 1))
# print(len(getPackages()))
# print(getTotalQty(getPackages()))


# for index, i in enumerate(getPackages()):
#     print(str(cfg.height[i[0]]))



# print(cfg.stateName.index('AMAPÁ'))