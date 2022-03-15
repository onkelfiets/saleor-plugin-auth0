from setuptools import setup

setup(
    name="auth0-auth",
    version="0.1.0",
    author="Marco Köppel",
    author_email="marco.koeppel@googlemail.com",
    packages=["auth0_auth"],
    entry_points={"saleor.plugins": ["auth0_auth = auth0_auth.plugin:Auth0AuthPlugin"]},
    install_requires=["auth0-python"],
)
