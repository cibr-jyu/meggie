from setuptools import setup

setup(
    name='meggie',
    version='0.3.9',
    description="",
    author='Erkka Heinila, Janne Pesonen',
    author_email='erkka.heinila@jyu.fi',
    url='https://yousource.it.jyu.fi/+hoksotin/hoksotin/lahdekoodit',
    license='BSD',
    packages=['meggie'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'mne==0.13.0',
    ],
    entry_points = {
        'console_scripts': ['meggie=meggie.run:main'],
    },
)
