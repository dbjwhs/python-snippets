# MIT License
# Copyright (c) 2025 dbjwhs

import sys
from pathlib import Path

# Add the src directory to sys.path to allow imports from the reader_writer package
root_dir = Path(__file__).parent.parent
src_dir = root_dir / "src"
sys.path.insert(0, str(src_dir))