import os 

def detect_circular_dependencies(dependency_graph):

    cycles = []

    for file, dependencies in dependency_graph.items():

        for dependency in dependencies:

            dependency_path = None

            for candidate in dependency_graph.keys():

                if candidate.endswith(dependency):
                    dependency_path = candidate
                    break

            if dependency_path:

                if os.path.basename(file) in dependency_graph[dependency_path]:

                    cycles.append([
                        os.path.basename(file),
                        dependency,
                        os.path.basename(file)
                    ])

    return {
        "found": len(cycles) > 0,
        "cycles": cycles
    }