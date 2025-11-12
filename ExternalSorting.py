# 두 리스트 합병정렬 메서드
def merge(list1,list2):
    result = []
    i, j = 0, 0  

    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1

    
    result += list1[i:]
    result += list2[j:]
    return result

# 2차원 리스트내 리스트 합병 정렬 메서드
def merge_2d(arr2d):
    
    result = arr2d[0]
    for i in range(1, len(arr2d)):
        result = merge(result, arr2d[i])
    return result

# 외부 정렬 메서드
def ExtSort(array,N,M,p):
    # array를 크기 M의 run들로 정렬하여 runs에 저장
    runs = [sorted(array[i:i+M]) for i in range(0,N,M)]

    # R = run의 개수
    R = len(runs)
    
    # 병합 개수 K 
    K = 0

    # 최대 p개의 run들을 병합 정렬해 새 run 한개로 만들기
    while len(runs) > 1:
        K+=1
        new_runs = []
        for i in range(0, len(runs), p):
            sortedarray = merge_2d(runs[i:i+p])
            new_runs.append(sortedarray)
        runs = new_runs
    sortedresult = runs[0]
    T = K+1
    return R, K, T, sortedresult
    

N, M, p = map(int, input().split())
array = list(map(int, input().split()))

if N % M == 0:
    R = N//M
else:
    R = N//M + 1
arry = []
R,K,T,result = ExtSort(array,N,M,p)

# 출력
print(R)
print(K,T)
print(*result)