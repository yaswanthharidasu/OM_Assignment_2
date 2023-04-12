from utils import *

def cost_to_incidence(n, A):
    c = []
    edges = 0
    edge_mappings = [[-1]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != 0:
                c.append(A[i][j])
                edge_mappings[i][j] = edges
                edge_mappings[j][i] = edges
                edges += 1

    inc = [[0] * edges for _ in range(n)]
    edge_idx = 0

    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != 0:
                inc[i][edge_idx] = 1
                inc[j][edge_idx] = 1
                edge_idx += 1

    return edges, edge_mappings, c, inc

vertices = int(input())
A = []
for i in range(vertices):
    row = list(map(float, input().split()))
    A.append(row)

# tableau consists cost vector, <= constrains, >= constraints
n, mapping, tableau, inc = cost_to_incidence(vertices, A)
b = []
tableau = [tableau]

# ===============================================================================================
# <= constraints
# ===============================================================================================

u = 0 # no.of <= constraints

# 1. xi <= 1 as it takes either 0 or 1
identity_matrix = [[0] * n for _ in range(n)]
identity_matrix_b = [1]*n

for i in range(n):
    identity_matrix[i][i] = 1

tableau.extend(identity_matrix)
b.extend(identity_matrix_b)
u += n

# 2. xe = 2 constraints
tableau.extend(inc)
b.extend([2]*vertices)
u += vertices

# ===============================================================================================
# >= constraints
# ===============================================================================================

v = 0 # no.of >= constraints

for i in range(1, 2**(vertices-1)):
    first = set()
    second = set()
    for j in range(vertices):
        if i & (1 << j):
            first.add(j+1)
        else:
            second.add(j+1)
    
    constraint = [0]*n

    for i in first:
        for j in second:
            constraint[mapping[i-1][j-1]] = 1
    
    tableau.append(constraint)
    b.append(2)
    v += 1

val, basicVars, tableau = twoPhaseSimplex(n, u, v, tableau, b)
    
if val == -1: 
    print("Infeasible")
elif val == 1:
    print("Unbounded")
else :
    cost, x = printAns(n, val, basicVars, tableau)
    print(cost)
    ans = [[0]*vertices for _ in range(vertices)]
    for i in range(0, vertices):
        for j in range(0, vertices):
            edge_num = mapping[i][j]
            if edge_num != -1 and x[edge_num] == 1:
                ans[i][j] = 1
    for i in ans:
        print(*i)
