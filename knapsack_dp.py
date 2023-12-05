# Sumber = https://www.geeksforgeeks.org/unbounded-knapsack-repetition-items-allowed/ 

# Python3 program to find maximum 
# achievable value with a knapsack 
# of weight W and multiple instances allowed. 
  
# Returns the maximum value  
# with knapsack of W capacity 
def knapsackdp(W, val, wt): 

    n = len(val)
    # dp[i] is going to store maximum  
    # value with knapsack capacity i. 
    dp = [0 for i in range(W + 1)] 
  
    # Fill dp[] using above recursive formula 
    for i in range(W + 1): 
        for j in range(n): 
            if (wt[j] <= i): 
                dp[i] = max(dp[i], dp[i - wt[j]] + val[j]) 
  
    return dp[W] 
  
# Contoh penggunaan
if __name__ == '__main__':
    # W = 90
    # val = [52, 14, 15, 20, 60] 
    # wt = [37, 20, 10, 23, 39] 

    W = 8
    val = [94, 17, 60, 60, 53] 
    wt = [6, 6, 4, 9, 11]
    print("Result: ", knapsackdp(W, val, wt)) 
  
# This code is contributed by Anant Agarwal. 