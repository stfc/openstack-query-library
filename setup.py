from setuptools import setup, find_packages

DESCRIPTION = "python package for openstack query library"
LONG_DESCRIPTION = (
    """Python package for running complex queries on OpenStack Resources"""
)

setup(
    name="openstackquery",
    version="0.1.1",
    author="Anish Mudaraddi",
    author_email="<anish.mudaraddi@stfc.ac.uk>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    keywords=["python, openstack"],
)
