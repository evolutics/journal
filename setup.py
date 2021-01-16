import setuptools

setuptools.setup(
    name="journal",
    entry_points={
        "console_scripts": [
            "journal=journal:main",
        ],
    },
    packages=[],
)
