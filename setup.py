from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'It is a utility pacakage created by Bits Robocon'
LONG_DESCRIPTION = "The package's purpose is to help ease the submission process for a recruitment task."


def get_install_requires():
    """
    parse requirements.txt, ignore links, exclude comments
    """
    requirements = []
    for line in open('requirements.txt').readlines():
        # skip to next iteration if comment or empty line
        if (
            line.startswith('#')
            or line == ''
            or line.startswith('http')
            or line.startswith('git')
        ):
            continue
        # add line to requirements
        requirements.append(line)
    return requirements

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="zipmysubmission",
    version=VERSION,
    author="Hardik Jain",
    author_email="hardikashishjain@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'robocon'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux :: Ubuntu",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=get_install_requires(),
    entry_points={
    "console_scripts": [
        "zipmysubmission=src.zip_folder:main"
        ]
    },
)
