import json
import logging
import setuptools
import sys
from pathlib import Path


HERE = Path(__file__).parent.resolve()

# Get the package info from package.json
pkg_json = json.loads((HERE / "package.json").read_bytes())

setup_args = dict(
    name="g2nb",
    version=pkg_json["version"],
    url=pkg_json["homepage"],
    author=pkg_json["author"]["name"],
    author_email=pkg_json["author"]["email"],
    description=pkg_json["description"],
    license=pkg_json["license"],
    long_description=(HERE / "README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "jupyterlab~=3.1",
        "jupyter-packaging>=0.12.0",
        "nbtools==22.3.0b2",
        "genepattern-notebook==22.3.0b1",
        "igv-jupyter",
        "py4cytoscape",
        "ndex2"
    ],
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
)

try:  # Import here and wrap in try block in case jupyter_packaging isn't installed on dev machine
    from jupyter_packaging import (
        wrap_installers,
        npm_builder,
    )
    post_develop = npm_builder(build_cmd="install:all")
    setup_args["cmdclass"] = wrap_installers(post_develop=post_develop)
except ImportError as e:
    logging.basicConfig(format="%(levelname)s: %(message)s")
    logging.warning("Build tool `jupyter-packaging` is missing. Install it with pip or conda.")
    if not ("--name" in sys.argv or "--version" in sys.argv):
        raise e

if __name__ == "__main__":
    setuptools.setup(**setup_args)
