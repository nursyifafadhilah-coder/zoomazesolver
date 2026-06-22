from collections import deque

def bfs(grid, start, end):

    queue = deque([start])
    visited = set()
    parent = {}

    visited.add(start)

    while queue:

        current = queue.popleft()

        if current == end:
            break

        x, y = current

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:

            nx = x + dx
            ny = y + dy

            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):

                if grid[nx][ny] == 0 and (nx, ny) not in visited:

                    visited.add((nx, ny))
                    queue.append((nx, ny))

                    parent[(nx, ny)] = current

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