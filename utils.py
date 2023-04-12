import copy
from tabulate import tabulate

def readInput():
    n, u, v = map(int, input().split())

    # Cost vector
    tableau = []
    tableau.append(list(map(float, input().split())))

    # <= constraints 
    for i in range(u):
        tableau.append(list(map(float, input().split())))

    # >= constraints 
    for i in range(v):
        tableau.append(list(map(float, input().split())))

    # RHS vector for all constraints
    b = list(map(float, input().split()))

    return n, u, v, tableau, b


def solve(basicVars, basicVarsList, tableau):
    # Solve until there is no positive value in the first row .i.e. optimal solution is reached
    while True:
        # Find the entering variable
        enteringInd = -1
        enteringVal = float('-inf')
        for i in range(len(tableau[0])-1):
            if tableau[0][i] > enteringVal:
                enteringVal = round(tableau[0][i], 7)
                enteringInd = i

        if enteringVal <= 0:
            break

        # Find the exiting variable
        exitingInd = -1
        exitingVal = float('inf')

        for i in range(1, len(tableau)):
            num = tableau[i][-1]
            den = tableau[i][enteringInd]
            if den <= 0:
                continue
            ratio = num/den
            if ratio <= exitingVal:
                exitingInd = i
                exitingVal = ratio

        basicVars[exitingInd] = enteringInd+1
        # Unbounded case
        if exitingInd == -1:
            return 1, basicVars, tableau
        
        # Cycling case
        curr = frozenset(basicVars)
        # print("================================")
        # print("Comparing ", curr)
        for prev in basicVarsList:
            if curr == prev:
                # print("============hereeee====================")
                return 2, basicVars, tableau
        # print("=================out=====================================")
        basicVarsList.add(curr)
        pivot = tableau[exitingInd][enteringInd]
        pivotRow = copy.deepcopy(tableau[exitingInd])

        for j in range(len(tableau[exitingInd])):
            tableau[exitingInd][j] /= pivot

        # Updating the tableau
        # new value = old value - (corresponding key row val * col val) / pivot ele
        for i in range(len(tableau)):
            pivotColVal = tableau[i][enteringInd]
            # print(pivotColVal)
            for j in range(len(tableau[i])):
                if i == exitingInd:
                    continue
                else:
                    tableau[i][j] -= pivotColVal * tableau[exitingInd][j]


        # print("==================================================")
        # print(basicVars)
        # for i in range(len(tableau)):
        #     print(*tableau[i], sep='\t')
        # print("==================================================")

    return 0, basicVars, tableau
        

def blandsRule(basicVars, tableau):
     # Solve until there is no positive value in the first row .i.e. optimal solution is reached
    while True:
        # Find the entering variable
        enteringInd = -1
        for i in range(len(tableau[0])-1):
            if tableau[0][i] > 0:
                enteringInd = i
                break

        if enteringInd == -1:
            break

        # Find the exiting variable
        exitingInd = -1
        exitingVal = float('inf')

        for i in range(1, len(tableau)):
            num = tableau[i][-1]
            den = tableau[i][enteringInd]
            if den <= 0:
                continue
            ratio = num/den
            if ratio < exitingVal:
                exitingInd = i
                exitingVal = ratio
            elif ratio == exitingVal:
                continue
        

        basicVars[exitingInd] = enteringInd+1

        # Unbounded case
        if exitingInd == -1:
            return 1, basicVars, tableau

        pivot = tableau[exitingInd][enteringInd]
        pivotRow = copy.deepcopy(tableau[exitingInd])

        # Updating the tableau
        # new value = old value - (corresponding key row val * col val) / pivot ele
        for i in range(len(tableau)):
            pivotColVal = tableau[i][enteringInd]
            # print(pivotColVal)
            for j in range(len(tableau[i])):
                if i == exitingInd:
                    tableau[i][j] = tableau[i][j]/pivot
                else:
                    tableau[i][j] = tableau[i][j] - (pivotColVal * pivotRow[j])/pivot


        # print("==================================================")
        # print(basicVars)
        # print(tabulate(tableau))
        # print("==================================================")

    return 0, basicVars, tableau
   

def simplex(n, u, tableau, b):
    # Adding -1 for the first row
    basicVars = [-1]

    # Add zeroes and b value for each row
    zeroes = [0]*(u+1)
    tableau[0].extend(zeroes)

    for i in range(1, u+1):
        zeroes = [0]*(u+1)
        zeroes[i-1] = 1
        zeroes[-1] = b[i-1]
        tableau[i].extend(zeroes)
        basicVars.append(n+i)

    tableau[0] = list(map(lambda x: -1 * x, tableau[0]))
    tab = copy.deepcopy(tableau)
    bas = copy.deepcopy(basicVars)

    # print("+++++++++++++++++++++++++++++++++++++++++")
    # print(basicVars)
    # for i in range(len(tableau)):
    #     print(*tableau[i], sep='\t')
    # print("+++++++++++++++++++++++++++++++++++++++++")
    basicVarsList = set()
    # basicVarsList.add(frozenset(basicVars))
    val, basicVars, tableau = solve(basicVars, basicVarsList, tableau) 

    if val == 2:
        # print("+++++++++++++++++++++++++++++++++++++++++")
        # print(bas)
        # print(tabulate(tab))
        # print("+++++++++++++++++++++++++++++++++++++++++")
        _, basicVars, tableau = blandsRule(bas, tab)
        
    return val, basicVars, tableau


