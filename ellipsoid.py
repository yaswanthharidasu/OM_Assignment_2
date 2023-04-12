import numpy as np
import math

# removes all warnings
np.seterr(all='ignore')

def ellipsoid(m, n, v, V, xt, Dt, A, b):
    try:
        iterations = math.ceil(2 * (n + 1) * math.log(V / v))
    except:
        iterations = 10**7
    
    i = 0
    while i < iterations:
        # Find a constraint that satisfies a.T xt < b
        idx = None
        for j in range(A.shape[0]):
            if np.dot(A[j].T, xt) < b[j]:
                idx = j
                break

            if j >= m and np.dot(A[j].T, xt) <= b[j]:
                idx = j
                break

        if idx is not None:
            ai = np.reshape(A[idx],(n,1))
            numerator = np.dot(Dt, ai)  
            denominator = np.dot(ai.T, np.dot(Dt, ai))[0][0]
            xt = xt + (1 / (n + 1)) * (numerator / np.sqrt(denominator))
            numerator = np.dot(np.dot(np.dot(Dt, ai), ai.T), Dt)
            Dt = (n**2 / ((n**2) - 1)) * (Dt - ((2 / (n + 1)) * (numerator / denominator)))
        else:
            return ["found", xt, Dt]
        
        i += 1

    return ["empty"]

# Read input
n, m = map(int, input().split()) 
c = np.array(list(map(float, input().split())), dtype=np.longdouble)
A = np.zeros((m, n), dtype=np.longdouble)  
for i in range(m):
    A[i] = np.array(list(map(float, input().split())), dtype=np.longdouble)  
b = np.array(list(map(float, input().split())), dtype=np.longdouble)  

# Add constraints x > 0 to A and b
A = np.vstack((A, np.eye(n, dtype=np.longdouble)))  
b = np.hstack((b, np.zeros(n, dtype=np.longdouble)))

# Initial ellipsoid has center at origin and D = n(nU)^(2n)I
U = max(np.max(np.abs(A)), np.max(np.abs(b)))
I = np.eye(n, dtype=np.longdouble)

x0 = np.zeros((n,1), dtype=np.longdouble)
D0 = n * (n * U) ** (2 * n) * I

# Calculate V and v based on the formulae
V = ((2 * n) ** n) * ((n * U) ** (n ** 2))
v = (n ** (-n)) * ((n * U) ** (-(n ** 2) * (n + 1)))

# pertubration
epsilon = (1 / (2 * (n + 1))) * (((n + 1) * U) ** (-(n + 1)))  
e = np.ones((m+n), dtype=np.longdouble)  
b = b - (epsilon * e) 

feasible = ellipsoid(m+n, n, v, V, x0, D0, A, b)

if feasible[0] == "empty" or np.isnan(feasible[1]).any() or np.isnan(feasible[2]).any():
    print("Infeasible") 
else:
    x0 = feasible[1]
    D0 = feasible[2]
    # Add the constraint c.T x < c.T x0
    
    while True:
        newA = np.vstack((A, -c.T))
        rhs = np.dot(c.T, x0)
        newb = np.hstack((b, -rhs))
        feasible = ellipsoid(m+n, n, v, V, x0, D0, newA, newb)

        if feasible[0] == "empty" or np.isnan(feasible[1]).any() or np.isnan(feasible[2]).any():
            print(round(rhs[0], 3))
            ans = [round(i[0], 3) for i in x0]
            print(*ans)
            break
        else:
            x0 = feasible[1]
            D0 = feasible[2]
