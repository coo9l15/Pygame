from setuptools import setup, find_packages

setup(
    name='flappybirdgame',
    version='0.1.0',
    description='A Flappy Bird game implemented in Python using Pygame',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'pygame',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