def twoPhaseSimplex(n, u, v, tableau, b):
    # print(u, v)
    # print(b)
    # for i in tableau:
    #     print(*i)

    # Adding -1 for the first row
    basicVars = [-1]

    # Add zeroes and b value for the first row
    zeroes = [0]*(u+v+v+1)
    tableau[0].extend(zeroes)

    # Artificial and basic variables
    ac = 1
    basicVars = [-1]
    artificialVars = []

    # Adding slack and surplus variables
    for i in range(1, u+v+1):
        zeroes = [0]*(u+v)
        if i>u:
            zeroes[i-1] = -1
        else:
            zeroes[i-1] = 1
            basicVars.append(n+i)

        tableau[i].extend(zeroes)


    # Adding artificial variables
    for i in range(1, len(tableau)):
        zeroes = [0]*(v+1)
        if i>u:
            zeroes[i-u-1] = 1
            artificialVars.append(n+u+v+ac)
            basicVars.append(n+u+v+ac)
            ac += 1

        zeroes[-1] = b[i-1]
        tableau[i].extend(zeroes)

    tableau[0] = list(map(lambda x: -1 * x, tableau[0]))
    tab = copy.deepcopy(tableau)
    bas = copy.deepcopy(basicVars)

    zeroes = [0]*(len(tableau[0]))
    for i in artificialVars:
        zeroes[i-1] = -1
    tableau[0] = zeroes
        
    
    # print("==================================================")
    # print("Basic variables", basicVars)
    # print("Artificial variables", artificialVars)
    # print(tabulate(tableau))
    # print("==================================================")


    # ============================================================================================= 
    # Phase 1: 
    # ============================================================================================= 
    # First make sure that first row values are zeroes for the basic variables
    for i in range(len(tableau)):
        if basicVars[i] not in artificialVars:
            continue
        for j in range(len(tableau[0])):
            tableau[0][j] += tableau[i][j]

    basicVarsList = set()
    # basicVarsList.add(frozenset(basicVars))
    val, basicVars, tableau = solve(basicVars, basicVarsList, tableau)
    
    if val == 1:
        return -1, basicVars, tableau 
    elif val == 2:
        _, basicVars, tableau = blandsRule(bas, tab)

    # print(basicVars)
    # print(tabulate(tableau))

    # print("++++++++++++++++++=Phase -1 Done+++++++++++++++++++++++++++")
    # ============================================================================================= 
    # Phase 2: 
    # ============================================================================================= 
    
    # print(tableau[0][-1], round(tableau[0][-1], 7))
    if round(tableau[0][-1], 7) != 0:
        return -1, basicVars, tableau
    else:
        # Check if there is any artificial variable in the basic variable list
        found = []
        for i in basicVars:
            if i in artificialVars:
                found.append(i)
        
        # There are no artificial variables in the basic variables
        if len(found) == 0:
            tableau[0] = tab[0]
            # Drop the aritificial variable cols
            newTableau = []
            for i in range(0, len(tableau)):
                row = []
                for j in range(0, len(tableau[0])):
                    if j+1 in artificialVars:
                        continue
                    row.append(tableau[i][j])
                newTableau.append(row)
            tableau = newTableau
        else:
            # Drop artificial variables cols and basic variable values whose value is negative
            oldFirstRow = copy.deepcopy(tableau[0])
            tableau[0] = tab[0]
            
            newTableau = []
            for i in range(0, len(tableau)):
                row = []
                for j in range(0, len(tableau[0])):
                    if j+1 in artificialVars and j+1 not in found:
                        continue
                    if j+1 not in artificialVars and oldFirstRow[j] < 0:
                        continue
                    row.append(tableau[i][j])
                newTableau.append(row)
            tableau = newTableau

        # print("========================Before==========================")
        # print("Basic variables", basicVars)
        # print(tabulate(tableau))
        # print("==================================================")

        # First make sure that first row values are zeroes for the basic variables
        # firstRow = copy.deepcopy(tableau[0])
        # for i in range(1,len(basicVars)):
        #     for j in range(len(tableau[0])):
        #         tableau[0][j] += (tableau[i][j] * (-1 * firstRow[i-1]))
        for j in range(len(tableau[0])):
            if j+1 in basicVars and tableau[0][j] != 0:
                # print(j)
                # Find i in that column
                idx = -1
                for i in range(1,len(tableau)):
                    if tableau[i][j] == 1:
                        idx = i
                        break
                # print(j, idx)
                val = tableau[0][j]
                for j in range(len(tableau[0])):
                    tableau[0][j] += (tableau[idx][j] * (-1*val))


        # print("======================After============================")
        # print("Basic variables", basicVars)
        # print(tabulate(tableau))
        # print("==================================================")


        basicVarsList = set()
        # basicVarsList.add(frozenset(basicVars))
        val, basicVars, tableau = solve(basicVars, basicVarsList, tableau)

        tab = copy.deepcopy(tableau)
        bas = copy.deepcopy(basicVars)

        if val == 2:
            _, basicVars, tableau = blandsRule(bas, tab)
        
        return val, basicVars, tableau


def printAns(n, val, basicVars, tableau, flag=True):
    if val == 2:
        print("Cycling detected") 
    cost = (round(tableau[0][-1], 7))
    ans = [0]*n
    for i in range(1, len(tableau)):
        if basicVars[i]-1 < n:
            ans[basicVars[i]-1] = round(tableau[i][-1], 7)
    if flag:
        ans = list(map(int, ans))
    # print(*ans)
    return cost, ans 