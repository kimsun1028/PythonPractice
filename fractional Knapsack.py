n,c= map(int,input().split())   # n,c 입력 받기
array = []                      # value, weight, 비율 저장할 list
parray = []                     # 출력값을 저장할 list   
for _ in range(n):              
    weight, value = map(int,input().split())    # weight, value 입력 받기
    ratio = value / weight                      # 비율 계산
    array.append((weight,value,ratio))          # weight, value, ratio 튜플로 array에 입력
newarray = sorted(array, key =lambda x : x[2], reverse=True)    # key = ratio로 오름차순 정렬
for row in newarray:
    weight, value, ratio = row
    if weight <= c:         # 최고가치 물건의 무게<=가방 공간이면
        c = c - weight      # 가방 공간 줄이기
        parray.append(1)    # 전부 들어가므로 1 삽입
    else :                              # 가방 공간이 더 적으면
        remain = value - c*ratio        
        remainratio = remain / value    # 남은 비율 계산
        c = 0                           # 가방 공간은 0으로 만들기
        parray.append(1-remainratio)    # 넣은 비율 삽입
    
    if c == 0:      # 가방 공간이 0이면 종료
        break

while len(parray) < n:  # 종료 이후 넣지 못한 물건 비율 = 0이므로 0 삽입
    parray.append(0)


for i in range(len(parray)):        #parray값에 따라 출력
    if parray[i] == 1:
        print("1.000000", end='')
    elif parray[i] == 0:
        print("0.000000", end='')
    else:
        print("%.6f" % parray[i], end='')
    if i != len(parray) - 1:
        print(' ', end='')
print()