from setuptools import setup, find_packages

setup(
    name="robottrace",
    version="0.1.0",
    packages=find_packages(),
    install_requires=['python-dotenv', 'requests', 'watchdog'],
    entry_points={
        'console_scripts': [
            'robottrace=scripts.trace:main',
        ],
    },
    # Metadata
    author="Ofer Rahat",
    author_email="leofer@gmail.com",
    description="A tool to generate slack alerts for robot errors.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gorefbitim/robottrace",
    classifiers=[
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Operating System :: Microsoft :: Windows",
         "Operating System :: POSIX :: Linux",
    ],
)
