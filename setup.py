from setuptools import setup

description = "User-friendly graphical user interface to do M/EEG analysis"

setup(
    name='meggie',
    version='1.6.1',
    description=description,
    long_description=description,
    long_description_content_type="text/plain",
    author='CIBR',
    author_email='erkka.heinila@jyu.fi',
    url='https://github.com/cibr-jyu/meggie',
    license='BSD',
    packages=['meggie'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['meggie=meggie.run:main'],
    },
)
