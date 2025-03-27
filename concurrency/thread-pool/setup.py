from setuptools import find_packages, setup

setup(
    name="thread_pool",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)