from setuptools import setup


def parse_requirements():
    try:
        f = open("requirements.txt", "rb")
        return [require for require in f.read().decode("utf-8").split("\n") if require and "#" not in require]
    except FileNotFoundError as e:
        print(e)
        return []


setup(
    name="mlvc",
    version="0.0.1",
    include_package_data=True,
    url="https://github.com/NUS-Fintech-Society/ML_VC-Library",
    license="MIT",
    packages=["mlvc"],
    install_requires=parse_requirements(),
    platform=["any"],
    python_requires=">=3.7",
    zip_safe=False
)
