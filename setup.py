from setuptools import setup

install_requires = [
    'mne>=0.23.0',
    'matplotlib',
    'scikit-learn',
    'python-json-logger',
    'pyqt5',
]

# As PyQt5 is PyQt5 in pypi and pyqt in conda-forge, avoid
# installing PyQt5 from pypi if already installed from conda.
try:
    import PyQt5
    install_requires.remove('pyqt5')
except ImportError:
    pass

setup(
    name='meggie',
    version='1.2.0',
    description="User-friendly graphical user interface to do M/EEG analysis",
    long_description="User-friendly graphical user interface to do M/EEG analysis",
    long_description_content_type="text/plain",
    author='CIBR',
    author_email='erkka.heinila@jyu.fi',
    url='https://github.com/cibr-jyu/meggie',
    license='BSD',
    packages=['meggie'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['meggie=meggie.run:main'],
    },
)
