from setuptools import setup, find_packages

setup(
    name='flappy_bird_game',  # Replace with your game name
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame',  # Add other dependencies if needed
    ],
    entry_points={
        'console_scripts': [
            'flappy_bird_game=python_script.main:main',  # Entry point to your game
        ],
    },
    package_data={
        '': ['images/*', 'sounds/*'],  # Include images and sounds in the package
    },
)

