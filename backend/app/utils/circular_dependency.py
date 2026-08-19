def detect_circular_dependencies(dependency_graph):

    cycles = []
    visited = set()
    recursion_stack = set()

    def dfs(file, path):

        if file in recursion_stack:

            cycle_start = path.index(file)
            cycle = path[cycle_start:] + [file]

            if cycle not in cycles:
                cycles.append(cycle)

            return

        if file in visited:
            return

        visited.add(file)
        recursion_stack.add(file)

        for dependency in dependency_graph.get(file, []):

            dfs(
                dependency,
                path + [dependency]
            )

        recursion_stack.remove(file)

    # Run DFS for every file
    for file in dependency_graph:

        if file not in visited:

            dfs(
                file,
                [file]
            )

    return {
        "found": len(cycles) > 0,
        "cycles": cycles
    }