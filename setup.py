from setuptools import setup, find_packages

setup(
    name='sortof',
    version='1.0.0',
    description='A tool to sort out directories and files',
    author='Michał Moroz <michal@makimo.pl>',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=('sortof', ),
    package_dir={'': 'src'},
    install_requires=['docopt', 'colorama'],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'sortof = sortof.sortof:main',
        ],
    }
)
