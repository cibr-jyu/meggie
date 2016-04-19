from setuptools import setup

setup(
    name='meggie',
    version='0.2.6',
    description="",
    author='Erkka Heinila',
    author_email='erkka.heinila@jyu.fi',
    url='https://yousource.it.jyu.fi/+hoksotin/hoksotin/lahdekoodit',
    license='BSD',
    packages=['meggie'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'mne==0.11.0',
    ],
    entry_points = {
        'console_scripts': ['meggie=meggie.run:main'],
    },
)
