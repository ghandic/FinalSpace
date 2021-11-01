import os
import sys
import glob
from pathlib import Path
from setuptools import setup


def fast_scandir(dirname: str) -> list[str]:
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


FOLDERS = fast_scandir("assets")

ASSETS = [("assets", glob.glob(os.path.join("assets", "*.*")))] + [
    (folder, glob.glob(os.path.join(folder, "*.*"))) for folder in FOLDERS
]
ICON = os.path.join("assets", "icon.ico")

if sys.platform == "darwin":
    extra_options = dict(
        options={"py2app": {"iconfile": ICON}},
        setup_requires=["py2app"],
    )
# Unable to test
elif sys.platform == "win32":
    extra_options = dict(
        setup_requires=["py2exe"],
        options={"py2exe": {"iconfile": ICON}},
    )
# Unable to test
else:
    extra_options = dict()
setup(name="Final Space", app=["game.py"], data_files=ASSETS, **extra_options)
