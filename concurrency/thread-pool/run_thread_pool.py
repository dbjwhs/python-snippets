#!/usr/bin/env python3
# MIT License
# Copyright (c) 2025 dbjwhs

"""
Launcher script for the thread pool demonstration.
"""

import sys
from pathlib import Path

# Add the project directory to the path so we can import the package
project_dir = Path(__file__).resolve().parent
src_dir = project_dir / "src"
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(src_dir))

try:
    from thread_pool.thread_pool import main
    main()
except ImportError as e:
    print(f"Error importing thread pool module: {e}")
    print(f"Paths searched: {sys.path}")
    sys.exit(1)
except Exception as e:
    print(f"Error running thread pool: {e}")
    sys.exit(1)