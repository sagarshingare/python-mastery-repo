"""PySpark package wrapper.

This package exposes local learning modules while seamlessly bridging to the
installed PySpark runtime and auto-configuring the Java 17+ environment.
"""

from __future__ import annotations

import os
import site
import sys

# 1. Prefer Java 17+ for PySpark 4 compatibility
for candidate in [
    "/opt/homebrew/opt/openjdk@17",
    "/opt/homebrew/opt/openjdk",
    "/usr/local/opt/openjdk@17",
    "/usr/local/opt/openjdk",
]:
    if os.path.exists(candidate):
        os.environ["JAVA_HOME"] = candidate
        os.environ["PATH"] = f"{candidate}/bin:{os.environ.get('PATH', '')}"
        break

# 2. Worker Python executable alignment
os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)

# 3. Extend __path__ with site-packages pyspark
_real_init = None
for base in site.getsitepackages() + [site.getusersitepackages()]:
    cand = os.path.join(base, "pyspark")
    if os.path.isdir(cand) and cand not in __path__:
        __path__.append(cand)
        init_candidate = os.path.join(cand, "__init__.py")
        if os.path.exists(init_candidate) and _real_init is None:
            _real_init = init_candidate

# 4. Populate namespace with real pyspark exports
if _real_init:
    with open(_real_init, "r", encoding="utf-8") as f:
        code = compile(f.read(), _real_init, "exec")
        exec(code, globals())
