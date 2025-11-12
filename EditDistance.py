# 두 문자열 입력받기
Sstr = str(input())
Tstr = str(input())

# 2차원 리스트 행, 열 길이 설정
row = len(Tstr)+1
col = len(Sstr)+1

# 2차원 리스트 0으로 초기화
E = [[0 for _ in range(row)] 
     for _ in range(col)]

# 2차원 리스트 1번째 행, 열 초기화
for i in range(row):
    E[0][i] = i
for j in range(col):
    E[j][0] = j

# 2차원 리스트의 원소를 위, 옆, 대각선 원소에 cost 고려하여 더한 값 중 최솟값으로 초기화
for i in range(1,col):
    for j in range(1,row):
        if(Sstr[i-1] == Tstr[j-1]):
            cost = 0
        else:
            cost = 1
        E[i][j] = min(
            E[i-1][j-1] + cost, 
            E[i][j-1]+1, 
            E[i-1][j]+1
            )

# 출력
print(E[col-1][row-1])