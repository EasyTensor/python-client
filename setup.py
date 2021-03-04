import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easytensor", # Replace with your own username
    version="0.0.3",
    author="Kamal Kamalaldin",
    author_email="kamal@easytensor.com",
    description="The official python cient of EasyTensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EasyTensor/python-client",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
