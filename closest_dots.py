# 제곱거리를 return 하는 함수 
def dist(p1,p2):    
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

# 점들의 list S에서 가장 짧은 제곱거리를 반환하는 함수   
def shortestD(S):   
    if len(S) == 3:
        return min(dist(S[1],S[2]),dist(S[1],S[0]),dist(S[0],S[2]))
    else:
        return dist(S[0],S[1])

#가장 짧은 점 사이 거리 반환하는 함수
def ClosestPair(S):
    if len(S) <= 3:     # 만약 리스트 내 점이 3개 이하라면 가장 짧은 제곱 거리 반환
        return shortestD(S)
    
    mid = len(S)//2     # 중앙 idx 계산
    S_L = S[:mid]       # 중앙 idx를 기준으로 S_L과 S_R로 분할
    S_R = S[mid:]

    Dl = ClosestPair(S_L)   #왼쪽 면적으로 분할 (Dl에 가장 짧은 제곱 거리 초기화)
    Dr = ClosestPair(S_R)   #오른쪽 면적으로 분할 (Dr에 가장 짧은 제곱 거리 초기화)
    d = min(Dl, Dr) # 두 면적의 가장 짧은 제곱 거리 d에 할당

    mid_x = S[mid][0]   # 중앙 idx인 점의 x값 할당

    # 중간 영역의 쌍들을 찾기 위해서는 분할한 지점에서 x 축으로 ±d**0.5 인 범위에 속한 점들만 검색 -> strip 리스트 구성
    strip = [p for p in S if abs((p[0] - mid_x )<d**0.5)] 

    strip = quicksort(strip,1) # strip 리스트를 y좌표 기준 퀵정렬
    Dm = d
    for j in range(i+1, len(strip)):
        if strip[j][1] - strip[i][1] >= d**0.5:  # y좌표 차이가 sqrt(d) 이상이면 종료
            break
        Dm = min(Dm, dist(strip[i], strip[j]))


    return min(d,Dm)  #두 영역 내 가장 짧은 제곱거리 d와 두 영역 사이의 점들 중 가장 짧은 제곱 거리 중 최솟값 반환

   

def quicksort(arr,a):   #퀵 정렬 함수 간단하게 선언(a값에 따라 x기준, y기준 달라짐)
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2][a]             # 중간값을 피벗으로 선택
    left  = [x for x in arr if x[a] < pivot]
    mid   = [x for x in arr if x[a] == pivot]
    right = [x for x in arr if x[a] > pivot]
    return quicksort(left,a) + mid + quicksort(right,a)    

n = int(input())
S = []
for i in range(n):
   t = tuple(map(int, input().split()))
   S.append(t)
S = quicksort(S,0)      # x값을 기준으로 정렬하여 저장
print(ClosestPair(S))   # 가까운 점 한 쌍 출력