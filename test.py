def solution(N, road, K):
    answer = 1
    graph = (N + 1) * [(N + 1) * [0]]
    connections = dict()

    # make a graph
    for a, b, c in road:
        if not 0 < graph[a][b] < c:
            graph[a][b] = c
            graph[b][a] = c
        connections.setdefault(a, [])
        connections.setdefault(b, [])
        connections[a].append(b)
        connections[b].append(a)
    print(graph)

    costs = [0] * (N + 1)
    costs = bfs(costs, connections, graph)
    for cost in costs:
        if 0 < cost <= K: answer += 1
    return answer


def bfs(costs, connections, graph):
    unvisited = [1]

    while unvisited != []:
        parent = unvisited.pop(0)
        for child in connections[parent]:
            costs[child] += graph[parent][child]
            connections[parent].remove(child)
            connections[child].remove(parent)
            unvisited.extend(connections[child])
    return costs

solution(5, [[1, 2, 1], [2, 3, 3], [5, 2, 2], [1, 4, 2], [5, 3, 1], [5, 4, 2]], 3)

