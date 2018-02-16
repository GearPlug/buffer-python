from setuptools import setup

setup(name='buffer-python',
      version='0.1',
      description='API wrapper for Buffer written in Python',
      url='https://github.com/GearPlug/buffer-python',
      author='Nerio Rincon',
      author_email='nrincon.mr@gmail.com',
      license='GPL',
      packages=['buffer'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
