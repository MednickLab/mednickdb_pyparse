from setuptools import setup

setup(name='mednickdb_pyparse',
      version='0.1',
      description='Extract data and metadata a variety of files types relevant to sleep science',
      url='https://github.com/MednickLab/mednickdb_pyparse',
      author='Ben Yetton',
      author_email='bdyetton@gmail.com',
      license='MIT',
      packages = ['mednickdb_pyparse'],
      requires=['pandas','numpy','glob','mne'],
      zip_safe=False,
      include_package_data=True,
      )