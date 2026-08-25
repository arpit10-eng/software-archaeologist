import os
import ast


def detect_dependency_graph(repo_path, files):

    graph = {}

    # =========================================================
    # 1. Get all Python files
    # =========================================================

    python_files = [
        file.replace("\\", "/")
        for file in files
        if file.endswith(".py")
    ]

    # =========================================================
    # 2. Create module -> file mapping
    # =========================================================

    module_map = {}

    for file in python_files:

        normalized_file = file.replace("\\", "/")

        module_path = normalized_file[:-3]

        # Handle __init__.py
        if module_path.endswith("/__init__"):
            module_path = module_path[:-9]

        module_path = module_path.replace("/", ".")

        # Full module path
        module_map[module_path] = normalized_file

        # Support imports starting with app.
        if module_path.startswith("backend."):
            app_module = module_path[len("backend."):]
            module_map[app_module] = normalized_file

    # =========================================================
    # 3. Helper: resolve relative imports
    # =========================================================

    def resolve_relative_import(current_file, module_name, level):

        current_module = current_file[:-3].replace("/", ".")

        # Remove filename from current module
        current_parts = current_module.split(".")

        if current_parts[-1] == "__init__":
            current_parts.pop()
        else:
            current_parts.pop()

        # Move up according to relative import level
        for _ in range(level - 1):
            if current_parts:
                current_parts.pop()

        if module_name:
            current_parts.extend(module_name.split("."))

        candidate = ".".join(current_parts)

        return module_map.get(candidate)

    # =========================================================
    # 4. Helper: resolve normal imports
    # =========================================================

    def resolve_absolute_import(module_name):

        if not module_name:
            return None

        # Exact match
        if module_name in module_map:
            return module_map[module_name]

        # Try parent modules
        parts = module_name.split(".")

        while parts:

            candidate = ".".join(parts)

            if candidate in module_map:
                return module_map[candidate]

            parts.pop()

        return None

    # =========================================================
    # 5. Analyze every Python file
    # =========================================================

    for file in python_files:

        graph[file] = []

        absolute_path = os.path.join(
            repo_path,
            file.replace("/", os.sep)
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

        # =====================================================
        # 6. Detect imports
        # =====================================================

        for node in ast.walk(tree):

            # -------------------------------------------------
            # import x
            # -------------------------------------------------

            if isinstance(node, ast.Import):

                for alias in node.names:

                    dependency = resolve_absolute_import(
                        alias.name
                    )

                    if dependency and dependency != file:

                        graph[file].append(
                            dependency
                        )

            # -------------------------------------------------
            # from x import y
            # -------------------------------------------------

            elif isinstance(node, ast.ImportFrom):

                # Relative import
                if node.level > 0:

                    dependency = resolve_relative_import(
                        file,
                        node.module,
                        node.level
                    )

                # Absolute import
                else:

                    dependency = resolve_absolute_import(
                        node.module
                    )

                if dependency and dependency != file:

                    graph[file].append(
                        dependency
                    )

        # =====================================================
        # 7. Remove duplicate dependencies
        # =====================================================

        graph[file] = sorted(
            set(graph[file])
        )

    return graph