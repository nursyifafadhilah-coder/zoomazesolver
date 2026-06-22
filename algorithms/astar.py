import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, end):

    open_list = []
    heapq.heappush(open_list, (0, start))

    g = {start: 0}
    parent = {}


    while open_list:

        _, current = heapq.heappop(open_list)

        if current == end:
            break

        x, y = current

        for dx, dy in [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if grid[nx][ny] == 0:
                    nxt = (nx, ny)
                    new_g = g[current] + 1
                    if nxt not in g or new_g < g[nxt]:

                        g[nxt] = new_g

                        f = new_g + heuristic(
                            nxt,
                            end
                        )
                        heapq.heappush(
                            open_list,
                            (f, nxt)
                        )
                        parent[nxt] = current

    # ===== RECONSTRUCT PATH =====

    path = []

    if end in parent or end == start:
        current = end
        while current != start:

            path.append(current)
            current = parent[current]

        path.append(start)
        
        path.reverse()

    return path