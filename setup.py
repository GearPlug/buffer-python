import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='buffer-python-lib',
      version='0.1.0',
      description='API wrapper for Buffer written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/buffer-python',
      author='Nerio Rincon',
      author_email='nrincon.mr@gmail.com',
      license='GPL',
      packages=['buffer'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
