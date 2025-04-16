from setuptools import setup, find_packages


setup(
    name="yndx_disk",
    version="0.3.1",
    packages=find_packages(),
    install_requires=[
        "httpx", "aiofiles"
    ],
    author="Tarasov Alexander",
    author_email="a.tevg@ya.ru",
    description="Wrapper for yandex disk rest api",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitverse.ru/arabian/yndx_disk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
