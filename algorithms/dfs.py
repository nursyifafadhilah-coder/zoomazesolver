def dfs(grid, start, end, visited=None, path=None):

    if visited is None:
        visited = set()

    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    if start == end:
        return path.copy()

    x, y = start

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    for dx, dy in directions:

        nx = x + dx
        ny = y + dy

        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):

            nxt = (nx, ny)

            if nxt not in visited:

                if grid[nx][ny] == 0:

                    result = dfs(
                        grid,
                        nxt,
                        end,
                        visited,
                        path
                    )

                    if result:
                        return result

    path.pop()
    return None