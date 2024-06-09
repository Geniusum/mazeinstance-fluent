import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

"""
Don't import this file on KER/ scripts
"""

try:
    import KER.path as kernel_path
    import KER.logger as logger
except Exception as e:
    raise ValueError(f"Import exception : {e}")