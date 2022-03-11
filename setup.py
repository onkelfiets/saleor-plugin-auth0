from setuptools import setup

setup(
    name="openid-auth",
    version="0.1.0",
    author="Marco Köppel",
    author_email="marco.koeppel@googlemail.com",
    packages=["openid_auth"],
    entry_points={
        "saleor.plugins": ["openid_auth = openid_auth.plugin:OpenIDAuthPlugin"]
    },
    install_requires=["Authlib"],
)
