def dfs(current, depth, currentCost, K):  # DFS 기반 백트래킹 함수
    global best

    # 현재 비용이 제한값 K를 넘으면 더 탐색할 필요 없음 (가지치기)
    if currentCost > K:
        return
    
    # 현재 비용이 이미 찾은 최소 비용(best) 이상이면 탐색 중단 (가지치기)
    if currentCost >= best:
        return
    
    # 모든 도시를 방문한 경우 (depth == N)
    if depth == N:
        returnCost = cost[current][0]  # 마지막 도시에서 출발 도시(0)로 돌아가는 비용

        # 돌아가는 길이 없으면 실패
        if returnCost == 0:
            return
        
        totalCost = currentCost + returnCost  # 전체 비용 계산

        # 전체 비용이 K 이하일 경우 best 갱신
        if totalCost <= K:
            best = min(best, totalCost)
        return
    
    # 아직 방문하지 않은 도시들 탐색
    for nextCity in range(N):
        # 아직 방문하지 않았고, current -> next 경로가 존재하면 탐색 진행
        if not visited[nextCity] and cost[current][nextCity] > 0:
            visited[nextCity] = True  # 방문 처리
            dfs(nextCity, depth + 1, currentCost + cost[current][nextCity], K)
            visited[nextCity] = False  # 백트래킹(상태 복구)


# 입력 처리
N, K = map(int, input().split())  # 도시 수 N, 비용 제한 K
cost = [list(map(int, input().split())) for _ in range(N)]  # 비용 행렬 입력

best = 10000  # 비교를 위한 매우 큰 초기값
visited = [False] * N  # 방문 여부 배열

visited[0] = True  # 출발 도시는 0번 도시로 고정
dfs(0, 1, 0, K)  # DFS 탐색 시작 (current=0, depth=1, 비용=0)

# 결과 출력
if best == 10000:  # 갱신되지 않았다면 조건 만족하는 경로 없음
    print(-1)
else:
    print(best)
