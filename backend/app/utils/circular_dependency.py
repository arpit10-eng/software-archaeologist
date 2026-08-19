def detect_circular_dependencies(dependency_graph):
    """
    Detect circular dependencies of any length
    using the existing dependency graph.

    Example:

    A -> B
    B -> C
    C -> A

    Result:

    found = True
    cycle = [A, B, C, A]
    """

    cycles = []
    visited = set()
    recursion_stack = set()

    def normalize_dependency(current_file, dependency):
        """
        Convert dependency references into the exact
        graph key whenever possible.
        """

        if dependency in dependency_graph:
            return dependency

        for candidate in dependency_graph:

            if candidate.endswith(dependency):
                return candidate

        return None

    def dfs(node, current_path):

        visited.add(node)
        recursion_stack.add(node)
        current_path.append(node)

        for dependency in dependency_graph.get(node, []):

            dependency_node = normalize_dependency(
                node,
                dependency
            )

            if dependency_node is None:
                continue

            # ------------------------------------------------
            # Found a cycle
            # ------------------------------------------------

            if dependency_node in recursion_stack:

                cycle_start = current_path.index(
                    dependency_node
                )

                cycle = (
                    current_path[cycle_start:]
                    + [dependency_node]
                )

                # Avoid duplicate cycles
                if cycle not in cycles:
                    cycles.append(cycle)

            # ------------------------------------------------
            # Continue searching
            # ------------------------------------------------

            elif dependency_node not in visited:

                dfs(
                    dependency_node,
                    current_path
                )

        current_path.pop()
        recursion_stack.remove(node)

    # --------------------------------------------------------
    # Start DFS from every file
    # --------------------------------------------------------

    for node in dependency_graph:

        if node not in visited:

            dfs(
                node,
                []
            )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return {
        "found": len(cycles) > 0,
        "cycle_count": len(cycles),
        "cycles": cycles,
        "status": (
            "Problem"
            if cycles
            else "Healthy"
        ),
        "message": (
            f"{len(cycles)} circular dependency "
            f"cycle(s) detected."
            if cycles
            else "No circular dependencies detected."
        )
    }