from setuptools import setup

setup(
    name='meggie',
    version='0.13.1',
    description="",
    author='CIBR',
    author_email='erkka.heinila@jyu.fi',
    url='https://yousource.it.jyu.fi/+hoksotin/hoksotin/lahdekoodit',
    license='BSD',
    packages=['meggie'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points = {
        'console_scripts': ['meggie=meggie.run:main'],
    },
)
