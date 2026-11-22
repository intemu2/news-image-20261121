"""news-image-20261121 entry (Python 3.13, standard library only).

The image is the entry.png beside this file; the program copies it to
/output/entry.png. Outside the grader's container, MAKEFUN_OUTPUT_DIR
stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))
