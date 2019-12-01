from setuptools import setup, find_packages

README = 'solve the tapering problem'

requires = [ 'scipy',
             'ipython',
             'python-box',
             'matplotlib' ]
tests_require = [
        'pytest',
        ]

setup(name='tapering',
      version='0.0.1',
      description=README,
      long_description=README,
      url='tbd',
      classifiers=[
          "Programming Language :: Python",
          "Operating System :: POSIX :: Linux",
      ],
      author='moran_netser',
      author_email='moran.netser@gmail.com',
      keywords='tapering',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points={
          'console_scripts': [ 'tap = tapering.main:main' ]
      },
      )
