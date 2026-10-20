"""AST guards shared by the six subcomponent test entrypoints."""

import ast
import sys

import mp_ports

SOURCES = {
    "ports": {"__init__.py", "types.py", "protocols.py", "records.py", "forge.py", "agents.py",
              "contract_records.py", "contract_forge.py", "contract_agents.py"},
    "story": {"__init__.py"}, "packet": {"__init__.py"}, "review": {"__init__.py"},
    "merge": {"__init__.py"}, "slice": {"__init__.py", "wiring.py", "orchestrator.py"},
}
PUBLIC = {"mp_story": "load", "mp_packet": "build", "mp_review": "collect", "mp_merge": "decide"}
FORBIDDEN = {"subprocess", "socket", "urllib", "http", "requests", "time", "datetime", "random", "uuid"}


def source_paths(root):
    paths = sorted((root / f"mp_{root.name}").rglob("*.py"))
    assert {path.name for path in paths} == SOURCES[root.name]
    assert len(paths) == len(SOURCES[root.name]) > 0
    return paths


def imports(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield node, alias.name, None
        elif isinstance(node, ast.ImportFrom):
            yield node, node.module or "", {alias.name for alias in node.names}


def check_import(root, path, node, module, names):
    own = f"mp_{root.name}"
    head = module.split(".")[0]
    if isinstance(node, ast.ImportFrom) and node.level:
        assert node.level == 1, (path, module, node.level)
        local = {p.stem for p in source_paths(root)}
        assert (head in local if module else names <= local), (path, module, names)
    elif path.is_relative_to(root / "tests") and head in {"pytest", "mp_examples", "mp_checks"}:
        return
    elif head == "mp_ports" and own != "mp_ports":
        assert module == "mp_ports", (path, module)
        assert names is None or names <= set(mp_ports.__all__), (path, names)
    elif head.startswith("mp_") and head != own:
        assert path.name == "wiring.py" and root.name == "slice", (path, module)
        assert module in PUBLIC and names == {PUBLIC[module]}, (path, module, names)
    else:
        assert head == own or head in sys.stdlib_module_names, (path, module)


def boundary(root):
    paths = source_paths(root) + sorted((root / "tests").rglob("*.py"))
    for path in paths:
        tree = ast.parse(path.read_text())
        aliases = {"mp_ports"}
        for node, module, names in imports(tree):
            check_import(root, path, node, module, names)
            if module == "mp_ports" and isinstance(node, ast.Import):
                aliases.update(alias.asname or alias.name for alias in node.names if alias.name == module)
        for node in ast.walk(tree):
            if root.name != "ports" and isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id in aliases:
                assert node.attr in mp_ports.__all__, (path, node.attr)
    print(f"boundary {root.name} checked {len(source_paths(root))} source files and {len(paths) - len(source_paths(root))} test files")


def pure(root):
    for path in source_paths(root):
        tree = ast.parse(path.read_text())
        aliases = {}
        for node, module, names in imports(tree):
            head = module.split(".")[0]
            assert head not in FORBIDDEN, (path, module)
            if isinstance(node, ast.Import):
                aliases.update({alias.asname or alias.name: alias.name for alias in node.names})
            if head == "os" and names is not None:
                assert not names & {"getenv", "environ"}, path
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                assert not (aliases.get(node.value.id, node.value.id) == "os" and
                            node.attr in {"environ", "getenv"}), path
    print(f"purity {root.name} pure source files={len(source_paths(root))}")


def check_tests_pure(root):
    paths = sorted((root / "tests").rglob("*.py"))
    assert paths and any(path.name.startswith("test_") for path in paths)
    for path in paths:
        tree = ast.parse(path.read_text())
        for _, module, _ in imports(tree):
            head = module.split(".")[0]
            if head == "subprocess":
                assert root.name == "slice" and path.name == "test_mp_wrapper.py", path
    print(f"purity {root.name} test files={len(paths)} subprocess policy checked")
