import os
import ast


def detect_dependency_graph(repo_path, files):

    graph = {}

    # --------------------------------------------------
    # 1. Get Python files
    # --------------------------------------------------

    python_files = [
        file.replace("\\", "/")
        for file in files
        if file.endswith(".py")
    ]

    # --------------------------------------------------
    # 2. Create module -> file mapping
    # --------------------------------------------------

    module_map = {}

    for file in python_files:

        normalized_file = file.replace("\\", "/")

        module_path = normalized_file[:-3]

        if module_path.endswith("/__init__"):
            module_path = module_path[:-9]

        module_path = module_path.replace("/", ".")

        # Full module path
        module_map[module_path] = normalized_file

        # Map:
        # backend.app.services.github_services
        #
        # to:
        # app.services.github_services

        if module_path.startswith("backend."):

            app_module = module_path[
                len("backend."):]
            
            module_map[app_module] = normalized_file

    # --------------------------------------------------
    # 3. Analyze every Python file
    # --------------------------------------------------

    for file in python_files:

        graph[file] = []

        absolute_path = os.path.join(
            repo_path,
            file
        )

        try:

            with open(
                absolute_path,
                "r",
                encoding="utf-8"
            ) as f:

                source = f.read()

            tree = ast.parse(source)

        except (OSError, SyntaxError):

            continue

        # --------------------------------------------------
        # 4. Detect imports
        # --------------------------------------------------

        for node in ast.walk(tree):

            # ----------------------------------------------
            # import x
            # ----------------------------------------------

            if isinstance(node, ast.Import):

                for alias in node.names:

                    module_name = alias.name

                    if module_name in module_map:

                        dependency = module_map[
                            module_name
                        ]

                        if dependency != file:

                            graph[file].append(
                                dependency
                            )

            # ----------------------------------------------
            # from x import y
            # ----------------------------------------------

            elif isinstance(node, ast.ImportFrom):

                if node.module is None:
                    continue

                module_name = node.module

                if module_name in module_map:

                    dependency = module_map[
                        module_name
                    ]

                    if dependency != file:

                        graph[file].append(
                            dependency
                        )

                else:

                    # Try parent modules

                    parts = module_name.split(".")

                    while parts:

                        candidate = ".".join(parts)

                        if candidate in module_map:

                            dependency = module_map[
                                candidate
                            ]

                            if dependency != file:

                                graph[file].append(
                                    dependency
                                )

                            break

                        parts.pop()

        # --------------------------------------------------
        # 5. Remove duplicate dependencies
        # --------------------------------------------------

        graph[file] = sorted(
            set(graph[file])
        )

    return graph