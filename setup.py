import setuptools

setuptools.setup(
    name="python_syringe_pump",
    version="0.1",
    author="Doug Ollerenshaw",
    author_email="d.ollerenshaw@gmail.com",
    description="open syringe pump",
    install_requires=[
        "pyfirmata==1.1.0",
        "pyserial==3.4",
        "Pyro4"
    ]
)