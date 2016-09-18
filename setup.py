from setuptools import setup

setup(name='lambdazen',
      version='0.1.7',
      description='Syntax changes for python lambdas.',
      url='http://github.com/brthornbury/lambdazen',
      author='Bryan Thornbury',
      author_email='author@example.com',
      license='MIT',
      packages=['lambdazen'],
      zip_safe=False,

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
      ])