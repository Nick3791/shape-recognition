import setuptools

setuptools.setup(
    name="shape-recognition",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "cmake"
        "scikit-build"
        "imutils",
        "opencv-python",
    ]
)
