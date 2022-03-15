from setuptools import setup

setup(
    name="auth0-auth",
    version="0.1.0",
    author="Marco Köppel",
    author_email="marco.koeppel@googlemail.com",
    packages=["auth0-auth"],
    entry_points={"saleor.plugins": ["auth0-auth = auth0-auth.plugin:Auth0AuthPlugin"]},
    install_requires=["auth0-python"],
)
