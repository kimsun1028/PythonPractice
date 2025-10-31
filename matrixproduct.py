n = int(input())
arry = []
for i in range(n):
    lst = list(map(int, input().split()))
    arry.append(lst)

inf = 100000
c = []
for i in range(n):
    if (i == 0):
        c.append(arry[i][0])
    c.append(arry[i][1])

S = [[inf for j in range (n)]for i in range(n)]
for i in range(n):
    S[i][i] = 0


for d in range(n):
    for i in range(n-d):
        j = i+d
        for k in range(i,j):
            S[i][j] = min(S[i][j],(S[i][k]+S[k+1][j]+c[i]*c[k+1]*c[j+1]))

print(S[0][n-1])