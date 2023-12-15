from setuptools import setup

setup(
    name="mltl2ltlf",
    version="0.2",
    packages=["mltl2ltlf"],
    package_data={"mltl2ltlf": ["mltl.lark"]},
    install_requires=[
        "lark"
    ],
    entry_points={
        "console_scripts": ["mltl2ltl = mltl2ltlf.mltl2ltlf:main", "mltl2ltlf = mltl2ltlf.mltl2ltlf:main"]
    }
)
