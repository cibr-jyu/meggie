from setuptools import setup

setup(
    name='meggie',
    version='0.17.0',
    description="",
    author='CIBR',
    author_email='erkka.heinila@jyu.fi',
    url='https://github.com/Teekuningas/meggie',
    license='BSD',
    packages=['meggie'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points={
        'console_scripts': ['meggie=meggie.run:main'],
    },
)
