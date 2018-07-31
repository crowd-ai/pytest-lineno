"""
pytest plugin to run tests by linenumber
"""
from setuptools import setup

setup(
    name='pytest-lineno',
    description='pytest plugin to run tests by linenumber',
    long_description=open("README.md").read(),
    version='1.0.0',
    author='Aleks Kamko',
    author_email='aykamko@crowdai.com',
    url='https://github.com/crowd-ai/pytest-lineno',
    license='MIT',
    py_modules=['pytest_lineno'],
    entry_points={'pytest11': ['lineno = pytest_lineno']},
    install_requires=['pytest>=3.6.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'Framework :: Pytest'
    ],
)
