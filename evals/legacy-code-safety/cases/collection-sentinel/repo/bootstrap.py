"""Inert fixture analogue of a legacy process initialization hook."""
import os
from pathlib import Path

record = Path(os.environ.get("CATALOG_STARTUP_RECORD", "operational-record.txt"))
record.write_text("startup executed\n")
