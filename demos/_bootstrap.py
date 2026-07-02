"""Put ``src/`` on the import path so demos can ``import contoso`` without an install.

Every demo does ``import _bootstrap`` as its first line. (Python automatically adds
the running script's own directory to ``sys.path``, so this module is importable.)
"""

import pathlib
import sys

_SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
