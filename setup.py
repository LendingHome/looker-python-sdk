from setuptools import setup

setup(name='looker_sdk',
      version='0.1',
      description='Python SDK for pulling data from Looker',
      url='https://github.com/llooker/python_sdk',
      author='Scott Hoover',
      author_email='scott@looker.com',
      license='MIT',
      packages=['looker'],
      install_requires=['requests'],
      zip_safe=False)