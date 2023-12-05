import math

def knapsackbnb(W, val, wt):

    # Step 1: Initialize
    barang = list(zip(val, wt))

    #Eliminate dominated items according to Procedure 1.
    N = list(range(len(barang)))
    j = 0
    while j < len(N) - 1:
        k = j + 1
        while k < len(N):
            wj, vj = barang[N[j]][1], barang[N[j]][0]
            wk, vk = barang[N[k]][1], barang[N[k]][0]
            if math.floor(wk / wj) * vj >= vk:
                N.pop(k)
            elif math.floor(wj / wk) * vk >= vj:
                N.pop(j)
                k = len(N)
            else:
                k += 1
        j += 1
    barang = [barang[i] for i in N]

    # Sort the non-dominated items according to decreasing vi/wi ratios.
    barang.sort(key=lambda i: i[0] / i[1], reverse=True)

    x = [0 for i in range(len(barang))]
    x_topi = [0 for i in range(len(barang))]
    i = 0 # index mulai dari 0
    z_topi = 0

    # Initialize empty sparse matrix M.
    M = [[0 for i in range(W + 1)] for j in range(len(barang))]

    x[i] = math.floor(W / barang[i][1])
    V_N = barang[i][0] * x[i]
    W_1 = W - barang[i][1] * x[i]

    # Calculate U
    U = cal_upper_bound(barang, W_1, V_N, i)

    m = [min(barang[j][1] for j, _ in enumerate(barang) if j > i) if any(j > i for j, _ in enumerate(barang)) else float('inf') for i, _ in enumerate(barang)]

    next = 2

    # Step 5: Finish
    # next = 5
    while next != 5:

        # Step 2: Develop
        if next == 2:
            M, barang, x, i, V_N, W_1, next, z_topi, x_topi = develop(M, barang, x, i, V_N, W_1, U, m, z_topi, x_topi)

        # Step 3: Backtrack
        if next == 3:
            M, barang, x, i, V_N, W_1, next, z_topi, x_topi = backtrack(M, barang, x, i, V_N, W_1, m, z_topi, x_topi)

        # Step 4: Replace
        if next == 4:
            M, barang, x, i, V_N, W_1, next, z_topi, x_topi = replace(M, barang, x, i, V_N, W_1, m, z_topi, x_topi)

    return z_topi, x_topi

def develop(M, barang, x, i, V_N, W_1, U, m, z_topi, x_topi):
    if W_1 < m[i]:
        if z_topi < V_N:
            z_topi = V_N
            x_topi = x[:]
            if z_topi == U:
                # Go to Step 5
                return M, barang, x, i, V_N, W_1, 5, z_topi, x_topi
        # Go to Step 3
        return M, barang, x, i, V_N, W_1, 3, z_topi, x_topi
    j = find_min_j(barang, W_1, i)
    if (V_N + cal_upper_bound(barang, W_1, V_N, j) <= z_topi) or (M[i][W_1] >= V_N):
        # Go to Step 3
        return M, barang, x, i, V_N, W_1, 3, z_topi, x_topi
    x[j] = math.floor(W_1 / barang[j][1])
    V_N += barang[j][0] * x[j]
    W_1 -= barang[j][1] * x[j]
    M[i][W_1] = V_N
    i = j
    # Go to Step 2
    return M, barang, x, i, V_N, W_1, 2, z_topi, x_topi

def backtrack(M, barang, x, i, V_N, W_1, m, z_topi, x_topi):
    j = find_max_j(x,i)
    if j < 1:
        # Go to Step 5
        return M, barang, x, i, V_N, W_1, 5, z_topi, x_topi
    i = j
    x[i] -= 1
    V_N -= barang[i][0]
    W_1 += barang[i][1]
    if W_1 < m[i]:
        # Go to Step 3
        return M, barang, x, i, V_N, W_1, 3, z_topi, x_topi
    if V_N + math.floor(W_1 * barang[i + 1][0] / barang[i + 1][1]) <= z_topi:
        V_N -= barang[i][0] * x[i]
        W_1 += barang[i][1] * x[i]
        x[i] = 0
        # Go to Step 3
        return M, barang, x, i, V_N, W_1, 3, z_topi, x_topi
    if W_1 >= m[i]:
        # Go to Step 2
        return M, barang, x, i, V_N, W_1, 2, z_topi, x_topi

# Replace a jth item with an hth item
def replace(M, barang, x, i, V_N, W_1, m, z_topi, x_topi):
    j = i
    h = j + 1
    if z_topi >= V_N + math.floor(W_1 * barang[h][0] / barang[h][1]):
        # Go to Step 3
        return M, barang, x, i, V_N, W_1, 3, z_topi, x_topi
    if barang[h][1] >= barang[j][1]:
        if (barang[h][1] == barang[j][1]) or (barang[h][1] > W_1) or (z_topi >= V_N + barang[h][0]):
            h += 1
            # Go to Step 4
            return M, barang, x, i, V_N, W_1, 4, z_topi, x_topi
        z_topi = V_N + barang[h][0]
        x_topi = x[:]
        x[h] = 1
        if z_topi == cal_upper_bound(barang, W_1, V_N, h):
            # Go to Step 5
            return M, barang, x, i, V_N, W_1, 5, z_topi, x_topi  
        j = h
        h += 1
        # Go to Step 4
        return M, barang, x, i, V_N, W_1, 4, z_topi, x_topi
    if W_1 - barang[h][1] < m[h - 1]:
        h += 1
        # Go to Step 4
        return M, barang, x, i, V_N, W_1, 4, z_topi, x_topi
    i = h
    x[i] = W_1 // barang[i][1]
    V_N += barang[i][0] * x[i]
    W_1 -= barang[i][1] * x[i]
    # Go to Step 2
    return M, barang, x, i, V_N, W_1, 2, z_topi, x_topi

def cal_upper_bound(barang, W_1, V_N, i):
    if i + 2 >= len(barang):
        return V_N
    v1, w1 = barang[i]
    v2, w2 = barang[i + 1]
    v3, w3 = barang[i + 2]
    z_1 = V_N + math.floor(W_1 / w2) * v2
    W_2 = W_1 - math.floor(W_1 / w2) * w2
    U_1 = z_1 + math.floor(W_2 * v3 / w3)
    U_2 = z_1 + math.floor(((W_2 + math.ceil((1 / w1) * (w2 - W_2)) * w1)* v2 / w2) - math.ceil((1 / w1) * (w2 - W_2)) * v1)
    U = max(U_1, U_2)
    return U

def find_max_j(x, i):
    # Find max j such that j<=i and xj>0
    max_j = []
    for j in range(i + 1):
        if x[j] > 0 and j<=i:
            max_j.append(j)
    if len(max_j) == 0:
        return -1
    return max(max_j)
    
def find_min_j(barang, W_1, i):
    # Find min j such that j>i and wj<=W'
    min_j = []
    for j in range(i + 1, len(barang)):
        if barang[j][1] <= W_1 and j>i:
            min_j.append(j)
    if len(min_j) == 0:
        return -1
    return (min(min_j))

# Contoh penggunaan
if __name__ == '__main__':
    W = 90
    val = [52, 14, 15, 20, 60] 
    wt = [37, 20, 10, 23, 39] 
    barang = list(zip(val, wt))

    print("barang:", barang)
    z_topi, x_topi = knapsackbnb(W, val, wt)

    print("best solution:", z_topi)
    print("best solution value:", x_topi)