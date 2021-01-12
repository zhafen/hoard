import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hoard",
    version="0.1",
    author="Zach Hafen",
    author_email="zachary.h.hafen@gmail.com",
    description="Loot distribution software.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhafen/hoard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy>=1.19.1',
        'google_api_python_client>=1.12.8',
        'httplib2>=0.18.1',
        'oauth2client>=4.1.3',
        'pandas>=1.2.0',
    ],
)
