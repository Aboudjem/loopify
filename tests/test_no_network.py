#!/usr/bin/env python3
"""
The "no network call" claim, as a test (a release gate; runs in CI with the other suites).

The README says loopify's scripts make no network call. This test reads every shipped Python script
under skills/ and fails if one imports a network module, or names curl or wget in its code (the way
a script would shell out to the network). It parses the code with `ast`, so a comment or a docstring
that mentions a module does not count, and an import hidden inside a function still does.

Standard library only. Run: python3 tests/test_no_network.py   (exit 0 = all pass)
"""
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHIPPED = os.path.join(ROOT, "skills")
NETWORK_MODULES = {"socket", "socketserver", "ssl", "urllib", "urllib2", "urllib3", "http", "httplib",
                   "requests", "httpx", "aiohttp", "ftplib", "smtplib", "poplib", "imaplib", "telnetlib",
                   "xmlrpc", "asyncio", "websocket", "websockets"}
NETWORK_COMMANDS = {"curl", "wget"}
failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


def docstring_nodes(tree):
    """The string nodes that are docstrings: prose, not code."""
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                ids.add(id(body[0].value))
    return ids


def network_uses(source):
    """Return 'line N: what' for every network import, or curl/wget string, in the code."""
    tree = ast.parse(source)
    prose = docstring_nodes(tree)
    found = []
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        elif (isinstance(node, ast.Call) and getattr(node.func, "id", "") in ("__import__", "import_module")
              or isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "import_module"):
            arg = node.args[0] if node.args else None
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                names = [arg.value]
        for n in names:
            if n.split(".")[0] in NETWORK_MODULES:
                found.append(f"line {node.lineno}: imports {n}")
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in prose:
            words = set(node.value.replace("/", " ").split())
            for cmd in sorted(words & NETWORK_COMMANDS):
                found.append(f"line {node.lineno}: names {cmd}")
    return found


# 1. The detector catches what it claims to catch.
CASES = [
    ("import socket", "import socket"),
    ("from urllib.request import urlopen", "from urllib.request"),
    ("import http.client", "import http.client"),
    ("import requests", "import requests"),
    ("import ssl", "import ssl"),
    ("from ftplib import FTP", "from ftplib"),
    ("import smtplib", "import smtplib"),
    ("__import__('socket')", "__import__('socket')"),
    ("import importlib\nimportlib.import_module('urllib.request')", "importlib.import_module"),
    ("def f():\n    import urllib.request", "an import inside a function"),
    ("import subprocess\nsubprocess.run(['curl', 'https://example.com'])", "a subprocess to curl"),
    ("import os\nos.system('wget https://example.com')", "os.system to wget"),
    ("import subprocess\nsubprocess.run('/usr/bin/curl -s x', shell=True)", "a full path to curl"),
]
for snippet, label in CASES:
    check(f"detector catches {label}", bool(network_uses(snippet)), snippet)
check("detector ignores a comment, a docstring and plain file work",
      not network_uses('"""Never calls curl."""\n# never import socket here\nimport os, re, sys\nopen("x").read()'))

# 2. Every shipped script is clean.
scripts = []
for dirpath, dirs, files in os.walk(SHIPPED):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    scripts += [os.path.join(dirpath, f) for f in sorted(files) if f.endswith(".py")]
check("the scan finds the three shipped scripts", len(scripts) >= 3, str(scripts))
for path in sorted(scripts):
    with open(path, encoding="utf-8") as f:
        uses = network_uses(f.read())
    check(f"{os.path.relpath(path, ROOT)} imports no network module and calls no curl or wget",
          not uses, "; ".join(uses))

print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
